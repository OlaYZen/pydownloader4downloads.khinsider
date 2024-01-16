import os
import requests
import multiprocessing
from bs4 import BeautifulSoup
from urllib.parse import unquote
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import aiohttp
import asyncio

MAX_RETRIES = 2

url = input("Enter the URL: ")

# Fetch HTML content from the specified URL
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'lxml')

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

# List to store failed URLs
failed_urls = []

# Lock to prevent concurrent printing of error messages
print_lock = asyncio.Lock()


# Function to fetch HTML content asynchronously
async def async_get_html_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response.raise_for_status()
                return await response.text()
    except aiohttp.ClientError as e:
        return None


# Function to find and save FLAC, MP3, or M4A URLs and album name
def find_audio_urls_and_album_name(html_content):
    audio_urls = []
    album_name = None

    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all links in the page
        links = soup.find_all("a", href=True)
        for link in links:
            href = link.get("href")
            if href.endswith(".flac"):
                audio_url = href
                audio_urls = [audio_url]
                break
            elif href.endswith(".mp3") or href.endswith(".m4a"):
                audio_urls.append(href)

        # Extract album name
        album_name_element = soup.select_one("#pageContent > p:nth-child(6) > b:nth-child(1)")
        if album_name_element:
            album_name = album_name_element.text.strip()

    return audio_urls, album_name


# Function to download a file asynchronously with retry
async def async_download_audio_file(session, url, directory, total_progress):
    retries = 0

    while retries <= MAX_RETRIES:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                content = await response.read()

                filename = unquote(os.path.join(directory, os.path.basename(url)))

                with open(filename, 'wb') as file:
                    file.write(content)

                total_progress.update(1)
                break  # Break the loop if download is successful
        except Exception as e:
            retries += 1
            if retries <= MAX_RETRIES:
                await asyncio.sleep(2)  # Wait for a moment before retrying
            else:
                async with print_lock:
                    failed_urls.append(url)
                break  # Break the loop if max retries reached


# Function to process a single URL asynchronously
async def async_process_url(session, url, total_progress):
    html_content = await async_get_html_content(url)
    audio_urls, album_name = find_audio_urls_and_album_name(html_content)

    if audio_urls and album_name:
        sanitized_album_name = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '' for c in album_name)
        album_directory = os.path.join('Audio files', sanitized_album_name)
        os.makedirs(album_directory, exist_ok=True)

        for audio_url in audio_urls:
            await async_download_audio_file(session, audio_url, album_directory, total_progress)
    else:
        pass  # No audio files found for the URL


def get_cpu_threads():
    try:
        num_threads = os.cpu_count() or 1
    except NotImplementedError:
        num_threads = multiprocessing.cpu_count() or 1

    return num_threads


async def main():
    cpu_threads = get_cpu_threads()

    async with aiohttp.ClientSession() as session:
        with ThreadPoolExecutor(max_workers=cpu_threads) as executor:
            total_items = len(urls)
            total_progress = tqdm(total=total_items, desc="Total Progress", position=0)

            futures = []
            loop = asyncio.get_event_loop()

            for url in urls:
                # Corrected: use loop.create_task() to ensure the coroutine is awaited properly
                future = loop.create_task(async_process_url(session, url, total_progress))
                futures.append(future)

            # Await all the futures
            await asyncio.gather(*futures)

            total_progress.close()

    # Display error messages for failed URLs after the download is complete
    if failed_urls:
        print("\nThe following files encountered errors during download:")
        for failed_url in failed_urls:
            print(f"- {failed_url}")


if __name__ == "__main__":
    asyncio.run(main())
