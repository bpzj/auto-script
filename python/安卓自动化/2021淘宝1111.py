
# pip install weditor  安装
# python -m weditor 开启浏览器，开启手机调试


import time

def click_auto_once(t):
    if d(text=t).exists:
        d(text=t).click()
        time.sleep(5)
        if d(text='亲，访问被拒绝').exists:
            d.press("back")
            time.sleep(0.05)
            d.press("back")
            time.sleep(5)
            click_auto_once(t)
        else:
            time.sleep(20)
            d.press('back')
            time.sleep(8)


def click_auto_times(t, times: int):
    if d(text=t).exists:
        for i in range(times):
            click_auto_once(t)


click_auto_times('去浏览',30)

click_auto_times('去完成',30)

