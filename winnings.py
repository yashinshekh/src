import scrapy
import json
import csv
import os
import datetime


class WinningsSpider(scrapy.Spider):
    name = 'winnings'
    allowed_domains = ['winnings.com.au']
    start_urls = ['http://winnings.com.au/']

    if 'winnings.csv' not in os.listdir(os.getcwd()):
        with open("winnings.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['date','url','category','title','sku','price','rrp','model_no','ean','key specifications','availability',
                             'image','image','image','image','image','image','image','image','image','image','image','image','image'])

    alreadyscrapped = []
    with open("winnings.csv","r",encoding="utf-8") as r:
        reader = csv.reader(r)
        for line in reader:
            alreadyscrapped.append(line[1])

    print(alreadyscrapped)

    cats = {
        "Refrigerators":"https://www.winnings.com.au/api/category/kitchen%2Frefrigerators?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Freezers":"https://www.winnings.com.au/api/category/kitchen%2Frefrigerators%2Ffreezers?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Wine Cabinets":"https://www.winnings.com.au/api/category/kitchen%2Fwine-cabinets?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Dishwashers":"https://www.winnings.com.au/api/category/kitchen%2Fdishwashers?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Ovens & Uprights":"https://www.winnings.com.au/api/category/kitchen%2Fovens-and-uprights?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Cooktops":"https://www.winnings.com.au/api/category/kitchen%2Fcooktops?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Rangehoods":"	https://www.winnings.com.au/api/category/kitchen%2Frangehoods?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Microwaves":"https://www.winnings.com.au/api/category/kitchen%2Fmicrowaves?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Coffee Machines":"https://www.winnings.com.au/api/category/kitchen%2Fcoffee-machines?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Small Appliances":"https://www.winnings.com.au/api/category/kitchen%2Fsmall-appliances?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Laundry":"https://www.winnings.com.au/api/category/laundry?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Alfresco":"https://www.winnings.com.au/api/category/alfresco?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Heating & Cooling":"https://www.winnings.com.au/api/category/heating-and-cooling?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Home Entertainment":"https://www.winnings.com.au/api/category/home-entertainment?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Health Beauty & Fitness":"https://www.winnings.com.au/api/category/health-beauty-and-fitness?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Vacuum Cleaners":"https://www.winnings.com.au/api/category/floor-care%2Fvacuum-cleaners?selectedStore=nsw-redfern&location=WA-DC-SYD",
        "Floor Cleaning":"https://www.winnings.com.au/api/category/floor-care%2Ffloor-cleaning?selectedStore=nsw-redfern&location=WA-DC-SYD"
    }

    def start_requests(self):
        for k,v in self.cats.items():
            yield scrapy.Request(
                url=v,
                callback=self.parse,
                meta={
                    'cat':k
                }
            )

            # break

    def parse(self, response,*args):
        datas = json.loads(response.text)['products']
        for data in datas:
            price = data['price']
            url = data['uri']

            # print(url)

            if int(price) >= 490:
                if "https://www.winnings.com.au/p"+str(url) not in self.alreadyscrapped:
                    yield scrapy.Request(
                        url="https://www.winnings.com.au/api/product"+str(url),
                        callback=self.getdata,
                        meta={
                            'cat':response.meta.get('cat'),
                            'url':"https://www.winnings.com.au/p"+str(url),
                            'slug':url
                        }
                    )

                else:
                    print("Exists ...")


    def getdata(self,response):
        date = datetime.datetime.today().strftime('%m/%d/%y')
        jsondata = json.loads(response.text)['product']

        title = jsondata['title']
        sku = jsondata['sku']
        price = jsondata['price']
        rrp = jsondata['rrp']

        model_no = ''
        for i in jsondata['attributes']:
            if i['name'] == "Model Number":
                model_no = i['value']

        ean = ''
        for a in jsondata['attributes']:
            if a['name'] == "EAN":
                ean = a['value']

        try:
            images = ['https://www.winnings.com.au'+i['high'] for i in jsondata['images'] if i['high']]
        except:
            images = []

        key_specifications = ''
        attributes = jsondata['attributes']
        for key in attributes:
            if key['displayCategory'] == "Key Specifications":
                key_specifications += key['name']+" : "+key['value']+'\n'


        yield scrapy.Request(
            'https://www.winnings.com.au/api/product/avail'+str(response.meta.get('slug'))+'/SYDNEY/2000',
            callback=self.findavailability,
            meta={
                'line':[date,response.meta.get('url'),response.meta.get('cat'),title,sku,price,rrp,model_no,ean,key_specifications,'']+images
            }
        )

    def findavailability(self,response):
        jsondata = json.loads(response.text)

        availability = "Add to cart" if jsondata['available'] == True else "Request Assistance"
        response.meta.get('line')[10] = availability

        with open("winnings.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(response.meta.get('line'))
            print(response.meta.get('line'))




