import pandas as pd
import random

from sklearn.preprocessing import MinMaxScaler
from detectgpt import detectgpt_scoring
from gptzero import gptzero_scoring
from grammarly import grammarly_scoring
from openai import openai_scoring
import re
 
unoriginal_dataset = pd.read_csv("GPT-wiki-intro.csv", nrows=20000)
original_dataset = pd.read_csv("Reviews.csv")
text_dataset = pd.DataFrame(columns = ['Text', 'Originality'])

def get_text(dataset, sentence_index, isHuman = False):
  list = []
  total_length = 0
  choice = random.randint(0, 1)
  if isHuman:
     choice = random.choice([0, 1, 1])
  if choice == 1:
    if isHuman:
       picker = random.randint(0, len(dataset) - 15)
       extent = random.randint(1,15)
    else:
       picker = random.randint(0, len(dataset) - 4)
       extent = random.randint(1,3)       
    for j in range(extent):
      sentence = dataset.iloc[picker + j, sentence_index]
      list.append(sentence)  
      sentence_length = len(re.findall(r'\w+', sentence))
      total_length += sentence_length
                                   
  return list, total_length

for iter in range(0, 2000):
    human_paras, human_length = get_text(original_dataset, 9, True)
    wiki_paras, wiki_length = get_text(unoriginal_dataset, 3)
    ai_paras, ai_length = get_text(unoriginal_dataset, 4)    
    total_length = wiki_length + ai_length + human_length

    if total_length < 150 or total_length > 1000: 
       continue
        
    originality = human_length * 1.0 / (wiki_length + ai_length + human_length)
    tmp = wiki_paras + ai_paras + human_paras
    random.shuffle(tmp)
    new_para = ""
    for para in tmp:
        new_para += para

    text_dataset = text_dataset.append({'Text': new_para, 'Originality': originality}, ignore_index = True)

text_dataset.to_csv("text_dataset.csv")

detectgpt_path = detectgpt_scoring(text_dataset)
gptzero_path = gptzero_scoring(text_dataset)
grammarly_path = grammarly_scoring(text_dataset)
openai_path = openai_scoring(text_dataset)

df1 = pd.read_csv(detectgpt_path)
df2 = pd.read_csv(gptzero_path)
df3 = pd.read_csv(grammarly_path)
df4 = pd.read_csv(openai_path)
df5 = pd.read_csv("text_dataset.csv")



merged_df = pd.concat([df1.loc[:800,["Score"]], df2.loc[:800,["Perplexity_Score", "Burstiness_Score"]], df3.loc[:800, ["Score"]], df4.loc[:800, ["Score"]], df5.loc[:800, ["Originality"]]], axis = 1)
merged_df.columns = ["DetectGPT", "Perplexity_Score", "Burstiness_Score", "Grammarly", "OpenAI", "Originality"]


merged_df.replace([np.inf, -np.inf], np.nan, inplace=True)

merged_df.dropna(inplace=True)

scaler = MinMaxScaler()
 
df_scaled = scaler.fit_transform(merged_df.to_numpy())
df_scaled = pd.DataFrame(df_scaled, columns=["DetectGPT", "Perplexity_Score", "Burstiness_Score", "Grammarly", "OpenAI", "Originality"])
 
print("Scaled Dataset Using MinMaxScaler")
df_scaled.head()

df_scaled.to_csv("Scores.csv", index=False)

