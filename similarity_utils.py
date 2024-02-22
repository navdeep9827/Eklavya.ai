#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def find_top_closest_indices(vector_df, wrong_questions_array, questions_array, top_k=5):
    result_dict = {}

    for index in wrong_questions_array:
        # Extract the embedding for the given index
        query_embedding = vector_df.loc[vector_df['index'] == index, 'combined_embedding'].values[0]

        # Calculate cosine similarity with all other embeddings
        similarities = cosine_similarity([query_embedding], vector_df['combined_embedding'].tolist())[0]

        # Get indices of top similar embeddings (excluding the query index itself)
        top_indices = np.argsort(similarities)[::-1][1:]

        # Filter out indices that are already in the questions_array
        top_indices = [i for i in top_indices if vector_df.loc[i, 'index'] not in questions_array]

        # Keep selecting indices until you have enough for top_k
        selected_indices = []
        for i in top_indices:
            if len(selected_indices) >= top_k:
                break
            if vector_df.loc[i, 'index'] not in selected_indices:
                selected_indices.append(vector_df.loc[i, 'index'])

        # Save the result in a dictionary
        result_dict[index] = selected_indices

        # Add the chosen index to the questions_array for exclusion in subsequent iterations
        questions_array.append(index)

    return result_dict


