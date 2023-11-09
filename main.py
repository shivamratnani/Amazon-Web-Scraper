import requests
from bs4 import BeautifulSoup
import webbrowser
import tkinter as tk
from tkinter import simpledialog
import sys

def is_valid_amazon_url(url):
    """
    Checks if the given URL is a valid Amazon URL.
    Returns True if the URL is valid, False otherwise.
    """
    try:
        response = requests.get(url)
        if response.status_code == 200 and 'www.amazon.' in response.url:
            return True
        else:
            return False
    except:
        return False

"""
    Scrapes an Amazon product page and returns the product title and price.
    Returns None if the URL is invalid or the product information cannot be found.
    """
def get_captcha_image(soup):
    captcha_url = soup.find('img').get('src')
    return captcha_url

def ask_for_captcha_solution(captcha_url):
    # Open a browser window with the captcha image
    webbrowser.open(captcha_url)
    
    # Ask user to solve the captcha
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    captcha_solution = simpledialog.askstring("Solve CAPTCHA", "Please enter the CAPTCHA:")
    return captcha_solution

def scrape_amazon(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    session = requests.Session()
    session.headers.update(headers)

    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Check if a CAPTCHA is being shown
    if "Enter the characters you see below" in response.text:
        captcha_url = get_captcha_image(soup)
        captcha_solution = ask_for_captcha_solution(captcha_url)

        # The CAPTCHA form data, including hidden fields and the user's solution, needs to be submitted
        # You will need to add the correct field names and action URL based on the form on Amazon's page
        data = {
            'field-keywords': captcha_solution,
            # Add any other required form fields here
        }

        # You will need to inspect the CAPTCHA form to get the correct action URL
        captcha_action_url = "URL where the CAPTCHA response should be submitted"
        session.post(captcha_action_url, data=data)

        # Try the request again
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

    # Now continue with the normal scraping process
    title = soup.find('span', {'id': 'productTitle'})
    price = soup.find('span', {'id': 'priceblock_ourprice'})
    
    if not price:
        price = soup.find('span', {'id': 'priceblock_dealprice'})
    
    if title and price:
        return {'title': title.get_text().strip(), 'price': price.get_text().strip()}
    else:
        print("Could not find title or price on the page.")
        return None


if __name__ == "__main__":
    input1 = True
    print("Welcome to the Amazon Scraper!")
    print("Enter 'exit' to quit the program.")
    while input1:
        if len(sys.argv) > 1:
            url = sys.argv[1]
        else:
            url = input("Please enter an Amazon product URL: ")
            if url == 'exit':
                sys.exit()
        
        if is_valid_amazon_url(url):
            product_info = scrape_amazon(url)
            
            if product_info is not None:
                print(f"Product Title: {product_info['title']}")
                print(f"Product Price: {product_info['price']}")
            else:
                print("Unable to scrape the product information.")
        else:
            print("Invalid Amazon product URL.")
    else:
        print("Thank you for using Amazon Web Scraper!")