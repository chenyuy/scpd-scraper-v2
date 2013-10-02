import os
import sys
import time

from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

driver = None

def login():
    global driver

    username = raw_input("Your SuID: ")
    password = getpass("Your password: ")

    driver = webdriver.Firefox()
    driver.implicitly_wait(2)
    driver.get("http://myvideosu.stanford.edu")

    suid_input = driver.find_element_by_id("username")
    suid_input.send_keys(username)

    passwd_input = driver.find_element_by_id("password")
    passwd_input.send_keys(password)
    passwd_input.send_keys(Keys.RETURN)

    try:
        suid_input = driver.find_element_by_id("username")
        print "Login failed. Please check your SUID and password."
        driver.close()
        sys.exit(1)
    except NoSuchElementException as e:
        pass

    try:
        code_input = driver.find_element_by_id("otp")
        code_input.send_keys(raw_input("Enter the authentication code: "))
        code_input.send_keys(Keys.RETURN)
    except NoSuchElementException as e:
        print "Two step authentication is not used."

    try:
        code_input = driver.find_element_by_id("otp")
        print "Two step authentication failed."
        driver.close()
        sys.exit(1)
    except NoSuchElementException as e:
        print "Login succeeded."

def getVideoLink(link):
    link.click()
    waiter = WebDriverWait(driver, 10)
    windows = waiter.until(lambda driver: driver.window_handles if len(driver.window_handles) > 1 else False)
    driver.switch_to_window(windows[1])
    video = driver.find_element_by_tag_name("object").get_attribute("data")
    video = video.replace("http", "mms").replace(" ", "%20")
    driver.close()
    driver.switch_to_window(windows[0])
    return video

def downloadAll(courses):
    course_links = {}
    for course in courses:
        try:
            links = []
            course_link = driver.find_element_by_link_text(course)
            course_link.click()

            header_links = driver.find_elements_by_class_name("accordion-header")
            for header_link in header_links:
                waiter = WebDriverWait(driver, 10)
                header_link.click()
                time.sleep(1)
                video_links = driver.find_elements_by_link_text("WMP")
                for link in video_links:
                    video_link = getVideoLink(link)
                    links.append(video_link)
                    print "Found link for %s: %s" % (course, video_link)

            course_links[course] = links
            driver.back()

        except NoSuchElementException as e:
            print 'The course "%s" is not found' % course
            continue
    driver.close()

    print "Ready to download the videos..."
    for course in course_links:
        print 'Downloading videos for "%s"' % course
        directory_path = os.path.join(".", course)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
        for link in course_links[course]:
            video_name = link.split("/")[-1]
            video_name_parts = video_name.split("-")
            video_name = video_name_parts[1] + "_" + video_name_parts[0]
            os.system('mimms -c "%s" "%s/%s"' % (link, directory_path, video_name))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Usage: python scraper.py course_name1 course_name2 ..."
        sys.exit(1)

    login()
    downloadAll(sys.argv[1:])

