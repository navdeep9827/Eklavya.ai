def softmax(x):
    """
    Compute softmax values for each sets of scores in x.
    """
    e_x = np.exp(-np.array(x))
    return e_x / e_x.sum()

# Function to calculate softmax after dividing by total marks
def softmax_with_total_marks(marks_list, total_marks_per_subject):
    normalized_marks = [mark / total_marks_per_subject for mark in marks_list]
    probabilities = softmax(normalized_marks)
    return probabilities

# Example usage:
marks = [20, 15, 18, 22, 13]  # Example marks for each subject
total_marks_per_subject = 25  # Total marks for each subject
probabilities = softmax_with_total_marks(marks, total_marks_per_subject)