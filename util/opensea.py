import requests
import copy

class OpenSea:
    def __init__(self, ETH_CONTRACT, API_KEY=""):
        self.API_KEY = API_KEY
        self.ETH_CONTRACT = ETH_CONTRACT

        self.SINGLE_ASSET_URL = "https://api.opensea.io/api/v1/asset/" + self.ETH_CONTRACT + "/"
        self.MULTI_ASSET_URL = "https://api.opensea.io/api/v1/assets?asset_contract_address=" + self.ETH_CONTRACT
        self.EVENT_URL = "https://api.opensea.io/api/v1/events"

    def single_asset(self, id):
        url = self.SINGLE_ASSET_URL + str(id)
        resp = requests.request("GET", url, headers={'X-API-KEY': self.API_KEY})
        return resp.json()

    def multi_asset(self, id_list):
        master_list = []
        this_list = []
        subend = 0
        for i in range(len(id_list)):
            subend += 1
            this_list.append(id_list[i])
            if(subend == 30):
                master_list.append(this_list)
                subend = 0
                this_list = []
        if(this_list != [] and subend != 30):
            master_list.append(this_list)
        master_return = []
        all_urls = []

        for tlist in master_list:

            this_asset_url = copy.copy(self.MULTI_ASSET_URL)
            for i in tlist:
                this_asset_url = this_asset_url + "&token_ids=" + str(i)

            resp = requests.request("GET", this_asset_url ,headers={'X-API-KEY': self.API_KEY})

            master_return = master_return + list(resp.json()["assets"])



        return master_return

    def get_bulk_pricing(self, master_list):
        test_list = master_list

        market = self.multi_asset(test_list)
        #iterate through response and get listed prices
        dl = []
        for item in market:
            this_seller = item["sell_orders"]

            if(this_seller):

                this_eth_price = int(float((this_seller[0]["current_price"])))/1000000000000000000

                this_usd_price = round(float(this_seller[0]["payment_token_contract"]["usd_price"])*this_eth_price,2)


                dl.append([item["name"], this_eth_price, this_usd_price])
        return dl

    def get_recent_sales(self):
        querystring = {"asset_contract_address":self.ETH_CONTRACT,"event_type":"successful","only_opensea": "false", "offset": "0", "limit": "50"}
        headers = {"Accept": "application/json"}
        resp = (requests.request("GET", self.EVENT_URL,headers=headers,params=querystring).json())["asset_events"]
        dl = []

        for i in range(len(resp)):

            if(resp[i]["asset"] != None): #asset bundle dgaf

                img = resp[i]["asset"]["image_url"]
                tid = resp[i]["asset"]["token_id"]
                total_price = int(resp[i]["total_price"])/1000000000000000000
                total_usd_price = round(float(resp[i]["payment_token"]["usd_price"])*total_price, 2)

                seller = resp[i]["seller"]["address"]
                buyer = resp[i]["winner_account"]["address"]
                transaction_id = resp[i]["id"]

                dl.append([transaction_id, tid,total_price,total_usd_price,seller,buyer,img])
        return dl


