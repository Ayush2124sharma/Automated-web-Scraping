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

class klubfox(scrapy.Spider):
    name = 'pasb_dac'
    brand_name = 'Punjab & Sind Bank'
    spider_type = 'chain'
    spider_chain_name = 'Punjab & Sind Bank'
    spider_chain_id = 2523
    spider_categories = [Code.BANK]
  

    def start_requests(self):
        url: str = "https://punjabandsindbank.co.in/"
        
        yield scrapy.Request(
            url=url,
            callback=self.parse
        )



    def parse(self, response):
        

        import requests

        url = "https://punjabandsindbank.co.in/?type=module&ajaxpage=branch_list"

        payload = "state=all&city=&branch=&code=&csrf_token=9eaa9f5ed0c401bba11570c38f99e0d017df3888&rand=51609&sEcho=1&iColumns=9&sColumns=%2C%2C%2C%2C%2C%2C%2C%2C&iDisplayStart=0&iDisplayLength=2000&mDataProp_0=0&bSortable_0=false&mDataProp_1=1&bSortable_1=false&mDataProp_2=2&bSortable_2=false&mDataProp_3=3&bSortable_3=false&mDataProp_4=4&bSortable_4=false&mDataProp_5=5&bSortable_5=false&mDataProp_6=6&bSortable_6=false&mDataProp_7=7&bSortable_7=false&mDataProp_8=8&bSortable_8=false&iSortCol_0=0&sSortDir_0=asc&iSortingCols=1"
        headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'hd_user_https=53a73e0a9f7834dd0b5c936cdf8114b6804f0cb70b57de9c4183386486d1b047:1690371782592; myCookie=value; PHPSESSID=bdbeb2e3587b7b1c8d710e69c796775d; _ga=GA1.1.1776997832.1690371770; _ga_LPMBF41TVD=GS1.1.1690371769.1.1.1690371881.0.0.0; myCookie=value',
        'DNT': '1',
        'Origin': 'https://punjabandsindbank.co.in',
        'Referer': 'https://punjabandsindbank.co.in/module/branch-list',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-gpc': '1'
        }

        response1 = requests.request("POST", url, headers=headers, data=payload, verify=False,)
        decoded_data = response1.text.encode().decode('utf-8-sig')
        data = json.loads(decoded_data)
        
        stores = data['aaData']
        for row in stores:
            store = {
                'chain_name': self.spider_chain_name,
                'chain_id': self.spider_chain_id,
                'brand': self.brand_name,
                "ref": uuid.uuid4().hex,
                "addr_full": row[4],
                "state": row[5],
                "phone": row[-2],
                "opening_hours": row[-1]
            }
            yield GeojsonPointItem(**store)