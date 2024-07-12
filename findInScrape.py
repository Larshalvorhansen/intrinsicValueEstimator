from bs4 import BeautifulSoup

html = open("parse_tree.html", "r")

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