import gold_bar_test_driver as driver_lib
import time


# Main function to execute the testing process
def main():
    gold_weights_url = "http://sdetchallenge.fetch.com/"
    gold_bars = list(range(0, 9))
    total_gold_bars = len(gold_bars)

    test_driver = driver_lib.GoldBarsTestDriver(url=gold_weights_url,
                                                total_gold_bars=total_gold_bars)
    test_driver.setup()

    # Function to recursively find the fake gold bar
    def find_the_fake_gold_bar(bars_left: list[int]):
        if len(bars_left) == 1:
            return bars_left[0]
        else:
            print("The fake gold bar must be one of these: " + str(bars_left))

        bar_groups = [[], [], []]
        for index in range(0, len(bars_left)):
            bar = bars_left[index]
            group_index = index % 3
            bar_groups[group_index].append(bar)

        test_driver.set_scale(bars=bar_groups[0], side="left")
        test_driver.set_scale(bars=bar_groups[1], side="right")
        test_driver.weigh_scales()
        result = test_driver.read_weigh_results()
        time.sleep(1)
        test_driver.reset_scales()

        if result == driver_lib.WeightResult.LEFT_HEAVIER:
            print(str(bar_groups[0]) + " > " + str(bar_groups[1]))
            return find_the_fake_gold_bar(bar_groups[1])
        elif result == driver_lib.WeightResult.RIGHT_HEAVIER:
            print(str(bar_groups[0]) + " < " + str(bar_groups[1]))
            return find_the_fake_gold_bar(bar_groups[0])
        elif result == driver_lib.WeightResult.EQUAL:
            print(str(bar_groups[0]) + " = " + str(bar_groups[1]))
            return find_the_fake_gold_bar(bar_groups[2])
        else:
            raise ValueError("Weight result should not be: " + str(result))

    # Find the fake gold bar
    fake_bar = find_the_fake_gold_bar(bars_left=gold_bars)
    print("The fake bar was found to be: " + str(fake_bar))

    # Click on the identified fake gold bar on the UI
    test_driver.click_on_fake_gold_bar(bar=fake_bar)

    # Check if the final result shown on the UI is correct
    final_success = test_driver.is_result_correct()

    if final_success:
        print("The answer was CORRECT as shown by the UI alert.")
    else:
        print("The answer was INCORRECT as shown by the UI alert.")

    # Wait for alerts to disappear and then tear down the WebDriver
    time.sleep(5)
    test_driver.dismiss_alert()
    time.sleep(3)
    test_driver.teardown()

    # Only exit cleanly if the algorithm was successful, otherwise, the test run has failed
    assert final_success


if __name__ == "__main__":
    main()