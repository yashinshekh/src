import scrapy
import xmltodict
import json
import datetime
import csv
import os

# https://www.appliancesonline.com.au/api/filter/path/v3/washers-and-dryers/washing-machines/front-loading/
# https://www.appliancesonline.com.au/api/v2/product/id/94280/


class AppliancesonlineSpider(scrapy.Spider):
    name = 'appliancesonline'
    allowed_domains = ['appliancesonline.com.au']
    start_urls = ['https://www.appliancesonline.com.au/public/sitemaps/sitemap-main.xml']

    if 'appliancesonline.csv' not in os.listdir(os.getcwd()):
        with open("appliancesonline.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['date','url','category','title','brand','model_no','price','rrp','discount','free_delivery','stock_status','estimated_delivery_date','delivery_location','image','image','image','image','image','image','image','image','image','image','image','image','image','image','image'])


    alreadyscrapped = []
    with open("appliancesonline.csv","r",encoding="utf-8") as r:
        reader = csv.reader(r)
        for line in reader:
            alreadyscrapped.append(line[1])

    cats = {
        'Wine':'https://www.appliancesonline.com.au/api/filter/path/v3/refrigeration/beverage-fridges/wine/',
        'Beverage Centers':'https://www.appliancesonline.com.au/api/filter/path/v3/refrigeration/beverage-fridges/beverage-centres/',
        'Bar Fridges':'https://www.appliancesonline.com.au/api/filter/path/v3/refrigeration/beverage-fridges/bar-fridges/',
        'Outdoor Fridges':'https://www.appliancesonline.com.au/api/filter/path/v3/refrigeration/beverage-fridges/outdoor/',
        'All Fridges':'https://www.appliancesonline.com.au/api/filter/path/v3/refrigeration/fridges/',
        'All Freezers':'https://www.appliancesonline.com.au/api/filter/path/v3/refrigeration/freezers/',
        'Front Loader Washing Machines':'https://www.appliancesonline.com.au/api/filter/path/v3/washers-and-dryers/washing-machines/front-loading/',
        'Top Loading Washing Machines':'https://www.appliancesonline.com.au/api/filter/path/v3/washers-and-dryers/washing-machines/top-load/',
        'Clothes Dryer':'https://www.appliancesonline.com.au/api/filter/path/v3/washers-and-dryers/dryers/',
        'Washer Dryer Combo':'https://www.appliancesonline.com.au/api/filter/path/v3/washers-and-dryers/combo/',
        'All Dishwashers':'https://www.appliancesonline.com.au/api/filter/path/v3/dishwashers/',
        'All Ovens':'https://www.appliancesonline.com.au/api/filter/path/v3/cooking-appliances/ovens/',
        'Freestanding Ovens':'https://www.appliancesonline.com.au/api/filter/path/v3/cooking-appliances/stoves/upright-ovens/',
        'Cooktops':'https://www.appliancesonline.com.au/api/filter/path/v3/cooking-appliances/cooktops/',
        'Rangehoods':'https://www.appliancesonline.com.au/api/filter/path/v3/cooking-appliances/rangehoods/',
        'Microwaves':'https://www.appliancesonline.com.au/api/filter/path/v3/cooking-appliances/microwaves/',
        'All TVs':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/tvs/',
        'Home Theatre':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/home-theatre/',
        'Portable Bluetooth Speakers':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/audio/portable-bluetooth-speakers/',
        'Home Theatre Speakers':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/audio/speakers/',
        'Wireless Speakers':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/audio/wireless-speakers/',
        'Party Speakers':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/audio/party-speakers/',
        'Headphones':'https://www.appliancesonline.com.au/api/filter/path/v3/consumer-electronics/headphones/',
        'Split System Air Conditioners':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/air-conditioning/split-system/',
        'Portable Air Conditioners':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/air-conditioning/portable/',
        'Window Air Conditioners':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/air-conditioning/window/',
        'All Heaters':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/heaters/',
        'Fans':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/fans/',
        'Air Purifiers':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/air-treatment/air-purifiers/',
        'Dehumidifiers':'https://www.appliancesonline.com.au/api/filter/path/v3/heating-and-cooling/air-treatment/dehumidifiers/',
        'Vacuum Cleaners':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/vacuum-cleaners/',
        'Carpet Washers':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/steam-mops-carpet-cleaners/carpet-washers-cleaners/',
        'Hard Floor Cleaners':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/vacuum-cleaners/hard-floor-cleaners/',
        'Juicers':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/beverage-preparation/juicers/',
        'Blenders':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/food-preparation/blenders/',
        'Food Mixers':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/food-preparation/food-mixers/',
        'Food Processors':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/food-preparation/food-processors/',
        'Air Fryers':'https://www.appliancesonline.com.au/api/filter/path/v3/cooking-appliances/airfryers/',
        'Benchtop & Toaster Ovens':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/benchtop-toaster-ovens/',
        'Steam Generators':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/garment-care-and-irons/steam-irons/',
        'Manual Coffee Machines':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/beverage-preparation/coffee-machines/manual/',
        'Automatic Coffee Machines':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/beverage-preparation/coffee-machines/automatic/',
        'Capsule Coffee Machines':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/beverage-preparation/coffee-machines/nespresso/',
        'Built-In Coffee Machines':'https://www.appliancesonline.com.au/api/filter/path/v3/small-appliances/beverage-preparation/coffee-machines/built-in/',
        'Portable Gas BBQs':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/portable-gas/',
        'Built In Barbeques':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/built-in/',
        'Freestanding Barbeques':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/freestanding/',
        'Outdoor BBQ Rangehoods':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/rangehoods/',
        'Charcoal Barbeques':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/charcoal/',
        'Outdoor Kitchens':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/outdoor/',
        'Pellet Grills':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/pellet-grills/',
        'Flat Top BBQs':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/flat-top-bbqs/',
        'Smoker Barbeques':'https://www.appliancesonline.com.au/api/filter/path/v3/bbq/smokers/'
    }


    def start_requests(self):
        for k,v in self.cats.items():
            yield scrapy.Request(
                url=v,
                callback=self.getdatas,
                meta={
                    'cat':k
                }
            )


    def getdatas(self,response):
        jsondata = json.loads(response.text)['products']
        for data in jsondata:
            url = data['uri']

            if 'https://www.appliancesonline.com.au'+url not in self.alreadyscrapped:
                yield scrapy.Request('https://www.appliancesonline.com.au/api/v2/product/slug/'+url.split('/')[-1],callback=self.getid,
                                     meta={
                                         'cat':response.meta.get('cat'),
                                         'url':'https://www.appliancesonline.com.au'+url,
                                         'slug':url.split('/')[-1]
                                     })
            else:
                print("Exists ...")



    def getid(self,response):
        id = json.loads(response.text)['productId']

        yield scrapy.Request(
            url="https://www.appliancesonline.com.au/api/v2/product/id/"+str(id),
            callback=self.getdata,
            meta={
                'cat':response.meta.get('cat'),
                'url':response.meta.get('url'),
                'slug':response.meta.get('slug')
            }
        )


    def getdata(self,response):
        date = datetime.datetime.today().strftime('%m/%d/%y')

        jsondata = json.loads(response.text)['product']

        title = jsondata['title']
        try:
            brand = jsondata['manufacturer']['name']
        except:
            brand = ''
        price = jsondata['price']
        rrp = jsondata['rrp']
        model_no = jsondata['sku']

        try:
            images = ['https://www.appliancesonline.com.au'+i['highUrl'] for i in jsondata['images']]
        except:
            images = []

        if int(price) >= 490:
            try:
                discount = str(round(((int(rrp)-int(price))/int(rrp)) * 100,2))+' %'
            except:
                discount = ''

            yield scrapy.Request(
                url="https://www.appliancesonline.com.au/api/v2/product/deliveryfeatures/slug/"+str(response.meta.get('slug'))+"/locality/id/5118",
                callback=self.getdeliveryinfo,
                meta={
                    'line':[date,response.meta.get('url'),title,response.meta.get('cat'),brand,model_no,price,rrp,discount],
                    'images':images
                }
            )

    # def start_requests(self):
    #     yield scrapy.Request(
    #         url="https://www.appliancesonline.com.au/api/v2/product/deliveryfeatures/slug/ah-beard-origins-planet-qi-medium-queen-mattress/locality/id/5119",
    #         callback=self.getdeliveryinfo
    #     )


    def getdeliveryinfo(self,response):

        jsondata = json.loads(response.text)['productPanelMessages']

        try:
            free_delivery = [i['name'] for i in jsondata if i['name'] == "Free delivery"][0]
        except:
            free_delivery = ''
        try:
            in_stock = [i['name'] for i in jsondata if i['name'] == "In stock"][0]
        except:
            in_stock = ''
        try:
            in_stock = [i['name'] for i in jsondata if i['name'] == "Out of stock"][0]
        except:
            pass

        try:
            estimated_delivery_date = [i['name'] for i in jsondata if "delivery" in i['name'] and 'Free' not in i['name']][0].replace('Estimated delivery date: ','')
        except:
            estimated_delivery_date = ''

        if free_delivery or in_stock:
            delivery_location = 'Melbourne VIC 3000'
        else:
            delivery_location = ''

        if in_stock:
            try:
                estimated_delivery_date = [i['description'] for i in jsondata if i['name'] == "In stock"][0]
            except:
                estimated_delivery_date = ''

        with open("appliancesonline.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(response.meta.get('line')+[free_delivery,in_stock,estimated_delivery_date,delivery_location]+response.meta.get('images'))
            print(response.meta.get('line')+[free_delivery,in_stock,estimated_delivery_date,delivery_location]+response.meta.get('images'))
