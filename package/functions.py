import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from pyautogui import click
from pynput.keyboard import Key,Controller

BASE_URL = "https://www.instagram.com/"

class AccountAlreadyFollowed(Exception):
  pass
class AccountAlreadyUnfollowed(Exception):
  pass
class AccountNotRequested(Exception):
  pass
class UnsuccessfulLogin(Exception):
  pass

class InstagramDriver(webdriver.Chrome):
  def start(self): self.get(BASE_URL); self.maximize_window()
  def stop(self): self.quit()
  def test(self):return test(self)
  def login(self, stop: bool = True):
    if not stop:
      login(self)
    else:
      try:
        login(self)
      except UnsuccessfulLogin:
        print(UnsuccessfulLogin)
        self.stop()
  def get_accounts_from_page(self,username):return get_accounts_from_page(self,username)
  def get_own_followers(self):return get_own_followers(self)
  def get_own_followings(self):return get_own_followings(self)
  def test(self):return get_own_followings(self)
  def follow_account(self, username, unconditionally: bool = False):return follow_account(self, username, unconditionally)
  def unfollow_account(self, username):return unfollow_account(self, username)
  def unrequest_account(self, username):return unrequest_account(self, username)


def test(driver: webdriver.Chrome):
  instagram = driver
  instagram.get('https://demo.guru99.com/test/selenium-xpath.html')
  instagram.implicitly_wait(3)
  name_input = instagram.find_element(By.XPATH, '/html/body/form/table/tbody/tr[1]/td[2]/input')
  pass_input = instagram.find_element(By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/input')
  name_input.send_keys('sanawar')
  time.sleep(1)
  pass_input.send_keys('sanawar')
  submit = instagram.find_element(By.XPATH, '/html/body/form/table/tbody/tr[3]/td[2]/input[1]')
  submit.click()
  time.sleep(2)
  instagram.close()

def login(driver: webdriver.Chrome):
  global username
  username = 'username'
  instagram = driver
  # username = 'sanawar_21'
  password = 'password'
  instagram.get(BASE_URL)
  time.sleep(3)  
  if password != '':
    name_input = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    pass_input = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
    name_input.send_keys(username)
    pass_input.send_keys(password)
  else:
    input("Enter the username and password and press enter when done. ")
  login_button = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'form#loginForm button[type="submit"] > div')))
  login_button.click()
  time.sleep(4)
  try:
    instagram.find_element(By.CSS_SELECTOR, "input[name='username']")
    raise UnsuccessfulLogin
  except NoSuchElementException:
    pass
  time.sleep(1)

def get_accounts_from_page(driver: webdriver.Chrome, username, by = 'comments') -> "list[str]":
  instagram = driver
  instagram.get(BASE_URL+username)
  if by == 'comments':
    pass
  elif by == 'likes':
    pass
  elif by == 'followers':
    pass
  
  def get_posts_links()-> 'list[str]':
    rows = instagram.find_elements(By.TAG_NAME, 'a')
    links = [link.get_attribute('href') for link in rows]
    post_links = []
    for link in links:
      link = link.split('/')
      if 'p' in link:
        link = '/'.join(link)
        post_links.append(link)
    print(f"All posts available: {len(post_links)}")
    if len(post_links) > 7:
      print('Reducing posts to 7 only.')
      post_links = post_links[:7]
    return post_links

  def get_accounts_from_post_likes(post_link):
    instagram.get(post_link)
    WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, 'section.EDfFK.ygqzn > div > div > a')
    )).click()
    time.sleep(3)
    accounts = []
    for n in range(100):
      n += 1
      try:
        username = instagram.find_element(By.CSS_SELECTOR,
        f'div:nth-child({n}) > div.qF0y9.Igw0E.IwRSH.YBx95.vwCYk > div:nth-child(1) > div > span > a')
        accounts.append(username.text)
      except:
        pass
    return list(set(accounts))

  def get_accounts_from_post_comments(post_link) -> 'list[str]':
    instagram.get(post_link)
    accounts = []
    for n in range(100):
      n += 2
      try:
        username = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable((
          By.CSS_SELECTOR, f'div#react-root ul:nth-child({n}) > div > li > div > div > div.C4VMK > h3 > div > span > a'
        )))
        print(username.text)
        accounts.append(username.text)
      except:
        break    
    return list(set(accounts))
  
  posts = get_posts_links()
  all_accounts = []
  for post in posts:
    accounts = get_accounts_from_post_comments(post)
    all_accounts.extend(accounts)
  
  return list(set(all_accounts))

def get_accounts_from_post_likes(driver: webdriver.Chrome ,post_link):
  instagram = driver
  instagram.get(post_link)
  WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
    (By.CSS_SELECTOR, 'section.EDfFK.ygqzn > div > div > a')
  )).click()
  time.sleep(3)
  accounts = []
  for n in range(100):
    n += 1
    try:
      username = instagram.find_element(By.CSS_SELECTOR,
       f'div:nth-child({n}) > div.qF0y9.Igw0E.IwRSH.YBx95.vwCYk > div:nth-child(1) > div > span > a')
      accounts.append(username.text)
    except:
      pass
  print(accounts)

