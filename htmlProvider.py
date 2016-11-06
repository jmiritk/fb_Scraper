
# -*- coding: utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


NUM_OF_SCROLL_DOWN = 1

class HtmlProvider(object):
    def __init__(self, config):
        self.config = config

    #config environment to use selenium with Chrome
    def openBrowser(self,):
        path = self.config["software_info"]["chrome_driver_path"]
        os.environ["webdriver.chrome.driver"] = path
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(path, chrome_options=chrome_options)


    def loginToFb(self):
        driver = self.openBrowser()
        driver.get(self.config["fb_link"]["group_path"])
        driver.find_element_by_id("email").send_keys(self.config["fb_auth"]["email"])
        driver.find_element_by_id("pass").send_keys(self.config["fb_auth"]["password"])
        button_id = 'loginbutton' #'u_0_9'#
        driver.find_element_by_id(button_id).send_keys(Keys.ENTER)
        return driver


    #We can only simulate real user - so we scroll down to have apreopreate amount of data
    def getFbHtml(self):
        driver = self.loginToFb()
        try:
            for i in xrange(0, NUM_OF_SCROLL_DOWN):
                #self.clickCommentButtons(driver)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            html = driver.page_source

        except Exception as e:
            print(e)

        finally:
            driver.close()

        if html:
            return html


    #click on the button at the bottom of the post - 'show all x comments'
    def clickCommentButtons(self, driver):
        comment_buttons = driver.find_elements_by_class_name('UFIPagerLink')
        for btn in comment_buttons:
            if btn.is_displayed():
                driver.execute_script("arguments[0].click();", btn)




