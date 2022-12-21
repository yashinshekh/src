import scrapy
from fake_headers import Headers
import datetime
import csv
import os
import json
import time

from scraper_api import ScraperAPIClient


# client = ScraperAPIClient('b5f9371a7ec41e33154080ca9ec9fb7e')
# client = ScraperAPIClient('eef8304a6f6ee928977bf87358d4c5cb')
# client = ScraperAPIClient('eed279f0ecd13299a2c9dc637d994890')
# client = ScraperAPIClient('563837594f87bca82448afefbce898ae')
# client = ScraperAPIClient('81632cde3084e9edb203c5568087a5f1')
# client = ScraperAPIClient('cf524982e4e3294f1918e6240f5f79ad')
# client = ScraperAPIClient('0d5f316df1595aaa2d11a6932a25a558')
# client = ScraperAPIClient('8cf0110b48f7ce675e6daf03e7643688')
# client = ScraperAPIClient('302d795db1c33f69c06e2ea59381e1b0')
# client = ScraperAPIClient('e88f328a042cf9820191467443290bb1')
# client = ScraperAPIClient('0d41221c896e4ad2ba67eff38507d527')
# client = ScraperAPIClient('43b295417586280624e40a63f644814b')
# client = ScraperAPIClient('2c5b7f2959292139c44309a845506883')
# client = ScraperAPIClient('2ee5003527b1f37d50af16bad97662f9')
# client = ScraperAPIClient('5b3f2338f71c21920c6edc0de8d110c7')
# client = ScraperAPIClient('0bfc9162949ffd1cb1d2aeeb419b60df')
# client = ScraperAPIClient('7ba33d306299b7e4b33e15b5b12b92a8')
# client = ScraperAPIClient('ccdfec9029c05ffc3d08419af4a25721')
# client = ScraperAPIClient('13f32d508780e398fd76fc70477deb39')
# client = ScraperAPIClient('cff5eba705394ed8d6994ca70c4ad78d')
# client = ScraperAPIClient('133f4fed7e331bdf7b33ac40d1216eca')
# client = ScraperAPIClient('139bd2d6764020d5641b1bd5499f1661')
# client = ScraperAPIClient('b921f89892c18c4ab5f4713c28e786e2')
# client = ScraperAPIClient('cd29fece45661acb1a307bc3acddc315')
# client = ScraperAPIClient('ab8c021783c7f6199d188da4f0b39e83')
# client = ScraperAPIClient('201a46dfe835de36df3ad68f2fdb4cd0')
# client = ScraperAPIClient('802a9d8e793cc9681acac91a7607db57')
# client = ScraperAPIClient('50ba4abca751fcbafab85122221cac94')
# client = ScraperAPIClient('02105c209b3300d543e7c2141c4963ac')
# client = ScraperAPIClient('4f90bc13e39894e07d5a4ffc739d96a5')
# client = ScraperAPIClient('a10a3f904f8fc9ca3c68b77671dca56b')
# client = ScraperAPIClient('03f8019853800c83e248baf5bb5659e4')
# client = ScraperAPIClient('53ae3528da5010e02ca79fa229f04b3e')
# client = ScraperAPIClient('c0bd697f76ab84d89091694fc8f004a2')
# client = ScraperAPIClient('394c359891c8d2830a7392d60847aab0')
# client = ScraperAPIClient('60c9a284549dd12cc0657688f6b9f7ef')
# client = ScraperAPIClient('8cce4b203a14eb5aaa2ab8741938bd2d')
# client = ScraperAPIClient('da80c5ffed971e85b714fde6f7227aae')
# client = ScraperAPIClient('65378c2f203e03b85cd7caec884ff012')
client = ScraperAPIClient('c558acdba187c8f0a66f82dddee3fcef')

