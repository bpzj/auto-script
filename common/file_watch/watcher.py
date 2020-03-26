import os
import sys
import time

import win32file
import win32con
import subprocess


def posix_run(path, func):
    # todo 待完善
    print("thread: start")
    wm = pyinotify.WatchManager()
    print("wathcing path", self.watch_path)
    ret = wm.add_watch(self.watch_path, pyinotify.IN_CLOSE_WRITE, self.onChange, False, False)
    print(ret)
    print("thread: start notifyer", self.notifier)
    self.notifier = pyinotify.Notifier(wm)
    try:
        while 1:
            self.notifier.process_events()
            if self.notifier.check_events():
                self.notifier.read_events()
    # self.notifier.loop()
    except:
        print("error in notify", sys.exc_info()[0])


def win_run(path, func, last_change):
    actions = {
        1: "Created",
        2: "Deleted",
        3: "Updated",
        4: "Renamed from something",
        5: "Renamed to something"
    }
    file_list_directory = 0x0001

    # path_to_watch = r'C:\Users\bpzj\Desktop\all-code\java-grammar\.git'
    print('Watching changes in', path)
    h_dir = win32file.CreateFile(
        path,
        file_list_directory,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    while True:
        results = win32file.ReadDirectoryChangesW(
            h_dir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
            win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
            win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
            win32con.FILE_NOTIFY_CHANGE_SIZE |
            win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
            win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None)
        func(last_change)
        # for action, filename in results:
        #     full_filename = os.path.join(path, filename)
        #     print(full_filename, actions.get(action, "Unknown"))


def dir_change_run(path: str, func, last_change):
    win_run(path, func, last_change) if os.name == 'nt' else posix_run(path, func)


if __name__ == '__main__':
    path = r"C:\Users\bpzj\Desktop\all-code\script\.git"

    os.chdir(r'C:\Users\bpzj\Desktop\all-code\script')

    res = subprocess.Popen('git log -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    last_commit = res.stdout.readlines()[0]


    def demo(last_commit):
        os.chdir(r'C:\Users\bpzj\Desktop\all-code\script')
        res = subprocess.Popen('git log -1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
        commit = res.stdout.readlines()[0]
        if last_commit != commit:
            print("last_commit" + last_commit)
            print("commit" + commit)
            print("有新提交")
            last_commit = commit


    dir_change_run(path, demo, last_commit)
