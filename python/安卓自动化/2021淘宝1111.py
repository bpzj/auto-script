
# pip install weditor  安装
# python -m weditor 开启浏览器，开启手机调试

import time
def click_then_back(pos: tuple, times: int):
    for i in range(times):
        d.click(*pos)
        time.sleep(30)
        d.press('back')
        time.sleep(8)


share_page_line_3 = (0.852, 0.687)
share_page_line_4 = (0.791, 0.756)
share_page_line_5 = (0.791, 0.846)

click_then_back(share_page_line_3,30)
