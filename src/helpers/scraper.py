import re
import requests
from bs4 import BeautifulSoup


class WebsiteScraper:
    def __init__(self):
        self.uah_url = "https://minfin.com.ua/ua/currency/auction/exchanger/usd/buy/kiev/"
    def _scrape_website(self):
        try:
            response = requests.get(self.uah_url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                average_div = soup.find('div', class_='average')

                if average_div:
                    return average_div.get_text()
                else:
                    print("Error: Unable to find div with class 'average'.")
            else:
                print(f"Error: Unable to fetch content. Status code: {response.status_code}")

        except Exception as e:
            print(f"An error occurred: {e}")

    def extract_prices(self):
        pattern = r'(\d+\,\d{2})'
        matches = re.findall(pattern, self._scrape_website())
        converted_prices = [float(match.replace(',', '.')) for match in matches]
        return self._calculator(converted_prices)

    @staticmethod
    def _calculator(prices):
        if len(prices) > 0:
            return round(sum(prices) / 2, 2)


website_scraper = WebsiteScraper()
