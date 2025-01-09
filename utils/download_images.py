import asyncio
import urllib.request
import os

import aiohttp
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import Dict

# Load environment variables
load_dotenv()


class AsyncImageDownloader:
    def __init__(self):
        self._dict = {}

    async def download_image(self, animal: str, local_url: str) -> None:
        url_complete = "https://en.wikipedia.org" + local_url
        file_path = '../images/tmp/'

        async with aiohttp.ClientSession() as session:
            async with session.get(url_complete) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                images = soup.select('table.infobox a.mw-file-description img.mw-file-element[src]')
                full_path = file_path + f"{animal}.jpg"

                if images:
                    img_url = images[0]['src']
                    if not img_url.startswith('http'):
                        img_url = 'https:' + img_url

                    async with session.get(img_url) as img_response:
                        if img_response.status == 200:
                            with open(full_path, 'wb') as f:
                                f.write(await img_response.read())
                            self._dict[animal] = full_path
                else:
                    await generate_image_animal(animal, file_path + f"{animal}.jpg")
                    self._dict[animal] = full_path

    async def download_all_images(self, animals_data: Dict[str, str]) -> Dict[str, str]:
        tasks = []
        for animal, url in animals_data.items():
            task = asyncio.create_task(self.download_image(animal, url))
            tasks.append(task)

        await asyncio.gather(*tasks)
        return self._dict


# def download_image_animal(local_url: str, file_name: str):
#     """
#     Returns the local_path to image for an animal
#
#     :param local_url: url of the animal page
#     :param file_name: the name of the animal
#     :return: full_path: a local_path to the image
#     """
#
#     # building the url of the animal page where there is an image
#     url_complete = "https://en.wikipedia.org" + local_url
#
#     # file_path to store the image
#     file_path = '../images/tmp/'
#
#     # use BeautifulSoup and requests to get and parse the page
#     page = requests.get(url_complete)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     image = soup.select_one('table.infobox a.mw-file-description img.mw-file-element[src]')
#     full_path = file_path + file_name + '.jpg'
#
#     # some animal has None url to image
#     if image is not None:
#         urllib.request.urlretrieve('https:' + image['src'], full_path)
#     else:
#         generate_image_animal(file_name, full_path)
#
#     return full_path


async def generate_image_animal(animal: str, output_path: str):
    # Set your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")  # Assumes the key is stored in an environment variable
    if not api_key:
        raise ValueError("OpenAI API key is missing. Set the OPENAI_API_KEY environment variable.")

    # Endpoint URL
    url = "https://api.openai.com/v1/images/generations"

    # Request headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Request payload
    data = {
        "model": "dall-e-3",
        "prompt": f"image of a {animal} in its natural habitat",
        "n": 1,
        "size": "1024x1024",
    }

    # Send the request
    response = requests.post(url, headers=headers, json=data)

    # Check for a successful response
    if response.status_code == 200:
        response_data = response.json()
        image_url = response_data["data"][0]["url"]

        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            # save the image
            file_name = os.path.join(output_path)
            with open(file_name, "wb") as f:
                f.write(image_response.content)
            print(f"Image saved : {file_name}")
        else:
            print(f"Error while downloading : {image_response.status_code}")
    else:
        print(f"error while generating the image : {response.status_code} - {response.text}")


async def main():
    downloader = AsyncImageDownloader()
    url = "/wiki/Bull"
    await downloader.download_image("Bull", url)

if __name__ == "__main__":
    asyncio.run(main())

