import time
import requests
import os
import urllib
import subprocess
import warnings
import timeout_decorator
from os.path import expanduser
from requests.exceptions import Timeout
from selenium import webdriver
from selenium.webdriver.common.by import By

warnings.simplefilter( 'ignore' )

proxyUse = True
DOMAIN_NAME = ""
domainFilePath = "/Volumes/Gilgamesh/proxy/domain"

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
    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36" }
    r = requests.post( url, headers = headers, data = data )

    if len( r.history ) == 0:
        print( "パスワードまたはメールアドレスが違います" )
        return None
    
    return r.history[0].cookies        
    
def wait_proxy( remove = False ):
    if remove:
        if os.path.isfile( domainFilePath ):
            print( "remove: {}".format( domainFilePath ) )
            os.remove( domainFilePath )

    while 1:
        if not os.path.isfile( domainFilePath ):
            time.sleep( 1 )
        else:
            break

    f = open( domainFilePath )
    strData = f.readlines()
    domainName = strData[0].replace( "\n", "" )
    return domainName
        
def request( setUrl, cookie = None ):
    global DOMAIN_NAME
    url = setUrl

    if not os.path.isfile( domainFilePath ) and proxyUse:
        DOMAIN_NAME = wait_proxy()

    host = urllib.parse.urlparse( setUrl ).netloc

    if len( DOMAIN_NAME ) == 0 and proxyUse:
        DOMAIN_NAME = wait_proxy()

    headers = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
                "Host": host }

    for i in range( 0, 15 ):
        if proxyUse:
            url = setUrl.replace( host, DOMAIN_NAME )

        try:
            r = requests.get( url, headers = headers, cookies = cookie, timeout = 3, verify = False )

            if not r.status_code == 200:
                print( "status:{} {}".format( r.status_code, url ) )
            
            if r.status_code == 400 and proxyUse:
                DOMAIN_NAME = wait_proxy( remove = True )
                continue

            return r, True
        except:
            if proxyUse:
                DOMAIN_NAME = wait_proxy()
            
            time.sleep( 3 )

    return 0, False

def driver_start():
    driver = webdriver.Chrome( os.environ['HOME'] + "/chrome/chromedriver" )
    return driver

@timeout_decorator.timeout( 15 )
def driverGet( driver, url ):
    driver.get( url )
    return driver

def driver_request( driver, url ):
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
    driver, _ = driver_request( driver, 'https://regist.netkeiba.com/account/?pid=login' )
    time.sleep( 1 )
    
    id_box = driver.find_element( By.NAME, "login_id" )
    id_box.send_keys( mail )

    ps_box = driver.find_element( By.NAME, "pswd" )
    ps_box.send_keys( password )

    driver.find_element( By.XPATH, '/html/body/div[1]/div/div/form/div/div[1]/input' ).click()
    time.sleep( 3 )

    return driver
