from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import numpy as np
import pandas as pd
import time
import pickle
from selenium.webdriver.common.keys import Keys;

def grammarly_scoring(text_dataset):
    driver_location = "/usr/bin/chromedriver"
    pickle_location = "grammarly.pkl"
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)
    grammarly_query = "https://app.grammarly.com" 
    grammarly_driver, grammarly_input = initialize_grammarly_driver(driver_location, chrome_options, grammarly_query, pickle_location)
    scores = pd.DataFrame(columns = ['Score'])
    checkpoint_after = 10

    for index, row in text_dataset.iterrows():
        try:
            score, grammarly_input, grammarly_driver = get_plagiarism(grammarly_driver, grammarly_input, row['Text'])
            scores = scores.append({'Score': score}, ignore_index = True)
        except:
            scores = scores.append({'Score': np.NAN}, ignore_index = True)
        
        if index % checkpoint_after == 0:
            scores.to_csv("Grammarly_Scores.csv")

    scores.to_csv("Grammarly_Scores.csv")

    return "Grammarly_Scores.csv"

def initialize_grammarly_driver(driver_location, chrome_options, query, pickle_location):    

    driver = webdriver.Chrome(driver_location, chrome_options = chrome_options) #Initializing selenium chromedriver
    
    driver.get(query)
    cookies = pickle.load(open(pickle_location, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get(query)

    time.sleep(5)
    new = driver.find_element(By.XPATH, "//*[@id='page']/div/div/main/div[4]/div/section/div/div/div[1]/div/div[2]/div")
    new.click()

    time.sleep(5)
    input = driver.find_element(By.XPATH, "//*[@id='page']/div/div[2]/div[2]/div/div[4]/div[3]/div/main/div/div/div[10]/div[1]/p")
    input.send_keys("Test")

    time.sleep(5)
    plag = driver.find_element(By.XPATH, "//*[@id='navbar-right']/div[2]/div/div[3]/div[3]")
    plag.click()

    return driver, input

def get_plagiarism(driver, input, text):
    
    input.send_keys(text)

    time.sleep(10)
    if(driver.find_elements(By.XPATH, "//*[name() = 'svg'][contains(@class, 'circular_f1rbnyxg')]/*[name()='text']")):
        b6 = driver.find_element(By.XPATH, "//*[name() = 'svg'][contains(@class, 'circular_f1rbnyxg')]/*[name()='text']")
        input.clear()
        return np.float16(b6.text.replace("%","")), input, driver

    input.clear()
    return 0, input, driver


