import numpy as np

def softmax_with_total_marks(marks_dict):
    """
    Compute softmax values for marks in each subject in the marks_dict.

    Args:
    - marks_dict (dict): A dictionary where keys represent subjects and values represent marks or scores.

    Returns:
    - probabilities_dict (dict): A dictionary where keys are subjects and values are their respective probabilities after applying softmax.
    """
    # Compute softmax values
    e_x = np.exp(-np.array(list(marks_dict.values())))
    probabilities = e_x / e_x.sum()

    # Create dictionary with subjects as keys and probabilities as values
    probabilities_dict = dict(zip(marks_dict.keys(), probabilities))
    
    return probabilities_dict

def dict_to_topic(similar_questions,df):
    ids = list(similar_questions.keys())
    topics = df[df["index"].isin(ids)]["Topic"].unique()
    final_dict = {key: [] for key in topics}
    for i in ids:
        if i <= 52:
            final_dict["Physics"] = final_dict["Physics"] + similar_questions[i]
        elif i>=53 and i<=98:
            final_dict["Polity"] = final_dict["Polity"] + similar_questions[i]
        elif i>=99:
            final_dict["Current Affairs"] = final_dict["Current Affairs"] + similar_questions[i]
    return final_dict
        



    return topics



