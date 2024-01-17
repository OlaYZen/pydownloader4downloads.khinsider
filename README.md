# pydownloader4[downloads.khinsider](https://downloads.khinsider.com/)
Download almost any album from [downloads.khinsider](https://downloads.khinsider.com/) using a multithreaded python script

## How to use the script

Download the source code by running git clone
```
git clone https://github.com/OlaYZen/pydownloader4downloads.khinsider.git
```

Install the required python libraries by downloading the requirements.txt found in the source code and running the following command
```
pip install -r requirements.txt
```
Start the program using Python and enter the album URL of the website by running

```
python Downloader.py
```

## Info
The script tries to find FLAC, MP3 and M4A files. It prioritizes FLAC files but if there isnt then it tries MP3 and if both are misisng then M4A.

The downloaded files will be "Audio files". By default the folder will be created where the python script is located.

## Settings
Some basic settings can be changed inside the settings.ini file. This file is needed to make the script work. Inside the file, you may find options such as changing the download path, amount of threads, priority of the downloads, and amount of retries before giving an error.

Here is the default settings
```
[Retries] ; Amount of retries per file before the script gives an error 
max_retries = 2

[Threads] ; Setting this value to 0, every thread on the cpu will be used
max_workers = 1

[Download]
priority_order = flac, mp3, m4a
; C:\example\for\windows
; /example/for/linux
; If empty, the downloads will be inside a folder called-
; "Audio files" in the same location as the script
download_path = 
```