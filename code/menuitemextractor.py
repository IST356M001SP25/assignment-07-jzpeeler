from menuitem import MenuItem

def clean_price(price: str) -> float:
    return float(price.replace('$', '').replace(',', '').strip())

def clean_scraped_text(scraped_text: str) -> list[str]:
    skip_words = {"NEW", "NEW!", "S", "V", "GS", "P"}
    return [line.strip() for line in scraped_text.split("\n") if line.strip() and line.strip().upper() not in skip_words]

def extract_menu_item(title: str, scraped_text: str) -> MenuItem:
    cleaned = clean_scraped_text(scraped_text)
    name = cleaned[0]
    price = clean_price(cleaned[1])
    description = cleaned[2] if len(cleaned) > 2 else "No description available"
    return MenuItem(category=title, name=name, price=price, description=description)