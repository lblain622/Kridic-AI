import re
def preprocess_menu_text(menu_text:str):
    # Remove non-ASCII characters and extra spaces

    menu_text = re.sub(r'[^\x00-\x7F]+', '', menu_text)
    menu_text = re.sub(r'\s+', ' ', menu_text).strip()
    # Normalize text
    menu_text = menu_text.lower()
    return menu_text

def segment_menu_text(menu_text):
    # Split text into lines based on common delimiters
    lines = re.split(r'[\r\n]+', menu_text)
    items = [l.strip() for l in lines if l.strip()]
    return items

def extract_dish_names(items):
    dish_names = []
    # Define a pattern for dish names: start with a capital letter, optionally contain special characters, and end with a price
    pattern = re.compile(r'^[a-z\s&]+ - \d+(\.\d+)?$', re.IGNORECASE)

    for item in items:
        if pattern.match(item):
            dish_names.append(item)
    return dish_names

def clean_dish_names(dish_names):
    cleaned_dish_names = []
    for dish in dish_names:
        # Remove numbers and special characters, keep only letters and spaces
        cleaned_dish = re.sub(r'[^A-Za-z\s&]', '', dish).strip()
        cleaned_dish_names.append(cleaned_dish)
    return cleaned_dish_names

