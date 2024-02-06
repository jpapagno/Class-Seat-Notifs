import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import base64
from email.mime.text import MIMEText
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime
from selenium.webdriver.chrome.options import Options

def main():
    while True:
        activate()
        time.sleep(300)

# Course: (course_code, course_name)
def activate():
    email_to_courses = {"example1@school.edu": [("16626", "international orgo", [18])],
                        "example2@gmail.com": [("18268", "AI")]}
    driver = setup_driver()
    for receiver, courses in email_to_courses.items():
        for course in courses:
            class_code = course[0]
            class_name = course[1]
            group_list = []
            if len(course) == 3:
                group_list = course[2]
            sel_call = None
            try:
                sel_call = check_course(class_code, driver, group_list)
            except Exception as e:
                print(f'sel failed with course: {class_name}({class_code}) and person: {receiver}, {e}')
            
            if sel_call:
                
                for group, spots_left in sel_call.items():
                    print(f"time: {datetime.now()}, course_code: {class_code}, group: {group}, spots_left: {spots_left}, for: {receiver}")
                    
                    try:
                        send_email(class_code, group, spots_left, class_name, receiver)
                    except Exception as e:
                        print(f'email failed with course: {class_name}({class_code}) and person: {receiver}, {e}')

def setup_driver():
    print(f'Activating Selenium at: {datetime.now()}')
    # driver = webdriver.Chrome()
    # options = Options()
    # options.add_argument('--headless=new')
    driver = webdriver.Chrome()
    user = 'USERNAME'
    passkey = 'PASSWORD'

    url = 'https://login.uc3m.es/index.php/CAS/login?service=https%3A%2F%2Fsigma.uc3m.es%2Fcosmos%2FentradaCAS%2F%3F%2540ebf2f349580da806%3D%25401bedd0984ff1624c%26%254057b88e10f1a90c1a%3D%2540f85cb32c02ba5707%26%2540d2e9d205e120747b%3D%2540a8d11ec374aa53249517ff409557c90948db35c1513aea9a%26%2540878832b545a60c10f8783e04f430b6cbcf0ca59017bf872c%3D%25404c3980ce660dc557%26iframe%3Dtrue%26css%3DcasSigma%26lang%3Des'
    driver.get(url)
    time.sleep(5)

    user_elem = driver.find_element(By.ID, 'edit-name')
    user_elem.send_keys(user)

    pass_elem = driver.find_element(By.ID, 'edit-pass')
    pass_elem.send_keys(passkey)

    driver.find_element(By.ID, 'submit_ok').click()
    time.sleep(5)

    # clicking big green thing
    driver.find_element(By.XPATH, '/html/body/div[3]/div[2]/div/div[2]/div/div/div/div/div[2]/div[2]/div[5]/a').click()
    time.sleep(5)

    # select ingles
    driver.find_element(By.CLASS_NAME, 'btnEng').click()
    time.sleep(5)

    # select dropdown of course registration cells
    select = Select(driver.find_element(By.NAME, '_codProceso'))
    select.select_by_value('1452')
    time.sleep(5)
    
    # accept for course reg cells
    driver.find_element(By.CLASS_NAME, 'btnAceptar').click()
    time.sleep(5)

    # change button
    driver.find_element(By.CLASS_NAME, 'btnModificar').click()
    time.sleep(5)

    return driver
 
# returns hashmap of {group_num : spots_left}
def check_course(course_code, driver, group_list):

    # text box for course code
    box = driver.find_element(By.NAME, '_asignatura')
    box.send_keys(Keys.CONTROL + "a")
    box.send_keys(Keys.DELETE)
    box.send_keys(course_code)
    box.send_keys(Keys.ENTER)
    time.sleep(2)

    out = {}
    for i in range(2, 10):
        for j in range(1, 3):
            try:
                lang = driver.find_element(By.XPATH, f"//*[@id=\"{j}\"]/td[2]/table[{i}]/tbody/tr[3]/td[2]/span/a").get_attribute('title')
                cur_group = int(driver.find_element(By.XPATH, f"//*[@id=\"{j}\"]/td[2]/table[{i}]/tbody/tr[1]/td[3]").get_attribute('innerHTML'))
                spots_left = int(driver.find_element(By.XPATH, f"//*[@id=\"{j}\"]/td[2]/table[{i}]/tbody/tr[2]/td[2]").get_attribute('innerHTML'))
                # if lang == "English" and spots_left > 0:
                #     print(f'NOT CHECKING GROUPS: course: {course_code}, cur_group: {cur_group}, spots_left: {spots_left}')
                if lang == "English" and (not group_list or cur_group in group_list) and spots_left > 0:
                    out[cur_group] = spots_left
            except Exception as error:
                if not type(error).__name__ == "NoSuchElementException":
                    print(f"THIS SHOULDNT HAPPEN, course: {course_code}, cur_group: {cur_group}, spots_left: {spots_left}, ERROR: {error}")
                continue
    return out


def send_email(class_code, group, spots_left, class_name, receiver):
    print('activating send_email: ', class_code, group, spots_left, class_name, receiver)
    SCOPES = [
            "https://www.googleapis.com/auth/gmail.send"
        ]
    credential_path = os.path.join('./', 'credential_sample.json')
    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets('token.json', SCOPES)
        credentials = tools.run_flow(flow, store)
    service = build('gmail', 'v1', credentials=credentials)

    message = MIMEText(f'Spot opened in class: {class_name}({class_code}), in group: {group}, with {spots_left} spots availabile')
    message['to'] = receiver
    message['subject'] = f'SPOT OPEN: {class_name}({group})'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

if __name__ == '__main__':
    main()
