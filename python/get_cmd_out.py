import os
import subprocess


# windows 平台下, 使用 os.popen() 后读取标准输出， 可能会乱码
def windows_cmd_stdout_gbk_cant_decode():
    # popen 返回文件对象，跟open操作一样
    with os.popen(r'git log -10', 'r') as f:
        text = f.read()

    print(text)


def use_subprocess_popen():
    res = subprocess.Popen('git log -3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    result = res.stdout.readlines()
    for r in result:
        print(str(r, encoding='utf-8'))
    # print(result)


# 打印cmd输出结果

if __name__ == '__main__':
    try:
        windows_cmd_stdout_gbk_cant_decode()
    except Exception as e:
        print(e)
    print("---------------------------------")
    use_subprocess_popen()
