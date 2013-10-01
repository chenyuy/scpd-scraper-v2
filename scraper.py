import os
import sys
import time

from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
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

def getVideoLink(link):
    time.sleep(3)
    link.click()
    time.sleep(3)
    windows = driver.window_handles
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
                header_link.click()
                time.sleep(2)
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
        for link in course_links[course]:
            os.system('mimms -c "%s"' % link)
        #directory = os.path.join("~", course)
        #if not os.path.exists(directory):
        #    os.makedirs(directory)
        #for link in course_links[course]:
        #    os.system('mimms -c "%s" "%s"' % (link, os.path.join(directory, link)))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Error: TODO"
        sys.exit(1)

    login()
    downloadAll(sys.argv[1:])

