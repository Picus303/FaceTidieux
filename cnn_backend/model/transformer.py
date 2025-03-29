import torch

import torch.nn as nn
from torch import sqrt



class InputEmbeddings(nn.Module):

	def __init__(self, vocab_size, dim):
		super().__init__()
		self.vocab_size = vocab_size
		self.dim = dim
		self.stabilisation_coef = sqrt(torch.tensor(self.dim))

		self.embedding = nn.Embedding(vocab_size, dim)

	def forward(self, x):
		return self.stabilisation_coef * self.embedding(x)


class NormalisationLayer(nn.Module):

	def __init__(self, dim, epsilon):
		super().__init__()

		self.layer_norm = nn.LayerNorm(dim, eps=epsilon)

	def forward(self, x):
		return self.layer_norm(x)


class MultiHeadAttentionBlock(nn.Module):

	def __init__(self, context_length, dim, head_count, abstraction_coef, dropout):
		super().__init__()
		self.context_length = context_length
		self.dim = dim
		self.head_count = head_count
		self.abstract_dim = int(dim * abstraction_coef)
		self.abstract_dim_sqrt = sqrt(torch.tensor(self.abstract_dim))
		self.mask_coef = torch.tensor(-1e12)

		self.q_weights = nn.Linear(dim, head_count*self.abstract_dim, bias=True)
		self.k_weights = nn.Linear(dim, head_count*self.abstract_dim, bias=True)
		self.v_weights = nn.Linear(dim, head_count*self.abstract_dim, bias=True)

		self.p_weights = nn.Linear(head_count*self.abstract_dim, dim, bias=True)
		self.dropout = nn.Dropout(dropout)

	def forward(self, q, k, v, mask=None):
		batch_size = q.size(0)

		# Transformation linéaire (B, C, H*D_a)
		q_vect = self.q_weights(q)
		k_vect = self.k_weights(k)
		v_vect = self.v_weights(v)

		# Réorganisation pour parallélisme (B, H, C, D_a)
		q_vect = q_vect.view(batch_size, self.context_length, self.head_count, self.abstract_dim).permute(0, 2, 1, 3)
		k_vect = k_vect.view(batch_size, self.context_length, self.head_count, self.abstract_dim).permute(0, 2, 1, 3)
		v_vect = v_vect.view(batch_size, self.context_length, self.head_count, self.abstract_dim).permute(0, 2, 1, 3)

		# Calcul des scores d'attention (B, H, C, C)
		attention_scores = torch.matmul(q_vect, k_vect.transpose(-2, -1)) / self.abstract_dim_sqrt
		if mask is not None:
			attention_scores = attention_scores.masked_fill(mask==0, self.mask_coef)
		attention_weights = torch.softmax(attention_scores, dim=-1)
		attention_weights = self.dropout(attention_weights)

		# Application des poids d'attention (B, H, C, D_a)
		attention_output = torch.matmul(attention_weights, v_vect)

		# Concaténation des résultats (B, C, H*D_a)
		attention_output = attention_output.permute(0, 2, 1, 3).contiguous().view(batch_size, self.context_length, self.head_count*self.abstract_dim)

		# Projection de sortie (B, C, D)
		output = self.p_weights(attention_output)

		return output


class FeedForwardBlock(nn.Module):

	def __init__(self, dim, abstraction_coef, dropout):
		super().__init__()
		abstract_dim = int(dim * abstraction_coef)

		self.block = nn.Sequential(
			nn.Linear(dim, abstract_dim, bias=True),
			nn.GELU(),
			nn.Dropout(dropout),
			nn.Linear(abstract_dim, dim, bias=True),
		)

	def forward(self, x):
		return self.block(x)


class ResidualConnectionGroup(nn.Module):

	def __init__(self, norm_params, dropout):
		super().__init__()
		self.norm = NormalisationLayer(*norm_params)
		self.dropout = nn.Dropout(dropout)

	def forward(self, x, layer):
		return x + self.dropout(layer(self.norm(x)))


class EncoderBlock(nn.Module):

	def __init__(self, norm_params, attention_params, feed_forward_params, dropout):
		super().__init__()
		self.rcg_1 = ResidualConnectionGroup(norm_params, dropout)
		self.attn = MultiHeadAttentionBlock(*attention_params, dropout)
		self.rcg_2 = ResidualConnectionGroup(norm_params, dropout)
		self.ffw = FeedForwardBlock(*feed_forward_params, dropout)

	def forward(self, x, mask):
		attn_call = lambda x: self.attn(x, x, x, mask)
		ffw_call = lambda x: self.ffw(x)

		x = self.rcg_1(x, attn_call)
		x = self.rcg_2(x, ffw_call)
		return x


class Encoder(nn.Module):

	def __init__(self, encoder_block_count, encoder_block_params, norm_params, dropout):
		super().__init__()
		self.encoder_blocks = nn.ModuleList([EncoderBlock(*encoder_block_params, dropout) for _ in range(encoder_block_count)])
		self.norm = NormalisationLayer(*norm_params)

	def forward(self, x, mask):
		for block in self.encoder_blocks:
			x = block(x, mask)
		return self.norm(x)


class ProjectionLayer(nn.Module):

	def __init__(self, dim, output_dim, context_length):
		super().__init__()
		self.proj1 = nn.Linear(dim, output_dim)
		self.proj2 = nn.Linear(context_length, 1)

	def forward(self, x):		# x: (B, C, D)
		x = self.proj1(x)		# x: (B, C, O)
		x = x.permute(0, 2, 1)	# x: (B, O, C)
		x = self.proj2(x)		# x: (B, O, 1)
		return x.squeeze(-1)	# x: (B, O)


class EncoderOnlyTransformer(nn.Module):

	def __init__(self, source_embeddings_params, encoder_params, projection_params, dropout):
		super().__init__()
		self.source_embeddings = InputEmbeddings(*source_embeddings_params)
		self.encoder = Encoder(*encoder_params, dropout)
		self.projection = ProjectionLayer(*projection_params)

	def encode(self, x, mask):
		x = self.source_embeddings(x)
		return self.encoder(x, mask)

	def project(self, x):
		return self.projection(x)
	
	def forward(self, x, mask=None):
		return self.project(self.encode(x, mask))


def build_encoder_only_transformer(
	dim: int, output_dim: int,
	source_vocab_size: int, context_length: int,
	encoder_block_count: int,
	encoder_self_attention_head_count: int,
	encoder_self_attention_abstraction_coef: float,
	encoder_feed_forward_abstraction_coef: float,
	epsilon: float, dropout: float
) -> EncoderOnlyTransformer:

	# Arguments for the embeddings
	source_embeddings_params = (source_vocab_size, dim)

	# Arguments for the encoder and decoder
	encoder_params = (encoder_block_count, ((dim, epsilon),
											(context_length, dim, encoder_self_attention_head_count, encoder_self_attention_abstraction_coef),
											(dim, encoder_feed_forward_abstraction_coef)), (dim, epsilon))

	# Arguments for the projection layer
	projection_params = (dim, output_dim, context_length)

	# Build the model
	encoder_only_transformer = EncoderOnlyTransformer(
									source_embeddings_params,
									encoder_params,
									projection_params,
									dropout
								)

	# Initialize the weights
	for param in encoder_only_transformer.parameters():
		if param.dim() > 1:
			nn.init.xavier_uniform_(param)

	return encoder_only_transformer