from datetime import datetime
import os
from typing import Any
import requests
from xml.dom import minidom

from .payment import Payment, PaymentInformation, PaymentStatus

class KapitalPayment:
    BASE_URL = os.getenv("KAPITAL_BASE_URL", "https://tstpg.kapitalbank.az")
    PORT = '5443'
    
    CERT_FILE = os.getenv("KAPITAL_CERT_FILE", "./certs/E1000010.crt")
    KEY_FILE = os.getenv("KAPITAL_KEY_FILE", "./certs/E1000010.key")

    def __init__(
        self,
        merchant_id: str,
        approve_url: str,
        cancel_url: str,
        decline_url: str,
        ) -> None:
        self.merchant_id=merchant_id 
        self.approve_url=approve_url
        self.cancel_url=cancel_url
        self.decline_url=decline_url

        self.__payment_instance=None
        self.__payment_status_instance=None
        self.__payment_information_instance=None

    def __post(self, data: str) -> str:
        headers = {'Content-Type': 'application/xml'} 
        r = requests.post(
            f'{self.BASE_URL}:{self.PORT}/Exec',
            data=data,
            verify=False,
            headers=headers,
            cert=(self.CERT_FILE, self.KEY_FILE)
        )
        return r.text

    def __build_createorder_xml(self, data: dict) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
        <TKKPG>
        <Request>
            <Operation>CreateOrder</Operation>
            <Language>{data['lang']}</Language>
            <Order>
                <OrderType>{data['order_type']}</OrderType>
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

    def __build_getorderstatus_xml(self, data: dict) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
        <TKKPG>
            <Request>
                <Operation>GetOrderStatus</Operation>
                <Language>{data['lang']}</Language>
                <Order>
                    <Merchant>{data['merchant']}</Merchant>
                    <OrderID>{data['order_id']}</OrderID>
                </Order>
                <SessionID>{data['session_id']}</SessionID>
            </Request>
        </TKKPG>'''
    
    def __build_getorderinformation_xml(self, data: dict) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
        <TKKPG>
            <Request>
                <Operation>GetOrderInformation</Operation>
                <Language>{data['lang']}</Language>
                <Order>
                    <Merchant>{data['merchant']}</Merchant>
                    <OrderID>{data['order_id']}</OrderID>
                </Order>
                <SessionID>{data['session_id']}</SessionID>
            </Request>
        </TKKPG>'''
    

    def __build_completion_xml(self, data: dict) -> str:
        return f'''<?xml version="1.0" encoding="UTF-8"?>
                <TKKPG>
                    <Request>
                            <Operation>Completion</Operation>
                            <Language>{data['lang']}</Language>
                            <Order>
                                    <Merchant>{data['merchant']}</Merchant>
                                    <OrderID>{data['order_id']}</OrderID>
                            </Order>
                            <SessionID>{data['session_id']}</SessionID>
                            <Amount>{data['amount']}</Amount>
                            <Description>{data['description']}</Description>
                    </Request>
                </TKKPG>'''
    
    def __build_reverse_xml(self,data: dict) -> str:
        return f'''
        <TKKPG>
            <Request>
                    <Operation>Reverse</Operation>
                    <Language>{data['lang']}</Language>
                    <Order>
                            <Merchant>{self.merchant_id}</Merchant>
                            <OrderID>{data['order_id']}</OrderID>
                            <Positions>
                                <Position>
                                    <PaymentSubjectType>1</PaymentSubjectType>
                                    <Quantity>1</Quantity>
                                    <PaymentType>2</PaymentType>
                                    <PaymentMethodType>1</PaymentMethodType>
                                </Position>
                            </Positions>
                    </Order>
                    <Description>{data['description']}</Description>
                    <SessionID>{data['session_id']}</SessionID>
                    <TranId></TranId>
                    <Source>1</Source>
            </Request>
        </TKKPG>'''

    def __build_payment_obj(self, initial_data: dict, response: str) -> None:
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

    def __build_payment_status_obj(self, response: str) -> None:
        xml_data=minidom.parseString(response).documentElement

        self.__payment_status_instance=PaymentStatus(
            order_id=int(xml_data.getElementsByTagName('OrderID')[0].firstChild.data),
            status_code=xml_data.getElementsByTagName('Status')[0].firstChild.data,
            state=xml_data.getElementsByTagName('OrderStatus')[0].firstChild.data,
        )
    def __build_payment_information_obj(self, response: str) -> None:
        xml_data=minidom.parseString(response).documentElement
        create_date = xml_data.getElementsByTagName('createDate')[0].firstChild.data
        pay_date_element = xml_data.getElementsByTagName('payDate')[0].firstChild
        pay_date = pay_date_element.data if pay_date_element else 'null'

        self.__payment_information_instance=PaymentInformation(
            order_id=int(xml_data.getElementsByTagName('id')[0].firstChild.data),
            session_id=xml_data.getElementsByTagName('SessionID')[0].firstChild.data,
            order_type=xml_data.getElementsByTagName('OrderType')[0].firstChild.data,
            state=xml_data.getElementsByTagName('Orderstatus')[0].firstChild.data,
            amount=int(xml_data.getElementsByTagName('Amount')[0].firstChild.data),
            order_description=xml_data.getElementsByTagName('Description')[0].firstChild.data,
            fee=int(xml_data.getElementsByTagName('Fee')[0].firstChild.data),
            create_date=datetime.strptime(create_date, '%Y-%m-%d %H:%M:%S'),
            pay_date=datetime.strptime(pay_date, '%Y-%m-%d %H:%M:%S') if pay_date != 'null' else None,
        )


    def get_payment(self) -> Payment:
        return self.__payment_instance

    def get_payment_status(self) -> PaymentStatus:
        return self.__payment_status_instance
    
    def get_payment_information(self) -> PaymentInformation:
        return self.__payment_information_instance

    def create_order(self, amount: int, currency: int, description: str, lang: str, pre_auth: bool=False) -> dict:
        order_data = {
            'merchant' : self.merchant_id,
            'amount' : amount,
            'currency': currency,
            'description': description,
            'lang': lang,
            'order_type': 'PreAuth' if pre_auth else 'Purchase'
        }
        xml_data=self.__build_createorder_xml(order_data)
        result=self.__post(xml_data)
        self.__build_payment_obj(order_data, result)
        payment=self.get_payment()
        return {'url' : f'{payment.payment_url}?ORDERID={payment.order_id}&SESSIONID={payment.session_id}'}

    def complete_order(self, order_id: int, session_id: str, amount: int, description: str, lang: str = "AZ") -> str:
        order_data = {
            'merchant' : self.merchant_id,
            'order_id' : order_id,
            'session_id': session_id,
            'amount': amount,
            'description': description,
            'lang' : lang
        }
        xml_data = self.__build_completion_xml(order_data)
        result=self.__post(xml_data)
        response_xml=minidom.parseString(result).documentElement
        status_code = response_xml.getElementsByTagName('Status')[0].firstChild.data
        return status_code
    
    def reverse_order(self, order_id:int, session_id, description, lang: str = "AZ"):
        order_data = {
            'merchant' : self.merchant_id,
            'order_id' : order_id,
            'session_id': session_id,
            'lang' : lang,
            'description': description
        }
        xml_data = self.__build_reverse_xml(order_data)
        result=self.__post(xml_data)
        response_xml=minidom.parseString(result).documentElement
        status_code = response_xml.getElementsByTagName('Status')[0].firstChild.data
        return status_code

    def get_order_status(self, order_id: int, session_id: str, lang: str = "AZ") -> PaymentStatus:
        order_data = {
            'merchant' : self.merchant_id,
            'order_id' : order_id,
            'session_id': session_id,
            'lang' : lang
        }
        xml_data = self.__build_getorderstatus_xml(order_data)
        result=self.__post(xml_data)
        self.__build_payment_status_obj(result)
        return self.get_payment_status()
    
    def get_order_information(self, order_id: int, session_id: str, lang: str = "AZ") -> PaymentInformation:
        order_data = {
            'merchant' : self.merchant_id,
            'order_id' : order_id,
            'session_id': session_id,
            'lang' : lang
        }
        xml_data = self.__build_getorderinformation_xml(order_data)
        result=self.__post(xml_data)
        self.__build_payment_information_obj(result)
        return self.get_payment_information()

