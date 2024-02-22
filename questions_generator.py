def random_questions_generator(df):
    topics = list(df["Topic"].unique())
    topics = topics[0:3]
    question_indexes = []
    for i in topics:
        random_sample = df[df["Topic"] == i].sample(5,random_state=42)["index"].tolist()
        question_indexes.append(random_sample)
    return sum(question_indexes, [])