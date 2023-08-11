import os
import time
import schedule
import threading
import sys
import random


# Constants
FOLDER_PATH = 'C:/ENTER/THE/PATH/TO/THE/FUCKING/FFMPEG.EXE'
STREAM_URL = 'rtmp://live.twitch.tv/app/'


# Add your own accounts here
ACCOUNTS = {
    '1. yung_blue1': {
        'key': 'live_901751223_tDs6rYddK6lqgMZT40nilAtQZTYeR7',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '2. yung_ftw': {
        'key': 'live_901752253_oojyd75Gr4tIButD0Av77ogSLEbmtE',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '3. downem_blue': {
        'key': 'live_901752938_yvONfKvyD1yl5ToScYn3DeIOasrQOo',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '4. yung_atw': {
        'key': 'live_901753515_B9v7M7rGJ1FEhSqDewM3cb3Ryf3ief',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '5. blue_atw': {
        'key': 'live_901754007_MQkQFsJBbHZkyDzTQ94zv6HuKg8N2u',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '6. blueyungin': {
        'key': 'live_901754983_k50sRLwmiSzcxoXtArq7Bh7ULGyqmN',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '7. LindaTheThird': {
        'key': 'live_936569791_bHtaem8nWqkYBkWx8Yb81Z6faYsw3i',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '8. massivemike243': {
        'key': 'live_936572030_RmH4QdmBqXIgNT1GSb6r4O5BeY6mqV',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '9. definitiveselene': {
        'key': 'live_936573143_RCJAdgwfC2KHW3EunIMEVt2aH4iWHc',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '10. thickrick02': {
        'key': 'live_936576426_cIBEFHGj6OzgiZgSX112hTEZieMdlA',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '11. joystickcasey': {
        'key': 'live_936577289_H29UVlAh5VQQIZSxrc44f0vOLZ7VE1',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '12. standardsarah': {
        'key': 'live_937379876_sBMY7FRe4yG3Oo4878TxHyh3TDrsID',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '13. solidsteven00': {
        'key': 'live_937533051_hJowSWawnlDQKWMrixGhIB14O0ckQA',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '14. tallterry': {
        'key': 'live_937535109_v8e9nHGagqwbTDnal1SJIvB3LmrnD1',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '15. colossalcody': {
        'key': 'live_937536493_itkNZne2W5QNXt1UeX3x7026vmsexe',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '16. jumbojim00': {
        'key': 'live_937537689_bOfz5zKSVcSJbFdZrxYT3azAejle1g',
        'url': 'rtmp://live.twitch.tv/app/'
    },
    '17. ProjectOden': {
        'key': 'sk_us-west-2_87WSgfz1ZmkR_tJI9rYvjJ6J5KKrBn3SHRpg1rK3uLr',
        'url': 'rtmps://fa723fc1b171.global-contribute.live-video.net/'
    }
}


VIDEO_PATHS = {
    'Fortnite': 'videos/fortnite.mp4',
    'Minecraft': 'videos/minecraft.mp4',
    'Stardew Valley': 'videos/stardew.mp4',
    'Fall Guys': 'videos/fallguys.mp4',
    'Animal Crossing': 'videos/animalcrossing.mp4',
}

def get_random_duration(min_hours=5, max_hours=6):
    return random.randint(min_hours * 60 * 60, max_hours * 60 * 60)


def stream_video_to_account(video_path, account_key, account_url):
    """
    Uses ffmpeg to stream a video to a given account.
    """
    try:
        print(f"Starting stream for account with key: {account_key}")  # Log when the stream starts

        duration = get_random_duration()
        cmd = f'{FOLDER_PATH} -re -stream_loop -1 -i {video_path} -c:v copy -c:a aac -strict experimental -t {duration} -f flv {account_url}{account_key}'

        # Print the command for debugging
        print("Executing command:", cmd)

        os.system(cmd)

        print(f"Finished streaming for account with key: {account_key}")  # Log when the stream ends
        print('')
    except Exception as e:
        print(f"Error streaming to account with key {account_key}. Error: {e}")


def job(job_name, accounts, video):
    print(f"{job_name} started streaming.")
    print('')
    threads = []
    for account_name in accounts:
        account = ACCOUNTS[account_name]
        t = threading.Thread(target=stream_video_to_account, args=(VIDEO_PATHS[video], account['key'], account['url']))
        t.start()
        threads.append(t)
        time.sleep(10)  # Small delay to stagger starting streams (optional)

    for t in threads:
        t.join()

# Schedule the tasks
schedule.every().day.at("00:00").do(job, 'Set 1', ['1. yung_blue1', '2. yung_ftw'], 'Fortnite') # Streams 1 and 2 at 12AM
schedule.every().day.at("06:00").do(job, 'Set 2', ['3. downem_blue', '4. yung_atw'], 'Minecraft') # Streams 3 and 4 at 6AM
schedule.every().day.at("12:00").do(job, 'Set 3', ['5. blue_atw', '6. blueyungin'], 'Stardew Valley') # Streams 5 and 6 at 12PM
#schedule.every().day.at("18:00").do(job, 'Set 4', ['7. LindaTheThird', '8. massivemike243'], 'Minecraft') # future schedule, Streams 7 and 8 at 6PM


def exit_program():
    sys.exit()

# To handle manual exit
print('24/7 live stream schedule has started!')
print('==========================================')
print('Accounts 1 & 2 will stream from 12AM - 6AM')
print('Accounts 3 & 4 will stream from 6AM - 12PM')
print('Accounts 5 & 6 will stream from 12PM - 6PM')
print('Accounts X & X will stream from 6PM - 12AM')
print('')

while True:
    schedule.run_pending()
    time.sleep(10)  # Check every 10 seconds
    if os.path.exists('exit.txt'):
        exit_program()
