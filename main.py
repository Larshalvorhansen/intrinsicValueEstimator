import requests
from bs4 import BeautifulSoup
import re
import csv

# Define the input filename
input_filename = 'parse_tree.html'

# Define the output CSV filename
output_filename = 'finnLenker.csv'

#url = 'https://www.finn.no/realestate/homes/ad.html?finnkode=360936703'
url = 'https://www.finn.no/realestate/homes/search.html?location=0.20061'


def scrape(url,output_filename):
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
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(parse_tree)
        
        print('Parse tree has been written to parse_tree.html')
    else:
        print('Failed to retrieve the webpage')


def getInfo(filePath):
    with open(filePath, "r", encoding="utf-8") as html_file:
        soup = BeautifulSoup(html_file, 'html.parser')

    # Extracting the address
    address = soup.find('span', {'data-testid': 'object-address'}).text.strip()

    # Extracting the indicative price
    indicative_price = soup.find('div', {'data-testid': 'pricing-incicative-price'}).find('span', {'class': 'text-28 font-bold'}).text.strip()
    indicative_price_short = indicative_price.replace(" ","")

    # Extracting the total price
    total_price = soup.find('div', {'data-testid': 'pricing-total-price'}).find('dd', {'class': 'm-0 font-bold'}).text.strip()

    info = [address, f"ind price {indicative_price_short}", total_price.replace(" ","")]
    return info


def writeInfoToCsv(filePath, csvFilePath):
    try:
        info = getInfo(filePath)
        
        # Writing to a CSV file
        with open(csvFilePath, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            #writer.writerow(["Address", "Indicative Price", "Total Price"])
            writer.writerow(info)
    except FileNotFoundError:
        print(f"The file {filePath} does not exist. Continuing without writing to CSV.")
    except Exception as e:
        print(f"An error occurred: {e}. Continuing without writing to CSV.")


def getFinnKode(input_filename,output_filename):
    # Read the content of the file
    with open(input_filename, 'r') as file:
        content = file.read()

    # Find all occurrences of 'finnkode=' followed by numbers
    finnkodes = re.findall(r'finnkode=(\d+)', content)

    # Write the extracted numbers and URLs to a CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Write the header
        csvwriter.writerow(['finnkode', 'URL'])
        # Write the finnkodes and URLs
        for finnkode in finnkodes:
            url = f"https://www.finn.no/realestate/homes/ad.html?finnkode={finnkode}"
            csvwriter.writerow([finnkode, url])

    print(f'Extracted finnkodes and URLs have been written to {output_filename}')


def main():
    finn_search_url = "https://www.finn.no/realestate/homes/search.html?location=0.20061&location=0.20018"
    scrape(url,"finn_seach_scrape.html")
    getFinnKode("finn_seach_scrape.html","finn_koder.csv")

    with open("data5.csv", mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Address", "Indicative Price", "Total Price"])

    with open("finn_koder.csv", newline='') as file:
        reader = csv.reader(file)
        # Skip header if your CSV has one
        next(reader, None)
        for row in reader:
            scrape(row[1],f"data/{row[0]}.html")
            writeInfoToCsv(f"data/{row[0]}.html", f"data5.csv")


# input Finn_search_url
# ⬇️
# scrape finn_seach_url
# ⬇️
# getFinnKode
# ⬇️
# For all finnKode:
# 	scrape html
# ⬇️
# For all scrape:
# 	Get info & write to csv


if __name__ == "__main__":
    main()