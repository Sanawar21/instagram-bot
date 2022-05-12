import time
import multiprocessing
from urllib import request
from package import functions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
  instagram = functions.InstagramDriver()
  instagram.login()
  instagram.start()

  requested = functions.read_backup('C:\\Users\\TOSHIBA\\Desktop\\instabot\\requested_accounts.txt')
  recently_followed = functions.read_backup('C:\\Users\\TOSHIBA\\Desktop\\instabot\\recently_followed.txt')

  all = requested + recently_followed

  for account in all:
    pass    

  # accounts = functions.read_backup('C:\\Users\\TOSHIBA\\Desktop\\instabot\\all_accounts.txt')
  # accounts = accounts[:10]
  
  # requested = ['_umair_qureshi516']
  # useless = []
  
  # for account in accounts:
  #   value = instagram.follow_account(account)
  #   if value:
  #     followed.append(account)
  #   elif value == False:
  #     useless.append(account)
  #   elif value == None:
  #     requested.append(account)

  # recently_followed_address = 'C:\\Users\\TOSHIBA\\Desktop\\instabot\\recently_followed.txt'
  # recently_requested_address = 'C:\\Users\\TOSHIBA\\Desktop\\instabot\\requested_accounts.txt'
  # useless_accounts_address = 'C:\\Users\\TOSHIBA\\Desktop\\instabot\\useless_accounts.txt'

  # functions.make_backup(recently_followed_address, followed)
  # functions.make_backup(recently_requested_address, requested)
  # functions.make_backup(useless_accounts_address, followed)


  # service = Service('chromedriver.exe')
  
  # driver1 = webdriver.Chrome(service=service)
  # driver1.maximize_window()

  # while True:
  #   try:
  #     functions.login(driver1)
  #     break
  #   except functions.UnsuccessfulLogin:
  #     time.sleep(5)
  #     driver1.quit()
  #     driver1 = webdriver.Chrome(service=service)
  
  # pages = ['irfanjunejo', 'mobeenansariphoto', 'khaula28', 'talhaghouri']
  
