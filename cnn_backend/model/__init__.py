import torch
import torch.nn as nn
from torch import Tensor
from typing import Tuple

from .transformer import build_encoder_only_transformer


class AdaIN(nn.Module):
    def __init__(self, style_dim: int, num_features: int) -> None:
        super().__init__()
        self.norm = nn.InstanceNorm2d(num_features)
        self.fc = nn.Linear(style_dim, num_features*2)

    def forward(self, x: Tensor, style: Tensor) -> Tensor:
        h: Tensor = self.fc(style)                  # (B, D) -> (B, C*2)
        gamma, beta = h.chunk(2, dim=1)             # (B, C), (B, C)

        gamma = gamma.unsqueeze(-1).unsqueeze(-1)   # (B, C, 1, 1)
        beta = beta.unsqueeze(-1).unsqueeze(-1)     # (B, C, 1, 1)

        out = self.norm(x)
        out = gamma * out + beta
        return out


class EncoderBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        conv_params: Tuple[int],
        style_dim: int,
        dropout: float,
    ) -> None:

        super().__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, 5, stride=conv_params[0], padding=conv_params[1])
        self.GELU = nn.GELU()
        self.adain = AdaIN(style_dim, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor, style: Tensor) -> Tensor:
        x = self.conv(x)
        x = self.GELU(x)
        x = self.adain(x, style)
        x = self.dropout(x)
        return x


class Encoder(nn.Module):
    def __init__(self, in_channels: int, style_dim: int, dropout: float) -> None:
        super().__init__()
        self.block1 = EncoderBlock(in_channels, 16, (3, 2), style_dim, dropout)  # (B, 3, 180, 216) -> (B, 16, 60, 72)
        self.block2 = EncoderBlock(16, 32, (3, 2), style_dim, dropout)           # (B, 16, 60, 72) -> (B, 32, 20, 24)
        self.block3 = EncoderBlock(32, 64, (2, 2), style_dim, dropout)           # (B, 32, 20, 24) -> (B, 64, 10, 12)
        self.block4 = EncoderBlock(64, 128, (2, 2), style_dim, dropout)          # (B, 64, 10, 12) -> (B, 128, 5, 6)

    def forward(self, x: Tensor, style: Tensor) -> Tensor:
        x = self.block1(x, style)
        x = self.block2(x, style)
        x = self.block3(x, style)
        x = self.block4(x, style)
        return x


class DecoderBlock(nn.Module):
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        style_dim: int,
        conv_params: Tuple[int, int, int],
        dropout: float,
    ) -> None:

        super().__init__()
        self.conv = nn.ConvTranspose2d(
            in_channels, out_channels, 5, stride=conv_params[0], padding=conv_params[1], output_padding=conv_params[2]
        )
        self.GELU = nn.GELU()
        self.adain = AdaIN(style_dim, out_channels)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor, style: Tensor) -> Tensor:
        x = self.conv(x)
        x = self.GELU(x)
        x = self.adain(x, style)
        x = self.dropout(x)
        return x


class Decoder(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, style_dim: int, dropout: float) -> None:
        super().__init__()
        self.block1 = DecoderBlock(in_channels, 192, style_dim, (2, 2, 1), dropout)
        self.conv1 = nn.ConvTranspose2d(192, 128, 5, stride=1, padding=2, output_padding=0)
        self.block2 = DecoderBlock(128, 96, style_dim, (2, 2, 1), dropout)
        self.conv2 = nn.ConvTranspose2d(96, 64, 5, stride=1, padding=2, output_padding=0)
        self.block3 = DecoderBlock(64, 48, style_dim, (3, 1, 0), dropout)
        self.conv3 = nn.ConvTranspose2d(48, 32, 5, stride=1, padding=2, output_padding=0)
        self.conv_out1 = nn.ConvTranspose2d(32, out_channels, 5, stride=3, padding=1, output_padding=0)
        self.conv_out2 = nn.ConvTranspose2d(out_channels, out_channels, 5, stride=1, padding=2, output_padding=0)

    def forward(self, x: Tensor, style: Tensor) -> Tensor:
        x = self.block1(x, style)   # (B, 256, 5, 6) -> (B, 192, 10, 12)
        x = self.conv1(x)           # (B, 192, 10, 12) -> (B, 128, 10, 12)
        x = self.block2(x, style)   # (B, 128, 10, 12) -> (B, 96, 20, 24)
        x = self.conv2(x)           # (B, 96, 20, 24) -> (B, 64, 20, 24)
        x = self.block3(x, style)   # (B, 64, 20, 24) -> (B, 48, 60, 72)
        x = self.conv3(x)           # (B, 48, 60, 72) -> (B, 32, 60, 72)
        x = self.conv_out1(x)       # (B, 32, 60, 72) -> (B, 3, 180, 216)
        x = self.conv_out2(x)       # (B, 3, 180, 216) -> (B, 3, 180, 216)
        return x


