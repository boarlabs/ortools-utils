from __future__ import annotations
from typing import List, Any, TypeVar, Callable, Type, cast, Optional
from enum import Enum
from dataclasses import dataclass

from operations_research import(
    ReferenceMPModelRequest,
    ExtendedMPModel,
    MPModelProto,
    ReferenceMPModel,
    ExpressionMPModel,
) 


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


@dataclass
class MPModelProtoExt(MPModelProto):

    @staticmethod
    def from_proto(obj:Any):
        pass


@dataclass
class ReferenceMPModelExt(ReferenceMPModel):

    @staticmethod
    def from_proto(obj:Any):
        pass




@dataclass
class MPVariableProtoExt(MPVariableProto):

    @staticmethod
    def from_proto(obj:Any):
        pass



@dataclass
class MPConstraintProtoExt(MPConstraintProto):

    @staticmethod
    def from_proto(obj:Any):
        pass


@dataclass
class MPGeneralConstraintProtoExt(MPGeneralConstraintProto):

    @staticmethod
    def from_proto(obj:Any):
        pass



@dataclass
class MPQuadraticObjectiveExt(MPQuadraticObjective):

    @staticmethod
    def from_proto(obj:Any):
        pass



@dataclass
class PartialVariableAssignmentExt(PartialVariableAssignment):

    @staticmethod
    def from_proto(obj:Any):
        pass


@dataclass
class MPExpressionExt(MPExpression):

    @staticmethod
    def from_proto(obj:Any):
        pass 


@dataclass
class ReferenceMPConstraintExt(ReferenceMPConstraint):

    @staticmethod
    def from_proto(obj:Any):
        pass 


@dataclass
class ExpressionMPModelExt(ExpressionMPModel):

    @staticmethod
    def from_proto(obj:Any):
        variable = from_list(MPVariableProtoExt.from_proto, obj.variable)
        constraint = from_list(MPConstraintProtoExt.from_proto, obj.constraint)
        general_constraint = from_list(MPGeneralConstraintProtoExt.from_prto, obj.general_constraint)
        maximize = obj.maximize
        objective_offset = obj.objective_offset 
        quadratic_objective = MPQuadraticObjectiveExt.from_proto(obj.quadratic_objective)
        name = obj.name
        solution_hint = PartialVariableAssignmentExt.from_proto(obj.solution_hint)
        expressions = from_list(MPExpressionExt.from_proto, obj.expressions)
        reference_constraints = from_list(ReferenceMPConstraintExt.from_proto, obj.reference_constraints)
        
        return ExpressionMPModelExt(
            variable,
            constraint,
            general_constraint,
            maximize,
            objective_offset,
            quadratic_objective,
            name,
            solution_hint,
            expressions,
            reference_constraints,
        )


@dataclass
class ExtendedMPModelExt(ExtendedMPModel):

    @staticmethod
    def from_proto(obj:Any):
        concrete_model = MPModelProtoExt.from_proto(obj.concrete_model)
        reference_model = ReferenceMPModelExt.from_proto(obj.reference_model)
        expression_model = ExpressionMPModelExt.from_proto(obj.expression_model)

        return ExtendedMPModelExt(
            concrete_model,
            reference_model,
            expression_model
        )


@dataclass
class ReferenceMPModelRequestExt(ReferenceMPModelRequest):

    @staticmethod
    def from_proto(obj:Any):
        model = ExtendedMPModelExt.from_proto(obj.model)

        return ReferenceMPModelRequestExt(
            model
        )



