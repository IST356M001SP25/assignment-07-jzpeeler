import re
import os
from dataclasses import asdict
from playwright.sync_api import Playwright, sync_playwright
from menuitemextractor import extract_menu_item
from menuitem import MenuItem
import pandas as pd

def tullyscraper(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://web.archive.org/web/20241111165815/https://www.tullysgoodtimes.com/menus/")

    extracted_items = []
    for title in page.query_selector_all("h3.foodmenu__menu-section-title"):
        title_text = title.inner_text()
        print("MENU SECTION:", title_text)
        
        # Get the div.row container after the title
        row = title.query_selector("~ *").query_selector("~ *")
        if not row:
            print(f"[DEBUG] No row found after section: {title_text}")
            continue

        for item in row.query_selector_all("div.foodmenu__menu-item"):
            item_text = item.inner_text()
            try:
                extracted_item = extract_menu_item(title_text, item_text)
                print(f"  MENU ITEM: {extracted_item.name}")
                extracted_items.append(asdict(extracted_item))
            except Exception as e:
                print(f"  [ERROR] Skipping item due to: {e}")
                continue

    # Ensure output folder exists
    os.makedirs("cache", exist_ok=True)

    # Save CSV
    output_path = "cache/tullys_menu.csv"
    print(f"[DEBUG] Writing {len(extracted_items)} items to {output_path}")
    df = pd.DataFrame(extracted_items)
    df.to_csv(output_path, index=False)

    context.close()
    browser.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        tullyscraper(playwright)