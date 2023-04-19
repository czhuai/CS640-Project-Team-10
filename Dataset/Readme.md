This directory contains the dataset of this project. The following is the introduciton of each file:

1. scores.csv: This is the csv files used to train the models. Inside there is four columns like the following:
    PapersOwl: The originality obtained from PapersOwl
    GPTZero: The originality obtained from GPTZero
    DetectGPT: The originality obtained from DetectGPT
    Originality: The actual originality as ground truth.

2. 100_Dataset.csv, 40_Dataset.csv, 20_Dataset.csv: Contains 100, 40, 20 dounments and their actual originality respectively.

3. 40_human_text.csv: Contains 40 paragraphs written by Chen Zhu and their length

4. 34_generated_intro, 34_wiki_intro: Contains 34 paragraphs from model or wikipedia and their length. These parapgraphs are obtained from GPT-wiki-intro dataset "https://huggingface.co/datasets/aadityaubhat/GPT-wiki-intro"

5. Build_Dataset.ipynb: The python program to build the dataset by random choosing paragraphs from 40_human_text.csv, 34_generated_intro, and 34_wiki_intro and concate these paragraphs into one document.
