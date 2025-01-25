import csv
import os
from typing import Union, Optional

# Define the attributes with their corresponding column indices from the old CSV
# ATTRIBUTES = [
#     ("رنگ", 3),
#     ("توان مصرفی", 4),
#     ("نوردهی (لومن)", 6),
#     ("دمای رنگ (کلوین)", 7),
#     ("لوکس", 7),
#     ("CRI", 8),
#     ("آی پی", 9),
#     ("گارانتی", 10),
#     ("محل نصب", 11),
#     ("برند", None)  # None means no corresponding column
# ]

ATTRIBUTES = [
    ("آمپر", 5),
    ("ولتاژ", 6),
    ("توان", 7),
    ("آی پی", 9),
    ("گارانتی", 10),
]

# Define the new CSV headers
HEADERS = [
    "ID", "Type", "SKU", "Name", "Published", "Is featured?", "Visibility in catalog",
    "Short description", "Description", "Date sale price starts", "Date sale price ends",
    "Tax status", "Tax class", "In stock?", "Stock", "Low stock amount",
    "Backorders allowed?", "Sold individually?", "Weight (kg)", "Length (cm)", "Width (cm)",
    "Height (cm)", "Allow customer reviews?", "Purchase note", "Sale price",
    "Regular price", "Categories", "Tags", "Shipping class", "Images",
    "Download limit", "Download expiry days", "Parent", "Grouped products",
    "Upsells", "Cross-sells", "External URL", "Button text", "Position",
    # Dynamically generate attribute headers
    *[f"Attribute {i+1} {field}"
      for i in range(len(ATTRIBUTES))
      for field in ["name", "value(s)", "visible", "global"]]
]

# Configuration
URL_PREFIX = "https://shop.perseuslighting.com/wp-content/uploads/2025/01/"
CATEGORIES = "سوئیچینگ ترانس درایور" 
TAGS = "پروژکتور"

def generate_image_sequence(filename: str, count: Union[int, str]) -> str:
    """
    Generate a sequence of image URLs based on filename and count.
    Supports both .jpeg and .png extensions.
    """
    if not filename:
        return ""

    try:
        count = int(count) if isinstance(count, str) else count
        if count <= 0:
            return ""
    except (ValueError, TypeError):
        return ""

    # Clean filename and determine extension
    filename = filename.replace(" ", "-")
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.jpeg', '.jpg', '.png']:
        return "" 
    main_image_number = int(filename[-(len(ext)+2):-(len(ext)+1)])

    
    # Remove extension and any trailing numbers
    base_name = filename[:-(len(ext)+3)]
    base_url = URL_PREFIX + base_name.strip()
    suffix = '-scaled' + ext

    if count == 1:
        return base_url + main_image_number + suffix

    # Generate URL sequence
    urls = [f"{base_url}{i}{suffix}" for i in range(1, count + 1) if i != main_image_number]
    return f"{base_url}{main_image_number}{suffix}, {', '.join(urls)}"

def create_product_row(old_row: list) -> list:
    """
    Create a new product row from old CSV data.
    """
    base_row = [
        "",  # ID
        "simple",  # Type
        "",  # SKU
        old_row[0],  # Name
        1,  # Published
        0,  # Is featured?
        "visible",  # Visibility
        "",  # Short description
        old_row[19],  # Description
        "",  # Sale price start
        "",  # Sale price end
        "taxable",  # Tax status
        "",  # Tax class
        1,  # In stock?
        "",  # Stock
        10,  # Low stock amount
        0,  # Backorders
        0,  # Sold individually
        old_row[18],  # Weight
        old_row[16],  # Length
        old_row[15],  # Width
        old_row[17],  # Height
        1,  # Allow reviews
        "",  # Purchase note
        "",  # Sale price
        old_row[21],  # Regular price
        CATEGORIES,  # Categories
        old_row[4],  # Tags
        "",  # Shipping class
        generate_image_sequence(old_row[22], old_row[23]),  # Images
        "",  # Download limit
        "",  # Download expiry
        "",  # Parent
        "",  # Grouped products
        "",  # Upsells
        "",  # Cross-sells
        "",  # External URL
        "",  # Button text
        0,  # Position
    ]

    # Add attributes dynamically
    for attr_name, col_index in ATTRIBUTES:
        value = old_row[col_index] if col_index is not None else ""
        base_row.extend([attr_name, value, 1, 0])

    return base_row

def transform_csv(input_file: str, output_file: str) -> None:
    """
    Transform old CSV format to new WordPress product format.
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