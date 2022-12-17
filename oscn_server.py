import scrapy
import datetime
from datetime import timedelta
import scraper_api
import csv
import os


# client = scraper_api.ScraperAPIClient("ad2c56cf179f64208ce93ad0d2047ba7")


class OscnSpider(scrapy.Spider):
    name = 'oscn'
    start_urls = ['http://oscn.net/']

    custom_settings = {
        "CONCURRENT_REQUESTS":5
    }

    if "oscn.csv" not in os.listdir(os.getcwd()):
        with open("oscn.csv","a") as f:
            writer = csv.writer(f)
            writer.writerow(['link','case_no','defendents','filed','closed','Judge','parties','attorneys','issue','filed_date','filed_by','defendent','disposition_information',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount',
                             'docket_date','docket_code','docket_description','party_name','count','amount'
                             ])

    alreadyscrapped = []
    with open("oscn.csv","r",newline="",encoding="utf-8") as r:
        reader = csv.reader(r)
        for line in reader:
            alreadyscrapped.append(line[0])

    def start_requests(self):
        dates = [(datetime.datetime.now()-timedelta(days=(datetime.datetime.now()-datetime.datetime.strptime('01/01/2016','%d/%m/%Y')).days)+timedelta(days=i)).strftime('%d/%m/%Y') for i in range(1,(datetime.datetime.now()-datetime.datetime.strptime('01/01/2016','%d/%m/%Y')).days)]

        for date in dates:
            print(date)
            yield scrapy.Request(
                url="https://www.oscn.net/dockets/Results.aspx?db=tulsa&number=&lname=&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=26&FiledDateL="+str(date)+"&FiledDateH="+str(date)+"&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=",
                # client.scrapyGet("https://www.oscn.net/dockets/Results.aspx?db=tulsa&number=&lname=&fname=&mname=&DoBMin=&DoBMax=&partytype=&apct=&dcct=26&FiledDateL=01/04/2016&FiledDateH=01/04/2016&ClosedDateL=&ClosedDateH=&iLC=&iLCType=&iYear=&iNumber=&citation=",country_code="+1"),
                callback=self.parse
            )

            # break

    def parse(self, response,*args):
        links = response.xpath('.//*[@class="resultTableRow oddRow"]/td[1]/a/@href | .//*[@class="resultTableRow evenRow"]/td[1]/a/@href').extract()
        for link in links:
            if "https://www.oscn.net/dockets/"+link not in self.alreadyscrapped:
                yield scrapy.Request(
                    url="https://www.oscn.net/dockets/"+link,
                    callback=self.getdata,
                    meta={
                        'link':"https://www.oscn.net/dockets/"+link
                    }
                )
            else:
                print("Exists ...")


    # def start_requests(self):
    #     yield scrapy.Request(
    #         url=client.scrapyGet("https://www.oscn.net/dockets/GetCaseInformation.aspx?db=tulsa&number=SC-2016-24&cmid=2906450"),
    #         callback=self.getdata
    #     )


    def getdata(self,response):

        case_no = response.xpath('.//strong[contains(.,"No. SC")]/text()').extract()[0]
        defendents = ''.join(response.xpath('.//h2[contains(.,"In the District Court in and for ")]/following-sibling::table/tr/td[1]/text()').extract())


        # print(response.xpath('.//h2[contains(.,"In the District Court in and for ")]/following-sibling::table/tr/td[2]/text()').extract_first())
        try:
            filed = [i for i in response.xpath('.//h2[contains(.,"In the District Court in and for ")]/following-sibling::table/tr/td[2]/text()').extract() if 'Filed:' in i][0].replace('Filed:','').strip()
        except:
            filed = ''
        try:
            closed = [i for i in response.xpath('.//h2[contains(.,"In the District Court in and for ")]/following-sibling::table/tr/td[2]/text()').extract() if 'Closed:' in i][0].replace('Closed:','').strip()
        except:
            closed = ''
        try:
            Judge = [i for i in response.xpath('.//h2[contains(.,"In the District Court in and for ")]/following-sibling::table/tr/td[2]/text()').extract() if 'Judge:' in i][0].replace('Judge:','').strip()
        except:
            Judge = ''

        try:
            parties = scrapy.Selector(text=response.xpath('.//h2[contains(.,"Parties")]/following-sibling::p').extract_first()).xpath('.//text()').extract_first()
        except:
            parties = ''
        try:
            attorneys = scrapy.Selector(text=response.xpath('.//h2[contains(.,"Attorneys")]/following-sibling::p').extract_first()).xpath('.//text()').extract_first()
        except:
            attorneys = ''

        try:
            issue = [i for i in response.xpath('.//h2[contains(.,"Issues")]/following-sibling::table/tr/td[2]/text()').extract() if 'Issue:' in i][0].strip().replace('Issue:','')
        except:
            issue = ''
        try:
            filed_date = [i for i in response.xpath('.//h2[contains(.,"Issues")]/following-sibling::table/tr/td[2]/text()').extract() if 'Filed Date:' in i][0].strip().replace('Filed Date:','')
        except:
            filed_date = ''
        try:
            filed_by = [i for i in response.xpath('.//h2[contains(.,"Issues")]/following-sibling::table/tr/td[2]/text()').extract() if 'Filed By:' in i][0].strip().replace('Filed By:','')
        except:
            filed_by = ''

        defendent = response.xpath('.//strong[contains(.,"Defendant:")]/following-sibling::nobr/text()').extract_first()
        disposition_information = ''.join(response.xpath('.//strong[contains(.,"Disposed:")]/text()').extract())

        temp = []
        for data in response.xpath('.//h2[contains(.,"Docket")]/following-sibling::table/tbody/tr').extract():
            sel = scrapy.Selector(text=data)
            docket_date = sel.xpath('.//td[1]/font/nobr/text()').extract_first()
            docket_code = sel.xpath('.//td[2]/font/nobr/text()').extract_first()
            docket_description = sel.xpath('.//td[3]/div/p/font/text()').extract_first()
            party_name = sel.xpath('.//*[@class="partyname"]/text()').extract_first()
            count = sel.xpath('.//*[@class="count_issue"]/text()').extract_first()
            amount = sel.xpath('.//td[6]/font/text()').extract_first()

            temp.append(docket_date)
            temp.append(docket_code)
            temp.append(docket_description)
            temp.append(party_name)
            temp.append(count)
            temp.append(amount)

        with open("oscn.csv","a",newline="",encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([a.strip() if a else '' for a in [response.meta.get('link'),case_no,defendents,filed,closed,Judge,parties,attorneys,issue,filed_date,filed_by,defendent,disposition_information]+temp])
            print([a.strip() if a else '' for a in [response.meta.get('link'),case_no,defendents,filed,closed,Judge,parties,attorneys,issue,filed_date,filed_by,defendent,disposition_information]+temp])
