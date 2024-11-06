# ATTENTION in the old csv file when inputting the file names the () around the number should be removed,
# because Wordpress will remove them when images are uploaded

import csv
from typing import Union, Optional

# Define the new CSV headers, obtained from WordPress product export
HEADERS = [
    "ID", "Type", "SKU", "Name", "Published", "Is featured?", "Visibility in catalog",
    "Short description", "Description", "Date sale price starts", "Date sale price ends",
    "Tax status", "Tax class", "In stock?", "Stock", "Low stock amount",
    "Backorders allowed?", "Sold individually?", "Weight (kg)", "Length (cm)", "Width (cm)",
    "Height (cm)", "Allow customer reviews?", "Purchase note", "Sale price",
    "Regular price", "Categories", "Tags", "Shipping class", "Images",
    "Download limit", "Download expiry days", "Parent", "Grouped products",
    "Upsells", "Cross-sells", "External URL", "Button text", "Position",
    # Attributes 1-10 (name, value, visible, global)
    *[f"Attribute {i} {field}"
      for i in range(1, 11)
      for field in ["name", "value(s)", "visible", "global"]]
]

# Configuration
URL_PREFIX = "https://shop.perseuslighting.com/wp-content/uploads/2024/11/"
SUFFIX = "-scaled.jpeg"
CATEGORIES = "لوازم روشنایی > پروژکتور, لوازم روشنایی"
TAGS = "پروژکتور"


def generate_image_sequence(filename: str, count: Union[int, str]) -> str:
    """
    Generate a sequence of image URLs based on filename and count.

    Args:
        filename (str): Base filename for the images
        count (Union[int, str]): Number of images to generate

    Returns:
        str: Comma-separated string of image URLs
    """
    # Validate inputs
    if not filename:
        return ""

    try:
        count = int(count) if isinstance(count, str) else count
        if count <= 0:
            return ""
    except (ValueError, TypeError):
        return ""

    # Clean filename
    filename = filename.replace(" ", "-")
    base = URL_PREFIX + filename[:-5].strip()

    if count == 1:
        return base + SUFFIX

    # Extract main image number
    main_image_number = int(filename[-6:-5]) if filename[-6:-5].isdigit() else 0
    base_url = URL_PREFIX + filename[:-6].strip()

    # Generate URL sequence excluding the main image number
    urls = [f"{base_url}{i}{SUFFIX}" for i in range(1, count + 1) if i != main_image_number]
    return f"{base}{SUFFIX}, {', '.join(urls)}"


def create_product_row(old_row: list) -> list:
    """
    Create a new product row from old CSV data.

    Args:
        old_row (list): Row data from old CSV

    Returns:
        list: Formatted row for new CSV
    """
    return [
        "",  # ID
        "simple",  # Type
        "",  # SKU
        old_row[1],  # Name
        1,  # Published
        0,  # Is featured?
        "visible",  # Visibility
        "",  # Short description
        old_row[21],  # Description
        "",  # Sale price start
        "",  # Sale price end
        "taxable",  # Tax status
        "",  # Tax class
        1,  # In stock?
        "",  # Stock
        10,  # Low stock amount
        0,  # Backorders
        0,  # Sold individually
        old_row[19],  # Weight
        old_row[17],  # Length
        old_row[15],  # Width
        old_row[20],  # Height
        1,  # Allow reviews
        "",  # Purchase note
        "",  # Sale price
        old_row[23],  # Regular price
        CATEGORIES,  # Categories
        TAGS,  # Tags
        "",  # Shipping class
        generate_image_sequence(old_row[25], old_row[26]),  # Images
        "",  # Download limit
        "",  # Download expiry
        "",  # Parent
        "",  # Grouped products
        "",  # Upsells
        "",  # Cross-sells
        "",  # External URL
        "",  # Button text
        0,  # Position
        # Attributes
        "رنگ", old_row[3], 1, 0,
        "توان مصرفی", old_row[4], 1, 0,
        "نوردهی (لومن)", old_row[6], 1, 0,
        "دمای رنگ (کلوین)", old_row[7], 1, 0,
        "لوکس", old_row[7], 1, 0,
        "CRI", old_row[8], 1, 0,
        "آی پی", old_row[9], 1, 0,
        "گارانتی", old_row[10], 1, 0,
        "محل نصب", old_row[11], 1, 0,
        "برند", "", 1, 0
    ]


def transform_csv(input_file: str, output_file: str) -> None:
    """
    Transform old CSV format to new WordPress product format.

    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output CSV file
    """
    try:
        with open(input_file, 'r', newline='', encoding='utf-8') as old_file, \
                open(output_file, 'w', newline='', encoding='utf-8') as new_file:

            reader = csv.reader(old_file)
            next(reader)  # Skip header

            writer = csv.writer(new_file)
            writer.writerow(HEADERS)

            for row in reader:
                writer.writerow(create_product_row(row))

        print(f"Data transformation complete. Output saved to {output_file}")

    except Exception as e:
        print(f"Error during transformation: {str(e)}")


if __name__ == "__main__":
    transform_csv('old.csv', 'new.csv')