def turn_to_int(text: str) -> int:
  digits = [x for x in text]
  if ',' in digits:
    digits.remove(',')
    return int(''.join(digits))
  elif 'm' in digits:
    digits.remove('m')
    return int(float(''.join(digits)) * 1000000)
  elif 'k' in digits:
    digits.remove('k')
    return int(float(''.join(digits)) * 1000)
  else:
    return int(text)

def load_list(x=689,y=284):
  """
  Written for follower and following list but can be customized for any.
  """
  keyboard = Controller()
  time.sleep(0.3)
  click(x, y)
  for _ in range(3):
    time.sleep(0.3)
    keyboard.press(Key.page_down)
    keyboard.release(Key.page_down)

def get_accounts_from_page_2(driver,username, from_, all:bool = False, amount: int = 100):
  """
  from_ valid values: 'followers','followings'
  """

  instagram = driver
  instagram.get(BASE_URL+username)
  accounts_list = []
  time.sleep(1)

  if from_ == 'followers':
    instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > a').click()
  elif from_ == 'followings':
    instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > a').click()

  time.sleep(3)
  try:
    followers = turn_to_int(
      instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > span > span').text)
    following = turn_to_int(
      instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > span > span').text)
  except:
    followers = turn_to_int(
      instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > a > span').text)
    following = turn_to_int(
      instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > a > span').text)

  account_count = {'followers':followers, 'followings':following}
  counter = 0
  max_accounts_reached = False

  def __get_accounts(counter):
    for i in range(12):
      counter += 1
      print(counter)
      # try:
      account = instagram.find_element(By.CSS_SELECTOR,
                                          f'li:nth-child({counter}) > div > div.qF0y9.Igw0E.IwRSH.YBx95.vwCYk > div:nth-child(1) > div > div > span > a > span').text
      accounts_list.append(account)
      print(account)
      # except NoSuchElementException:
      #   print(NoSuchElementException)
    load_list()
    return counter

  # if all:
  #   while not max_accounts_reached:
  #     counter = __get_accounts(counter)
  #     if len(accounts_list) >= followers:
  #       max_accounts_reached = True
  # else:
  #   while not max_accounts_reached and len(accounts_list) < amount:
  #     counter = __get_accounts(counter)
  #     if len(accounts_list) >= followers:
  #       max_accounts_reached = True
  try:  counter = __get_accounts(counter)
  except: pass
  try:  counter = __get_accounts(counter)
  except: pass
  try:  counter = __get_accounts(counter)
  except: pass
  try:  counter = __get_accounts(counter)
  except: pass  
  try:  counter = __get_accounts(counter)
  except: pass

  return  list(set(accounts_list))

def get_accounts_from_page_followers(driver: webdriver.Chrome, username, from_='followers', all = False):
  instagram = driver
  instagram.get(BASE_URL+username)
  follower_list = []
  own_name = username
  time.sleep(1)
  instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > a').click()
  time.sleep(3)
  followers_window = instagram.find_element(
    By.CSS_SELECTOR, 'div > div.isgrP'
  )

  try:
    followers = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > span > span').text)
  except:
    followers = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > a > span').text)

  counter = 0
  max_followers_reached = False

  while not max_followers_reached and len(follower_list) < 50:
    counter += 1    
    try:
      follower = instagram.find_element(By.CSS_SELECTOR, f'li:nth-child({counter}) > div > div.t2ksc > div.enpQJ > div.d7ByH > span > a > span').text
      follower_list.append(follower)
      print(follower)
    except NoSuchElementException:
      print(NoSuchElementException)
    load_list()
    if len(follower_list)>followers:
      max_followers_reached= True
  return follower_list

def follow_account(driver: webdriver.Chrome,username, unconditionally: bool = False):
  """
  Follower to Following ratio must be less than 2, 
  exception made if the account has greater than 500 following.
  Returns True if the account is followed now.
  Returns False if the account fell short on the ratio.
  Return None if the account is requested.
  """  
  instagram = driver
  instagram.get(BASE_URL+username)
  time.sleep(2)

  if unconditionally:
    try:
      button = instagram.find_element(By.XPATH, "//button[contains(text(),'Follow')]")
      time.sleep(1)
      button.click()
      print(f"Followed {username}")
    except:
      raise AccountAlreadyFollowed

  is_public = True
  has_correct_ratio = True

  try:
    instagram.find_element(By.CSS_SELECTOR, 'div#react-root div._4Kbb_ > div > h2')
    is_public = False
  except NoSuchElementException as e:
    is_public = True

  if not is_public:
    followers = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > span > span').text)
    following = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > span > span').text)
  else:
    followers = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > a > span').text)
    following = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > a > span').text)
  
  ratio = followers/following
  
  if ratio <= 2:
    has_correct_ratio = True
  elif ratio < 3 and following > 500:
    has_correct_ratio = True
  elif ratio > 3:
    has_correct_ratio = False
    
  if has_correct_ratio:
    try:
      button = instagram.find_element(By.XPATH, "//button[contains(text(),'Follow')]")
      time.sleep(1)
      button.click()
      print(f"Followed {username}")
    except:
      raise AccountAlreadyFollowed
    if not is_public:
      return None
    return True
  else:
    return False

def unfollow_account(driver: webdriver.Chrome, username):
  instagram = driver
  instagram.get(BASE_URL+username)
  time.sleep(1)
  try:
    try:
      button = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div#react-root span.vBF20._1OSdk > button')
      ))
    except:
      button = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, 'div#react-root button[type="button"] > div > span')
      ))
    button.click()
    confirm = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, 'div.mt3GC > button.aOOlW.-Cab_')
    ))
    confirm.click()
    print(f"Unfollowed {username}")
    return True
  except:
    raise AccountAlreadyUnfollowed

