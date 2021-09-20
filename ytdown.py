import os
import pafy
import argparse
from pytube import Playlist, YouTube

global progress_
progress_ = 0

def mycb(total, recvd, ratio, rate, eta):
    global progress_
    var_i = int(ratio * 10000) * 1.0 / 100.0
    if var_i > progress_:
        percent = var_i
        print(f"\r %{percent} downloaded from {int((total / (1024 * 1024))*100)/100} MB data...",end="")
        progress_ = var_i

def down(link):
    yt = pafy.new(link)
    print("Video's name: " + yt.title)
    yt.getbest(preftype="mp4").download(quiet=True, callback=mycb)

def down_playlist(playlist_url,rangeofvideos=["1"]):
    global progress_
    p = Playlist(playlist_url)
    dir_title = str(p.title())
    print("Playlist's name: " + dir_title)
    dir_title2 = ""
    for x in dir_title:
        if x.isalnum():
            dir_title2 += x
        elif x.isspace():
            dir_title2 += "_"
        else:
            dir_title2 += "-"
    dir_title = dir_title2
    cur_dir = os.getcwd()
    try:
        os.mkdir(cur_dir + "\\" + dir_title)
        os.chdir(dir_title)
    except FileExistsError:
        print("Directory is already exits!!!")
        os.chdir(dir_title)
    except FileNotFoundError as fnfe:
        raise fnfe
    except Exception as e:
        raise e
    
    if len(rangeofvideos) == 1:
        for url in p.video_urls:
            down(url)
            progress_ = 0
    elif len(rangeofvideos) == 2:
        first = int(rangeofvideos[0])
        second = int(rangeofvideos[1])
        for url in p.video_urls[first-1:second]:
            down(url)
            print()
            progress_ = 0
    os.chdir("..")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', dest='url',help='Url for single video')
    parser.add_argument('-p', '--playlist', dest='playlist',help='Url for entire playlist')
    parser.add_argument('-r', '--range', dest='range_playlist',help='Download a specific range of playlists videos via x-y like 1-10')
    args = parser.parse_args()

    if args.url:
        down(args.url)
        exit()
    elif args.playlist:
        playlist_url = args.playlist
        if args.range_playlist:
            if "-" not in args.range_playlist or not (args.range_playlist.split("-")[0]).isnumeric() or not (args.range_playlist.split("-")[1]).isnumeric():
                print("Please only give numeric inputs like 1-10 or don't forget to type a dash (-) between the numbers!!")
                exit()
            rangeofvideos = args.range_playlist.split("-")
            down_playlist(playlist_url,rangeofvideos)
        else:
            down_playlist(playlist_url)