from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from login import username, password
import numpy as np
import random
import traceback


class InstagramBot():
    def __init__(self, email, password):
        driver_path = '/home/carmelo/Documents/ig_bot/chromedriver_linux64/chromedriver'
        # brave_path = '/opt/brave.com/brave/brave-browser'
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(driver_path, chrome_options=self.browserProfile)
        self.email = email
        self.password = password

    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/')
        time.sleep(2)
        emailInput = self.browser.find_elements_by_css_selector('form input')[0]
        passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(2)

    def followWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text != 'Following'):
            followButton.click()
            time.sleep(2)
        else:
            print("You are already following this user")

    def unfollowWithUsername(self, username):
        self.browser.get('https://www.instagram.com/' + username + '/')
        time.sleep(2)
        followButton = self.browser.find_element_by_css_selector('button')
        if (followButton.text == 'Following'):
            followButton.click()
            time.sleep(2)
            confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
            confirmButton.click()
        else:
            print("You are not following this user")

    def getUserFollowers(self, username, max_followers):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < max_followers):
            followersList.click()
            time.sleep(0.5)
            followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            time.sleep(0.5)
            actionChain.key_down(Keys.SPACE).perform()
            time.sleep(0.5)
            actionChain.key_up(Keys.SPACE).perform()
            time.sleep(0.5)
            numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)

        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

    def closeBrowser(self):
        self.browser.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


def waitbar(current, total):
    current += 2
    done = int(np.round(((100 * (current / total)) / 2) - 1))
    togo = int(np.round(((100 * ((total - current) / total)) / 2)))
    per = str(np.round(100 * current / total, 1))
    print(done * '-' + '>' + togo * '.' + per + '%', end='\r')


bot = InstagramBot(username, password)
bot.signIn()
time.sleep(2)
# bot.followWithUsername('sunset_and_sunrise_photos')
# bot.unfollowWithUsername('sunset_and_sunrise_photos')
with open('popular_accounts.txt', 'r') as p:
    popular = p.read().split('\n')[:-1]
    random.shuffle(popular)
for celeb in popular:
    try:
        users = bot.getUserFollowers(celeb, 20)
        users = [user.split('/')[-2] for user in users]
        for user in users:
            print('\n'+ user + '\n')
            try:
                bot.followWithUsername(user)
                with open('following.txt', 'a') as f:
                    f.write(user + '\n')
                time_now = time.time()
                sleep_for = np.random.randint(350, 450, 1)[0]
                waited_time = time.time() - time_now
                while waited_time < sleep_for:
                    time.sleep(1)
                    waited_time = time.time() - time_now
                    waitbar(waited_time, sleep_for)
            except Exception:
                print(traceback.format_exc())
                pass
        print(users)
    except Exception:
        print(traceback.format_exc())
        pass
