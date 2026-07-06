"""Streamlit 앱 절전 방지 스크립트 (GitHub Actions에서 주기적으로 실행).

헤드리스 브라우저로 앱에 실제 접속해서 방문 기록을 남기고,
앱이 잠들어 있으면 깨우기 버튼을 눌러준다.
"""
import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

APP_URL = os.environ.get("APP_URL", "https://bongscript.streamlit.app")


def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        print(f"접속 중: {APP_URL}")
        driver.get(APP_URL)
        time.sleep(15)

        # 앱이 잠들어 있으면 깨우기 버튼 클릭
        woke = False
        for button in driver.find_elements(By.TAG_NAME, "button"):
            text = button.text.lower()
            if "back up" in text or "wake" in text:
                button.click()
                woke = True
                print("잠든 앱을 깨웠습니다. 부팅 대기 중...")
                time.sleep(90)
                break

        # 방문으로 집계되도록 세션을 잠시 유지
        time.sleep(30)
        print("깨어난 상태 확인 완료" if woke else "앱이 이미 깨어 있습니다.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
