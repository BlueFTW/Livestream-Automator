import os
import time
import schedule
import threading
import sys
import random
from constants import VIDEO_PATHS, ACCOUNTS, FOLDER_PATH, STREAM_URL

def get_random_duration(min_hours=5, max_hours=6):
    return random.randint(min_hours * 60 * 60, max_hours * 60 * 60)


def get_random_video():
    return random.choice(list(VIDEO_PATHS))


def stream_video_to_account(video_path, account_key):
    try:
        print(f"Starting stream for account with key: {account_key}")
        duration = get_random_duration()
        cmd = f'{FOLDER_PATH} -re -stream_loop -1 -i {video_path} -c:v copy -c:a aac -strict experimental -t {duration} -f flv {STREAM_URL}{account_key}'
        print("Executing command:", cmd)
        os.system(cmd)
        print(f"Finished streaming for account with key: {account_key}\n")
    except Exception as e:
        print(f"Error streaming to account with key {account_key}. Error: {e}")


def job(job_name, account_keys, video):
    print(f"{job_name} started streaming.")
    print('')
    threads = []
    for account_key in account_keys:
        t = threading.Thread(target=stream_video_to_account, args=(VIDEO_PATHS[video], account_key))
        t.start()
        threads.append(t)
        time.sleep(10)
    for t in threads:
        t.join()


for index, set in enumerate(ACCOUNTS):
    accounts_to_stream = []
    for account in set["accounts"]:
        accounts_to_stream.append(account["key"])
    schedule.every().day.at(set["time"]).do(job, f"Set {index+1}", accounts_to_stream, get_random_video())


def exit_program():
    sys.exit()

# To handle manual exit
print('24/7 live stream schedule has started!')
print('==========================================')
for index, val in enumerate(ACCOUNTS):
    print(f"Accounts {val['accounts'][0]} through {val['accounts'][-1]} will stream from {val['time']}")
print('')

try:
    while True:
        schedule.run_pending()
        time.sleep(10)  # Check every 10 seconds
        if os.path.exists('exit.txt'):
            exit_program()
except KeyboardInterrupt:
    exit_program()