"""
LoL Esports Auto Viewer

"""

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re
import time

HOMEPAGE_URL = "https://lolesports.com/"
VOD_URL = "https://lolesports.com/vods/lec/lec_2021_summer"
REGEX = r"vod/\d{18}/\d" # RegEx for URL pattern, e.g.: /vod/123456789012345678/1
NUMBER_OF_GAMES = 15 # Set the number of games to watch
WATCH_TIME_IN_MINUTES = 13 # Should watch long enough for it to count towards missions
MUTE_AUDIO = True

# Open a Chrome browser window
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
if MUTE_AUDIO:
    chrome_options.add_argument("--mute-audio")
    print("\nOpening browser (muted)\n")
else:
    print("\nOpening browser\n")
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_position(0, 0)
driver.set_window_size(1050, 768)

# Get rid of the cookie popup and visit the login page
driver.get(HOMEPAGE_URL)
WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div[2]/button[1]'))).click()
login_button = driver.find_element_by_xpath('//*[@id="riotbar-right-content"]/div[3]/div/a')
login_button.click()

# Enter your login details within 20 seconds. Note: The script will automatically click the login button afterwards.
time.sleep(20)
try:
    driver.find_element_by_xpath('//*[@title="Sign In"]').click()
except NoSuchElementException:
    pass

# Create an empty VOD list
url_list = []

# Wait until page is loaded before visiting the selected VOD url
WebDriverWait(driver, 30).until(ec.visibility_of_element_located((By.ID, "riotbar-account-bar")))
driver.get(VOD_URL)

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
url_list.reverse()
print("List of unwatched games obtained\n")

# Watch games and logout/quit after NUMBER_OF_GAMES
watch_counter = 0
youtube_frame = '//iframe[starts-with(@src, "https://www.youtube.com/embed")]'
for i, url in enumerate(url_list):
    driver.get(url)
    time.sleep(10)
    driver.switch_to.frame(driver.find_element_by_xpath(youtube_frame))
    WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play (k)"]'))).click()
    print("[{}/{}] Now watching {}".format(i + 1, NUMBER_OF_GAMES, url))
    for minute in range(WATCH_TIME_IN_MINUTES):
        time.sleep(60)
        print("{}.. ".format(minute + 1), end="")
    print("Done!\n")
    watch_counter += 1
    if watch_counter != NUMBER_OF_GAMES:
        continue
    else:
        driver.switch_to.default_content()
        hover_element = driver.find_element_by_id("riotbar-account-bar")
        ActionChains(driver).move_to_element(hover_element).perform()
        driver.find_element_by_xpath('//*[@id="riotbar-account-dropdown-links"]/a[2]').click()
        driver.quit()
        print("Task completed: " + str(NUMBER_OF_GAMES) + " game(s) watched.\n")
        break
