from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Handle the GET request, this is the main function of the script"""

        query_dict = self.query()
        response_code = 200

        response_text: str = "you should add query capital or country to the url"
        try:
            if 'capital' in query_dict and 'country' in query_dict:
                response_text = self.generate_matching_query_response(query_dict)
            elif 'country' in query_dict:
                response_text = self.generate_country_resp(query_dict)
            elif 'capital' in query_dict:
                response_text = self.generate_capital_resp(query_dict)
        except TypeError as e:
            response_code = 404
            response_text = 'Country not found'
        except Exception as e:
            response_code = 500
            response_text = "`restcountries` api is down please try again later"

        self.send_response(response_code)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_text.encode('utf-8'))
        return

    def query(self):
        """Parse the query string and return a dictionary of the query string"""
        s = self.path
        url_components = parse.urlsplit(s)
        query_strings_list = parse.parse_qsl(url_components.query)
        return dict(query_strings_list)

    def get_data_from_name(self, country):
        """Get the country data from the name of the country"""
        resp = requests.get(f"https://restcountries.com/v3.1/name/{country}")
        data = resp.json()
        try:
            return data[0]
        except Exception as e:
            raise TypeError("response data is not a country") from e

    def get_data_from_capital(self, capital):
        """Get the country data from the capital of the country"""
        resp = requests.get(f"https://restcountries.com/v3.1/capital/{capital}")
        data = resp.json()
        try:
            return data[0]
        except Exception as e:
            raise TypeError("response data is not a country") from e

    def generate_capital_resp(self, query_dict):
        """Generate the response for the capital query"""
        country_data = self.get_data_from_capital(query_dict['capital'])
        return f"{query_dict['capital']} is the capital of {country_data['name']['common']}\n{self.generate_extra_country_data(country_data)}"

    def generate_country_resp(self, query_dict):
        """Generate the response for the country query"""
        country_data = self.get_data_from_name(query_dict['country'])
        return f"Capital of {query_dict['country']} is {self.parse_country_capitals(country_data)}\n{self.generate_extra_country_data(country_data)}"

    def generate_matching_query_response(self, query_dict) -> str:
        """Generate the response for the matching query"""
        country_from_name = self.get_data_from_name(query_dict['country'])
        capital = query_dict['capital'].capitalize()
        capitals = country_from_name['capital']
        if capital in capitals:
            return f"Yes, {query_dict['capital']} is the capital of {query_dict['country']},\n{self.generate_extra_country_data(country_from_name)}"
        else:
            return f"No, {query_dict['capital']} is not the capital of {query_dict['country']}, \nCapital of {query_dict['country']} is {self.parse_country_capitals(country_from_name)}"

    def parse_country_capitals(self, data) -> str:
        """Parse the country data to get the capital, like this: capital1, capital2 and capital3"""
        capitals = data['capital']
        return ", ".join(capitals)

    def generate_extra_country_data(self, country: dict):
        """Generate the extra data for the country, like the currency and the population"""
        currencies = country.get('currencies', {})
        currencies_str = ", ".join(f"{currency}, " for currency in currencies.keys())

        languages = country.get('languages', {})
        languages_str = ", ".join(f"{language}, " for language in languages.values())
        return f"its currency is {currencies_str}and the population is {country.get('population')}, the Language is {languages_str}"
