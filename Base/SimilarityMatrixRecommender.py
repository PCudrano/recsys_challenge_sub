#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 16/09/2017

@author: Maurizio Ferrari Dacrema
"""

import pickle
from src.libs.similarity import dot_product



class SimilarityMatrixRecommender(object):
    """
    This class refers to a Recommender KNN which uses a similarity matrix, it provides two function to compute item's score
    bot for user-based and Item-based models as well as a function to save the W_matrix
    """

    def __init__(self):
        super(SimilarityMatrixRecommender, self).__init__()

        self.sparse_weights = True

        self.compute_item_score = self.compute_score_item_based


    # def compute_score_item_based(self, user_id):
    #
    #     if self.sparse_weights:
    #         user_profile = self.URM_train[user_id]
    #
    #         return user_profile.dot(self.W_sparse).toarray()
    #
    #     else:
    #
    #         assert False
    #
    #         user_profile = self.URM_train.indices[self.URM_train.indptr[user_id]:self.URM_train.indptr[user_id + 1]]
    #         user_ratings = self.URM_train.data[self.URM_train.indptr[user_id]:self.URM_train.indptr[user_id + 1]]
    #
    #         relevant_weights = self.W[user_profile]
    #         return relevant_weights.T.dot(user_ratings)

    def compute_score_item_based(self, user_id, k = 160):

        if self.sparse_weights:
            user_profile = self.URM_train[user_id]
            est_ratings = dot_product.dot_product(user_profile, self.W_sparse, k=k)
            #return user_profile.dot(self.W_sparse).toarray()
            return est_ratings.tocsr()


        else:

            assert False

            user_profile = self.URM_train.indices[self.URM_train.indptr[user_id]:self.URM_train.indptr[user_id + 1]]
            user_ratings = self.URM_train.data[self.URM_train.indptr[user_id]:self.URM_train.indptr[user_id + 1]]

            relevant_weights = self.W[user_profile]
            return relevant_weights.T.dot(user_ratings)





    def compute_score_user_based(self, user_id, k = 160):

        if self.sparse_weights:
            # assert False
            #return self.W_sparse[user_id].dot(self.URM_train) # .toarray()

            est_ratings = dot_product.dot_product(self.W_sparse.T, self.URM_train, k=k)
            est_ratings = est_ratings.tocsr()
            return est_ratings[user_id]

        else:
            # Numpy dot does not recognize sparse matrices, so we must
            # invoke the dot function on the sparse one
            assert False
            return self.URM_train.T.dot(self.W[user_id])










    def saveModel(self, folder_path, file_name = None):

        if file_name is None:
            file_name = self.RECOMMENDER_NAME

        print("{}: Saving model in file '{}'".format(self.RECOMMENDER_NAME, folder_path + file_name))

        dictionary_to_save = {"sparse_weights": self.sparse_weights}


        if self.sparse_weights:
            dictionary_to_save["W_sparse"] = self.W_sparse

        else:
            dictionary_to_save["W"] = self.W


        pickle.dump(dictionary_to_save,
                    open(folder_path + file_name, "wb"),
                    protocol=pickle.HIGHEST_PROTOCOL)


        print("{}: Saving complete".format(self.RECOMMENDER_NAME))


