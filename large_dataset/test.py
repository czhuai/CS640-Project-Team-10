from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import numpy as np
import pandas as pd
import time
import pickle
from selenium.webdriver.common.keys import Keys;

driver_location = "/usr/bin/chromedriver"
pickle_location = "grammarly.pkl"
query = "https://app.grammarly.com" 
scores = pd.read_csv('Grammarly_Scores.csv', index_col = None)
checkpoint_after = 10
text_dataset = pd.read_csv('text_dataset.csv')
driver = webdriver.Chrome(driver_location) #Initializing selenium chromedriver
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

time.sleep(5)

for index, row in text_dataset.iterrows():
    try:
        input.send_keys(Keys.CONTROL, "a")
        input.send_keys(Keys.DELETE)

        input = driver.find_element(By.XPATH, "//*[@id='page']/div/div[2]/div[2]/div/div[4]/div[3]/div/main/div/div/div[10]/div[1]/p")
        input.send_keys(row["Text"])

        time.sleep(10)

        if(driver.find_elements(By.XPATH, "//*[name() = 'svg'][contains(@class, 'circular_f1rbnyxg')]/*[name()='text']")):
            b6 = driver.find_element(By.XPATH, "//*[name() = 'svg'][contains(@class, 'circular_f1rbnyxg')]/*[name()='text']")
            score = np.float16(b6.text.replace("%",""))
        else:
            score = 0

        scores = scores.append({'Score': score}, ignore_index = True)

    except:
        driver.close()
        driver = webdriver.Chrome(driver_location) #Initializing selenium chromedriver
        driver.get(query)
        cookies = pickle.load(open(pickle_location, "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie
                              )
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

        time.sleep(5)

        scores = scores.append({'Score': np.NAN}, ignore_index = True)

    if index % checkpoint_after == 0:
        scores.to_csv("Grammarly_Scores.csv", index = False)

scores.to_csv("Grammarly_Scores.csv", index = False)




