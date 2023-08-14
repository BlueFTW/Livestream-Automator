import os
import time
import schedule
import threading
import sys
import random


# Constants
FOLDER_PATH = r'C:\Users\abdul\.local\bin\ffmpeg.exe'
STREAM_URL = 'rtmp://live.twitch.tv/app/'
ACCOUNTS = [
    {
        "accounts": [
            {
                "name": "yung_blue1",
                "key": "live_901751223_tDs6rYddK6lqgMZT40nilAtQZTYeR7",
            },
            {
                "name": "yung_ftw",
                "key": "live_901752253_oojyd75Gr4tIButD0Av77ogSLEbmtE",
            },
            {
                "name": "downem_blue",
                "key": "live_901752938_yvONfKvyD1yl5ToScYn3DeIOasrQOo",
            },
            {
                "name": "yung_atw",
                "key": "live_901753515_B9v7M7rGJ1FEhSqDewM3cb3Ryf3ief",
            }
        ],
        "url": "rtmp://live.twitch.tv/app/",
        "time": "00:00",
    },
    {
        "accounts": [
            {
                "name": "blue_atw",
                "key": "live_901754007_MQkQFsJBbHZkyDzTQ94zv6HuKg8N2u",
            },
            {
                "name": "blueyungin",
                "key": "live_901754983_k50sRLwmiSzcxoXtArq7Bh7ULGyqmN",
            },
            {
                "name": "LindaTheThird",
                "key": "live_936569791_bHtaem8nWqkYBkWx8Yb81Z6faYsw3i",
            },
            {
                "name": "massivemike243",
                "key": "live_936572030_RmH4QdmBqXIgNT1GSb6r4O5BeY6mqV",
            }
        ],
        "url": "rtmp://live.twitch.tv/app/",
        "time": "06:00",
    },
    {
        "accounts": [
            {
                "name": "definitiveselene",
                "key": "live_936573143_RCJAdgwfC2KHW3EunIMEVt2aH4iWHc",
            },
            {
                "name": "thickrick02",
                "key": "live_936576426_cIBEFHGj6OzgiZgSX112hTEZieMdlA",
            },
            {
                "name": "joystickcasey",
                "key": "live_936577289_H29UVlAh5VQQIZSxrc44f0vOLZ7VE1",
            },
            {
                "name": "standardsarah",
                "key": "live_937379876_sBMY7FRe4yG3Oo4878TxHyh3TDrsID",
            }
        ],
        "url": "rtmp://live.twitch.tv/app/",
        "time": "12:00",
    },
    {
        "accounts": [
            {
                "name": "solidsteven00",
                "key": "live_937533051_hJowSWawnlDQKWMrixGhIB14O0ckQA",
            },
            {
                "name": "tallterry",
                "key": "live_937535109_v8e9nHGagqwbTDnal1SJIvB3LmrnD1",
            },
            {
                "name": "colossalcody",
                "key": "live_937536493_itkNZne2W5QNXt1UeX3x7026vmsexe",
            },
            {
                "name": "jumbojim",
                "key": "live_937537689_bOfz5zKSVcSJbFdZrxYT3azAejle1g",
            }
        ],
        "url": "rtmp://live.twitch.tv/app/",
        "time": "18:00",
    }
]
VIDEO_PATHS = {
    'Fortnite': 'videos/fortnite.mp4',
    'Minecraft': 'videos/minecraft.mp4',
    'Stardew Valley': 'videos/stardew.mp4',
    'Fall Guys': 'videos/fallguys.mp4',
    'Animal Crossing': 'videos/animalcrossing.mp4',
}

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
    schedule.every().day.at(set["time"], "America/New_York").do(job, f"Set {index+1}", accounts_to_stream, get_random_video())



def exit_program():
    sys.exit()

# To handle manual exit
print('24/7 live stream schedule has started!')
print('==========================================')
account_index = 1
up_till_account = 4
for index, val in enumerate(ACCOUNTS):
    print(f"Accounts {account_index} through {up_till_account} will stream from {val['time']}")
    account_index += len(val["accounts"])
    up_till_account += len(val["accounts"])
print('')

try:
    while True:
        schedule.run_pending()
        time.sleep(10)  # Check every 10 seconds
        if os.path.exists('exit.txt'):
            exit_program()
except KeyboardInterrupt:
    exit_program()