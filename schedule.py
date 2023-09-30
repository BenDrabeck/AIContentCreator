import os
import csv
from datetime import *
import pandas as pd

def get_datetime(str, format) -> datetime:
    return datetime.strptime(str, format)

def isPast(schedule: datetime):
    now = datetime.now()
    return schedule < now

#adds a channel, cokies_path, and 
def new_channel(name, cookies_path, genre, platform, schedule = None):
    # Read the existing CSV file
    try:
        channels = pd.read_csv("channels.csv")
    except FileNotFoundError:
        channels = pd.DataFrame(columns=['NAME', 'COOKIES_PATH', 'SCHEDULE', 'GENRE', 'PLATFORM'])

    if name in channels['NAME'].values:
        print(f"Channel {name} already exists.")
        return

    # Use default_schedule if schedule is None
    default_schedule = "7_8_16\n3_7_22\n2_4_6\n7_8_23\n9_12_19\n5_13_15\n11_19_20"
    if schedule is None:
        schedule = default_schedule

    new_channel_row = {
        'NAME': name,
        'COOKIES_PATH': cookies_path,
        'SCHEDULE': schedule,
        'GENRE': genre,
        'PLATFORM': platform
    }

    # Append the new row to the channels DataFrame
    channels = channels.append(new_channel_row, ignore_index=True)

    # Save the updated DataFrame to the CSV file
    channels.to_csv('channels.csv', index=False)
    print(f"Channel {name} has been added successfully.")

    channel_schedule_file = f'{name}_schedule.txt'
    with open(channel_schedule_file, 'w') as file:
        file.write(schedule)
    print(f"Cache text file created for channel {name}.")


#make it delete from a file
def delete_channel(name):
    verify = input("ARE YOU SURE?(YES): ")
    if verify == "YES":
        channels = pd.read_csv("channels.csv")
        channels = channels[channels['NAME'] != name] # Drop the row for the channel
        channels.to_csv('channels.csv', index=False)


        channel_schedule_file = f'{name}_schedule.txt'
        try:
            os.remove(channel_schedule_file)
            print(f"Channel {name} and its corresponding schedule file have been deleted.")
        except FileNotFoundError:
            print(f"Channel {name} deleted, but corresponding schedule file was not found.")
    else:
        print(f"Channel {name} does not exist.")
    
def new_video(id, title, channel):
    cached = pd.read_csv("cached.csv")
    channels = pd.read_csv("channels.csv")
    videos = {}
    for column in cached.columns:
        if column == "ID":
            videos[column] = id
        elif column == "TITLE":
            videos[column] = title
        elif column == "CHANNEL":
            videos[column] = channel
        elif column == "SCHEDULE":
            videos[column] = get_next_post_time(channel) #get_schedule(channel)
        elif column == "UPLOAD":
            videos[column] = "W"
        elif column == "GENRE":
            videos[column] = get_genre_from_channel(channel)
    cached = cached.append(videos, ignore_index=True)
    cached.to_csv('cached.csv', index=False)

def get_genre_from_channel(channel):
    with open('channels.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['CHANNEL'] == channel:
                return row['GENRE']
    return None

def get_next_post_time(channel, schedule_file = 'schedule.txt') -> datetime:
    cached = pd.read_csv("cached.csv")
    current = datetime.now()

    schedule_file = f'{channel}_schedule.txt'
    #if there is already an item in cached, set current to the latest time in the cached
    if len(cached) > 0:
        current = datetime.strptime(cached.tail()["SCHEDULE"].iloc[0], "%Y-%m-%d %H:%M:%S")

    #create list of times to post
    times: list
    with open(schedule_file) as schedule:
        times = schedule.read().split("\n")

    times = [item.split("_") for item in times]

    #if it is past the last posting time of the day, make the current time tomorrow 
    if current.hour > int(times[datetime.weekday(current)][-1]):
        current = (current+timedelta(days = 1)).replace(hour= 0, minute= 0, second= 0, microsecond=0)
        
    #now that we are on the correct day, find the posting time that has not been reached yet
    for time in times[datetime.weekday(current)]:
        if current.hour < int(time):
            current = current.replace(hour = int(time))
            return current
    

#if __name__ == "__main__":
    #get_next_post_time()

def set_posted(channel, video_id, set_to_posted=True):
    cached = pd.read_csv("cached.csv")
    if 'UPLOAD' not in cached.columns:
        cached['UPLOAD'] = 'W'

    video_index = cached[cached['ID'] == video_id].index

    if not video_index.empty:
        if set_to_posted:
            cached.loc[video_index, 'UPLOAD'] = "S"
        else:
            cached.loc[video_index, 'UPLOAD'] = "F"

        cached.to_csv('cached.csv', index=False)
        print(f"Status for video {video_id} in channel {channel} has been set to {'S' if set_to_posted else 'W'}.")
    else:
        print(f"No video found with ID {video_id}.")


def get_channels_and_cookies():
    channels_df = pd.read_csv("channels.csv")
    channels_and_cookies = {row['NAME']: row['COOKIES_PATH'] for index, row in channels_df.iterrows()}
    return channels_and_cookies

def get_cookies(channel_name):
    channels = pd.read_csv("channels.csv")
    cookies_path = channels[channels['NAME'] == channel_name]['COOKIES_PATH'].iloc[0]
    return cookies_path

def get_video_id(title=None, channel=None):
    cached = pd.read_csv("cached.csv")
    if title:
        video_id = cached[cached['TITLE'] == title]['ID'].iloc[0]
    elif channel:
        video_id = cached[cached['CHANNEL'] == channel]['ID'].iloc[0]
    else:
        return "Criteria not specified"
    return video_id

def get_post_time(video_id):
    cached = pd.read_csv("cached.csv")
    post_time = cached[cached['ID'] == video_id]['SCHEDULE'].iloc[0]
    return datetime.strptime(post_time, "%Y-%m-%d %H:%M:%S")

def get_channel_name(video_id):
    cached = pd.read_csv("cached.csv")
    channel_name = cached[cached['ID'] == video_id]['CHANNEL'].iloc[0]
    return channel_name


def get_unlinked_cookies():

    linked_cookies = pd.read_csv("channels.csv")['COOKIES_PATH'].values.tolist()
    cookies_directory = 'cookies_tiktok'
    if not os.path.exists(cookies_directory):
        print(f"The directory {cookies_directory} does not exist.")
        return
    unlinked_cookies = []

    for filename in os.listdir(cookies_directory):
        file_path = os.path.join(cookies_directory, filename)
        if file_path not in linked_cookies:
            unlinked_cookies.append(file_path)

    if unlinked_cookies:
        print("Here are all the cookies that haven't been linked to a channel:")
        for cookie in unlinked_cookies:
            print(cookie)
        response = input("Would you like to link these cookies to a new channel? (YES/NO): ")
        if response == "YES":
            for cookie in unlinked_cookies:
                name = input(f"Enter the channel name for cookie {cookie}: ")
                schedule = input(f"Enter the schedule for channel {name}: ")
                new_channel(name, cookie, schedule)
                print(f"Channel {name} has been added successfully.")
    else:
        print("No unlinked cookies found.")

