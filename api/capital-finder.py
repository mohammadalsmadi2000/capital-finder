from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests

class handler(BaseHTTPRequestHandler):
    """
    A simple HTTP request handler that retrieves information about countries and their capitals.
    Supports two query parameters: 'name' for country name and 'capital' for capital name.
    """

    def do_GET(self):
        """
        Handles the GET request and retrieves information based on the query parameters.

        Retrieves the country name or capital name from the query parameters and makes a request
        to the REST Countries API to fetch the corresponding information. Returns the result as a
        plain text response.

        If 'name' parameter is provided, it returns the capital of the specified country.
        If 'capital' parameter is provided, it returns the country name for the specified capital.
        If neither parameter is provided, it returns an "Invalid query" message.
        """
        m = self.path
        url_components = parse.urlsplit(m)
        query_dict = dict(parse.parse_qsl(url_components.query))
        country = query_dict.get("name")
        capital = query_dict.get("capital")
        helper_msg = ""

        if country:
            U = f"https://restcountries.com/v3.1/name/{country}"
            respons = requests.get(U)
            data = respons.json()
            temp_capital = data[0]["capital"][0]
            helper_msg = f"The capital of {country} is {temp_capital}."
        elif capital:
            U = f"https://restcountries.com/v3.1/capital/{capital}"
            respons = requests.get(U)
            data = respons.json()
            temp_country = data[0]["name"]["common"]
            helper_msg = f"{capital} is the capital of {temp_country}"
        else:
            helper_msg = "Invalid query"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(helper_msg.encode("utf-8"))
        return
