from __future__ import print_function
import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import get_code

Student_ID = "Your Student ID"
Password = "Your Password"

def auto_login():
    #ログイン後ブラウザが自動で閉じないように起動時にdetachオプションをTrueにする
    #ソフトウェアによって制御されていますを非表示
    #パスワードを保存するを非表示
    options = Options()
    options.add_experimental_option('detach', True)
    options.add_experimental_option("excludeSwitches", ['enable-automation', 'load-extension'])
    prefs = {'profile.password_manager_enabled' : False,
		     'credentials_enable_service': False}
    options.add_experimental_option("prefs", prefs)

    #LMSへの画面遷移
    # 自動で最新バージョンをダウンロードしてパス名を返してくれる。
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=Service(executable_path=driver_path), options=options)
    #driver = webdriver.Chrome(options=options)
    driver.get('https://mdl.media.gunma-u.ac.jp/GU/index.php')

    login_button = driver.find_element(By.ID, "loginbutton")
    login_button.click()

    #待機
    time.sleep(2)

    #入力場所の情報取得
    username = driver.find_element(By.NAME, "username")
    password = driver.find_element(By.NAME, "password")
    login = driver.find_element(By.ID, "login_button")

    #ユーザ名入力
    username.clear()
    username.send_keys(Student_ID)

    #パスワード入力
    password.clear()
    password.send_keys(Password)

    #ログインボタン
    login.click()

    #ページ遷移待機(URLの変更待ち)
    time.sleep(5)

    #認証コード取得をlogin_code.pyを利用
    authentication_code = driver.find_element(By.NAME, "password")
    get_code.authentication_code()
    code = get_code.mail_code

    #コード確認用
    #print(code)

    #認証コード入力
    authentication_code.clear()
    authentication_code.send_keys(code)

    #ページが遷移したので再度ログインボタンの情報取得
    input_login = driver.find_element(By.ID, "login_button")
    input_login.click()

auto_login()
