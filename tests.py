import torch

# Here is a test file
# This shouldn't appear in the final version of the project

from genetic_operations import Mutations

#test = Mutations(2)
#test.fusion()

#test2 = Mutations(3, 14)
#test2.fusion()



# Unitary tests :
# list_of_latent_vectors is a list containing the latent vectors
# weight is an optional parameter use to modify the weight if wanted

# Test without anything (error)
"""
list_of_latent_vectors = []
test_unitary = Mutations(list_of_latent_vectors)
test_unitary.fusion()
"""

# Test this time with some latent_vectors loaded :

# Generate a random latent vector
#latent = torch.randn(1, 64, 8, 8)  
# Save a latent_vector :
#torch.save(latent, "randn_latent_tensor.pt")
# Load it :
"""
latent_loaded = torch.load("randn_latent_tensor.pt")
list_of_latent_vectors = []
list_of_latent_vectors.append(latent_loaded)
print(f"This is an extract of the first latent vector from the actual list : {list_of_latent_vectors[0][0, :4, :2, :2]}")

test_unitary2 = Mutations(list_of_latent_vectors)
res = test_unitary2.fusion()
print(f"This is an extract of the first latent vector from the new list : {res[0][0, :4, :2, :2]}")
"""


latent_loaded = torch.load("randn_latent_tensor.pt")
latent_loaded2 = torch.load("randn_latent_tensor_copie.pt")
list_of_latent_vectors = []
list_of_latent_vectors.append(latent_loaded)
list_of_latent_vectors.append(latent_loaded2)
print(f"This is an extract of the first latent vector from the actual list : {list_of_latent_vectors[0][0, :4, :2, :2]}")

test_unitary2 = Mutations(list_of_latent_vectors)
res = test_unitary2.fusion()
if len(res) != 0:
    print(f"This is an extract of the first latent vector from the new list : {res[0][0, :4, :2, :2]}")
else:
    print(" Nothing has been done")