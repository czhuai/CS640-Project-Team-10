from detector import OpenaiDetector
import numpy as np
import pandas as pd
import time

def openai_scoring(text_dataset):
    bearer_token = 'Bearer sess-hyJIx4OQkCXIv92XAHcRxu4Qj29NTV5Fj84vuABp'
    scores = pd.DataFrame(columns = ['Score'])
    checkpoint_after = 10

    for index, row in text_dataset.iterrows():
        time.sleep(1)
        try:
            score = openai_similarity(row['Text'], bearer_token)
            scores = scores.append({'Score': score}, ignore_index = True)
        except:
            scores = scores.append({'Score': np.NaN}, ignore_index = True)
        
        if index % checkpoint_after == 0:
            scores.to_csv("OpenAI_Scores.csv")

    scores.to_csv("OpenAI_Scores.csv")

    return "OpenAI_Scores.csv"

def openai_similarity(text, bearer_token):
    od = OpenaiDetector(bearer_token)
    response = od.detect(text)
    return np.float16(response.get("AI-Generated Probability"))                        
                            

