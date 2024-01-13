from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium_stealth import stealth
import math

def search_google_web_automation(query, num_results):
    # Enforce limits on num_results
    if num_results < 5:
        num_results = 5
    elif num_results > 100:
        num_results = 100

    # Calculate the number of pages
    n_pages = math.ceil(num_results / 10)

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    results = []
    counter = 0
    for page in range(1, n_pages + 1):
        url = (
            "http://www.google.com/search?q="
            + str(query)
            + "&start="
            + str((page - 1) * 10)
        )

        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        search = soup.find_all("div", class_="yuRUbf")

        for h in search:
            if counter == num_results:
                break
            counter += 1
            title = h.a.h3.text
            link = h.a.get("href")
            rank = counter
            results.append(
                {
                    "title": title,
                    "url": link,
                    "domain": urlparse(link).netloc,
                    "rank": rank,
                }
            )

        if counter == num_results:
            break

    driver.quit()
    return results
