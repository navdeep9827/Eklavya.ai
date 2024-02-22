import streamlit as st
import pandas as pd
from pymongo import MongoClient
import questions_generator
import model as softmax
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from similarity_utils import find_top_closest_indices
import pickle
import random

# Connecting to client and fetching the questions data
client = MongoClient('mongodb+srv://bnslaman999:amidst12345@cluster0.faeaq5c.mongodb.net/')
database = client['Questions_Recommendation'] 
collection = database['Questions'] 
data = list(collection.find()) 
df = pd.DataFrame(data)
question_df = df[df["index"].isin(questions_generator.random_questions_generator(df))]
topics = list(question_df["Topic"].unique())[0:3]
ids = question_df["index"].to_list()
vector_df = pd.read_pickle('vector_df.pkl')
# # Streamlit app

st.title("Quiz App")

# Display questions
answers = []
for index, row in question_df.iterrows():
    st.header(row["Question"])
    options = [row["Option1"], row["Option2"], row["Option3"], row["Option4"]]
    answer = st.radio("Select the correct answer:", options)
    answers.append(answer)

# Submit button
# import streamlit as st

# ... (previous code remains unchanged)

if st.button("Submit"):
    st.success("Quiz Submitted Successfully!")

    marks = []
    wrong_ids = []

    for i, (given, correct, index) in enumerate(zip(answers, question_df["Correct Answer"], question_df["index"])):
        marks.append(1 if given == correct else 0)
        if given != correct:
            wrong_ids.append(index)

    total_score = sum(marks)
    st.write("Your score is:", total_score)

    split_lists = [marks[i:i + 5] for i in range(0, len(marks), 5)]
    topic_wise_marks = dict(zip(topics, [sum(sublist) / len(sublist) for sublist in split_lists]))

    st.write("Your result in quiz is:",topic_wise_marks)

    st.session_state.quiz_results = {
        "total_score": total_score,
        "topic_wise_marks": topic_wise_marks,
        "wrong_ids": wrong_ids,
        "ids": ids
    }
    next_batch_distribution = {key: round(value * 15) for key, value in softmax.softmax_with_total_marks(topic_wise_marks).items()} 
    result = find_top_closest_indices(vector_df, wrong_ids, ids, top_k=4)
    st.write("Next Batch Recommendation:",next_batch_distribution)
    recommended_questions_dictionry = softmax.dict_to_topic(result,df)
    st.write("Similar Question indexes are:",recommended_questions_dictionry)
    # recommended_df = pd.DataFrame(data=[], columns = list(df.columns)[1:])
    recommended_qids = []
    for i in list(recommended_questions_dictionry.keys()):
        qids = recommended_questions_dictionry[i]
        no_of_questions = next_batch_distribution[i]
        selected_qids = random.sample(qids, no_of_questions)
        recommended_qids.append(selected_qids)




    recommended_qids = [item for sublist in recommended_qids for item in sublist]
    # recommendation_indexes = [item for sublist in recommended_questions_dictionry.values() for item in sublist]
    recommended_df = df[df["index"].isin(recommended_qids)]
    # recommended_df = df[df["index"].isin(recommendation_indexes)]

    st.session_state.next_df = recommended_df

if st.button("Recommend next batch"):

    # if "quiz_results" in st.session_state:
    #     recommendation_data = st.session_state.quiz_results
    #     # st.write("Incorrect Question IDs for Recommendation:", recommendation_data["wrong_ids"])
    #     # st.write("Question IDs", recommendation_data["ids"])
    for index, row in st.session_state.next_df.iterrows():
        st.header(row["Question"])
        options = [row["Option1"], row["Option2"], row["Option3"], row["Option4"]]
        next_answer = st.radio("Select the correct answers:", options)
        # answers.append(answer)



