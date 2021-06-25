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
    ReferenceMPConstraint,
    MPExpression,
    ReferenceMPVariable,
    PartialVariableAssignment,
    MPQuadraticObjective,
    MPGeneralConstraintProto,
    MPConstraintProto,
) 


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]





@dataclass
class MPArrayWithConstantConstraintExt(MPArrayWithConstantConstraint):

    @staticmethod
    def from_proto(obj:Any):
        pass

@dataclass
class MPArrayConstraintExt(MPArrayConstraint):

    @staticmethod
    def from_proto(obj:Any):
        pass

@dataclass
class MPAbsConstraintExt(MPAbsConstraint):

    @staticmethod
    def from_proto(obj:Any):
        pass


@dataclass
class MPQuadraticConstraintExt(MPQuadraticConstraint):

    @staticmethod
    def from_proto(obj:Any):
        pass

@dataclass
class MPSosConstraintExt(MPSosConstraint):

    @staticmethod
    def from_proto(obj:Any):
        pass


@dataclass
class MPIndicatorConstraintExt(MPIndicatorConstraint):

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
        var_index = obj.var_index
        coefficient = obj.coefficient
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound
        name = obj.name
        is_lazy = obj.is_lazy

        return MPConstraintProtoExt(
            var_index,
            coefficient,
            lower_bound,
            upper_bound,
            name,
            is_lazy,
        )


@dataclass
class MPGeneralConstraintProtoExt(MPGeneralConstraintProto):

    @staticmethod
    def from_proto(obj:Any):
        name = obj.name
        indicator_constraint = MPIndicatorConstraintExt.from_proto(obj.indicator_constraint)        
        sos_constraint = MPSosConstraintExt.from_proto(obj.sos_constraint)
        quadratic_constraint = MPQuadraticConstraintExt.from_proto(obj.quadratic_constraint)
        abs_constraint = MPAbsConstraintExt.from_proto(obj.abs_constraint)
        and_constraint = MPArrayConstraintExt.from_proto(obj.and_constraint)
        or_constraint =  MPArrayConstraintExt.fromm_proto(obj.or_constraint)
        min_constraint = MPArrayWithConstantConstraintExt.from_proto(obj.min_constraint)
        max_constraint = MPArrayWithConstantConstraintExt.from_proto(obj.max_constraint)

        return MPGeneralConstraintProtoExt(
            name,
            indicator_constraint,
            sos_constraint,
            quadratic_constraint,
            abs_constraint,
            and_constraint,
            or_constraint,
            min_constraint,
            max_constraint,
        )
       

@dataclass
class MPQuadraticObjectiveExt(MPQuadraticObjective):

    @staticmethod
    def from_proto(obj:Any):
        qvar1_index = obj.qvar1_index 
        qvar2_index = obj.qvar2_index
        coefficient = obj.coefficient

        return MPQuadraticObjectiveExt(
            qvar1_index,
            qvar2_index,
            coefficient,
        )


@dataclass
class PartialVariableAssignmentExt(PartialVariableAssignment):

    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        var_value = obj.var_value
        
        return PartialVariableAssignmentExt(
            var_index,
            var_value,
        )


@dataclass
class ReferenceMPVariableExt(ReferenceMPVariable):

    @staticmethod
    def from_proto(obj:Any):
        
        var_name = obj.var_name
        model_name = obj.model_name
        var_index  = obj.var_index
        reference_name = obj.reference_name
        tags = obj.tags

        return ReferenceMPVariableExt(
            var_name,
            model_name,
            var_index,
            reference_name,
            tags,
        )


@dataclass
class MPExpressionExt(MPExpression):

    @staticmethod
    def from_proto(obj:Any):
        name = obj.name
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound 
        objective_coefficient = obj.objective_coefficient
        variables = from_list(ReferenceMPVariableExt.from_proto, obj.variables) 
        variables_names = obj.variables_names
        variable_coefficients = obj.variable_coefficients
        tags = obj.tags
        
        return MPExpressionExt(
            name,
            lower_bound,
            upper_bound,
            objective_coefficient,
            variables,
            variables_names,
            variable_coefficients,
            tags,
        )

@dataclass
class ReferenceMPConstraintExt(ReferenceMPConstraint):

    @staticmethod
    def from_proto(obj:Any):
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound
        name = obj.name
        ref_var_coefficients = obj.ref_var_coefficients
        variable_references = from_list(ReferenceMPVariableExt.from_proto, obj.variable_references)
        variable_reference_names = obj.variable_reference_names
        variables = from_list(MPVariableProtoExt.from_proto, obj.variables)
        variable_names = obj.variable_names
        var_coefficients = obj.var_coefficients
        expressions = from_list(MPExpressionExt.from_proto, obj.expressions)
        expression_names = obj.expression_names
        expression_coefficients = obj.expression_coefficients

        return ReferenceMPConstraintExt(
            lower_bound,
            upper_bound,
            name,
            ref_var_coefficients,
            variable_references,
            variable_reference_names,
            variables,
            variable_names,
            var_coefficients,
            expressions,
            expression_names,
            expression_coefficients,
        ) 


@dataclass
class MPModelProtoExt(MPModelProto):

    @staticmethod
    def from_proto(obj:Any):
        variable = from_list(MPVariableProtoExt.from_proto, obj.variable) 
        constraint = from_list(MPConstraintProtoExt.from_proto, obj.constraint)
        general_constraint = from_list(MPGeneralConstraintProtoExt.from_proto, obj.general_constraint)
        maximize = obj.maximize
        objective_offset = obj.objective_offset
        quadratic_objective = MPQuadraticObjectiveExt.from_proto(obj.quadratic_objective)
        name = obj.name
        solution_hint = PartialVariableAssignmentExt.from_proto(obj.solution_hint)

        return  MPModelProtoExt(
            variable,
            constraint,
            general_constraint,
            maximize,
            objective_offset,
            quadratic_objective,
            name,
            solution_hint,
        )

@dataclass
class ReferenceMPModelExt(ReferenceMPModel):

    @staticmethod
    def from_proto(obj:Any):
        name = obj.name
        variables = from_list(MPVariableProtoExt.from_proto, obj.variables)  
        constraints =  from_list(MPConstraintProtoExt.from_proto, obj.constraints)
        maximize = obj.maximize
        reference_variables = from_list(ReferenceMPVariableExt.from_proto, obj.reference_variables) 
        reference_constraints = from_list(ReferenceMPConstraintExt.from_proto, obj.reference_constraints)
        expressions = from_list(MPExpressionExt.from_proto, obj.expressions)
        tags = obj.tags
        model_dependencies = obj.model_dependencies
        build_final = obj.build_final

        return ReferenceMPModelExt(
            name,
            variables,
            constraints,
            maximize,
            reference_variables,
            reference_constraints,
            expressions,
            tags,
            model_dependencies,
            build_final,
        )

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



