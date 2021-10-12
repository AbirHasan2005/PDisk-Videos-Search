# (c) @AbirHasan2005
# PDisk Login using selenium & Google Chrome Driver part of https://t.me/PDiskRobot
# Sorry for RIP coding quality. I don't use selenium much. If you can help to improve more than go for it.

from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    ElementClickInterceptedException
)


async def pdisk_login(username: str, password: str):
    print("Bot on Standby ...")
    login_url = "https://www.pdisk.net/login?type=login"
    get_id_page_url = "https://www.pdisk.net/withdraw"
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(options=options)
    print("Trying to Login to PDisk Account ...")
    driver.get(login_url)
    print("Adding Username in Box ...")
    driver.find_element_by_xpath("//input[@placeholder='Username/Email']").send_keys(username)
    print("Adding Password in Box ...")
    driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(password)
    print("Clicking Login Button ...")
    driver.find_element_by_xpath("//button[@type='button']").click()
    count = 0
    login_success = None
    while count < 4:
        try:
            driver.find_element_by_class_name("btn").click()
            login_success = True
            count += 1
        except (NoSuchElementException, StaleElementReferenceException):
            pass
        except ElementClickInterceptedException:
            print("Failed to Login !!\n\n"
                  f"Username: '{username}'\n"
                  f"Password: '{password}'")
            login_success = False
            break
    if login_success is True:
        print("Successfully Logged In !!\n\n"
              f"Username: '{username}'\n"
              f"Password: '{password}'")
        driver.get(get_id_page_url)
        try:
            user_id = driver.find_element_by_class_name("account-id").text.split(' ', 1)[-1]
        except NoSuchElementException:
            user_id = None
        print(f"PDisk User ID: '{user_id}'")
        ## --- Collect Cookies --- ##
        cookies = ""
        cookie_names = ["lang", "user_uid", "uid", "EGG_SESS", "csrfToken", "pdisksid"]
        for cookie in range(len(cookie_names)):
            cookies += f"{cookie_names[cookie]}={driver.get_cookie(cookie_names[cookie])['value']}; "
        driver.quit()
        print("Bot Working Now ...")
        cookies = cookies.rsplit("; ", 1)[0]
        return user_id, cookies
    else:
        driver.quit()
        print("Bot Working Now ...")
        return None, None
