#=====================================================================
# Title     : HOYOLAB DAILY CHECK-IN AUTO BOT
# Script    : main.py
# Author    : Muhammad Irfan Azam
# Created   : 1 July 2025
# License   : © 2025 Muhammad Irfan Azam. All rights reserved.
# Note      : This script is protected by copyright law.
#             Do not redistribute, modify, or sell without permission.
#
# Documentation / Changes:
#       2025-07-09: Finished full working script
#
#=====================================================================

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys
import pickle
import pyautogui

# CONFIG
cookies_path = "hoyolab_cookies.pkl"
if getattr(sys, 'frozen', False):
    # If running as .exe
    base_path = sys._MEIPASS
else:
    # If running as .py
    base_path = os.path.dirname(os.path.abspath(__file__))

driver_path = os.path.join(base_path, "msedgedriver.exe")
dropdown_path = os.path.join(base_path, "game_dropdown.png")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

tile_base_folder = resource_path("tiles")

# Games to process
games = {
    "genshin": "Genshin Impact",
    "honkai": "Honkai Impact 3rd",
    "starrail": "Honkai: Star Rail",
    "zzz": "Zenless Zone Zero"
}

# Setup Browser
options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Edge(service=Service(driver_path), options=options)

# Login Using Saved Cookies
def login_with_cookies():
    driver.get("https://www.hoyolab.com/home")
    if os.path.exists(cookies_path):
        with open(cookies_path, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.refresh()
        print("✅ Cookies loaded")
    else:
        print("🔐 Please log in manually (60 seconds)")
        time.sleep(60)
        with open(cookies_path, "wb") as f:
            pickle.dump(driver.get_cookies(), f)
        print("✅ Cookies saved!")

# Skip Interest Pop-up
def skip_interest_popup():
    try:
        skip_button = driver.find_element(By.XPATH, "//*[contains(text(), 'Skip')]")
        skip_button.click()
        print("✅ Skipped the interest pop-up")
    except:
        print("ℹ️ Skip button not found")

# Close Daily Check-In Pop-up
def close_checkin_popup(game_name):
    try:
        # Default close button (for Genshin & Honkai Impact 3rd)
        default_xpath = "/html/body/div[5]/div/div/span"
        # For Star Rail & ZZZ
        alternate_xpath = "/html/body/div[3]/div[2]/div[2]/div"

        if game_name in ["Honkai: Star Rail", "Zenless Zone Zero"]:
            close_button = driver.find_element(By.XPATH, alternate_xpath)
        else:
            close_button = driver.find_element(By.XPATH, default_xpath)

        driver.execute_script("arguments[0].click();", close_button)
        print(f"✅ Closed the reminder pop-up for {game_name}.")
    except:
        print(f"ℹ️ No reminder pop-up to close for {game_name}.")

# Claim Daily Reward
def claim_reward(game_key, game_name):
    print(f"\n🎮 Processing: {game_name.upper()}")
    tile_folder = os.path.join(tile_base_folder, game_key)
    found = False

    # Return to home
    driver.get("https://www.hoyolab.com/home")
    time.sleep(2)

    # Open dropdown using image recognition
    try:
        location = pyautogui.locateCenterOnScreen(dropdown_path, confidence=0.88) # Your screenshot of the dropdown arrow
        if location:
            pyautogui.moveTo(location)
            pyautogui.click()
            print("✅ Opened game dropdown using image recognition")
            time.sleep(2)
        else:
            print("❌ Dropdown image not found on screen")
    except Exception as e:
        print(f"❌ Failed to open game dropdown using image: {e}")

    try:
        # Wait for the game list to load
        dropdown_items = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ul.game-list > li.game-item"))
        )

        for item in dropdown_items:
            text = item.text.strip().lower().replace(" ", "").replace(":", "")
            game_match = game_name.lower().replace(" ", "").replace(":", "")

            if text == game_match:
                driver.execute_script("arguments[0].click();", item)
                print(f"✅ Selected {game_name}")
                time.sleep(2)
                break
        else:
            print(f"❌ Could not find {game_name} in dropdown")
            return

    except Exception as e:
        print(f"❌ Could not select {game_name}: {e}")
        return
    # Click check-in icon
    try:
        checkin_button = driver.find_element(By.XPATH, "//div[contains(text(), 'Check-In') or contains(text(), 'Check In')"
        "or @aria-label='Check-In' or @aria-label='Check In']")
        checkin_button.click()
        print("✅ Clicked the Check-In icon")
        time.sleep(5)
    except:
        print("❌ Could not find Check-In button")
        return

    # Switch to check-in tab
    driver.switch_to.window(driver.window_handles[-1])
    print("✅ Switched to Check-In tab!")

    # Close pop-up if present
    close_checkin_popup(game_name)

    # Match and click tile
    time.sleep(3)
    print("🔍 Searching for reward tile image...")

    if os.path.exists(tile_folder):
        print(f"📁 Looking in tile folder: {tile_folder}")
        for filename in os.listdir(tile_folder):
            if filename.endswith(".png"):
                img_path = os.path.join(tile_folder, filename)
                print(f"🔎 Trying tile: {filename}")
                try:
                    location = pyautogui.locateCenterOnScreen(img_path, confidence=0.97)
                    if location:
                        pyautogui.moveTo(location)
                        pyautogui.click()
                        print(f"✅ Claimed reward by clicking tile: {filename}")
                        found = True
                        break
                except Exception as e:
                    print(f"⚠️ Error locating {filename}: {e}")

        # ✅ Fallback if no tile matched
        if not found:
            print("🔁 No tile matched - trying fallback claim button by XPath...")
            try:
                fallback_xpath = {
                    "genshin": "/html/body/div[1]/div[5]/div/div/div/div[3]/span[2]",
                    "starrail": "/html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div[2]/span",
                    "zzz": "/html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div[2]/span",
                    "honkai": "/html/body/div[1]/div[2]/div/div[2]/div[4]/div[3]",
                }

                xpath = fallback_xpath.get(game_key)
                if xpath:
                    fallback_button = driver.find_element(By.XPATH, xpath)
                    driver.execute_script("arguments[0].scrollIntoView();", fallback_button)
                    time.sleep(1)
                    fallback_button.click()
                    print("✅ Fallback claim button clicked")

                    # Try pyautogui again after fallback
                    time.sleep(2)
                    for filename in os.listdir(tile_folder):
                        if filename.endswith(".png"):
                            img_path = os.path.join(tile_folder, filename)
                            print(f"🔁 Retry tile: {filename}")
                            try:
                                location = pyautogui.locateCenterOnScreen(img_path, confidence=0.97)
                                if location:
                                    pyautogui.moveTo(location)
                                    pyautogui.click()
                                    print(f"✅ Claimed reward after fallback: {filename}")
                                    found = True
                                    break
                            except Exception as e:
                                print(f"⚠️ Retry error: {e}")
                else:
                    print("❌ No fallback XPath found for this game.")
            except Exception as e:
                print(f"❌ Fallback claim failed: {e}")
    else:
        print(f"❌ Tile folder not found: {tile_folder}")

    # Close this tab and switch back
    time.sleep(3)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# ========== MAIN FLOW ==========
login_with_cookies()
time.sleep(2)
skip_interest_popup()
time.sleep(2)

for key, name in games.items():
    claim_reward(key, name)
    time.sleep(3)

driver.quit()