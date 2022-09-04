# Auto-Channel-Archiver
Automatically downloads a youtube channels latest videos

Requires:

    #pip packages
    colorama
    #programs
    yt-dlp
    
How to use:

1. Have a folder where all of your archives are and create a folder for each channel you intend to archive
2. In the autoarchive.py file, edit line 67 to have the correct data, where the data file name can be whatever you want (i use 'LatestVideos.txt') and the root folder is the directory above all the individual channel folders
3. In the autoarchive.py file, edit line 65 so the dictionary is formatted key=channel id beggining with UC, value=archive subfolder from root. To get the channel id either use the channel url or this [https://commentpicker.com/youtube-channel-id.php](https://commentpicker.com/youtube-channel-id.php)
4. Run autoArchive.py with python, it only does one sweep, so i reccomend using a bash while loop like this: <code>while true; do python3 autoArchive.py; done</code>
