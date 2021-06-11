# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: linear_extension.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import linear_solver_pb2 as linear__solver__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='linear_extension.proto',
  package='operations_research',
  syntax='proto2',
  serialized_options=b'Z\'operations_research;operations_research',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x16linear_extension.proto\x12\x13operations_research\x1a\x13linear_solver.proto\"v\n\x13ReferenceMPVariable\x12\x12\n\x08var_name\x18\x05 \x01(\t:\x00\x12\x12\n\nmodel_name\x18\x06 \x01(\t\x12\x11\n\tvar_index\x18\x07 \x01(\x05\x12\x16\n\x0ereference_name\x18\x08 \x01(\t\x12\x0c\n\x04tags\x18\x0b \x03(\t\"\xdf\x01\n\x0cMPExpression\x12\x0e\n\x04name\x18\x05 \x01(\t:\x00\x12\x19\n\x0blower_bound\x18\x06 \x01(\x01:\x04-inf\x12\x18\n\x0bupper_bound\x18\x07 \x01(\x01:\x03inf\x12 \n\x15objective_coefficient\x18\x08 \x01(\x01:\x01\x30\x12;\n\tvariables\x18\x0b \x03(\x0b\x32(.operations_research.ReferenceMPVariable\x12\x1d\n\x15variable_coefficients\x18\x0c \x03(\x01\x12\x0c\n\x04tags\x18\x0f \x03(\t\"\xaa\x04\n\x11\x45xpressionMPModel\x12\x36\n\x08variable\x18\x03 \x03(\x0b\x32$.operations_research.MPVariableProto\x12:\n\nconstraint\x18\x04 \x03(\x0b\x32&.operations_research.MPConstraintProto\x12I\n\x12general_constraint\x18\x07 \x03(\x0b\x32-.operations_research.MPGeneralConstraintProto\x12\x17\n\x08maximize\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x1b\n\x10objective_offset\x18\x02 \x01(\x01:\x01\x30\x12\x46\n\x13quadratic_objective\x18\x08 \x01(\x0b\x32).operations_research.MPQuadraticObjective\x12\x0e\n\x04name\x18\x05 \x01(\t:\x00\x12\x45\n\rsolution_hint\x18\x06 \x01(\x0b\x32..operations_research.PartialVariableAssignment\x12\x36\n\x0b\x65xpressions\x18\x0b \x03(\x0b\x32!.operations_research.MPExpression\x12I\n\x15reference_constraints\x18\x0c \x03(\x0b\x32*.operations_research.ReferenceMPConstraint\"\xbd\x01\n\x15ReferenceMPConstraint\x12\x19\n\x0blower_bound\x18\x02 \x01(\x01:\x04-inf\x12\x18\n\x0bupper_bound\x18\x03 \x01(\x01:\x03inf\x12\x0e\n\x04name\x18\x04 \x01(\t:\x00\x12\x18\n\x0c\x63oefficients\x18\x07 \x03(\x01\x42\x02\x10\x01\x12\x45\n\x13variable_references\x18\x08 \x03(\x0b\x32(.operations_research.ReferenceMPVariable\"\xc1\x03\n\x10ReferenceMPModel\x12\x0e\n\x04name\x18\x05 \x01(\t:\x00\x12\x37\n\tvariables\x18\x03 \x03(\x0b\x32$.operations_research.MPVariableProto\x12;\n\x0b\x63onstraints\x18\x04 \x03(\x0b\x32&.operations_research.MPConstraintProto\x12\x17\n\x08maximize\x18\x01 \x01(\x08:\x05\x66\x61lse\x12\x45\n\x13reference_variables\x18\n \x03(\x0b\x32(.operations_research.ReferenceMPVariable\x12I\n\x15reference_constraints\x18\x0b \x03(\x0b\x32*.operations_research.ReferenceMPConstraint\x12\x36\n\x0b\x65xpressions\x18\x0f \x03(\x0b\x32!.operations_research.MPExpression\x12\x0c\n\x04tags\x18\x10 \x03(\t\x12\x1a\n\x12model_dependencies\x18\x11 \x03(\t\x12\x1a\n\x0b\x62uild_final\x18\x14 \x01(\x08:\x05\x66\x61lse\"\xe2\x01\n\x0f\x45xtendedMPModel\x12;\n\x0e\x63oncrete_model\x18\x01 \x01(\x0b\x32!.operations_research.MPModelProtoH\x00\x12@\n\x0freference_model\x18\x02 \x01(\x0b\x32%.operations_research.ReferenceMPModelH\x00\x12\x42\n\x10\x65xpression_model\x18\x03 \x01(\x0b\x32&.operations_research.ExpressionMPModelH\x00\x42\x0c\n\nmodel_type\"N\n\x17ReferenceMPModelRequest\x12\x33\n\x05model\x18\x01 \x01(\x0b\x32$.operations_research.ExtendedMPModelB)Z\'operations_research;operations_research'
  ,
  dependencies=[linear__solver__pb2.DESCRIPTOR,])




