import torch
# The following class will be used to do various operations on the latent_vector

class Mutations:
    """
    This class is used to do every modification wanted on the latent vectors of the pictures selected on the GUI.
    Attributes :
    list_latent_vector (list) : this is a list containing all the latent vectors of the selected pictures
    weight (int) : this is the weight use for the fusion of pictures. If it isn't specified, it will take a default value of 0.5
    
    Return :
    It returns a list of latent vectors (list_new_latent_vectors) used that will be use to generate new pictures.
    """
    def __init__(self, list_latent_vectors, weight=None):
        self.list_latent_vectors = list_latent_vectors
        self.weight = weight

    def fusion(self):
        print("\n Next test :")
        if len(self.list_latent_vectors) == 0:
            print(" There is an error, you don't have selected any picture. \n You should at least select one picture that looks the most like your suspect.")
            res = []
        else:
            if len(self.list_latent_vectors) != 1:
                print(" Going to fuse multiples pictures")
                if self.weight is not None:
                    res = self._multiple_weighted_fusion()
                res = self._multiple_weighted_fusion()
            else:
                if self.weight is not None:
                    res = self._single_weighted_fusion()
                print(" Going to modify only one picture")
                res = self._single_weighted_fusion()
        return res



    def _single_weighted_fusion(self):
        """
        This function is use to modify a single latent vector with the default weight parameter. If this parameter if given, it takes this specific value.
        It returns a list containing the modified latent vector.
        """
        list_new_latent_tensor = []
        if self.weight is not None:
            alpha = self.weight
        else:
            alpha = 0.5
        randn_latent_vector_modifier = torch.randn(1, 128)

        latent_tensor_modified = alpha * self.list_latent_vectors[0] + (1 - alpha) * randn_latent_vector_modifier
        list_new_latent_tensor.append(latent_tensor_modified)
        return list_new_latent_tensor


    def _multiple_weighted_fusion(self):
        """
        This function is use to modify a selection of latent vectors with a very basic default weight parameter. It can be modify in order to use a different type of fusion.
        It returns a list containing the modified latent vector.
        """
        list_new_latent_tensors = []
        
        sum_latent_vectors = torch.stack(self.list_latent_vectors)
        latent_tensor_modified = sum_latent_vectors.mean(dim=0)
        list_new_latent_tensors.append(latent_tensor_modified)
        return list_new_latent_tensors
