# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: bank.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nbank.proto\x12\x0c\x63om.zxc.grpc\":\n\x0e\x64\x65positRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61sh_amount\x18\x02 \x01(\x05\";\n\x0fwithdrawRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61sh_amount\x18\x02 \x01(\x05\"I\n\x0bsendRequest\x12\x13\n\x0b\x63ustomer_id\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61sh_amount\x18\x02 \x01(\x05\x12\x10\n\x08taker_id\x18\x03 \x01(\x05\"#\n\x12validationResponce\x12\r\n\x05valid\x18\x01 \x01(\t2\xe3\x01\n\x04\x62\x61nk\x12I\n\x07\x64\x65posit\x12\x1c.com.zxc.grpc.depositRequest\x1a .com.zxc.grpc.validationResponce\x12K\n\x08withdraw\x12\x1d.com.zxc.grpc.withdrawRequest\x1a .com.zxc.grpc.validationResponce\x12\x43\n\x04send\x12\x19.com.zxc.grpc.sendRequest\x1a .com.zxc.grpc.validationResponceb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'bank_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_DEPOSITREQUEST']._serialized_start=28
  _globals['_DEPOSITREQUEST']._serialized_end=86
  _globals['_WITHDRAWREQUEST']._serialized_start=88
  _globals['_WITHDRAWREQUEST']._serialized_end=147
  _globals['_SENDREQUEST']._serialized_start=149
  _globals['_SENDREQUEST']._serialized_end=222
  _globals['_VALIDATIONRESPONCE']._serialized_start=224
  _globals['_VALIDATIONRESPONCE']._serialized_end=259
  _globals['_BANK']._serialized_start=262
  _globals['_BANK']._serialized_end=489
# @@protoc_insertion_point(module_scope)
