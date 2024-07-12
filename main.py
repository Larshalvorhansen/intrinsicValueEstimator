import requests
from bs4 import BeautifulSoup

url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=360936703'

def scrape(url):
    # URL to scrape

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


def getInfo(filePath):
    html = open(filePath, "r")

    soup = BeautifulSoup(html, 'html.parser')

    # Extracting the address
    address = soup.find('span', {'data-testid': 'object-address'}).text.strip()

    # Extracting the indicative price
    indicative_price = soup.find('div', {'data-testid': 'pricing-incicative-price'}).find('span', {'class': 'text-28 font-bold'}).text.strip()

    # Extracting the total price
    total_price = soup.find('div', {'data-testid': 'pricing-total-price'}).find('dd', {'class': 'm-0 font-bold'}).text.strip()

    print(f"Address: {address}")
    print(f"Indicative Price: {indicative_price}")
    print(f"Total Price: {total_price}")

def main():
    scrape(url)
    getInfo("parse_tree.html")

if __name__ == "__main__":
    main()