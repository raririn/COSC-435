# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='message.proto',
  package='tutorial',
  syntax='proto2',
  serialized_pb=_b('\n\rmessage.proto\x12\x08tutorial\"6\n\x08\x42\x61sicMsg\x12\x10\n\x08nickname\x18\x01 \x02(\t\x12\x0c\n\x04text\x18\x02 \x02(\t\x12\n\n\x02iv\x18\x03 \x02(\t')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_BASICMSG = _descriptor.Descriptor(
  name='BasicMsg',
  full_name='tutorial.BasicMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nickname', full_name='tutorial.BasicMsg.nickname', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='text', full_name='tutorial.BasicMsg.text', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iv', full_name='tutorial.BasicMsg.iv', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=27,
  serialized_end=81,
)

DESCRIPTOR.message_types_by_name['BasicMsg'] = _BASICMSG

BasicMsg = _reflection.GeneratedProtocolMessageType('BasicMsg', (_message.Message,), dict(
  DESCRIPTOR = _BASICMSG,
  __module__ = 'message_pb2'
  # @@protoc_insertion_point(class_scope:tutorial.BasicMsg)
  ))
_sym_db.RegisterMessage(BasicMsg)


# @@protoc_insertion_point(module_scope)