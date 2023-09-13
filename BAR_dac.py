# -*- coding: utf-8 -*-
import scrapy
import re
import uuid
from locations.items import GeojsonPointItem
from locations.categories import Code
from scrapy import Selector
from typing import List, Dict
import pycountry
import requests
import json
from bs4 import BeautifulSoup

class klubfox(scrapy.Spider):
    name = 'BAREZZITO_dac'
    brand_name = 'BAREZZITO'
    spider_type = 'chain'
    spider_chain_name = 'BAREZZITO'
    spider_chain_id = 27342
    spider_categories = [Code.NIGHTLIFE_ENTERTAINMENT]
  

    def start_requests(self):
        url: str = "https://barezzito.bookersnap.com/"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )



    def parse(self, response):
        

        url = "https://barezzito.bookersnap.com/"

        payload = {}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'PHPSESSID=ontbmo309vfn828abmivh8jpe1; user_cookie=169036967715602; key=214aa5e8-765f-4379-9b06-5030a38faff8',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1'
        }

        response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)
        soup = BeautifulSoup(response.text, "html.parser")
        hidden_divs = soup.find_all('div', class_='hidden')
        for hidden_div in hidden_divs:
            name_tag = hidden_div.find('h2')
            name = name_tag.text.strip() if name_tag else None
            address_tag = hidden_div.find('p')
            address = address_tag.text.strip() if address_tag else None
            if name == None:
                continue
            else:
                
                store = {
                    'chain_name': self.spider_chain_name,
                    'chain_id': self.spider_chain_id,
                    'brand': self.brand_name,
                    "ref": uuid.uuid4().hex,
                    "addr_full": address,
                    "name": name
                }
                yield GeojsonPointItem(**store)