_REFERENCEMPVARIABLE = _descriptor.Descriptor(
  name='ReferenceMPVariable',
  full_name='operations_research.ReferenceMPVariable',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='var_name', full_name='operations_research.ReferenceMPVariable.var_name', index=0,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model_name', full_name='operations_research.ReferenceMPVariable.model_name', index=1,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='var_index', full_name='operations_research.ReferenceMPVariable.var_index', index=2,
      number=7, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reference_name', full_name='operations_research.ReferenceMPVariable.reference_name', index=3,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='operations_research.ReferenceMPVariable.tags', index=4,
      number=11, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=68,
  serialized_end=186,
)


_MPEXPRESSION = _descriptor.Descriptor(
  name='MPExpression',
  full_name='operations_research.MPExpression',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.MPExpression.name', index=0,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='lower_bound', full_name='operations_research.MPExpression.lower_bound', index=1,
      number=6, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=-1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='upper_bound', full_name='operations_research.MPExpression.upper_bound', index=2,
      number=7, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='objective_coefficient', full_name='operations_research.MPExpression.objective_coefficient', index=3,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variables', full_name='operations_research.MPExpression.variables', index=4,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variable_coefficients', full_name='operations_research.MPExpression.variable_coefficients', index=5,
      number=12, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='operations_research.MPExpression.tags', index=6,
      number=15, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=189,
  serialized_end=412,
)


_EXPRESSIONMPMODEL = _descriptor.Descriptor(
  name='ExpressionMPModel',
  full_name='operations_research.ExpressionMPModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='variable', full_name='operations_research.ExpressionMPModel.variable', index=0,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraint', full_name='operations_research.ExpressionMPModel.constraint', index=1,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='general_constraint', full_name='operations_research.ExpressionMPModel.general_constraint', index=2,
      number=7, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maximize', full_name='operations_research.ExpressionMPModel.maximize', index=3,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='objective_offset', full_name='operations_research.ExpressionMPModel.objective_offset', index=4,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='quadratic_objective', full_name='operations_research.ExpressionMPModel.quadratic_objective', index=5,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.ExpressionMPModel.name', index=6,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='solution_hint', full_name='operations_research.ExpressionMPModel.solution_hint', index=7,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expressions', full_name='operations_research.ExpressionMPModel.expressions', index=8,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reference_constraints', full_name='operations_research.ExpressionMPModel.reference_constraints', index=9,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=415,
  serialized_end=969,
)


_REFERENCEMPCONSTRAINT = _descriptor.Descriptor(
  name='ReferenceMPConstraint',
  full_name='operations_research.ReferenceMPConstraint',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='lower_bound', full_name='operations_research.ReferenceMPConstraint.lower_bound', index=0,
      number=2, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=-1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='upper_bound', full_name='operations_research.ReferenceMPConstraint.upper_bound', index=1,
      number=3, type=1, cpp_type=5, label=1,
      has_default_value=True, default_value=1e10000,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.ReferenceMPConstraint.name', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='coefficients', full_name='operations_research.ReferenceMPConstraint.coefficients', index=3,
      number=7, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=b'\020\001', file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variable_references', full_name='operations_research.ReferenceMPConstraint.variable_references', index=4,
      number=8, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=972,
  serialized_end=1161,
)


