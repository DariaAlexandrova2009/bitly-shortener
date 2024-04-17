import requests
import os
from dotenv import load_dotenv
import argparse


URL = 'https://api-ssl.bitly.com/v4/'

def is_bitlink(bitlink, url):
    url = "{}bitlinks/{}".format(URL, url)
    headers = {
        'Authorization': f"Bearer {bitlink}"
    }
    response = requests.get(
        url,
        headers=headers
    )
    return response.ok
    
        
def count_clicks(bitly_token, bitlink):
    url = "{}bitlinks/{}/clicks/summary".format(URL, bitlink)
    params = {
        "unit": "month",
        "units": "-1"
    } 
    headers = {
        'Authorization': f"Bearer {bitly_token}"
    }
    response_post = requests.get(
        url,
        params=params,
        headers=headers
    )
    response_post.raise_for_status()
    return response_post.json()["total_clicks"]

    
def shorten_link(bitly_token, url):
    bitly_url = "{}shorten".format(URL)
    params = {
        "long_url": url
    }
    headers = {
        'Authorization': f"Bearer {bitly_token}"
    }
    response_post = requests.post(
        bitly_url,
        json=params,
        headers=headers
    )
    response_post.raise_for_status()
    short_link = response_post.json()["link"]
    return short_link

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Link shortener and clicks calculator'
    )
    parser.add_argument('user_link', help='Введите ссылку ')
    args = parser.parse_args()
    #print(args.name)
    load_dotenv()
    #user_link = input("Введите ссылку: ")
    bitly_token = os.environ["BITLY_TOKEN"]
    if is_bitlink(bitly_token, args):
        try:
            print(f"Число кликов: {count_clicks(bitly_token, args)}")
        except requests.exceptions.HTTPError as error:
            print("Can't get data from server:\n{0}".format(error))
    else:
        try:
            print(shorten_link(bitly_token, URL))
        except requests.exceptions.HTTPError as error:
            print("Can't get data from server:\n{0}".format(error))