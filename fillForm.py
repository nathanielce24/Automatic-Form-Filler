import time
import json
import selenium
from os import path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

def readBrokerInfo(path):
    with open(path, 'r') as broker_info:
        return json.load(broker_info)
    
def readUserInfo(path):
    with open(path, 'r') as user_info:
        return json.load(user_info)
   
def loadPage(broker_info):
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(broker_info["url"])
    wait = WebDriverWait(browser, 10)
    return browser, wait

def clickXpath(xPath, browser, wait):  #clicks an element given the xpath of the element
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xPath)))
    browser.execute_script("arguments[0].scrollIntoView();", element)  
    element.click()

def clickID(id, browser, wait):   #clicks an element given the id of the element
    element = wait.until(EC.element_to_be_clickable((By.ID, id)))
    browser.execute_script("arguments[0].scrollIntoView();", element)  
    element.click()

def dropMenu(id, value, browser, wait):   #selects an option from a dropdown menu given the id and intended value
    element = wait.until(EC.presence_of_element_located((By.ID, id))) 
    browser.execute_script("arguments[0].scrollIntoView();", element)
    select = Select(element)
    select.select_by_value(value)

def fillTextbox(name, value, browser, wait):  #fills a textbox given the name of the box and value
    element = wait.until(EC.presence_of_element_located((By.NAME, name)))
    browser.execute_script("arguments[0].scrollIntoView();", element)
    element.send_keys(value) 

def fillForm(broker_path, user_path): 
    broker_info = readBrokerInfo(broker_path)
    user_info = readUserInfo(user_path)
    browser, wait = loadPage(broker_info)

    browser.execute_script("window.scrollBy(0, 1);")

    if (broker_info.get("iFrame") != ""):    #switches to iframe if neccesary
        iframe = broker_info.get("iFrame")
        browser.switch_to.frame(iframe)

    for action in broker_info["Actions"]:  #iterates sequentially through actions

        actionType = broker_info["Actions"][action][0]
        byType = broker_info["Actions"][action][1]
        id = broker_info["Actions"][action][2]
        value = ''

        if len(broker_info["Actions"][action])>=4: #Checks if element needs a value (Ex. Textboxes)
            value = broker_info["Actions"][action][3]
        if "USER" in value:
             value = user_info[value.split()[1]]
             
        match actionType:  #Executes action
            case 'click':
                if byType == 'xpath':      
                    clickXpath(id, browser, wait)        
                if byType == 'ID':
                    clickID(id, browser, wait)
            case 'dropmenu':
                if byType == 'ID':
                    dropMenu(id, value, browser, wait)
            case 'text':
                if byType == 'name':
                    fillTextbox(id, value, browser, wait)

    time.sleep(100)

fillForm(r'C:\Users\natha\projects\EzOptOut\acxiom.json', 
         r'C:\Users\natha\projects\EzOptOut\userinfo.json')



