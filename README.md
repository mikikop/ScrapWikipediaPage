# Scraping a wikipedia page

Scraping a wikipedia page

Using the page https://en.wikipedia.org/wiki/List_of_animal_names, write a python program that will output all of the “collateral adjectives” and all of the “animals” which belong to it. If an animal has more than one collateral adjective, use all of them (mentioning it more than once).
{
  "Animals":
   	“Aardvark”: [orycteropodian],
  	“Ant”: [formic, myrmicine],
   ....
}

- Download the picture of each animal into /tmp/ and add a local link when displaying the animals.
  {
  "Animals":
   	“Aardvark”: [orycteropodian],
  	“Ant”: [formic, myrmicine],
   ....
  "Images":
    “Aardvark”: "/tmp/aardvark.jpeg",
  	“Ant”: "/tmp/ant.jpeg",
   ....
}

- Write at least 2 test cases for the code you just wrote.
  
- Output the results to an html file.

Using BeautifulSoup and Requests (but not pandas)
