import time
import requests
import os
import subprocess
import timeout_decorator
from os.path import expanduser
from requests.exceptions import Timeout
from selenium import webdriver
from selenium.webdriver.common.by import By

driver_login_check = False
proxy = ""

def netkeibaLogin():
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
    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36" }
    r = requests.post( url, headers = headers, data = data )

    if len( r.history ) == 0:
        print( "パスワードまたはメールアドレスが違います" )
        return None
    
    return r.history[0].cookies        

def proxyStart():
    shellPath = "./module/proxy-manage.sh"

    if not os.path.isfile( shellPath ):
        exit( 1 )
    
    shellResult = subprocess.run("./module/proxy-manage.sh", shell = True, capture_output = True, encoding = "utf-8" )
    return shellResult.stdout.replace( "\n", "" )

def request( url, proxyUse = True, cookie = None ):
    if len( proxy ) == 0 and proxyUse:
        proxy = proxyStart()

    host = "race.netkeiba.com"
    url = url.replace( host, proxy )
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Host": "race.netkeiba.com"}
    
    for i in range( 0, 15 ):
        try:
            r = requests.get( url, headers = headers, cookies = cookie, timeout = 3 )

            if r.status_code == 400:
                proxy = proxyStart()
                continue
            
            time.sleep( 2 )
            return r, True
        except:
            time.sleep( 3 )

    return 0, False

def driverStart():
    driver = webdriver.Chrome( os.environ['HOME'] + "/chrome/chromedriver" )
    return driver

@timeout_decorator.timeout( 15 )
def driverGet( driver, url ):
    driver.get( url )
    return driver

def driverRequest( driver, url ):
    driver.set_page_load_timeout( 20 )

    for i in range( 0, 10 ):
        try:
            driver = driverGet( driver, url )
            break
        except timeout_decorator.timeout_decorator.TimeoutError:
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
    driver, _ = driverRequest( driver, 'https://regist.netkeiba.com/account/?pid=login' )
    time.sleep( 1 )
    
    id_box = driver.find_element( By.NAME, "login_id" )
    id_box.send_keys( mail )

    ps_box = driver.find_element( By.NAME, "pswd" )
    ps_box.send_keys( password )

    driver.find_element( By.XPATH, '/html/body/div[1]/div/div/form/div/div[1]/input' ).click()
    time.sleep( 3 )

    driver_login_check = True
    return driver

