from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import yaml
import sys


def check(user, password):
    driver = webdriver.Chrome('./chromedriver.exe')
    driver.get('https://becasprogresar.educacion.gob.ar/#sesion')
    eleShowMsgBtn = driver.find_element_by_class_name('btn-success')
    eleShowMsgBtn.click()
    time.sleep(1)
    user_input = driver.find_element_by_id("usuarioz")
    user_input.click()
    user_input.send_keys(user)
    password_input = driver.find_element_by_name("contraz")
    password_input.click()
    password_input.send_keys(password)
    button = driver.find_element_by_id("ingreza")
    button.click()
    time.sleep(1)
    page = driver.page_source
    parsed_html = BeautifulSoup(page, features="html.parser")
    driver.close()
    return parsed_html.body.find('div', attrs={'class':'alert alert-primary'}).text


def get_credentials():
    with open('credentials.yaml', 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def log_in_email(mail_credentials):
    import smtplib

    gmail_user = mail_credentials['user']  
    gmail_password = mail_credentials['password']

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:  
        print('Something went wrong logging in ...')
    return server


def send_email(mail_credentials, send_to, message):
    server = log_in_email(mail_credentials)
    sent_from = mail_credentials["user"]
    to = send_to
    subject = 'Hubieron cambios en la pagina de progresar'  
    body = 'Wacho entra ya a la pagina: https://becasprogresar.educacion.gob.ar'

    msg = "\r\n".join([
    "From: {}".format(sent_from),
    "To: {}".format(to),
    "Subject: {}".format(subject),
    "",
    "` {} `".format(body)
    ])

    try:  
        server.sendmail(sent_from, to, msg)
        server.close()

        print('Email sent!')
    except:  
        print('Something went wrong while sending the email...')


def demon(user, password, mail_credentials, send_to):
    result = check(user, password)
    print(result)
    new_result = result
    while result == new_result:
        time.sleep(1800)
        new_result = check(user, password)
        print(new_result)
        # break
    send_email(mail_credentials, send_to, new_result)


def main(send_to):
    credentials = get_credentials() 
    demon(credentials["progresar"]["user"], credentials["progresar"]["password"], credentials["mail"], send_to)
    

if __name__ == '__main__':
    args = sys.argv
    emails_to = args[1:]
    main(emails_to)