# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: reco.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='reco.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\nreco.proto\"[\n\x0bUserRequest\x12\x12\n\nchannel_id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x13\n\x0b\x61rticle_num\x18\x03 \x01(\x05\x12\x12\n\ntime_stamp\x18\x04 \x01(\x03\"E\n\x05Track\x12\r\n\x05\x63lick\x18\x01 \x01(\t\x12\x0f\n\x07\x63ollect\x18\x02 \x01(\t\x12\x0e\n\x06liking\x18\x03 \x01(\t\x12\x0c\n\x04read\x18\x04 \x01(\t\"4\n\x07\x41rticle\x12\x12\n\narticle_id\x18\x01 \x01(\x03\x12\x15\n\x05track\x18\x02 \x01(\x0b\x32\x06.Track\"U\n\x0f\x41rticleResponse\x12\x12\n\ntime_stamp\x18\x01 \x01(\x03\x12\x10\n\x08\x65xposure\x18\x02 \x01(\t\x12\x1c\n\nrecommends\x18\x03 \x03(\x0b\x32\x08.Article2C\n\rUserRecommend\x12\x32\n\x0euser_recommend\x12\x0c.UserRequest\x1a\x10.ArticleResponse\"\x00\x62\x06proto3')
)




_USERREQUEST = _descriptor.Descriptor(
  name='UserRequest',
  full_name='UserRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='channel_id', full_name='UserRequest.channel_id', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='user_id', full_name='UserRequest.user_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='article_num', full_name='UserRequest.article_num', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='UserRequest.time_stamp', index=3,
      number=4, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=14,
  serialized_end=105,
)


_TRACK = _descriptor.Descriptor(
  name='Track',
  full_name='Track',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='click', full_name='Track.click', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='collect', full_name='Track.collect', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='liking', full_name='Track.liking', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='read', full_name='Track.read', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=107,
  serialized_end=176,
)


_ARTICLE = _descriptor.Descriptor(
  name='Article',
  full_name='Article',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='article_id', full_name='Article.article_id', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='track', full_name='Article.track', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=178,
  serialized_end=230,
)


_ARTICLERESPONSE = _descriptor.Descriptor(
  name='ArticleResponse',
  full_name='ArticleResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='time_stamp', full_name='ArticleResponse.time_stamp', index=0,
      number=1, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='exposure', full_name='ArticleResponse.exposure', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='recommends', full_name='ArticleResponse.recommends', index=2,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=232,
  serialized_end=317,
)

_ARTICLE.fields_by_name['track'].message_type = _TRACK
_ARTICLERESPONSE.fields_by_name['recommends'].message_type = _ARTICLE
DESCRIPTOR.message_types_by_name['UserRequest'] = _USERREQUEST
DESCRIPTOR.message_types_by_name['Track'] = _TRACK
DESCRIPTOR.message_types_by_name['Article'] = _ARTICLE
DESCRIPTOR.message_types_by_name['ArticleResponse'] = _ARTICLERESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

UserRequest = _reflection.GeneratedProtocolMessageType('UserRequest', (_message.Message,), dict(
  DESCRIPTOR = _USERREQUEST,
  __module__ = 'reco_pb2'
  # @@protoc_insertion_point(class_scope:UserRequest)
  ))
_sym_db.RegisterMessage(UserRequest)

Track = _reflection.GeneratedProtocolMessageType('Track', (_message.Message,), dict(
  DESCRIPTOR = _TRACK,
  __module__ = 'reco_pb2'
  # @@protoc_insertion_point(class_scope:Track)
  ))
_sym_db.RegisterMessage(Track)

Article = _reflection.GeneratedProtocolMessageType('Article', (_message.Message,), dict(
  DESCRIPTOR = _ARTICLE,
  __module__ = 'reco_pb2'
  # @@protoc_insertion_point(class_scope:Article)
  ))
_sym_db.RegisterMessage(Article)

ArticleResponse = _reflection.GeneratedProtocolMessageType('ArticleResponse', (_message.Message,), dict(
  DESCRIPTOR = _ARTICLERESPONSE,
  __module__ = 'reco_pb2'
  # @@protoc_insertion_point(class_scope:ArticleResponse)
  ))
_sym_db.RegisterMessage(ArticleResponse)



_USERRECOMMEND = _descriptor.ServiceDescriptor(
  name='UserRecommend',
  full_name='UserRecommend',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=319,
  serialized_end=386,
  methods=[
  _descriptor.MethodDescriptor(
    name='user_recommend',
    full_name='UserRecommend.user_recommend',
    index=0,
    containing_service=None,
    input_type=_USERREQUEST,
    output_type=_ARTICLERESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_USERRECOMMEND)

DESCRIPTOR.services_by_name['UserRecommend'] = _USERRECOMMEND

# @@protoc_insertion_point(module_scope)
