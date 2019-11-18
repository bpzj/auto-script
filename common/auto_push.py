import os
import subprocess
import sys

from file_watch.watcher import dir_change_run


def push_grammar_project():
    os.chdir(r"C:\Users\bpzj\Desktop\all-code\java-grammar")
    ps = subprocess.Popen('git show --stat', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    lines = ps.stdout.readlines()
    time = str(lines)[str(lines).index("Date")+8:str(lines).index("Date")+27].strip()
    sys.stdout.write(time)
    sys.stdout.flush()


if __name__ == '__main__':
    # 配置 日期格式 git config --global log.date format:"%Y-%m-%d %H:%M:%S"
    dir_change_run(path=r"C:\Users\bpzj\Desktop\all-code\java-grammar\.git", func=push_grammar_project)
