# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: linprog_service.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import linear_solver_pb2 as linear__solver__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='linprog_service.proto',
  package='operations_research',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x15linprog_service.proto\x12\x13operations_research\x1a\x13linear_solver.proto2m\n\x0eLinProgService\x12[\n\tMILPModel\x12#.operations_research.MPModelRequest\x1a\'.operations_research.MPSolutionResponse\"\x00\x62\x06proto3'
  ,
  dependencies=[linear__solver__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_LINPROGSERVICE = _descriptor.ServiceDescriptor(
  name='LinProgService',
  full_name='operations_research.LinProgService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=67,
  serialized_end=176,
  methods=[
  _descriptor.MethodDescriptor(
    name='MILPModel',
    full_name='operations_research.LinProgService.MILPModel',
    index=0,
    containing_service=None,
    input_type=linear__solver__pb2._MPMODELREQUEST,
    output_type=linear__solver__pb2._MPSOLUTIONRESPONSE,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_LINPROGSERVICE)

DESCRIPTOR.services_by_name['LinProgService'] = _LINPROGSERVICE

# @@protoc_insertion_point(module_scope)