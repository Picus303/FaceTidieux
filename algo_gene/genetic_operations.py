import torch


class Mutations:
    """
    This class is used to do every modification wanted on the latent vectors of the pictures selected on the GUI.
    Parameters :
    ------------
    list_latent_vector (list) : this is a list containing all the latent vectors of the selected pictures
    weight (int) : this is the weight use for the fusion of pictures. If it isn't specified, it will take a default value of 0.5
    number_of_new (int) : this is the number of new latent vectors that we want to generate. It is by default set to 1.
    Return :
    ------------
    It returns a list of latent vectors (list_new_latent_vectors) used that will be use to generate new pictures.
    """
    def __init__(self, list_latent_vectors, weight=None, number_of_new=None):
        self.list_latent_vectors = list_latent_vectors
        self.weight = weight
        self.number_of_new = number_of_new

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def fusion(self):
        print("\n Next test :")
        if len(self.list_latent_vectors) == 0:
            print(" There is an error, you don't have selected any picture. \n You should at least select one picture that looks the most like your suspect.")
            res = []
        else:
            if len(self.list_latent_vectors) != 1:
                print(" Going to fuse multiples pictures")
                if self.number_of_new is not None:
                    res = self._multiple_weighted_fusion_x_times()
                res = self._multiple_weighted_fusion()
            else:
                if self.number_of_new is not None:
                    res = self._single_weighted_fusion_x_times()
                print(" Going to modify only one picture")
                res = self._single_weighted_fusion()
        return res



    def _single_weighted_fusion(self):
        """
        This function is use to modify a single latent vector with the default weight parameter. If this parameter if given, it takes this specific value.
        It returns a list containing the modified latent vector.
        """
        list_new_latent_tensor = []
        if self.weight is not None and self.weight <= 1 and self.weight >= 0:
            alpha = self.weight
        else:
            alpha = 0.5
        randn_latent_vector_modifier = torch.randn(1, 128, device=self.device)

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


    def _single_weighted_fusion_x_times(self):
        """
        This function is use to create multiple outputs (multiple latent vectors) base on only one latent vector (origin_vector).
        It is triggered when the parameter number_of_new is different from 0 (when we want more than only one new picture).
        It reuse the function _single_weighted_fusion.
        """
        list_x_new_latent_tensors = []
        for i in range(self.number_of_new):
            latent_vector_i_modified = self._single_weighted_fusion()
            list_x_new_latent_tensors.append(latent_vector_i_modified[0])
        print(f" There is {len(list_x_new_latent_tensors)} new latent vectors generated.")
        return list_x_new_latent_tensors


    def _multiple_weighted_fusion_x_times(self):
        """
        This function is use to create multiple outputs (multiple latent vectors) base, this time, on multiple latent vectors in input.
        It is also triggered when the parameters number_of_new is different from 0 (when we want more than only one new picture).
        This time, it doesn't reuse the _multiple_weighted_fusion as we want to create different kind of ponderation.
        Indeed, if we want 4 pictures, the first picture will have more characteristic coming from the first latent vector, the second picture, will have more form the second latent vector, and so on...
        A random_latent_vector is also generated to create a little random modification. This is useful in the case that we have less pictures in input than in output : it allows to still generate differents pictures. 
        """
        list_x_new_latent_tensors = []
        main_weight = 0.4
        noise_weight = 0.05
        nb_inputs = len(self.list_latent_vectors)
        for i in range(self.number_of_new):
            idx = i % nb_inputs
            privilege_latent_vector = main_weight * self.list_latent_vectors[idx]
            randn_latent_vector_modifier = torch.randn(1, 128, device=self.device)
            latent_vector_i_modified = privilege_latent_vector.clone()
            latent_vector_i_modified += noise_weight * randn_latent_vector_modifier

            other_latent_vectors = self.list_latent_vectors.copy()
            other_latent_vectors.pop(idx)
            for latent_vector in other_latent_vectors:
                other_latent_vector_weighted = (1-main_weight-noise_weight)/len(other_latent_vectors) * latent_vector
                latent_vector_i_modified += other_latent_vector_weighted

            list_x_new_latent_tensors.append(latent_vector_i_modified)
            print(f" Picture {i} has a major weight coming from latent vector {idx}")
        print(f" There is {len(list_x_new_latent_tensors)} new latent vectors generated.")
        return list_x_new_latent_tensors
