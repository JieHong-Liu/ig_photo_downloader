import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


# A subprogram that check wether any pic is the same, make sure that there is no pic is the same as new pic.

def check(img_list, new_pic):
    for i in img_list:
        if i == new_pic:
            return 0
    return 1


def ig_download():

    driver = webdriver.Chrome()

    id = input('Enter the id you want to download: ')
    user_id = input('Enter your account: ')
    user_password = input('Enter your password: ')

    annoymus = 0  # initial the annoymus variable
    # if you don't want to login your account, only you can download is the public accounts.
    if user_id == '0' and user_password == '0':
        annoymus = 1

    # open the url
    if(not annoymus):
      # if you want to login, goto the login page.
        driver.get(
            'https://www.instagram.com/accounts/login/?source=private_profile')
        try:
            # login part
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            login_user = driver.find_element_by_name('username')
            login_user.send_keys(user_id)

            login_password = driver.find_element_by_name('password')
            login_password.send_keys(user_password)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
                ))
            login = driver.find_element_by_xpath(
                '//*[@id="loginForm"]/div/div[3]/button')
            login.click()
            # sometimes the page will ask me to save the password

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/section/main/div/div/div/section/div/button"))
            )
            save = driver.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/div/div/section/div/button")
            save.click()

            # open the notification window

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[4]/div/div/div/div[3]/button[2]"))
            )
            later = driver.find_element_by_xpath(
                "/html/body/div[4]/div/div/div/div[3]/button[2]")
            later.click()
        finally:
            print("finished login")

    driver.get("https://www.instagram.com/"+id+"/")

    driver.maximize_window()

    # write the html.txt
    time.sleep(1)  # wait it to ready
    soup = BeautifulSoup(driver.page_source, 'lxml')

    numbers = soup.find_all('span', class_='g47SY')
    #     posts
    print("This id has " + str(numbers[0].text) + " posts. ")
    #     followers
    print("This id has " + str(numbers[1].text) + " followers. ")
    #     following
    print("This id is following " + str(numbers[2].text) + " people")

    time.sleep(1)

    img_list = []  # list of saving image
    soup = BeautifulSoup(driver.page_source, 'lxml')
    time.sleep(1)  # wait it to ready

    div_list = []
    div_list = soup.find_all('div', class_='KL4Bh')

    if (not len(div_list)):
        print('This ID is private! ')
        driver.close()
    else:
        print('The download is going to start : ')
        i = 1
        # make sure that the scrolling is enough
        for j in range(0, int(int(numbers[0].text) / 10)):
            soup = BeautifulSoup(driver.page_source, 'lxml')
            time.sleep(1)  # wait it to ready

            div_list = soup.find_all('div', class_='KL4Bh')

            for div in div_list:
                # check if there is any pic is the same.
                if check(img_list, div.img.get('src')):
                    # print the post which is downloaded
                    print(div.img.get('src'))
                    with open(id+'['+str(i)+'].jpg', 'wb') as file:
                        download = requests.get(div.img.get('src'))
                        file.write(download.content)
                        # save to image list
                        img_list.append(div.img.get('src'))
                        i = i + 1
            driver.execute_script(
                'window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(1)
        print("Download finished!")


ig_download()
