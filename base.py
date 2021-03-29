import os
import requests
from xml.dom import minidom

from payment import Payment


class KapitalPayment:
    SERVICE_URL = 'https://e-commerce.kapitalbank.az:5443/Exec'
    
    CERT_FILE = os.getenv("KAPITAL_CERT_FILE", "certs/E1000010.crt")
    KEY_FILE = os.getenv("KAPITAL_KEY_FILE", "certs/E1000010.key")

    def __init__(
        self,
        merchant_id,
        approve_url,
        cancel_url,
        decline_url,
        ) -> None:
        self.merchant_id=merchant_id 
        self.approve_url=approve_url
        self.cancel_url=cancel_url
        self.decline_url=decline_url

    def __post(self, data):
        headers = {'Content-Type': 'application/xml'} 
        r = requests.post(self.SERVICE_URL, data=data, verify=False, headers=headers, cert=(self.CERT_FILE, self.KEY_FILE))
        return r.text

    def __build_createorder_xml(self, data):
        return f'''<?xml version="1.0" encoding="UTF-8"?>
        <TKKPG>
        <Request>
            <Operation>CreateOrder</Operation>
            <Language>{data['lang']}</Language>
            <Order>
                <OrderType>Purchase</OrderType>
                <Merchant>{data['merchant']}</Merchant>
                <Amount>{data['amount']}</Amount>
                <Currency>{data['currency']}</Currency>
                <Description>{data['description']}</Description>
                <ApproveURL>{self.approve_url}</ApproveURL>
                <CancelURL>{self.cancel_url}</CancelURL>
                <DeclineURL>{self.decline_url}</DeclineURL>
            </Order>
        </Request>
        </TKKPG>'''

    def create_order(self, amount: int, currency: int, description: str, lang: str):
        order_data = {
            'merchant' : self.merchant_id,
            'amount' : amount,
            'currency': currency,
            'description': description,
            'lang': lang
        }
        xml_data=self.__build_createorder_xml(order_data)
        result=self.__post(xml_data)
        return self.__handle_response(order_data, result)

    def __handle_response(self, initial_data, response):
        xml_data=minidom.parseString(response).documentElement

        payment_instance=Payment(
            amount=initial_data.get('amount'),
            order_id=int(xml_data.getElementsByTagName('OrderID')[0].firstChild.data),
            session_id=xml_data.getElementsByTagName('SessionID')[0].firstChild.data,
            payment_url=xml_data.getElementsByTagName('URL')[0].firstChild.data,
            status_code=xml_data.getElementsByTagName('Status')[0].firstChild.data,
            order_description=initial_data.get('description'),
            currency=initial_data.get('currency'),
            language_code=initial_data.get('lang')
        )

        return payment_instance
