import configparser
import datetime
import email
import imaplib
import inspect
import json
import os
import smtplib
import time
import traceback
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import parse_qs, urlparse

import numpy as np
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from url_endpoints import *

message = []
error_msg = ""
initial_start_time = ''




def get_company():                                          #2
    global message, error_msg
    try:
        authorization_code = get_access_code()
        print("access code --------------------------", authorization_code)
        access_token_response = get_access_token(authorization_code)
        print("access_token_response--------------------------", access_token_response)
        tokens = json.loads(access_token_response.text)
        print("tokenss------------------------------", tokens)
        access_token = tokens['access_token']
        api_call_headers = {'Authorization': 'Bearer ' + access_token,
                            'x-myobapi-cftoken': 'base64_username:base64_password',
                            'x-myobapi-key': client_id,
                            'x-myobapi-version': 'v2'}
        api_call_response = requests.get(test_api_url, headers=api_call_headers)
        company_data = api_call_response.text
        company_data = json.loads(company_data)
        company_data_df = pd.DataFrame(company_data)
        return company_data_df, tokens
    except Exception as e:
        print("Error :", e)
        print(traceback.format_exc())
        if len(message) <= 0:
            message.append("Access Code is not correct")
            error_msg = error_msg + str(e) + "\n" + str(traceback.format_exc())
        return

def get_access_code():                                                         #3
    global message, error_msg
    try:
        initial_start_time = datetime.now()
        settings = propertyConnection()          #.....4
        xero_username = settings.get('xero', 'username')
        xero_password = settings.get('xero', 'password')
        print("credential---------------", xero_username, xero_password)
        executable_path = settings.get('path', 'executable_path')                  #?
        print("Executable path------------", executable_path, authorize_url, callback_url)
        authorization_redirect_url = authorize_url + '?response_type=code&client_id=' + client_id + \
                                     '&redirect_uri=' + callback_url + '&scope=' + scope
        print("authorization_redirect_url--------------------", authorization_redirect_url)
        options = webdriver.FirefoxOptions()                                                #open browser
        print("here@@@@@@@@@@@@@@@@@@@@@@@@@")
        options.add_argument("start-maximized")
        print("here###############")
        options = Options()
        # options.add_argument('--headless')
        browser = webdriver.Firefox(options=options, executable_path=executable_path + "\geckodriver.exe",
                                    service_log_path=executable_path + "\log\geckodriver.log")
        browser.get(authorization_redirect_url)
        # time.sleep(2)
        action = webdriver.ActionChains(browser)

        # emailElem = browser.find_element_by_id('UserName')
        emailElem = browser.find_element_by_id('xl-form-email')
        print("xero_username", xero_username)
        emailElem.send_keys(xero_username)
        browser.find_element_by_xpath('//button[@type="submit"]').click()
        passwordElem = browser.find_element_by_id('Password')
        passwordElem.send_keys(xero_password)
        browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(50)
        # otp = get_email_otp()
        otp = 123
        print("otp :", otp)
        if len(otp) <= 0:
            message.append("Invalid OTP")
            return
        otpElem = browser.find_element_by_id('Token')
        otpElem.send_keys(otp)
        time.sleep(5)
        browser.find_element_by_xpath('//button[@type="submit"]').click()
        time.sleep(10)
        redirected_url = browser.current_url
        # browser.close()
        browser.quit()
        redirect_params = dict(parse_qs(urlparse(redirected_url).query))
        authorization_code = redirect_params['code']
        return authorization_code
    except Exception as e:
        message.append("Access code generation failed")
        error_msg = error_msg + str(e) + "\n" + str(traceback.format_exc())
        return

def get_access_token(authorization_code):
    data = {'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': callback_uri,
            'scope': 'CompanyFile'}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    access_token_response = requests.post(token_url, data=data, headers=headers)
    print("Got access token successfully")
    return access_token_response

def propertyConnection():                                             #4   p
    """Import ini config file"""
    settings = configparser.ConfigParser()
    settings._interpolation = configparser.ExtendedInterpolation()    #ExtendedInterpolation()..??
    dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    settings.read(dir + os.sep + 'config.ini')
    settings.sections()
    return settings

settings = propertyConnection()      #p
authorize_url = settings.get('urls', 'authorize_url')
token_url = settings.get('urls', 'token_url')
callback_uri = settings.get('urls', 'callback_uri')
callback_url = settings.get('urls', 'callback_url')     #not in myob
scope = settings.get('urls', 'scope')                   #not in myob
test_api_url = settings.get('urls', 'test_api_url')
client_id = settings.get('client', 'client_id')
client_secret = settings.get('client', 'client_secret')
ROOT_DIR = os.path.abspath(os.curdir)

def main():                                                      #1

    global message, error_msg

    initial_start_time = datetime.now()                         #to get current date time
    current_time = initial_start_time.strftime("%H:%M:%S")      #to extract H M S
    print("Execution started : ", current_time)
    company_data_df, tokens = get_company()
    print("running..........")
    return



if __name__ == '__main__':
    main()