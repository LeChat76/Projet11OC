import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from server import replace_data_files


@pytest.mark.func_test
def testFonctional():
    # replace json files for the test
    replace_data_files()

    # create firefox session
    browser = webdriver.Firefox()

    # open GUDLFT web site
    browser.get("http:/localhost:5000")
    assert 'GUDLFT Registration' == browser.title

    # search 'email' input field + fillin with value 'admin@irontemple.com'
    search_field = browser.find_element(By.NAME, 'email')
    search_field.send_keys('admin@irontemple.com')
    time.sleep(1)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)

    # click on link for purchase places in 'Fall Classic' competition
    browser.find_element(By.XPATH, '//a[@href="/book/Fall%20Classic/Iron%20Temple"]').click()

    # search 'places' input field
    search_field = browser.find_element(By.NAME, 'places')
    time.sleep(1)

    # fillin with value '3'
    search_field.send_keys('1')
    time.sleep(1)
    search_field.send_keys(Keys.RETURN)
    time.sleep(1)

    #logout
    browser.find_element(By.XPATH, '//a[@href="/logout"]').click()

    # Close web browser
    browser.quit()
