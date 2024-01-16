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
Not all albums have mp3 or flac, If one does not work try the other

```
python downloader-flac.py
```
or 
```
python downloader-mp3.py
```

## Info
The downloaded files will be in either "MP3 files" or "FLAC files". The folders will be created where the python script is located.


## Custom path download

<details>
 <summary><b>MP3</b></summary>

### Windows
Replace "album_directory = os.path.join('MP3 files', sanitized_album_name)" with
```
base_directory = 'C:\\your\\custom\\path'
album_directory = os.path.join(base_directory, 'MP3 files', sanitized_album_name)
```
### Linux
Replace "album_directory = os.path.join('MP3 files', sanitized_album_name)" with
```
base_directory = '/your/custom/path'
album_directory = os.path.join(base_directory, 'MP3 files', sanitized_album_name)
```
</details>
<details>
 <summary><b>FLAC</b></summary>

### Windows
Replace "album_directory = os.path.join('FLAC files', sanitized_album_name)" with
```
base_directory = 'C:\\your\\custom\\path'
album_directory = os.path.join(base_directory, 'FLAC files', sanitized_album_name)
```
### Linux
Replace "album_directory = os.path.join('FLAC files', sanitized_album_name)" with
```
base_directory = '/your/custom/path'
album_directory = os.path.join(base_directory, 'FLAC files', sanitized_album_name)
```
</details>







