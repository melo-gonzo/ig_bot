from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from login_carmelo import username, password, account
from selenium import webdriver
from time import sleep
import numpy as np
import traceback
import random
import time


class InstagramBot():
    def __init__(self, email, password):
        driver_path = '/home/carmelo/Documents/ig_bot_carmelo/chromedriver_linux64/chromedriver'
        # brave_path = '/opt/brave.com/brave/brave-browser'
        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(chrome_options=self.browserProfile)
        self.email = email
        self.password = password
        self.account = account

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
        followButton = self.browser.find_element_by_class_name('_5f5mN.-fzfL._6VtSN.yZn4P')
        followButton.click()
        time.sleep(2)
        confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
        confirmButton.click()

    def getUserFollowers(self, username, max_followers):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(followersList.find_elements_by_css_selector('li'))
        actionChain = webdriver.ActionChains(self.browser)
        tries = 0
        while (numberOfFollowersInList < max_followers):
            tries += 1
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
            if tries > 10: break
        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            followers.append(userLink)
            if (len(followers) == max):
                break
        return followers

    def do_sleep(self, min, max):
        time_now = time.time()
        sleep_for = np.random.randint(min, max, 1)[0]
        waited_time = time.time() - time_now
        print('\n')
        while waited_time < sleep_for:
            time.sleep(1)
            waited_time = time.time() - time_now
            waitbar(waited_time, sleep_for)

    def search_bar(self, search_value):
        searchbox = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        searchbox.send_keys(search_value)
        time.sleep(10)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(2)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(4)

    def add_to_following(self, user):
        with open(account + '_following.txt', 'a') as f:
            f.write(user + '\n')

    def remove_followers(self, num_to_remove):
        f = open(account + '_following.txt', 'r').read().split('\n')[:-1]
        print('\n following: ' + str(len(f)) + '\n')
        unfollow_amount = num_to_remove
        if len(f) > num_to_remove:
            unfollow = f[:unfollow_amount]
            for un in unfollow:
                try:
                    bot.unfollowWithUsername(un)
                    self.do_sleep(60, 120)
                except Exception:
                    print(traceback.format_exc())
                    pass
            new_f = '\n'.join(f[unfollow_amount:])
            with open(account + '_following.txt', 'w') as f:
                f.write(new_f + '\n')
            print('Unfollowed: ' + ' '.join(them) for them in unfollow)

    def follow_from_tilepage(self, num_to_follow):
        # first_sq = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
        first_sq = self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
        self.do_sleep(60, 120)
        first_sq.click()
        self.do_sleep(60, 120)
        done = 0
        for k in range(num_to_follow):
            try:
                self.do_sleep(60, 120)
                username = self.browser.find_element_by_xpath(
                    '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                follow_button = self.browser.find_element_by_xpath("//button[contains(.,'Follow')]")
                follow_button.click()
                self.do_sleep(60, 120)
                self.add_to_following(username)
                self.browser.find_element_by_xpath("//span[@class='fr66n']").click()
                self.browser.find_element_by_link_text('Next').click()
                self.do_sleep(60, 120)
                done += 1
            except Exception:
                try:
                    cancel_button = self.browser.find_element_by_xpath("//button[contains(.,'Cancel')]")
                    self.do_sleep(60, 120)
                    cancel_button.click()
                    self.do_sleep(60, 120)
                    self.browser.find_element_by_link_text('Next').click()
                    self.do_sleep(60, 120)
                except Exception:
                    print(traceback.format_exc())
                    pass
                print(traceback.format_exc())
                pass
        if done == num_to_follow: self.remove_followers(int(num_to_follow * 2))

    def getUserFollowing(self, username, max_following):
        self.browser.get('https://www.instagram.com/' + username)
        wait = WebDriverWait(self.browser, 10)
        followingList = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/following')]")))
        followingList.click()
        time.sleep(2)
        followingList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
        numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
        actionChain = webdriver.ActionChains(self.browser)
        tries = 0
        while (numberOfFollowingInList < max_following):
            # tries += 1
            # followingList.click()
            time.sleep(0.5)
            followingList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            time.sleep(0.5)
            actionChain.key_down(Keys.SPACE).perform()
            time.sleep(0.5)
            actionChain.key_up(Keys.SPACE).perform()
            time.sleep(0.5)
            numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
            print(numberOfFollowingInList)
            # if tries > 10: break
        following = []
        for user in followingList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            following.append(userLink)
            if (len(following) == max):
                break
        return following

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
time.sleep(5)
locations = ['santa barbara, california',
             'goleta, california',
             'mission, santa barbara',
             'mesa lane, santa barbara',
             'butterfly beach, santa barbara',
             'east beach, santa barbara',
             'isla vista, california',
             'state street, santa barbara',
             'ucsb, santa barbara',
             'hendry\s beach, santa barbara',
             'inspiration point, santa barbara',
             'lizards mouth, santa barbara',
             'montecito, california',
             'thousand steps beach, santa barbara',
             'campus point, santa barbara',
             'stearns warf, santa barbara',
             '34 anacapa street, santa barbara',
             'courthouse, santa barbara',
             'mesa, santa barbara',
             'shoreline park, santa barbara',
             'chase palm park, santa barbara',
             'arroyo burro beach, santa barbara']

idx = random.sample(range(len(locations)), len(locations))
locs = [locations[ii] for ii in idx]
for loc in locs:
    bot.search_bar(loc)
    time.sleep(10)
    bot.follow_from_tilepage(9)

# bot.followWithUsername('sunset_and_sunrise_photos')
# bot.unfollowWithUsername('sunset_and_sunrise_photos')
# following = bot.getUserFollowing('melo.moments', 2000)
#
# with open('popular_accounts.txt', 'r') as p:
#     popular = p.read().split('\n')[:-1]
#     random.shuffle(popular)
# for celeb in popular:
#     try:
#         users = bot.getUserFollowers(celeb, 20)
#         users = [user.split('/')[-2] for user in users]
#         for user in users:
#             print('\n' + user + '\n')
#             try:
#                 # bot.followWithUsername(user)
#                 # time.sleep(5)
#                 with open('following.txt', 'a') as f:
#                     f.write(user + '\n')
#                 f = open('following.txt', 'r').read().split('\n')[:-1]
#                 print('\n following: ' + str(len(f)) + '\n')
#                 unfollow_amount = 1
#                 if len(f) > 0:
#                     unfollow = f[:unfollow_amount]
#                     for un in unfollow:
#                         try:
#                             bot.unfollowWithUsername(un)
#                             time.sleep(np.random.randint(5, 10, 1)[0])
#                         except Exception:
#                             print(traceback.format_exc())
#                             pass
#                     new_f = '\n'.join(f[unfollow_amount:])
#                     with open('following.txt', 'w') as f:
#                         f.write(new_f + '\n')
#                 time_now = time.time()
#                 # sleep_for = np.random.randint(250, 350, 1)[0]
#                 # waited_time = time.time() - time_now
#                 # print('\n')
#                 # while waited_time < sleep_for:
#                 #     time.sleep(1)
#                 #     waited_time = time.time() - time_now
#                 #     waitbar(waited_time, sleep_for)
#             except Exception:
#                 print(traceback.format_exc())
#                 pass
#         print(users)
#     except Exception:
#         print(traceback.format_exc())
#         pass


# first_sq = self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a')
# sleep(2)
# first_sq.click()
# sleep(5)
