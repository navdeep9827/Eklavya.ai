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

