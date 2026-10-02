import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time


# -----------------------------------------
# SETTINGS
# -----------------------------------------

BASE_URL = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


# -----------------------------------------
# FUNCTION: SCRAPE ONE PAGE
# -----------------------------------------

def scrape_page(page_number):

    url = BASE_URL

    if page_number > 1:
        url = f"{BASE_URL}?page={page_number}"

    print(f"Scraping page {page_number}...")

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=15
    )

    print("Status Code:", response.status_code)

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.select("div.thumbnail")

    page_data = []

    for product in products:

        # -----------------------------
        # Product name
        # -----------------------------

        name_element = product.select_one("a.title")

        if name_element:
            product_name = name_element.get_text(strip=True)
        else:
            product_name = None


        # -----------------------------
        # Price
        # -----------------------------

        price_element = product.select_one("h4.price")

        if price_element:
            price_text = price_element.get_text(strip=True)
        else:
            price_text = None


        # -----------------------------
        # Description
        # -----------------------------

        description_element = product.select_one("p.description")

        if description_element:
            description = description_element.get_text(
                " ",
                strip=True
            )
        else:
            description = None


        # -----------------------------
        # Reviews
        # -----------------------------

        reviews_element = product.select_one("p.pull-right")

        if reviews_element:
            reviews_text = reviews_element.get_text(
                " ",
                strip=True
            )
        else:
            reviews_text = None


        # -----------------------------
        # Rating
        # -----------------------------

        rating_element = product.select_one("div.ratings")

        if rating_element:

            stars = rating_element.select("span.glyphicon-star")

            rating = len(stars)

        else:
            rating = None


        # -----------------------------
        # Price numeric
        # -----------------------------

        if price_text:

            price_numeric = float(
                re.sub(r"[^0-9.]", "", price_text)
            )

        else:

            price_numeric = None


        # -----------------------------
        # Extract screen size
        # -----------------------------

        screen_size = None

        if description:

            screen_match = re.search(
                r'([\d.]+)"',
                description
            )

            if screen_match:
                screen_size = float(
                    screen_match.group(1)
                )


        # -----------------------------
        # Extract RAM
        # -----------------------------

        ram = None

        if description:

            ram_match = re.search(
                r'(\d+)\s*GB',
                description,
                re.IGNORECASE
            )

            if ram_match:
                ram = int(
                    ram_match.group(1)
                )


        # -----------------------------
        # Extract storage
        # -----------------------------

        storage = None

        if description:

            storage_match = re.search(
                r'(\d+(?:\.\d+)?)\s*(GB|TB)(?:\s+SSD)?',
                description,
                re.IGNORECASE
            )

            if storage_match:

                storage = (
                    storage_match.group(1)
                    + " "
                    + storage_match.group(2)
                )


        # -----------------------------
        # Extract operating system
        # -----------------------------

        operating_system = None

        if description:

            operating_system = description.split(",")[-1].strip()


        # -----------------------------
        # Extract CPU
        # -----------------------------

        cpu = None

        if description:

            parts = [
                part.strip()
                for part in description.split(",")
            ]

            if len(parts) >= 2:
                cpu = parts[1]


        # -----------------------------
        # Extract brand
        # -----------------------------

        brand = None

        if product_name:

            known_brands = [
                "Acer",
                "Asus",
                "Dell",
                "HP",
                "Lenovo",
                "Toshiba",
                "Packard",
                "Samsung",
                "Sony",
                "Apple",
                "MSI",
                "Microsoft"
            ]

            for known_brand in known_brands:

                if known_brand.lower() in product_name.lower():

                    brand = known_brand
                    break


        # -----------------------------
        # Store record
        # -----------------------------

        page_data.append({

            "Brand": brand,

            "Model": product_name,

            "Price": price_numeric,

            "CPU": cpu,

            "RAM_GB": ram,

            "Storage": storage,

            "GPU": None,

            "Screen_Size_Inches": screen_size,

            "Resolution": None,

            "Operating_System": operating_system,

            "Weight_KG": None,

            "Rating": rating,

            "Review_Count": reviews_text,

            "Description": description

        })


    return page_data


# -----------------------------------------
# MAIN SCRAPING PROGRAM
# -----------------------------------------

all_laptops = []


# The website has 20 pages.
# We will scrape all 20 pages.

for page in range(1, 21):

    try:

        data = scrape_page(page)

        all_laptops.extend(data)

        print(
            f"Products collected so far: {len(all_laptops)}"
        )

        time.sleep(1)

    except Exception as e:

        print(
            f"Error while scraping page {page}: {e}"
        )


# -----------------------------------------
# CREATE DATAFRAME
# -----------------------------------------

df = pd.DataFrame(all_laptops)


# -----------------------------------------
# REMOVE EXACT DUPLICATES
# -----------------------------------------

df = df.drop_duplicates()


# -----------------------------------------
# SAVE RAW DATA
# -----------------------------------------

df.to_csv(
    "laptop_raw_data.csv",
    index=False
)


# -----------------------------------------
# FINAL OUTPUT
# -----------------------------------------

print("\n===================================")
print("SCRAPING COMPLETED")
print("===================================")

print(
    f"Total laptops collected: {len(df)}"
)

print(
    f"Total columns: {len(df.columns)}"
)

print("\nColumns:")

print(
    df.columns.tolist()
)

print("\nFirst 5 rows:")

print(
    df.head()
)

print("\nRaw dataset saved as:")

print(
    "laptop_raw_data.csv"
)
