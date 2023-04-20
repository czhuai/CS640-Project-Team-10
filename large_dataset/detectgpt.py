import pandas as pd
from DetectGPT.model import GPT2PPLV2

def detectgpt_scoring(text_dataset):
    model = GPT2PPLV2()
    scores = pd.DataFrame(columns = ['Score'])
    checkpoint_after = 10

    for index, row in text_dataset.iterrows():
        score = detectgpt_similarity(model, row['Text'])
        scores = scores.append({'Score': score}, ignore_index = True)
        if index % checkpoint_after == 0:
            scores.to_csv("DetectGPT_Scores.csv")

    scores.to_csv("DetectGPT_Scores.csv")

    return "DetectGPT_Scores.csv"

def detectgpt_similarity(model, sentence):
    results = model(sentence, 100, "v1.1")
    return results.get("score")
