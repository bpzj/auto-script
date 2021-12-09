import time


def click_sleep_back(x, y, before_click: int, after_click: int, times: int):
    for i in range(times):
        time.sleep(before_click)
        d.click(x, y)
        time.sleep(after_click)
        d.press("back")


click_sleep_back(0.825, 0.795, 10, 10, 5)
