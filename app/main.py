import asyncio
import re
from typing import Dict, Any
import requests
from bs4 import BeautifulSoup

from utils.cleaning import cleaning_list
from utils.download_images import AsyncImageDownloader


async def animals_and_adjectives_scrapping(url_to_scrap: str) -> Dict[str, Dict[str, Any]]:
    f"""
    function that scraps a specific table of a wikipedia page and return a dictionary of 
    Animals with name and corresponding collaborative adjectives and also Images with animal's name and
    local_path 
    :param url_to_scrap: the url of wikipedia page to scrap
    :return: results: return a dict of animals, adjectives and local_path to images
    """

    # using BeautifulSoup and requests libraries to get and parse the web page
    page = requests.get(url_to_scrap)
    soup = BeautifulSoup(page.content, 'html.parser')
    tb = soup.find('table', class_='wikitable sortable sticky-header')

    # final result to return
    results = {}
    # intermediate result of animals with their collaborative adjectives
    results_animal = {}
    # intermediate dict of animal's name and their wikipedia page used to scrap and download images and finish
    # to build the results dict
    animals_details = {}

    # for each row in the table
    for row in tb.find_all('tr'):
        # find every cell
        cells = row.find_all('td')
        if len(cells) >= 6:
            # get the first cell that is the name of the animal
            animal_name = cells[0].find('a').get_text('title')
            animal_link = cells[0].find('a', href=True)
            # get the animal page from href
            animal_page = animal_link['href']

            # remove the reference that is sometimes on the animal's name
            animal_name = re.sub(r'\[\d+\]', '', animal_name)
            # fix the issue where an animal's name is like ass/donkey
            # could cause issue to download image
            name_animal = animal_name.replace("/", "-")

            # get the collaborative adjectives and make it a list separated by , when there are
            # multiple adjectives
            collateral_adjectives = cells[5].get_text(separator=',', strip=True).split(',')

            # cleaning the list when in the adjectives list there are things like '[', 'd', ']' IN
            # 'Cattle': ['bovine', '[', 'd', ']', 'taurine (male)', 'vaccine (female)', 'vituline (young)']
            collateral_adjectives = cleaning_list(collateral_adjectives)

            # build the intermediate dict
            results_animal[name_animal] = collateral_adjectives
            animals_details[name_animal] = animal_page

    # calls the function to scrap every page of every animal to download the image
    downloader = AsyncImageDownloader()
    results_image_animal = await downloader.download_all_images(animals_details)

    # build the result dict included 2 keys:
    # Key:"Animals" Value: a dict of animal_name and collaborative_adjectives
    # Key:"Images" Value: a dict of animal_name and local_path to image
    results["Animals"] = results_animal
    results["Images"] = results_image_animal

    return results


# generated in part (the html part) with ChatGPT
def html_output(dict_result, title="Results", output_file="results.html"):
    """
        Creates an HTML page displaying animal details in a table format.

        :param dict_result: dict, the nested dictionary with animal data and images.
        :param title: str, the title of the HTML page.
        :param output_file: str, the name of the output HTML file.
        """
    # Start building the HTML content
    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f4f4f4;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            img {{
                max-width: 100px;
                height: auto;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <table>
            <thead>
                <tr>
                    <th>Animal</th>
                    <th>Adjectives</th>
                    <th>Image</th>
                </tr>
            </thead>
            <tbody>
    """

    # Iterate over animals and their details
    animals = dict_result.get("Animals", {})
    images = dict_result.get("Images", {})
    # print(animals)
    # print(images)
    for animal, adjectives in animals.items():
        image_path = images.get(animal, "No image available")
        print(f"{animal}: {image_path}")
        # Add a table row for each animal
        html += f"""
                <tr>
                    <td>{animal}</td>
                    <td>{", ".join(adjectives)}</td>
                    <td><img src="{image_path}" alt="{animal}"></td>
                </tr>
            """

    # Close the HTML content
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """

    # Write the HTML to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"HTML file created: {output_file}")


async def main():
    url = "https://en.wikipedia.org/wiki/List_of_animal_names"
    animals_final = await animals_and_adjectives_scrapping(url)
    html_output(animals_final)


if __name__ == "__main__":
    asyncio.run(main())
