from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class depositRequest(_message.Message):
    __slots__ = ["customer_id", "cash_amount"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    CASH_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    customer_id: int
    cash_amount: int
    def __init__(self, customer_id: _Optional[int] = ..., cash_amount: _Optional[int] = ...) -> None: ...

class withdrawRequest(_message.Message):
    __slots__ = ["customer_id", "cash_amount"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    CASH_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    customer_id: int
    cash_amount: int
    def __init__(self, customer_id: _Optional[int] = ..., cash_amount: _Optional[int] = ...) -> None: ...

class sendRequest(_message.Message):
    __slots__ = ["customer_id", "cash_amount", "taker_id"]
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    CASH_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TAKER_ID_FIELD_NUMBER: _ClassVar[int]
    customer_id: int
    cash_amount: int
    taker_id: int
    def __init__(self, customer_id: _Optional[int] = ..., cash_amount: _Optional[int] = ..., taker_id: _Optional[int] = ...) -> None: ...

class validationResponce(_message.Message):
    __slots__ = ["valid"]
    VALID_FIELD_NUMBER: _ClassVar[int]
    valid: str
    def __init__(self, valid: _Optional[str] = ...) -> None: ...
