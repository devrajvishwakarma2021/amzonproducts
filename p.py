import csv
import requests
from bs4 import BeautifulSoup
import time

# Scrape product URLs from the initial search page
base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
pages_to_scrape = 20
product_urls = []

for page_num in range(1, pages_to_scrape + 1):
    url = f"{base_url}{page_num}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_containers = soup.find_all('div', class_='s-result-item')
    
    for container in product_containers:
        product_link = container.find('a', class_='a-link-normal')
        if product_link:
            product_urls.append("https://www.amazon.in" + product_link['href'])

# Scrape individual product pages
csv_filename = 'amazon_products_extended.csv'
csv_headers = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer']

with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_headers)

    for product_url in product_urls:
        response = requests.get(product_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_name_tag = soup.find('span', class_='a-size-large')
        product_name = product_name_tag.text if product_name_tag else 'N/A'

        product_price_tag = soup.find('span', {'id': 'priceblock_ourprice'})
        product_price = product_price_tag.text.strip() if product_price_tag else 'N/A'

        rating_tag = soup.find('span', {'class': 'a-icon-alt'})
        rating = rating_tag.text.split()[0] if rating_tag else 'N/A'

        num_reviews_tag = soup.find('span', {'id': 'acrCustomerReviewText'})
        num_reviews = num_reviews_tag.text.split()[0] if num_reviews_tag else 'N/A'

        product_description_tag = soup.find('div', {'id': 'productDescription'})
        product_description = product_description_tag.get_text(strip=True) if product_description_tag else 'N/A'

        asin_tag = soup.find('th', string='ASIN')
        asin = asin_tag.find_next('td').get_text(strip=True) if asin_tag else 'N/A'

        manufacturer_tag = soup.find('th', string='Manufacturer')
        manufacturer = manufacturer_tag.find_next('td').get_text(strip=True) if manufacturer_tag else 'N/A'

        csv_writer.writerow([product_url, product_name, product_price, rating, num_reviews, product_description, asin, product_description, manufacturer])

        time.sleep(2)  # Sleep to avoid overloading the server

print(f"Scraping completed. Extended data saved to {csv_filename}")




# import requests
# from bs4 import BeautifulSoup
# import csv

# # Define the base URL and headers
# base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
# headers = {
#     "User-Agent": "Your User Agent Header Here"
# }

# # Initialize lists to store scraped data
# product_data = []

# # Iterate through multiple pages
# for page in range(1, 21):  # Scrape at least 20 pages
#     url = f"{base_url}&page={page}"
#     response = requests.get(url, headers=headers)
#     soup = BeautifulSoup(response.content, "html.parser")
    
#     # Extract product details
#     products = soup.find_all("div", class_="s-result-item")
#     for product in products:
#         product_name_element = product.find("span", class_="a-text-normal")
#         if product_name_element:
#             product_name = product_name_element.get_text(strip=True)
#         else:
#             product_name = "N/A"

#         product_price_element = product.find("span", class_="a-price-symbol")
#         if product_price_element:
#             product_price = product_price_element.get_text(strip=True) + product.find("span", class_="a-price-whole").get_text(strip=True)
#         else:
#             product_price = "N/A"

#         product_rating_element = product.find("span", class_="a-icon-alt")
#         if product_rating_element:
#             product_rating = product_rating_element.get_text(strip=True).split()[0]
#         else:
#             product_rating = "N/A"

#         product_reviews_element = product.find("span", class_="a-size-base")
#         if product_reviews_element:
#             product_reviews = product_reviews_element.get_text(strip=True)
#         else:
#             product_reviews = "N/A"

#         # Extract product URL with error handling
#         product_url_element = product.find("a", class_="a-link-normal")
#         if product_url_element and product_url_element.has_attr("href"):
#             product_url = "https://www.amazon.in" + product_url_element["href"]
#         else:
#             product_url = "N/A"
        
#         product_data.append([product_url, product_name, product_price, product_rating, product_reviews])

# # Export data to CSV
# with open("product_listings.csv", "w", newline="", encoding="utf-8") as csvfile:
#     csv_writer = csv.writer(csvfile)
#     csv_writer.writerow(["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"])
#     csv_writer.writerows(product_data)



















# import time

# # Load CSV file and retrieve product URLs
# product_urls = []
# with open('product_listing.csv', 'r', encoding='utf-8') as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)  # Skip header row
#     for row in reader:
#         product_urls.append(row[0])

# # Initialize a new CSV file for detailed product information
# detailed_csv_filename = 'detailed_amazon_products.csv'
# detailed_csv_header = ['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer']
# with open(detailed_csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(detailed_csv_header)

# # Scrape details for each product URL
# for product_url in product_urls:
#     response = requests.get(product_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
    
#     # Extract product details
#     description = soup.find('meta', {'name': 'description'})['content']
#     asin = soup.find('th', {'class': 'a-span7'}).find_next('td').text
#     product_description = soup.find('div', {'id': 'productDescription'}).text.strip()
#     manufacturer = soup.find('a', {'id': 'bylineInfo'}).text
    
#     with open(detailed_csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
#         writer = csv.writer(csvfile)
#         writer.writerow([product_url, description, asin, product_description, manufacturer])
    
#     # Amazon might block excessive requests, so adding a delay between requests
#     time.sleep(2)
