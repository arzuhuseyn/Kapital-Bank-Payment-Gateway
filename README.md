Kapital-Bank-Payment-Gateway
=======

Kapital Bank Payment Gateway for python based projects.

 ### Compatibility

Tested on Python 3.7+

### Get Started

First step: set your crt and key files path as environment variables. (SEE `.env` file)


Example:

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

Result:

```python
>>> {'url' : 'https://e-commerce.kapitalbank.az/?ORDERID=<Order Id>&SESSIONID=<Session Id>'}
```