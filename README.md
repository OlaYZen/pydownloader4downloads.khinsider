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

## Custom download path
Find "album_directory = os.path.join('Audio files', sanitized_album_name)" and replace it with the following code

### Windows
```
album_directory = os.path.join(r'C:\your\custom\path', sanitized_album_name)
```
### Linux
```
album_directory = os.path.join('/your/custom/path', sanitized_album_name)
```








