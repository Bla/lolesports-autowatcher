"""
LoL Esports Auto Viewer

"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import time

HOMEPAGE_URL = "https://watch.lolesports.com/"
LEC_VOD_URL = "https://watch.lolesports.com/vods/lec/lec-summer-2020"
LCS_VOD_URL = "https://watch.lolesports.com/vods/lcs/lcs-summer-2020"
LCK_VOD_URL = "https://watch.lolesports.com/vods/lck/lck-summer-2020"
LPL_VOD_URL = "https://watch.lolesports.com/vods/lpl/lpl-summer-2020"
REGEX = r"vod/\d{18}/\d" # RegEx for URL pattern, e.g.: /vod/123456789012345678/1
NUMBER_OF_GAMES = 15 # Set the number of games to watch

# Open a Chrome browser window
driver = webdriver.Chrome()

# Visit the login page
driver.get(HOMEPAGE_URL)
driver.find_element_by_xpath("//*[@data-riotbar-link-id='login']").click()

# Enter your login details within x seconds. 
# Note: The script will automatically click the login button afterwards.
time.sleep(30)
driver.find_element_by_xpath('//*[@title="Sign In"]').click()

# Create an empty VOD list
url_list = []

# Wait until page is loaded before visiting the selected VOD url
WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.ID, "riotbar-account")))
driver.get(LEC_VOD_URL)

# Populate VOD list with URL of unwatched games
vod_urls = driver.find_elements_by_class_name("games")
for vod in vod_urls:
    innerHTML = vod.get_attribute("innerHTML")
    if "watched" in innerHTML:
        pass
    else:
        vod_url = HOMEPAGE_URL + re.search(REGEX, innerHTML).group()
        url_list.append(vod_url)

# Watch games and logout/quit after NUMBER_OF_GAMES
watch_counter = 0
watch_time_in_minutes = 13 # Should watch long enough for it to count towards missions
for url in url_list:
    driver.get(url)
    time.sleep(watch_time_in_minutes * 60)
    watch_counter += 1
    if watch_counter == NUMBER_OF_GAMES:
        driver.find_element_by_id("riotbar-account-bar").click()
        driver.find_element_by_xpath("//*[@data-riotbar-account-action='logout']").click()
        driver.quit()
        break
