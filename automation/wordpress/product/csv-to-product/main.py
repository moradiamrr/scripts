import csv
import os
from typing import Union, Optional

# Define the attributes with their corresponding column indices from the old CSV
ATTRIBUTES = [
    ("رنگ", 8),
    ("توان مصرفی", 9),
    ("نوردهی (لومن)", 11),
    ("دمای رنگ (کلوین)", 12),
    ("CRI", 13),
    ("آی پی", 14),
    ("گارانتی", 15),
    ("محل نصب", 16),
    ("برند", 4),
    ("نوع اتصال", 17),
    ("خروجی نور", 18)
]

# ATTRIBUTES = [
#     ("آمپر", 5),
#     ("ولتاژ", 6),
#     ("توان", 7),
#     ("آی پی", 9),
#     ("گارانتی", 10),
# ]

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
CATEGORIES = "روشنایی" 
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
    #suffix = '-scaled' + ext
    suffix = ext

    if count == 1:
        return base_url + str(main_image_number) + suffix

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
        old_row[31],  # Description
        "",  # Sale price start
        "",  # Sale price end
        "taxable",  # Tax status
        "",  # Tax class
        1,  # In stock?
        "",  # Stock
        10,  # Low stock amount
        0,  # Backorders
        0,  # Sold individually
        old_row[33],  # Weight
        old_row[31],  # Length
        old_row[30],  # Width
        old_row[32],  # Height
        1,  # Allow reviews
        "",  # Purchase note
        "",  # Sale price
        old_row[33],  # Regular price
        CATEGORIES,  # Categories
        old_row[6],  # Tags
        "",  # Shipping class
        generate_image_sequence(old_row[34], old_row[35]),  # Images
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


def create_product_rows(old_row: list) -> list:
    """
    Create product rows for both simple and variable products.
    """
    product_rows = []
    
    # Check if the product has variations (comma-separated values in old_row[8])
    variations = old_row[8].split(', ') if ',' in old_row[8] else None
    
    if variations:
        # Create a variable product (parent)
        base_row = [
            "",  # ID
            "variable",  # Type
            "",  # SKU
            old_row[0],  # Name
            1,  # Published
            0,  # Is featured?
            "visible",  # Visibility
            "",  # Short description
            old_row[30],  # Description
            "",  # Sale price start
            "",  # Sale price end
            "taxable",  # Tax status
            "",  # Tax class
            1,  # In stock?
            100,  # Stock
            10,  # Low stock amount
            0,  # Backorders
            0,  # Sold individually
            old_row[29],  # Weight
            old_row[27],  # Length
            old_row[26],  # Width
            old_row[28],  # Height
            1,  # Allow reviews
            "",  # Purchase note
            "",  # Sale price
            old_row[32],  # Regular price
            CATEGORIES,  # Categories
            old_row[6],  # Tags
            "",  # Shipping class
            generate_image_sequence(old_row[33], old_row[34]),  # Images
            "",  # Download limit
            "",  # Download expiry
            "",  # Parent
            "",  # Grouped products
            "",  # Upsells
            "",  # Cross-sells
            "",  # External URL
            "",  # Button text
            0,  # Position
            "Attribute 1 name", "رنگ", 1, 0,  # Color attribute
        ]
        # Add attributes dynamically
        for attr_name, col_index in ATTRIBUTES:
            value = old_row[col_index] if col_index is not None else ""
            base_row.extend([attr_name, value, 1, 0])

        product_rows.append(base_row)

        # Create variation products
        for variation in variations:
            variation_row = base_row.copy()
            variation_row[1] = "variation"  # Set type to variation
            variation_row[3] = f"{old_row[0]} - {variation}"  # Append variant name
            variation_row[8] = ""  # set description to none
            variation_row[12] = "parent"  # set tax class to parent
            variation_row[32] = f"id:{old_row[35]}"  # Set Parent
            variation_row[44] = variation  # Set the color variant
            variation_row[45] = ""  # Set the color attribute visibility
            product_rows.append(variation_row[:47])
    
    else:
        # Create a simple product
        product_rows.append(create_product_row(old_row))
    
    return product_rows

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
                writer.writerows(create_product_rows(row))

        print(f"Data transformation complete. Output saved to {output_file}")

    except Exception as e:
        print(f"Error during transformation: {str(e)}")

if __name__ == "__main__":
    transform_csv('old.csv', 'new.csv')