from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoAlertPresentException
from enum import Enum
import time


# Enum to represent different outcomes of weighing on the balance scale
class WeightResult(Enum):
    UNKNOWN = 1
    LEFT_HEAVIER = 2
    RIGHT_HEAVIER = 3
    EQUAL = 4


# Class to interact with the web application for testing gold bars
class GoldBarsTestDriver:
    def __init__(self, url, total_gold_bars):
        # Initialize WebDriver and URLs
        self.driver = webdriver.Chrome()
        self.url = url
        self.total_gold_bars = total_gold_bars
        self.left_bar_ids = [f"left_{i}" for i in range(self.total_gold_bars)]
        self.right_bar_ids = [f"right_{i}" for i in range(self.total_gold_bars)]
        self.clickable_bar_ids = [f"coin_{i}" for i in range(self.total_gold_bars)]
        self.reset_xpath = "//button[text()=\"Reset\"]"
        self.result_xpath = "//div[@class='result']/button[@id='reset']"
        self.weigh_id = "weigh"
        self.success_alert_text = "Yay! You find it!"
        self.failure_alert_text = "Oops! Try Again!"

    def setup(self) -> None:
        # Load the web application
        self.driver.get(self.url)
        # Ensure the page loaded
        wait = WebDriverWait(self.driver, 10)
        wait.until(expected_conditions.presence_of_element_located((By.TAG_NAME, 'body')))

    def set_scale(self, bars: list[int], side: str) -> None:
        # Set the weight on the scale for a given side
        if side == "left":
            id_list = self.left_bar_ids
        elif side == "right":
            id_list = self.right_bar_ids
        else:
            raise ValueError("Side value should be 'left' or 'right', not: " + str(side))

        index = 0
        for bar in bars:
            slot_id = id_list[index]
            element = self.driver.find_element(By.ID, slot_id)
            element.send_keys(str(bar))
            time.sleep(0.5)
            index += 1

    def weigh_scales(self) -> None:
        # Click on the 'Weigh' button to measure weights
        weigh_element = self.driver.find_element(By.ID, self.weigh_id)
        weigh_element.click()

    def read_weigh_results(self, retries=10) -> WeightResult:
        # Read the result of the weighing operation
        time.sleep(1)
        result_element = self.driver.find_element(By.XPATH, self.result_xpath)
        if result_element.text == "<":
            return WeightResult.RIGHT_HEAVIER
        elif result_element.text == ">":
            return WeightResult.LEFT_HEAVIER
        elif result_element.text == "=":
            return WeightResult.EQUAL
        elif retries <= 0:
            return WeightResult.UNKNOWN
        else:
            return self.read_weigh_results(retries=retries - 1)

    def click_on_fake_gold_bar(self, bar: int):
        # Click on the identified fake gold bar
        bar_id = self.clickable_bar_ids[bar]
        element = self.driver.find_element(By.ID, bar_id)
        element.click()

    def is_result_correct(self) -> bool:
        # Check if the result shown in the UI is correct
        alert_text = self.driver.switch_to.alert.text
        if self.success_alert_text == alert_text:
            return True
        elif self.failure_alert_text == alert_text:
            return False
        else:
            raise ValueError("Alert text: '" + str(alert_text) + "' not recognized")

    def dismiss_alert(self) -> None:
        # Dismiss any alert present on the UI
        try:
            self.driver.switch_to.alert.dismiss()
        except NoAlertPresentException:
            pass

    def reset_scales(self) -> None:
        # Reset the weighing scales to their initial state
        element = self.driver.find_element(By.XPATH, self.reset_xpath)
        element.click()

    def teardown(self) -> None:
        # Close the browser
        self.driver.quit()