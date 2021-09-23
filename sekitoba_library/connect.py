import time
import requests
from os.path import expanduser
from requests.exceptions import Timeout

def request( url ):
    for i in range( 0, 15 ):
        try:
            r = requests.get( url, timeout = 3 )
            return r, True
        except:
            time.sleep( 3 )

    return 0, False

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
    id_box = driver.find_element_by_name("login_id")
    id_box.send_keys( mail )

    ps_box = driver.find_element_by_name("pswd")
    ps_box.send_keys( password )

    driver.find_element_by_xpath( '/html/body/div[1]/div/div/form/div/div[1]/input' ).click()
    time.sleep( 3 )
    return driver

