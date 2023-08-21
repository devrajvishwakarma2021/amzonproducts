import csv
import requests
from bs4 import BeautifulSoup

base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_"
pages_to_scrape = 20

# Create a CSV file to store the scraped data
csv_filename = 'amazonproducts.csv'
csv_headers = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews']

with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(csv_headers)

    for page_num in range(1, pages_to_scrape + 1):
        url = f"{base_url}{page_num}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        product_containers = soup.find_all('div', class_='s-result-item')

        for container in product_containers:
            # product_url = container.find('a', class_='a-link-normal')['href']

            product_link = soup.find('a', class_='a-link-normal')
            if product_link:
                product_url = "https://www.amazon.in" + product_link.get('href')
            else:
               product_url = 'N/A'

            product_name = container.find('span', class_='a-text-normal')
            if product_name:
                product = product_name.text
            else:
                product_price = 'N/A'

            product_price_tag = container.find('span', class_='a-offscreen')
            if product_price_tag:
                product_price = product_price_tag.text
            else:
                product_price = 'N/A'

            rating_tag = container.find('span', class_='a-icon-alt')
            if rating_tag:
                rating = rating_tag.text.split()[0]
            else:
                rating = 'N/A'

            num_reviews_tag = container.find('span', {'class': 'a-size-base'})
            if num_reviews_tag:
                num_reviews = num_reviews_tag.text.split()[0]
            else:
                num_reviews = 'N/A'

            csv_writer.writerow([f"https://www.amazon.in{product_url}", product_name, product_price, rating, num_reviews])

print(f"Scraping completed. Data saved to {csv_filename}")


















# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

# # base_url = "https://www.amazon.in/s"
# base_url="https://www.amazon.in/stores/page/AFEC9EAB-D144-42D1-A8B2-6AD10432EEEE/?_encoding=UTF8&store_ref=SB_A072331553KWLRQ46GJ&pd_rd_plhdr=t&aaxitk=4397a6b50ace29544018357823e930ba&hsa_cr_id=0&lp_asins=B09PRH27MV%2CB0BKL2ML5R%2CB0B7521SSD&lp_query=bags&lp_slot=auto-sparkle-hsa-tetris&ref_=sbx_be_s_sparkle_lsi4d_ls&pd_rd_w=7gxTf&content-id=amzn1.sym.df9fe057-524b-4172-ac34-9a1b3c4e647d%3Aamzn1.sym.df9fe057-524b-4172-ac34-9a1b3c4e647d&pf_rd_p=df9fe057-524b-4172-ac34-9a1b3c4e647d&pf_rd_r=4ACFRD32ZMB58T3GRZAD&pd_rd_wg=3qJkc&pd_rd_r=ff3291e4-0a3e-4690-b73f-22673bc9fafe"
# # base_url ="https://www.amazon.in/s?k=product"
# search_params = {
#     "k": "bags",
#     "crid": "2M096C61O4MLT",
#     "qid": "1653308124",
#     "sprefix": "ba%2Caps%2C283",
#     "ref": "sr_pg_1"
# }

# data = []
# pages_to_scrape = 20

# for page in range(1, pages_to_scrape + 1):
#     search_params["page"] = page
#     response = requests.get(base_url, params=search_params)
#     soup = BeautifulSoup(response.content, "html.parser")
    
#     products = soup.find_all("div", class_="s-result-item")
    
#     for product in products:
#         product_url = product.find("a", class_="a-link-normal").get("href")
#         product_name = product.find("span", class_="a-size-large product-title-word-break").text
#         # product_name = product.find("span", class_="a-text-normal").text
#         product_price = product.find("span", class_="a-price-symbol").text + product.find("span", class_="a-offscreen").text
#         # product_rating = product.find("span", class_="a-icon-alt").text.split()[0]
#         product_rating = product.find("span", class_="reviewCountTextLinkedHistogram noUnderline").text.split()[0]
#         num_reviews = product.find("span", class_="a-size-base").text


#         # product_url = "https://www.amazon.in" + product.find("a", class_="a-link-normal").get("href")
#         # product_name = product.find("span", class_="a-size-large product-title-word-break").text
#         # product_price = product.find("span", class_="a-price-symbol").text + product.find("span", class_="a-offscreen").text
#         # product_rating = product.find("span", class_="reviewCountTextLinkedHistogram noUnderline").text.split()[0]
#         # num_reviews = product.find("span", class_="a-size-base").text

# # a-icon-alt
#         data.append({
#             "Product URL": product_url,
#             "Product Name": product_name,
#             "Product Price": product_price,
#             "Rating": product_rating,
#             "Number of Reviews": num_reviews
#             # "Product URL": product_url,
#             # "Product Name": product_name,
#             # "Product Price": product_price,
#             # "Rating": product_rating,
#             # "Number of Reviews": num_reviews
#         })

# df = pd.DataFrame(data)
# df.to_csv("product_listings.csv", index=False)


# # Part 2: Scraping Individual Product Pages

# # python
# # Copy code
# # product_data = []

# # for product_url in df["Product URL"]:
# #     response = requests.get(product_url)
# #     soup = BeautifulSoup(response.content, "html.parser")
    
# #     asin = soup.find("th", string="ASIN").find_next("td").text
# #     description = soup.find("div", id="productDescription").text.strip()
# #     manufacturer = soup.find("th", string="Manufacturer").find_next("td").text
    
# #     product_data.append({
# #         "Product URL": product_url,
# #         "ASIN": asin,
# #         "Product Description": description,
# #         "Manufacturer": manufacturer
# #     })

# # product_df = pd.DataFrame(product_data)
# # final_df = df.merge(product_df, on="Product URL")
# # final_df.to_csv("final_product_data.csv", index=False)




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



# import requests
# from bs4 import BeautifulSoup
# # import csv
# import pandas as pd

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

# # Create a Pandas DataFrame
# columns = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
# df = pd.DataFrame(product_data, columns=columns)
# # df.to_csv("product_listings_dataframe.csv", index=False, encoding="utf-8")
# # Print the DataFrame
# print(df)




# import requests
# from bs4 import BeautifulSoup
# import pandas as pd

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
    
#     # Extract product details (same code as before)

# # Create a Pandas DataFrame
# columns = ["Product URL", "Product Name", "Product Price", "Rating", "Number of Reviews"]
# df = pd.DataFrame(product_data, columns=columns)

# # Save the DataFrame to a CSV file
# csv_filename = "product_listings_dataframe.csv"
# df.to_csv(csv_filename, index=False, encoding="utf-8")
# print(f"DataFrame saved as {csv_filename}")

# # Print the first few rows of the DataFrame
# print(df.head())
