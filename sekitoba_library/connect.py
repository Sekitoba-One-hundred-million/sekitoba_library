import time
import requests
import os
from os.path import expanduser
from requests.exceptions import Timeout
from selenium import webdriver
from selenium.webdriver.common.by import By

def netkeiba_login():
    f = open( expanduser( "~" ) + "/.pwd/password.txt" )
    str_data = f.readlines()
    str_data = str_data[0].replace( "\n", "" ).split( " " )
    f.close()

    mail = str_data[0]
    password = str_data[1]

    data = {}
    data["pid"] = "login"
    data["action"] = "auth"
    data["return_url2"] = ""
    data["mem_tp"] = ""
    data["login_id"] = mail
    data["pswd"] = password
    data["x"] = 270
    data["y"] = 7

    url = "https://regist.netkeiba.com/account/"
    r = requests.post( url, data = data )

    if len( r.history ) == 0:
        print( "パスワードまたはメールアドレスが違います" )
        return None
    
    return r.history[0].cookies        

def request( url, cookie = None ):
    for i in range( 0, 15 ):
        try:
            r = requests.get( url, cookies = cookie, timeout = 3 )
            return r, True
        except:
            time.sleep( 3 )

    return 0, False

def driver_start():
    return webdriver.Chrome( os.environ['HOME'] + "/chrome/chromedriver" )

def driver_request( driver, url ):
    driver.set_page_load_timeout( 6 )

    for i in range( 0, 15 ):
        try:
            driver.get( url )
            return driver, False
        except:
            time.sleep( 2 )

    return driver, True

def login( driver ):
    f = open( expanduser( "~" ) + "/.pwd/password.txt" )
    str_data = f.readlines()
    str_data = str_data[0].replace( "\n", "" ).split( " " )
    f.close()

    mail = str_data[0]
    password = str_data[1]
    driver, _ = driver_request( driver, 'https://regist.netkeiba.com/account/?pid=login' )
    time.sleep( 1 )
    
    id_box = driver.find_element( By.NAME, "login_id" )
    id_box.send_keys( mail )

    ps_box = driver.find_element( By.NAME, "pswd" )
    ps_box.send_keys( password )

    driver.find_element( By.XPATH, '/html/body/div[1]/div/div/form/div/div[1]/input' ).click()
    time.sleep( 3 )
    return driver

