import os
import requests
import multiprocessing
from bs4 import BeautifulSoup
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

url = input("Enter the URL: ")

# Fetch HTML content from the specified URL
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all elements with class 'playlistDownloadSong'
elements = soup.find_all(class_='playlistDownloadSong')

# Store URLs in a list
urls = []
for index, element in enumerate(elements):
    link = element.find('a')
    if link:
        url = link.get('href')
        full_url = f'https://downloads.khinsider.com{url}'
        urls.append(full_url)


# Function to fetch and parse HTML content
def get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


# Function to find and save MP3 URLs and album name
def find_mp3_urls_and_album_name(html_content):
    mp3_urls = []
    album_name = None

    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all links in the page
        links = soup.find_all("a", href=True)
        for link in links:
            href = link.get("href")
            if href.endswith(".mp3"):
                mp3_url = href
                mp3_urls.append(mp3_url)

        # Extract album name
        album_name_element = soup.select_one("#pageContent > p:nth-child(6) > b:nth-child(1)")
        if album_name_element:
            album_name = album_name_element.text.strip()

    return mp3_urls, album_name


# Function to download a file
def download_file(url, directory, total_progress):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Unquote the filename to convert %20 back to spaces
        filename = unquote(os.path.join(directory, os.path.basename(url)))

        with open(filename, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                file.write(data)
        total_progress.update(1)  # Update the total progress by 1 for each file downloaded

        # print(f"Downloaded: {filename}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")


# Function to process a single URL
def process_url(url, total_progress):
    # print(f"Scraping {url} for MP3 files...")
    html_content = get_html_content(url)
    mp3_urls, album_name = find_mp3_urls_and_album_name(html_content)

    if mp3_urls and album_name:
        # Sanitize album name for creating a directory
        sanitized_album_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '' for c in album_name)
        album_directory = os.path.join('MP3 files', sanitized_album_name)
        os.makedirs(album_directory, exist_ok=True)

        # print(f"MP3 files found for album '{album_name}':")
        for mp3_url in mp3_urls:
            download_file(mp3_url, album_directory, total_progress)
    else:
        # No need to print an error message here
        pass


def get_cpu_threads():
    try:
        # For Linux/Unix/MacOS
        num_threads = os.cpu_count() or 1
    except NotImplementedError:
        # For Windows
        num_threads = multiprocessing.cpu_count() or 1

    return num_threads

if __name__ == "__main__":
    cpu_threads = get_cpu_threads()

# Use ThreadPoolExecutor to run the process_url function concurrently
with ThreadPoolExecutor(max_workers=cpu_threads) as executor:
    total_items = len(urls)
    total_progress = tqdm(total=total_items, desc="Total Progress", position=0)

    futures = []
    for url in urls:
        future = executor.submit(process_url, url, total_progress)
        futures.append(future)

    # Wait for all futures to complete
    for future in futures:
        future.result()

    total_progress.close()

# Display the final message based on the download results
downloaded_files = total_progress.n
error_message = None

if downloaded_files == 0:
    error_message = "Album name missing from site."
elif downloaded_files < total_items:
    error_message = f"{total_items - downloaded_files} files not downloaded. Missing MP3 files."

if error_message:
    print(error_message)
