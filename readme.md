# 🕹️ Hoyodaily Bot - Automated Daily Check-In for HoYoLAB

A fully automated Python bot using Selenium + PyAutoGUI that logs into HoYoLAB and claims daily rewards for:
- Genshin Impact
- Honkai Impact 3rd
- Honkai: Star Rail
- Zenless Zone Zero

No more forgetting to check in - just run and AFK 😎

---

## ✨ Features

- ✅ Supports 4 games from HoYoLAB
- ✅ Image-based detection using PyAutoGUI
- ✅ Cookie-based login (only login once)
- ✅ Handles pop-ups and game switching
- ✅ Can run daily via Task Scheduler

---

## 🖥️ How to Use

If you don't have Python installed, just download and run the .exe version of this bot:

👉 Download Hoyodaily Bot .exe from the Releases tab.

First run:

1. Run the app and manually log in within 60 seconds
2. Your session cookies will be saved (no need to log in again next time)
3. The bot will automatically claim daily rewards for supported games

---

## 🧪 Manual Run (Python Required)

1. Launch `main.py` and **log in manually within 60 seconds**
2. Your session cookies will be saved automatically
3. After that, the bot will log in silently and auto-check-in
4. All image tiles used to identify rewards are stored in folders under `/tiles`

---

## ⏰ Optional: Task Scheduler Setup (Windows Only)

You can schedule this script to run every day automatically using **Windows Task Scheduler**.

Make sure:
- Your laptop is powered on
- You use full path to Python + script
- You enable “Run with highest privileges” if needed

---

## 📁 Folder Structure

hoyodaily_bot/
├── main.py # Main bot script
├── requirements.txt # Dependencies
├── tiles/ # Folder containing reward image tiles
│ ├── genshin/
│ ├── honkai/
│ ├── starrail/
│ └── zzz/
└── hoyolab_cookies.pkl # Stored login session (auto-generated)

---

## 📦 Requirements

```txt
selenium==4.15.2
pyautogui==0.9.54
pillow==10.2.0

```bash
pip install -r requirements.txt
```
---

## 🧰 Tech Stack

Language: Python 3.12

Automation: Selenium, PyAutoGUI

GUI Image Processing: Pillow

Packaging: PyInstaller (to create .exe)

Platform: Windows 11

Task Automation: Windows Task Scheduler

---

## 🧠 Notes

tiles/ folder stores all image references for clickable rewards

If a new reward appears (e.g., Day 3), screenshot it and add it to the right folder

If no tile is matched, the bot will try fallback XPaths for each game

The script uses screen image recognition. Keep your display unchanged when running

---

## ⚠️ Disclaimer

Built for personal use.
Be cautious with automation - respect game rules and avoid spamming.

---

## 📜 License

Copyright © 2025 Muhammad Irfan Bin Azam

This software and its source code are proprietary and confidential.

You are allowed to use this application for personal, non-commercial purposes only.

You may not copy, modify, redistribute, or use any part of the code in other projects without explicit permission from the author.

All rights reserved.