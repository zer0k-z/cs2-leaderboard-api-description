# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: detailData.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x64\x65tailData.proto\"\xb8\x02\n\x14ScoreLeaderboardData\x12\x10\n\x08quest_id\x18\x01 \x01(\x04\x12\r\n\x05score\x18\x02 \x01(\r\x12<\n\x0e\x61\x63\x63ountentries\x18\x03 \x03(\x0b\x32$.ScoreLeaderboardData.AccountEntries\x12\x31\n\x0cmatchentries\x18\x05 \x03(\x0b\x32\x1b.ScoreLeaderboardData.Entry\x12\x18\n\x10leaderboard_name\x18\x06 \x01(\t\x1a!\n\x05\x45ntry\x12\x0b\n\x03tag\x18\x01 \x01(\r\x12\x0b\n\x03val\x18\x02 \x01(\r\x1aQ\n\x0e\x41\x63\x63ountEntries\x12\x11\n\taccountid\x18\x01 \x01(\r\x12,\n\x07\x65ntries\x18\x02 \x03(\x0b\x32\x1b.ScoreLeaderboardData.Entry')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'detailData_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_SCORELEADERBOARDDATA']._serialized_start=21
  _globals['_SCORELEADERBOARDDATA']._serialized_end=333
  _globals['_SCORELEADERBOARDDATA_ENTRY']._serialized_start=217
  _globals['_SCORELEADERBOARDDATA_ENTRY']._serialized_end=250
  _globals['_SCORELEADERBOARDDATA_ACCOUNTENTRIES']._serialized_start=252
  _globals['_SCORELEADERBOARDDATA_ACCOUNTENTRIES']._serialized_end=333
# @@protoc_insertion_point(module_scope)