class HarveynormanSpider(scrapy.Spider):
    name = 'harveynorman'

    start_urls = [
        "https://www.harveynorman.com.au/phones-accessories-gps/wearables/smart-watches?price=490-",
        "https://www.harveynorman.com.au/cameras-printers-photocentre/drones/drones?price=490-",
        "https://www.harveynorman.com.au/smart-home/smart-home-entertainment/smart-home-tvs?price=490-",
        "https://www.harveynorman.com.au/tv-blu-ray-home-theatre/tvs-by-screen-size/all-tvs?price=490-",
        "https://www.harveynorman.com.au/tv-blu-ray-home-theatre/home-theatre-speakers?price=490-",
        "https://www.harveynorman.com.au/tv-blu-ray-home-theatre/home-theatre-speakers/soundbars_speaker+systems/1065?price=490-",
        "https://www.harveynorman.com.au/headphones-audio-music/sound-systems?price=490-",
        "https://www.harveynorman.com.au/headphones-audio-music/sound-systems/hi-fi-systems?price=490-",
        "https://www.harveynorman.com.au/headphones-audio-music/headphones?price=490-",
        "https://www.harveynorman.com.au/headphones-audio-music/headphones/wireless-headphones?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/coffee-beverage/coffee-machines?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/coffee-beverage/drink+makers_juicers_milkshake+maker/1065?price=500-",
        "https://www.harveynorman.com.au/kitchen-appliances/small-kitchen-appliances?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/freestanding-cookers?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/microwave-ovens?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/rangehoods?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/ovens/warming+drawers/1065?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/ovens?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/cooktops?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/fridges?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/freezers?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/beer-wine-appliances?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/microwave-ovens/built-in+microwaves_compact+microwaves_convection+microwaves_flatbed+microwaves_inverter+microwave_inverter+microwaves_microwaves/1065?price=490-",
        "https://www.harveynorman.com.au/kitchen-appliances/appliances/dishwashers?price=490-",
        "https://www.harveynorman.com.au/vacuum-laundry-appliances/vacuum-cleaners/vacuum-cleaners?price=490-",
        "https://www.harveynorman.com.au/vacuum-laundry-appliances/washing-machines-dryers/washing-machines?price=490-",
        "https://www.harveynorman.com.au/vacuum-laundry-appliances/washing-machines-dryers/dryers?price=490-",
        "https://www.harveynorman.com.au/vacuum-laundry-appliances/irons-steam-stations/steam-stations?price=490-",
        "https://www.harveynorman.com.au/vacuum-laundry-appliances/steam-cleaners-shampooers?price=490-",
        "https://www.harveynorman.com.au/heating-cooling-air-treatment/air-conditioning?price=490-",
        "https://www.harveynorman.com.au/heating-cooling-air-treatment/fans?price=490-",
        "https://www.harveynorman.com.au/heating-cooling-air-treatment/heating?price=490-",
        "https://www.harveynorman.com.au/heating-cooling-air-treatment/air-treatment?price=490-",
        "https://www.harveynorman.com.au/health-fitness-beauty/home-gym-equipment?price=490-",
        "https://www.harveynorman.com.au/furniture-outdoor-bbqs/outdoor-living/bbqs?price=490-",
        "https://www.harveynorman.com.au/toys-baby-hobbies/baby?price=490-"
    ]


    if 'harveynorman.csv' not in os.listdir(os.getcwd()):
        with open("harveynorman.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['url','date','category','name','product_page_url','model','model 2','gtin','price','key_features','specifications','brand','status'])



    alreadyscrapped = []
    with open("harveynorman.csv","r",encoding="utf-8") as r:
        reader = csv.reader(r)
        for line in reader:
            alreadyscrapped.append(line[4])

    custom_settings = {
        "CONCURRENT_REQUESTS":5,
        # 'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                client.scrapyGet(url=url),
                callback=self.getlinks,
                meta={
                    'url':url
                }
            )

    def getlinks(self,response):
        links = response.xpath('.//*[@class="name fn l_mgn-tb-sm l_dsp-blc"]/@href').extract()
        for link in links:
            if link not in self.alreadyscrapped:
                yield scrapy.Request(
                    client.scrapyGet(link),
                    callback=self.getdata,
                    meta={
                        'link':link,
                        'url':response.meta.get('url')
                    }
                )
            else:
                print("Exists ")

        nextlink = response.xpath('.//a[contains(.,"Next")]/@href').extract_first()
        # print("Nextlink: "+str(nextlink))
        if nextlink:
            yield scrapy.Request(
                client.scrapyGet(nextlink),
                callback=self.getlinks,
                meta={
                    'url':response.meta.get('url')
                }
            )



    def getdata(self,response):
        model_no_2 = response.xpath('.//*[@class="product-id meta quiet p_txt-sm"]/text()').extract_first()
        date = datetime.datetime.today().strftime('%m/%d/%y')
        category = response.xpath('.//*[@id="breadcrumbs"]/li[6]/a/text()').extract_first()
        name = response.xpath('.//*[@class="product-name"]/text()').extract_first()
        product_page_url = response.meta.get('link')
        status = ''

        try:
            if 'Add to cart' in response.xpath('.//*[@class="product-view-sales"]').extract_first():
                status = "Add to cart"
            elif "In-store only" in response.xpath('.//*[@class="product-view-sales"]').extract_first():
                status = 'In-store only'
            elif "Buy at Miele" in response.xpath('.//*[@class="product-view-sales"]').extract_first():
                status = 'Buy at Miele'
        except:
            status = 'ask a question'

        try:
            key_features = '\n'.join(response.xpath('.//h6[contains(.,"Key Features")]/following-sibling::ul/li/text()').extract())
        except:
            key_features = ''
        brand = response.xpath('.//th[contains(.,"Brand")]/following-sibling::td/text()').extract_first()

        try:
            datas = response.xpath('.//*[@type="text/javascript"]/text()[contains(.,"var spConfig = new Product.Config(")]').extract_first().replace('var spConfig = new Product.Config(','').replace(');','')
        except:
            datas = ''

        if datas:
            jsondata = json.loads(datas)

            product_id = jsondata['productId']
            ids = jsondata['childProducts'].keys()

            for id in ids:
                child_price = jsondata['childProducts'][id]['price']
                yield scrapy.Request('https://www.harveynorman.com.au/oi/ajax/specs?id='+str(id)+'&pid='+str(product_id),callback=self.getchilds,
                                     meta={
                                         'line':[response.meta.get('url'),date,category,name,product_page_url,'',model_no_2,'',child_price,key_features,'',brand,status]
                                     })

        else:
            model = response.xpath('.//th[contains(.,"Model")]/following-sibling::td/text()').extract_first()
            gtin = response.xpath('.//th[contains(.,"GTIN")]/following-sibling::td/text()').extract_first()
            price = response.xpath('.//*[@id="product-view-price"]/@data-price').extract_first()

            try:
                specifications = '\n'.join([scrapy.Selector(text=i).xpath('.//th/text()').extract_first()+' : '+scrapy.Selector(text=i).xpath('.//td/text()').extract_first() for i in response.xpath('.//*[@id="product-attribute-specs-table"]//tr').extract()])
            except:
                specifications = ''

            with open("harveynorman.csv","a",newline="",encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([response.meta.get('url'),date,category,name,product_page_url,model,model_no_2,gtin,price,key_features,specifications,brand,status])
                print([response.meta.get('url'),date,category,name,product_page_url,model,model_no_2,gtin,price,key_features,specifications,brand,status])



    def getchilds(self,response):
        model = response.xpath('.//th[contains(.,"Model")]/following-sibling::td/text()').extract_first()
        gtin = response.xpath('.//th[contains(.,"GTIN")]/following-sibling::td/text()').extract_first()
        try:
            specifications = '\n'.join([scrapy.Selector(text=i).xpath('.//th/text()').extract_first()+' : '+scrapy.Selector(text=i).xpath('.//td/text()').extract_first() for i in response.xpath('.//*[@id="product-attribute-specs-table"]//tr').extract()])
        except:
            specifications = ''

        response.meta.get('line')[5] = model
        response.meta.get('line')[7] = gtin
        response.meta.get('line')[10] = specifications


        with open("harveynorman.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(response.meta.get('line'))
            print(response.meta.get('line'))


    def close(spider, reason):
        print("Sleeping for 60 seconds")
        time.sleep(600)
        os.system("scrapy runspider harveynorman.py")