def make_backup(file_address, accounts: list, append: bool = False):
  if append:
    with open(file_address, 'a') as file:
     for account in accounts:
      file.write(f'{account}\n')
  else:
    with open(file_address, 'w') as file:
      for account in accounts:
        file.write(f'{account}\n')

def read_backup(file_address) -> list:
  with open(file_address, 'r') as file:
     lines = file.readlines()
     new_lines = []
     for line in lines:
       new_lines.append(line.strip())
  return new_lines

def unrequest_account(driver: webdriver.Chrome, username):
  """
  Returns True if the account gets unrequested successfully.
  Raises AccountNotRequested Error if the account was not requested before.
  """
  instagram = driver
  instagram.get(BASE_URL+username)
  time.sleep(1)
  try:
    button = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, 'div#react-root div.qF0y9.Igw0E.IwRSH.eGOV_.ybXk5._4EzTm.bPdm3 > div > div > button[type="button"]')
    ))
    button.click()
    confirm = WebDriverWait(instagram, 10).until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, 'div.mt3GC > button.aOOlW.-Cab_')
    ))
    confirm.click()
    print(f"Unrequested {username}")
    return True
  except:
    raise AccountNotRequested

def get_own_followers(driver: webdriver.Chrome) -> 'list[str]':
  return get_accounts_from_page_2(driver,username,'followers',True)
  
def get_own_followings(driver: webdriver.Chrome) -> 'list[str]':
  return get_accounts_from_page_2(driver, username, 'followings', True)
  # instagram = driver
  # instagram.get(BASE_URL+username)
  # following_list = []
  # time.sleep(1)
  # instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > a').click()
  # time.sleep(3)
  # following_window = instagram.find_element(
  #   By.CSS_SELECTOR, 'div > div.isgrP'
  # )
  #
  # def load_following_list():
  #   keyboard = Controller()
  #   time.sleep(0.3)
  #   click(x=689, y=284)
  #   for _ in range(3):
  #     time.sleep(0.3)
  #     keyboard.press(Key.page_down)
  #
  # try:
  #   followings = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > span > span').text)
  # except:
  #   followings = turn_to_int(instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(2) > a > span').text)
  #
  # counter = 0
  # max_followers_reached = False
  #
  # while not max_followers_reached:
  #   counter += 1
  #   try:
  #     following = instagram.find_element(By.CSS_SELECTOR, f'li:nth-child({counter}) > div > div.t2ksc > div.enpQJ > div.d7ByH > span > a > span').text
  #     following_list.append(following)
  #     print(following)
  #   except NoSuchElementException:
  #     print(NoSuchElementException)
  #   load_following_list()
  #   if len(following_list)>followings:
  #     max_followers_reached= True
  # return follower_list
  
  # followings = []
  # own_name = username
  # instagram = driver
  # instagram.get(BASE_URL+own_name)
  # time.sleep(1)
  # instagram.find_element(By.CSS_SELECTOR, 'div#react-root li:nth-child(3) > a').click()
  # time.sleep(3)
  # n = 0
  # while True:
  #   n += 1    
  #   try:
  #     following = instagram.find_element(By.CSS_SELECTOR, f'li:nth-child({n}) > div > div.qF0y9.Igw0E.IwRSH.YBx95.vwCYk > div:nth-child(1) > div > div > span > a > span').text
  #     followings.append(following)
  #   except NoSuchElementException:
  #     break
  # return followings

if __name__ == '__main__':
  instagram = InstagramDriver()
  instagram.start()
  instagram.login()
  irfan_followers = get_accounts_from_page_2(instagram,'irfanjunejo','followers',amount=20)
  print(irfan_followers)
  print(len(irfan_followers))
  irfan_followings = get_accounts_from_page_2(instagram, 'irfanjunejo', 'followings', amount=20)
  print(irfan_followings)
  print(len(irfan_followings))
  own_followers = get_own_followers(instagram)
  print(own_followers)
  print(len(own_followers))
  own_followings = get_own_followings(instagram)
  print(own_followings)
  print(len(own_followings))

  instagram.stop()
