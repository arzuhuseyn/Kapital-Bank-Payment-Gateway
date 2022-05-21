Kapital-Bank-Payment-Gateway
=======

Kapital Bank Payment Gateway for python based projects.

 ### Compatibility

Tested on Python 3.8+


### Get Started

First step: set your crt and key files path as environment variables. (SEE `.env` file)


```bash
-> pip install requests
```

**Example (Create Order):**

```python
>>> from kapital_gateway import KapitalPayment
>>> 
>>> gateway = KapitalPayment(
>>>        merchant_id="E1000010",
>>>        approve_url="https://test.com/approve",
>>>        cancel_url="https://test.com/cancel",
>>>        decline_url="https://test.com/decline",
>>>    )

>>> result = gateway.create_order(amount=10, currency=944, description="12345/TAKSIT=5", lang="AZ")
>>> print(result)
```

**Result:**

```python
>>> {'url' : 'https://e-commerce.kapitalbank.az/?ORDERID=12345&SESSIONID=A12345'}
```

**Example (Check Order Status):**

```python
>>> result = gateway.get_order_status(order_id=12345, session_id="A12345", lang="AZ")
>>> print(result)
```

**Result:**

 returns `PaymentStatus` object

```python
>>> PaymentStatus(order_id=12345, status_code='00', state='CREATED')
```


**Example (Get Order Information):**

```python
>>> result = gateway.get_order_information(order_id=12345, session_id="A12345", lang="AZ")
>>> print(result)
```

**Result:**

 returns `PaymentInformation` object

```python
>>> PaymentInformation(order_id=12345, state='CREATED', amount=10, order_description='12345/TAKSIT=5', fee=0,           create_date=datetime.datetime(2022, 5, 21, 3, 45, 4), pay_date=datetime.datetime(2022, 5, 21, 3, 45, 31))
```

### Methods

**Example: get_payment()**

```python
>>> payment_obj = gateway.get_payment()
>>> payment_obj
>>> Payment(amount=10, order_id=12345, session_id='A12345', payment_url='https://e-commerce.kapitalbank.az/index.jsp', status_code='00',order_description='12345/TAKSIT=5', currency=944, language_code='RU')
```

**Example: get_payment_status()**

```python
>>> payment_status_obj = gateway.get_payment_status()
>>> payment_status_obj
>>> PaymentStatus(order_id=12345, status_code='00', state='CREATED')
```

**Example: get_payment_information()**

```python
>>> payment_information_obj = gateway.get_payment_information()
>>> payment_information_obj
>>> PaymentInformation(order_id=12345, state='CREATED', amount=10, order_description='12345/TAKSIT=5', fee=0,           create_date=datetime.datetime(2022, 5, 21, 3, 45, 4), pay_date=datetime.datetime(2022, 5, 21, 3, 45, 31))

***(C) Arzu Hussein***
