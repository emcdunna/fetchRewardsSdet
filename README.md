Author: Evan McDonough
Email: emcdunna@gmail.com

# Gold Bars Test Automation with Selenium

    This project provides an automated testing solution to identify a fake gold bar among a set of gold bars using a balance scale on the website http://sdetchallenge.fetch.com/. The solution is implemented using Selenium WebDriver in Python.

## Table of Contents

    1. Overview
    2. Requirements
    3. Installation
    4. Usage
    5. Code Structure

## 1. Overview

    The goal of this project is to find a fake gold bar among 9 gold bars using a balance scale. The fake gold bar is lighter than the others. This automation script interacts with the web application available at `http://sdetchallenge.fetch.com/` to determine and identify the fake gold bar.

## 2. Requirements

    - Python 3.x
    - Google Chrome Browser
    - Chrome WebDriver
    - Selenium

## 3. Installation

    MacOS:
        Install homebrew with:
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            ** Don't forget to add brew to your PATH variable with "export PATH=/opt/homebrew/bin:$PATH" in the ~/.bashrc file

        Install Python3:
           brew update
           brew install python3

        Install Chrome:
            brew install --cask google-chrome

        Download Chrome WebDriver:
            brew install --cask chromedriver
            ... or download the Chrome WebDriver from https://sites.google.com/a/chromium.org/chromedriver/downloads and place it in a directory included in your system PATH.

        Start a virtual environment to run python with dependencies
            python3 -m venv path/to/venv
            source path/to/venv/bin/activate

        Install Selenium
            python3 -m pip install selenium

    Windows:
        Download Python:
            Go to the official Python website.
            Download the latest Python installer for Windows.
            Run the Installer:

        Run the downloaded installer.
            Ensure you check the box that says "Add Python to PATH".
            Click on "Install Now" to install Python with default settings.

        Download ChromeDriver:
            Go to the ChromeDriver download page.
            Download the version of ChromeDriver that matches your Chrome version.
            Extract the downloaded chromedriver_win32.zip file.

        Move ChromeDriver:
            Move the extracted chromedriver.exe file to a directory of your choice (e.g., C:\chromedriver).

        Add ChromeDriver to PATH:
            Right-click on This PC or Computer on the desktop or File Explorer.
            Click on Properties.
            Click on Advanced system settings.
            Click on Environment Variables.
            In the System variables section, find the Path variable and select it. Click on Edit.
            Click on New and add the path to the directory where you moved chromedriver.exe (e.g., C:\chromedriver).
            Click OK to close all windows.

4. Usage
    Clone the repository or download the script.

    Run the script:
        python3 main.py

    The script will:
        * Load the web application.
        * Interact with the balance scale to compare groups of gold bars using the optimal algorithm
        * Determine and the fake gold bar with 2 iterations of weighing bars
        * Click on the fake bar
        * Display the result in the console.

    WARNING: Do not interact with the web page at all during the automated tests, or it can throw off the web driver's state. A common example I found is clicking "OK" on the alert window before the automation tries to do this, but there could be other issues.

5. Code Structure
    The main components of the code are:

    gold_bar_test_driver.py
        * WeightResult Enum: Defines the possible outcomes of a weighing operation (UNKNOWN, LEFT_HEAVIER, RIGHT_HEAVIER, EQUAL).
        * GoldBarsTestDriver Class: Handles interactions with the web application.
            * setup: Loads the web application.
            * set_scale: Sets the weight on the scale for a given side.
            * weigh_scales: Clicks on the 'Weigh' button to measure weights.
            * read_weigh_results: Reads the result of the weighing operation.
            * click_on_fake_gold_bar: Clicks on the identified fake gold bar.
            * is_result_correct: Checks if the alert shown in the UI confirms our choice.
            * dismiss_alert: Dismisses any alert present on the UI.
            * reset_scales: Resets the weighing scales to their initial state.
            * teardown: Closes the browser window.

    main.py
        * main (function): Executes the testing process to find the fake gold bar and defines the algorithm to optimally find the answer in only 2 iterations.