class CVAEGenerator(nn.Module):
    def __init__(
        self,
        latent_dim: int = 128,
        label_embed_dim: int = 128,
        color_count: int = 3,
        dropout: float = 0.1,
    ) -> None:

        super().__init__()
        self.hidden_dim: int = latent_dim + label_embed_dim

        self.reduced_img_dim: Tuple[int, int] = (5, 6)
        total_reduced_size_encoder: int = latent_dim * self.reduced_img_dim[0] * self.reduced_img_dim[1]
        total_reduced_size_decoder: int = self.hidden_dim * self.reduced_img_dim[0] * self.reduced_img_dim[1]

        # Label encoder
        self.label_encoder: nn.Module = build_encoder_only_transformer(
            dim=label_embed_dim,
            output_dim=label_embed_dim,
            source_vocab_size=58,
            context_length=19,
            encoder_block_count=3,
            encoder_self_attention_head_count=4,
            encoder_self_attention_abstraction_coef=0.25,
            encoder_feed_forward_abstraction_coef=2.0,
            epsilon=1e-9,
            dropout=dropout,
        )

        # Encoder
        self.encoder: nn.Module = Encoder(color_count, label_embed_dim, dropout=dropout)
        self.encoder_projection_mu: nn.Linear = nn.Linear(total_reduced_size_encoder, latent_dim)
        self.encoder_projection_logvar: nn.Linear = nn.Linear(total_reduced_size_encoder, latent_dim)
        self.flatten: nn.Flatten = nn.Flatten()

        # Decoder
        self.decoder_projection: nn.Linear = nn.Linear(self.hidden_dim, total_reduced_size_decoder)
        self.decoder: nn.Module = Decoder(self.hidden_dim, color_count, label_embed_dim, dropout=dropout)
        self.sigmoid: nn.Sigmoid = nn.Sigmoid()

    def encode(self, x: Tensor, label: Tensor) -> Tuple[Tensor, Tensor]:
        label_embed: Tensor = self.label_encoder(label)
        x: Tensor = self.encoder(x, label_embed)
        x = self.flatten(x)

        mu: Tensor = self.encoder_projection_mu(x)
        logvar: Tensor = self.encoder_projection_logvar(x)
        return mu, logvar

    def reparameterize(self, mu: Tensor, logvar: Tensor) -> Tensor:
        std: Tensor = torch.exp(0.5 * logvar)
        eps: Tensor = torch.randn_like(std)
        return mu + eps * std

    def decode(self, z: Tensor, label: Tensor) -> Tensor:
        label_embed: Tensor = self.label_encoder(label)
        x: Tensor = torch.cat([z, label_embed], dim=1)
        x = self.decoder_projection(x)
        x = x.view(-1, self.hidden_dim, self.reduced_img_dim[0], self.reduced_img_dim[1])

        x = self.decoder(x, label_embed)
        return self.sigmoid(x)

    def forward(self, x: Tensor, label: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
        mu, logvar = self.encode(x, label)
        z = self.reparameterize(mu, logvar)
        return self.decode(z, label), mu, logvar