Kapital-Bank-Payment-Gateway
=======

Kapital Bank Payment Gateway for python based projects.

 ### Compatibility

Tested on Python 3.8+

### Get Started

First step: set your crt and key files path as environment variables. (SEE `.env` file)


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

>>> result = gateway.create_order(amount=10, currency=944, description="Test", lang="AZ")
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

### Methods

**Example: get_payment()**

```python
>>> payment_obj = gateway.get_payment()
>>> payment_obj
>>> Payment(amount=123456, order_id=12345, session_id='A12345', payment_url='https://e-commerce.kapitalbank.az/index.jsp', status_code='00',order_description='xxxxxx', currency=944, language_code='RU')
```

**Example: get_payment_status()**

```python
>>> payment_status_obj = gateway.get_payment_status()
>>> payment_status_obj
>>> PaymentStatus(order_id=12345, status_code='00', state='CREATED')
```

***(C) Arzu Hussein***