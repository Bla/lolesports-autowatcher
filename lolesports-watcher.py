"""
LoL Esports Auto Viewer

"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import time

HOMEPAGE_URL = "https://watch.lolesports.com/"
WORLDS_VOD_URL = "https://lolesports.com/vods/worlds/worlds_2020"
# LEC_VOD_URL = "https://watch.lolesports.com/vods/lec/lec-summer-2020"
# LCS_VOD_URL = "https://watch.lolesports.com/vods/lcs/lcs-summer-2020"
# LCK_VOD_URL = "https://watch.lolesports.com/vods/lck/lck-summer-2020"
# LPL_VOD_URL = "https://watch.lolesports.com/vods/lpl/lpl-summer-2020"
REGEX = r"vod/\d{18}/\d" # RegEx for URL pattern, e.g.: /vod/123456789012345678/1
NUMBER_OF_GAMES = 15 # Set the number of games to watch
MUTE_AUDIO = True 

# Open a Chrome browser window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
if MUTE_AUDIO:
    chrome_options.add_argument("--mute-audio")
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_position(0, 0)
driver.set_window_size(1050, 768)

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
driver.get(WORLDS_VOD_URL)

# Populate VOD list with URL of unwatched games
WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.CLASS_NAME, "game-selector")))
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
youtube_frame = '//iframe[starts-with(@src, "https://www.youtube.com/embed")]'
for url in url_list:
    driver.get(url)
    WebDriverWait(driver, 10).until(ec.visibility_of_element_located((By.XPATH, youtube_frame)))
    driver.switch_to.frame(driver.find_element_by_xpath(youtube_frame))
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play (k)"]'))).click()
    print("Now watching " + url)
    time.sleep(watch_time_in_minutes * 60)
    print("Done!\n")
    watch_counter += 1
    if watch_counter == NUMBER_OF_GAMES:
        hover_element = driver.find_element_by_id("riotbar-account");
        action = ActionChains(driver)
        action.move_to_element(hover_element).perform()
        driver.find_element_by_xpath("//*[@data-riotbar-account-action='logout']").click()
        driver.quit()
        print(str(NUMBER_OF_GAMES) + "game(s) watched.")
        break