_REFERENCEMPMODEL = _descriptor.Descriptor(
  name='ReferenceMPModel',
  full_name='operations_research.ReferenceMPModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='operations_research.ReferenceMPModel.name', index=0,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=True, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='variables', full_name='operations_research.ReferenceMPModel.variables', index=1,
      number=3, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='constraints', full_name='operations_research.ReferenceMPModel.constraints', index=2,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='maximize', full_name='operations_research.ReferenceMPModel.maximize', index=3,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reference_variables', full_name='operations_research.ReferenceMPModel.reference_variables', index=4,
      number=10, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reference_constraints', full_name='operations_research.ReferenceMPModel.reference_constraints', index=5,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expressions', full_name='operations_research.ReferenceMPModel.expressions', index=6,
      number=15, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='tags', full_name='operations_research.ReferenceMPModel.tags', index=7,
      number=16, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='model_dependencies', full_name='operations_research.ReferenceMPModel.model_dependencies', index=8,
      number=17, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='build_final', full_name='operations_research.ReferenceMPModel.build_final', index=9,
      number=20, type=8, cpp_type=7, label=1,
      has_default_value=True, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1164,
  serialized_end=1613,
)


_EXTENDEDMPMODEL = _descriptor.Descriptor(
  name='ExtendedMPModel',
  full_name='operations_research.ExtendedMPModel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='concrete_model', full_name='operations_research.ExtendedMPModel.concrete_model', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reference_model', full_name='operations_research.ExtendedMPModel.reference_model', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='expression_model', full_name='operations_research.ExtendedMPModel.expression_model', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='model_type', full_name='operations_research.ExtendedMPModel.model_type',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=1616,
  serialized_end=1842,
)


_REFERENCEMPMODELREQUEST = _descriptor.Descriptor(
  name='ReferenceMPModelRequest',
  full_name='operations_research.ReferenceMPModelRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='model', full_name='operations_research.ReferenceMPModelRequest.model', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1844,
  serialized_end=1922,
)

_MPEXPRESSION.fields_by_name['variables'].message_type = _REFERENCEMPVARIABLE
_EXPRESSIONMPMODEL.fields_by_name['variable'].message_type = linear__solver__pb2._MPVARIABLEPROTO
_EXPRESSIONMPMODEL.fields_by_name['constraint'].message_type = linear__solver__pb2._MPCONSTRAINTPROTO
_EXPRESSIONMPMODEL.fields_by_name['general_constraint'].message_type = linear__solver__pb2._MPGENERALCONSTRAINTPROTO
_EXPRESSIONMPMODEL.fields_by_name['quadratic_objective'].message_type = linear__solver__pb2._MPQUADRATICOBJECTIVE
_EXPRESSIONMPMODEL.fields_by_name['solution_hint'].message_type = linear__solver__pb2._PARTIALVARIABLEASSIGNMENT
_EXPRESSIONMPMODEL.fields_by_name['expressions'].message_type = _MPEXPRESSION
_EXPRESSIONMPMODEL.fields_by_name['reference_constraints'].message_type = _REFERENCEMPCONSTRAINT
_REFERENCEMPCONSTRAINT.fields_by_name['variable_references'].message_type = _REFERENCEMPVARIABLE
_REFERENCEMPMODEL.fields_by_name['variables'].message_type = linear__solver__pb2._MPVARIABLEPROTO
_REFERENCEMPMODEL.fields_by_name['constraints'].message_type = linear__solver__pb2._MPCONSTRAINTPROTO
_REFERENCEMPMODEL.fields_by_name['reference_variables'].message_type = _REFERENCEMPVARIABLE
_REFERENCEMPMODEL.fields_by_name['reference_constraints'].message_type = _REFERENCEMPCONSTRAINT
_REFERENCEMPMODEL.fields_by_name['expressions'].message_type = _MPEXPRESSION
_EXTENDEDMPMODEL.fields_by_name['concrete_model'].message_type = linear__solver__pb2._MPMODELPROTO
_EXTENDEDMPMODEL.fields_by_name['reference_model'].message_type = _REFERENCEMPMODEL
_EXTENDEDMPMODEL.fields_by_name['expression_model'].message_type = _EXPRESSIONMPMODEL
_EXTENDEDMPMODEL.oneofs_by_name['model_type'].fields.append(
  _EXTENDEDMPMODEL.fields_by_name['concrete_model'])
