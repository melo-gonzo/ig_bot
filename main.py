from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from login import username, password, account
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
        print('\n' + 'click unfollow button' + '\n')
        followButton.click()
        time.sleep(2)
        confirmButton = self.browser.find_element_by_xpath('//button[text() = "Unfollow"]')
        print('\n' + 'click unfollow confirm button' + '\n')
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
        print(5 * '\n' + search_value + 5 * '\n')
        searchbox = WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search']")))
        searchbox.send_keys(search_value)
        time.sleep(10)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(5)
        searchbox.send_keys(Keys.ENTER)
        time.sleep(7)

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
                    self.do_sleep(sleep_low, sleep_high)
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
        self.do_sleep(sleep_low, sleep_high)
        first_sq.click()
        done = 0
        for k in range(num_to_follow):
            try:
                self.do_sleep(sleep_low, sleep_high)
                username = self.browser.find_element_by_xpath(
                    '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[1]/span/a').text
                # follow_button = self.browser.find_element_by_xpath("//button[contains(.,'Follow')]")
                fb_xp = '/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button'
                follow_button = self.browser.find_element_by_xpath(fb_xp)
                print('\n' + 'click follow button' + '\n')
                follow_button.click()
                self.do_sleep(sleep_low, sleep_high)
                self.add_to_following(username)
                print('\n' + 'click like button' + '\n')
                self.browser.find_element_by_xpath("//span[@class='fr66n']").click()
                print('\n' + 'click next button' + '\n')
                time.sleep(5)
                self.browser.find_element_by_link_text('Next').click()
                self.do_sleep(sleep_low, sleep_high)
                done += 1
            except Exception:
                try:
                    cancel_button = self.browser.find_element_by_xpath("//button[contains(.,'Cancel')]")
                    self.do_sleep(sleep_low, sleep_high)
                    print('\n' + 'click cancel button' + '\n')
                    cancel_button.click()
                    self.do_sleep(sleep_low, sleep_high)
                    print('\n' + 'click next button' + '\n')
                    self.browser.find_element_by_link_text('Next').click()
                    self.do_sleep(sleep_low, sleep_high)
                except Exception:
                    print(traceback.format_exc())
                    pass
                print(traceback.format_exc())
                pass
        self.remove_followers(int(num_to_follow * 2))

    def getUserFollowing(self, username, max_following=1000):
        self.browser.get('https://www.instagram.com/' + username)
        wait = WebDriverWait(self.browser, 10)
        followingList = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'/following')]")))
        followingList.click()
        time.sleep(2)
        fBody = self.browser.find_element_by_xpath("//div[@class='isgrP']")
        self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", fBody)
        num_followers = 0
        tries = 0
        while tries < 10:
            time.sleep(0.5)
            followingList = self.browser.find_element_by_css_selector('div[role=\'dialog\'] ul')
            time.sleep(0.5)
            time.sleep(0.5)
            numberOfFollowingInList = len(followingList.find_elements_by_css_selector('li'))
            print(numberOfFollowingInList)
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", fBody)
            if numberOfFollowingInList > num_followers:
                num_followers = numberOfFollowingInList
                tries = 0
            else:
                num_followers = numberOfFollowingInList
                tries += 1
            print(tries)
        following = []
        for user in followingList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector('a').get_attribute('href')
            print(userLink)
            following.append(userLink)
            if (len(following) == max):
                break

        f = open(username + '_following.txt','w')
        followers_list = [person.split('/')[-2] for person in following]
        for person in followers_list:
            f.write(person+'\n')
        f.close()
        return

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


sleep_low = 5
sleep_high = 10
bot = InstagramBot(username, password)
bot.signIn()
time.sleep(5)
bot.getUserFollowing(username, max_following=1000)
bot.remove_followers(10)
locations = open('locations.txt','r').read().split('\n')[:-1]
idx = random.sample(range(len(locations)), len(locations))
locs = [locations[ii] for ii in idx]
while True:
    try:
        for loc in locs:
            locs_seen = open('locs_seen.txt', 'r').read().split('\n')
            if len(locs_seen) == len(locs):
                f = open('locs_seen.txt','w')
                f.write('')
                f.close()
            if loc not in locs_seen:
                bot.search_bar(loc)
                time.sleep(10)
                bot.follow_from_tilepage(9)
                with open('locs_seen.txt', 'a') as f:
                    f.write(loc + '\n')
    except Exception:
        print(traceback.format_exc())
        pass

