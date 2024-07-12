import requests
from bs4 import BeautifulSoup

# URL to scrape
url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=360936703'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get the entire parse tree
    parse_tree = soup.prettify()
    
    # Write the parse tree to a file
    with open('parse_tree.html', 'w', encoding='utf-8') as file:
        file.write(parse_tree)
    
    print('Parse tree has been written to parse_tree.html')
else:
    print('Failed to retrieve the webpage')
