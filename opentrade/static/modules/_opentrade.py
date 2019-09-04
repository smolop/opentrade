import requests
import getpass
import json



class OpenTradeActions(object):
    
    def __init__(self, *args, **kwargs):
        super(OpenTradeActions, self).__init__()
        self.__host = "http://localhost:8000/api"
        self.__username = kwargs['username']
        passwd = getpass.getpass('Password:')
        self.__token=self.__get_token(passwd)
        print(self.__username)

    def __get_token(self, password):
        response = requests.post(
            url='{}/users/signin/'.format(
                self.__host
                ),
            data={
                'username': self.__username, 
                'password': password
                },
            headers={
                'Accept': 'application/json',
            }
        )

        json_response = response.json()

        token=json.loads(
            str(
                json.dumps(
                    json_response['token']
                )
            )
        )

        return token

    def __get_url(self, path):
        return '{}{}'.format(self.__host, path)

    def __get_headers(self):
        return {
                'Accept': 'application/json',
                'Authorization': 'Token {}'.format(self.__token),
                }

    def __body_request(self, path):
        url = self.__get_url(path)
        headers = self.__get_headers()
        return url, headers

    def __post(self, data, path):
        url, headers = self.__body_request(path)
        response = requests.post(url=url, data=data, headers=headers)
        return response.json()

    def __get(self, data, path):
        url, headers = self.__body_request(path)
        response = requests.get(url=url, data=data, headers=headers)
        return response.json()

    def __patch(self, data, path):
        url, headers = self.__body_request(path)
        response = requests.patch(url=url, data=data, headers=headers)
        return response.json()

    def __put(self, data, path):
        url, headers = self.__body_request(path)
        response = requests.put(url=url, data=data, headers=headers)
        return response.json()

    # ----------------
    # User functions
    # ----------------
    def sign_up(self, data={}):
        path = "/users/signup/"
        return self.__post(data, path)

    def get_user_details(self):
        path = "/users/{}/".format(self.__username)
        return self.__get({}, path)

    def user_patch(self, data={}):
        path = "/users/{}/".format(self.__username)
        return self.__patch(data, path)

    def user_update(self, data={}):
        path = "/users/{}/".format(self.__username)
        return self.__put(data, path)
    
    def verify_account(self, data={}):
        path = "/users/verify/"
        return self.__post(data, path)

   
    # ----------------
    # Share funcitons 
    # ----------------

    def get_quote_info(self, data={}):
        path = "/shares/quotes/"
        return self.__post(data, path)

    def get_quote_price(self, data={}):
        path = "/shares/price/"
        return self.__post(data, path)

    def get_quote_history(self, data={}):
        path = "/shares/history/"
        return self.__post(data, path)

    def buy(self, data={}):
        path = "/shares/buy/"
        return self.__post(data, path)    

    def sell(self, data={}):
        path = "/shares/sell/"
        return self.__post(data, path)    

    def close_order(self, data={}):
        path = "/shares/close/"
        return self.__post(data, path)    

    # -------------------
    # Favorites funcitons 
    # -------------------

    def get_favorites(self):
        path = "/shares/favorites/"
        return self.__post({}, path) 

    def follow(self, data={}):
        path = "/shares/follow/"
        return self.__post(data, path) 
        
    def unfollow(self, data={}):
        path = "/shares/unfollow/"
        return self.__post(data, path) 

    def is_followed(self, data={}):
        path = "/shares/is_followed/"
        return self.__post(data, path) 
        

    # -------------------
    # Portfolio functions
    # -------------------

    def get_all_portfolio_info(self):
        path = "/portfolio/all/"
        return self.__post({}, path)  

    def get_summary(self):
        path = "/portfolio/summary/"
        return self.__post({}, path)  

    def get_buyings_info(self):
        path = "/portfolio/buyings/"
        return self.__post({}, path) 

    def get_sellings_info(self):
        path = "/portfolio/sellings/"
        return self.__post({}, path) 
        
    def get_portfolio_value(self):
        path = "/portfolio/value/"
        return self.__post({}, path)


    # -------------------
    # Wallet functions
    # -------------------

    def get_wallet_amount(self):
        path = "/wallet/amount/"
        return self.__post({}, path)


    # --------------------------------
    # Schedule operation funcitons 
    # --------------------------------

    def get_schedule_shares_operations(self):
        path = "/shares/get_schedule_shares_operations/"
        return self.__post({}, path)  

    def schedule_share_operation(self, data={}):
        path = "/shares/schedule_share_operation/"
        return self.__post(data, path)  

    def cancel_schedule_share_operation(self, data={}):
        path = "/shares/cancel_schedule_share_operation/"
        return self.__post(data, path)  

    

    