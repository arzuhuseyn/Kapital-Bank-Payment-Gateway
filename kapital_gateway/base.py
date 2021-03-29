import os
from typing import Any
import requests
from xml.dom import minidom

from .payment import Payment


class KapitalPayment:
    BASE_URL = 'https://e-commerce.kapitalbank.az'
    PORT = '5443'
    
    CERT_FILE = os.getenv("KAPITAL_CERT_FILE", "../certs/E1000010.crt")
    KEY_FILE = os.getenv("KAPITAL_KEY_FILE", "../certs/E1000010.key")

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
        self.__payment_instance=None

    def __post(self, data: str) -> str:
        headers = {'Content-Type': 'application/xml'} 
        r = requests.post(f'{self.BASE_URL}:{self.PORT}/Exec', data=data, verify=False, headers=headers, cert=(self.CERT_FILE, self.KEY_FILE))
        return r.text

    def __build_createorder_xml(self, data: str) -> str:
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

    def __build_getorderstatus_xml(self, data: str) -> str:
        return f'''<?xml version="1.0"encoding="UTF-8"?>
        <TKKPG>
            <Request>
                <Operation>GetOrderStatus</Operation>
                <Language>{data['lang']}</Language>
                <Order>
                    <Merchant>{self.merchant_id}</Merchant>
                    <OrderID>{data['order_id']}</OrderID>
                </Order>
                <SessionID>{data['session_id']}</SessionID>
            </Request>
        </TKKPG>'''

    def __handle_response(self, initial_data: str, response: str) -> None:
        xml_data=minidom.parseString(response).documentElement

        self.__payment_instance=Payment(
            amount=initial_data.get('amount'),
            order_id=int(xml_data.getElementsByTagName('OrderID')[0].firstChild.data),
            session_id=xml_data.getElementsByTagName('SessionID')[0].firstChild.data,
            payment_url=xml_data.getElementsByTagName('URL')[0].firstChild.data,
            status_code=xml_data.getElementsByTagName('Status')[0].firstChild.data,
            order_description=initial_data.get('description'),
            currency=initial_data.get('currency'),
            language_code=initial_data.get('lang')
        )
    
    def get_payment_obj(self) -> Payment:
        return self.__payment_instance

    def create_order(self, amount: int, currency: int, description: str, lang: str) -> dict:
        order_data = {
            'merchant' : self.merchant_id,
            'amount' : amount,
            'currency': currency,
            'description': description,
            'lang': lang
        }
        xml_data=self.__build_createorder_xml(order_data)
        result=self.__post(xml_data)
        self.__handle_response(order_data, result)
        payment=self.get_payment_obj()
        return {'url' : f'{self.BASE_URL}/?ORDERID={payment.order_id}&SESSIONID={payment.session_id}'}
