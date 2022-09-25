"""
IMPORTANT NOTE: Do not have 2FA for either facebook or tinder.  This script will not work if it is turned on for either.

This script will log into your tinder account through your facebook that should be linked prior.
Keep in mind the amount of swipes to the right will be limited by your tinder account type.  At the time of writing this
the maximum amount of right swipes is limited to 100/day for a free account.  You can change the swipe variable below if
 you have a different account type.  I also set the "swipe direction" as a variable if you want to change that easily.

Another note to keep in mind is this script allows for tinder to access your location.  This script will automatically
select "Allow" if this notification pops up.  This needs to be allowed to use tinder.

This script also automatically turns off notifications if you do not already have it set in your settings.

I recommend adding tinder to your homepage through settings to eliminate a popup to do so.  This will happen after
about 6 right swipes.

"""

"""Import and install appropriate modules below."""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
import random

# Put your own credentials here.  Ensure there is no 2FA turned on for tinder or facebook or this will not work.
EMAIL_ADDRESS = "YOUR OWN EMAIL ADDRESS HERE"
FACEBOOK_PASSWORD = "YOUR FACEBOOK PASSWORD"

# Set how many times you want to swipe right.  Depending on your account type this will be limited.  For the free
# account, you are only allowed 100 swipes to the right per day.
amount_of_swipes = 100

# This switches the direction of the swipe.  It is by default set to "RIGHT" but you can set it to "LEFT" if you would
# like to never meet anyone.
swipe_direction = Keys.RIGHT

"""Need to install the appropriate browser driver and place .exe in accessible file."""
# Chrome driver path should reference the .exe browser driver.
chrome_driver_path = "E:\Py Code\Development\chromedriver.exe"

# Access the driver
driver = webdriver.Chrome(executable_path=chrome_driver_path)

# URL for front page of tinder.
URL = "https://tinder.com/"

# Open the website.
driver.get(url=URL)

# Setting the current window handle to get back to dashboard
main_page = driver.current_window_handle

# Sleep for 1 seconds to load page.
time.sleep(1)

# Click on "Sign In" Button.
driver.find_element(
    By.XPATH,
    "//*[@id='s1362659109']/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]"
).click()

# Sleep for 1 seconds to load page.
time.sleep(1)

# Click on "Login with facebook" button.
driver.find_element(By.XPATH, "//button[@aria-label='Log in with Facebook']").click()

# Sleep for 2 seconds to load page.
time.sleep(2)

# Utilizing driver.window_handles, we can access the list of current handles.  Only two should exist, the main page and
# the login page.  Since we set the main page above, then the other handle should be login page.
# Change the handle to access the login page that pops up
for handle in driver.window_handles:
    if handle != main_page:
        login_page = handle

# Change the controls to the login page
driver.switch_to.window(login_page)

# Autofill the Email or Phone Input box.  Feel free to change the above email address to either.
# Do not use any symbols or country codes when putting in your phone number.
driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/form/div/div[1]/div/input").send_keys(EMAIL_ADDRESS)

# Autofill the Password input.
driver.find_element(By.XPATH, "//*[@id='pass']").send_keys(FACEBOOK_PASSWORD)

# Click on "Log In" button.
driver.find_element(By.ID, "loginbutton").click()

# Switch back to the main page for control.
driver.switch_to.window(main_page)

# Sleep for 5 seconds to load page.
time.sleep(5)

# Click the "ALLOW" button for tinder to access your location.  This may not appear for some depending on your allowed
# settings through your browser.
try:
    driver.find_element(By.XPATH, "//*[@id='s-365721967']/main/div/div/div/div[3]/button[1]").click()
except NoSuchElementException:
    pass

# Click the "NOT INTERESTED" button for disabling notifications if it is not already set.  If you have already set this
# in your settings than it will pass the try.
try:
    driver.find_element(By.XPATH, "//*[@id='s-365721967']/main/div/div/div/div[3]/button[2]/span").click()
except NoSuchElementException:
    pass

# Sleep for 2 seconds to see if cookies pops up.
time.sleep(2)

# Click the "Allow Cookies" button if it pops up.
try:
    driver.find_element(By.XPATH, "//*[@id='content']/div/div[2]/div/div/div[1]/button").click()
except NoSuchElementException:
    pass

# Sleep for 5 seconds to load page.
time.sleep(5)

# Run while loop that will continually wipe right while there are swipes available
while amount_of_swipes != 0:
    # Send the right arrow to the main page to swipe right.  This can be changed to the left arrow.  This try will
    # also catch instances where a match may pop up.
    try:
        driver.find_element(By.XPATH, "//body").send_keys(swipe_direction)
    except ElementClickInterceptedException:
        try:
            driver.find_element(By.CSS_SELECTOR, ".itsAMatch a").click()
        except NoSuchElementException:
            pass
        # Sometimes a popup will after 6 swipes asking if you want to add Tinder to your home screen.  This
        # clicks "Not Interested".  I would recommend adding it to your home screen to avoid this issue.  Or you can
        # wait till the 6th swipe and click "Not Interested" yourself.  This will not interrupt the script.
        try:
            driver.find_element(By.XPATH, "//*[@id='s-365721967']/main/div/div[2]/button[2]/div[2]/span[2]")
        except NoSuchElementException:
            pass
    # This time delay is here to try to throw tinder off from spotting a bot.
    time.sleep(random.randint(2, 8))
    amount_of_swipes -= 1