_EXTENDEDMPMODEL.fields_by_name['concrete_model'].containing_oneof = _EXTENDEDMPMODEL.oneofs_by_name['model_type']
_EXTENDEDMPMODEL.oneofs_by_name['model_type'].fields.append(
  _EXTENDEDMPMODEL.fields_by_name['reference_model'])
_EXTENDEDMPMODEL.fields_by_name['reference_model'].containing_oneof = _EXTENDEDMPMODEL.oneofs_by_name['model_type']
_EXTENDEDMPMODEL.oneofs_by_name['model_type'].fields.append(
  _EXTENDEDMPMODEL.fields_by_name['expression_model'])
_EXTENDEDMPMODEL.fields_by_name['expression_model'].containing_oneof = _EXTENDEDMPMODEL.oneofs_by_name['model_type']
_REFERENCEMPMODELREQUEST.fields_by_name['model'].message_type = _EXTENDEDMPMODEL
DESCRIPTOR.message_types_by_name['ReferenceMPVariable'] = _REFERENCEMPVARIABLE
DESCRIPTOR.message_types_by_name['MPExpression'] = _MPEXPRESSION
DESCRIPTOR.message_types_by_name['ExpressionMPModel'] = _EXPRESSIONMPMODEL
DESCRIPTOR.message_types_by_name['ReferenceMPConstraint'] = _REFERENCEMPCONSTRAINT
DESCRIPTOR.message_types_by_name['ReferenceMPModel'] = _REFERENCEMPMODEL
DESCRIPTOR.message_types_by_name['ExtendedMPModel'] = _EXTENDEDMPMODEL
DESCRIPTOR.message_types_by_name['ReferenceMPModelRequest'] = _REFERENCEMPMODELREQUEST
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ReferenceMPVariable = _reflection.GeneratedProtocolMessageType('ReferenceMPVariable', (_message.Message,), {
  'DESCRIPTOR' : _REFERENCEMPVARIABLE,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.ReferenceMPVariable)
  })
_sym_db.RegisterMessage(ReferenceMPVariable)

MPExpression = _reflection.GeneratedProtocolMessageType('MPExpression', (_message.Message,), {
  'DESCRIPTOR' : _MPEXPRESSION,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.MPExpression)
  })
_sym_db.RegisterMessage(MPExpression)

ExpressionMPModel = _reflection.GeneratedProtocolMessageType('ExpressionMPModel', (_message.Message,), {
  'DESCRIPTOR' : _EXPRESSIONMPMODEL,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.ExpressionMPModel)
  })
_sym_db.RegisterMessage(ExpressionMPModel)

ReferenceMPConstraint = _reflection.GeneratedProtocolMessageType('ReferenceMPConstraint', (_message.Message,), {
  'DESCRIPTOR' : _REFERENCEMPCONSTRAINT,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.ReferenceMPConstraint)
  })
_sym_db.RegisterMessage(ReferenceMPConstraint)

ReferenceMPModel = _reflection.GeneratedProtocolMessageType('ReferenceMPModel', (_message.Message,), {
  'DESCRIPTOR' : _REFERENCEMPMODEL,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.ReferenceMPModel)
  })
_sym_db.RegisterMessage(ReferenceMPModel)

ExtendedMPModel = _reflection.GeneratedProtocolMessageType('ExtendedMPModel', (_message.Message,), {
  'DESCRIPTOR' : _EXTENDEDMPMODEL,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.ExtendedMPModel)
  })
_sym_db.RegisterMessage(ExtendedMPModel)

ReferenceMPModelRequest = _reflection.GeneratedProtocolMessageType('ReferenceMPModelRequest', (_message.Message,), {
  'DESCRIPTOR' : _REFERENCEMPMODELREQUEST,
  '__module__' : 'linear_extension_pb2'
  # @@protoc_insertion_point(class_scope:operations_research.ReferenceMPModelRequest)
  })
_sym_db.RegisterMessage(ReferenceMPModelRequest)


DESCRIPTOR._options = None
_REFERENCEMPCONSTRAINT.fields_by_name['coefficients']._options = None
# @@protoc_insertion_point(module_scope)
