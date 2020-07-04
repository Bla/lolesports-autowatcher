# LoL Esports Autowatcher
This script automatically rotates between unwatched LoL Esports games to help you finish your Esports missions.

## Getting Started
### Requirements:
- Python 3
- Selenium (`pip install selenium`)
- Google Chrome WebDriver
  - Visit: https://sites.google.com/a/chromium.org/chromedriver/ 
  - Download the ChromeDriver with the same version number as your installed Google Chrome browser (most likely the latest stable release)
  - Unpack the driver and place it in the same folder as `lolesports-watcher.py`

### Customization:
- This script uses Google Chrome by default. If you use another browser, get the appropriate WebDriver and change the following line in the code to reflect this:  
`driver = webdriver.Chrome()`
- To change the number of games to watch, find the following line and change the value:  
`NUMBER_OF_GAMES = 15`
- The script will wait for 30 seconds at the login page. If you need more time to fill in your login details, find the following line and change the value:  
`time.sleep(30)`
- The script will watch games from the LEC league by default. If you want to watch a different league instead, find the following line and replace LEC_VOD_URL with your league of choice (other options: `LCS_VOD_URL`, `LCK_VOD_URL`, `LPL_VOD_URL`):  
`driver.get(LEC_VOD_URL)`
- The script will wait 13 minuntes before rotating to the next game. This should be more than enough for the game to count towards your missions. To change this, edit the following line:  
`watch_time_in_minutes = 13`

## Running the script
- Run `python lolesports-watcher.py`. _A new Chrome window be started and you will be redirected to the lolesports.com login page._
- Fill in your username and password and wait. _It is not necessary to click the login button, as the script will automatically do it for you after 30 seconds._
- Do whatever you want, the script will finish your missions for you (:
