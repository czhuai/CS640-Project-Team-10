import numpy as np
import pandas as pd
from GPTZero.model import GPT2PPL

def gptzero_scoring(text_dataset):
    model = GPT2PPL()
    scores = pd.DataFrame(columns = ['Perplexity_Score', 'Burstiness_Score'])
    checkpoint_after = 10

    for index, row in text_dataset.iterrows():
        try:
            perplexity_score, burstiness_score = gptzero_similarity(model, row['Text'])
            scores = scores.append({'Perplexity_Score': perplexity_score, 'Burstiness_Score': burstiness_score}, ignore_index = True)
        except:
            scores = scores.append({'Perplexity_Score': np.NAN, 'Burstiness_Score': np.NaN}, ignore_index = True)
        
        if index % checkpoint_after == 0:
            scores.to_csv("GPTZero_Scores.csv")

    scores.to_csv("GPTZero_Scores.csv")

    return "GPTZero_Scores.csv"

def gptzero_similarity(model, sentence):
    results, out = model(sentence)
    return np.float16(results.get("Perplexity")), np.float16(results.get("Burstiness"))
