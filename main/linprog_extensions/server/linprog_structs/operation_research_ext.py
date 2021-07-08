from __future__ import annotations
from typing import List, Any, TypeVar, Callable, Type, cast, Optional
from enum import Enum
from dataclasses import dataclass
from ..struct_utils import Container, Content, HierarchyMixin

from .operations_research import(
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
    MPVariableProto,
    MPIndicatorConstraint,
    MPSosConstraint,
    MPQuadraticConstraint,
    MPAbsConstraint,
    MPArrayConstraint,
    MPArrayWithConstantConstraint
) 


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    # assert isinstance(x, list)
    return [f(y) for y in x]





@dataclass
class MPArrayWithConstantConstraintExt(MPArrayWithConstantConstraint, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        constant = obj.constant
        resultant_var_index = obj.resultant_var_index

        return MPArrayWithConstantConstraintExt(
            var_index,
            constant,
            resultant_var_index,
        )

@dataclass
class MPArrayConstraintExt(MPArrayConstraint, Container):


    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        resultant_var_index = obj.resultant_var_index

        return MPArrayConstraintExt(
            var_index,
            resultant_var_index,
        )

@dataclass
class MPAbsConstraintExt(MPAbsConstraint, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index 
        resultant_var_index = obj.resultant_var_index

        return MPAbsConstraintExt(
            var_index,
            resultant_var_index,
        )


@dataclass
class MPQuadraticConstraintExt(MPQuadraticConstraint, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        #  List[int] = betterproto.int32_field(1)
        coefficient = obj.coefficient
        qvar1_index = obj.qvar1_index
        qvar2_index = obj.qvar2_index
        qcoefficient = obj.qcoefficient
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound

        return MPQuadraticConstraintExt(
            var_index,
            coefficient,
            qvar1_index,
            qvar2_index,
            qcoefficient,
            lower_bound,
            upper_bound,
        )


@dataclass
class MPSosConstraintExt(MPSosConstraint, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        
        type = obj.type
        # : "MPSosConstraintType" = betterproto.enum_field(1)
        var_index = obj.var_index
        #  List[int] = betterproto.int32_field(2)
        weight = obj.weight

        return MPSosConstraintExt(
            type,
            var_index,
            weight,
        )
        

@dataclass
class MPConstraintProtoExt(MPConstraintProto, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class MPIndicatorConstraintExt(MPIndicatorConstraint, Container):


    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        var_value = obj.var_value
        constraint =  MPConstraintProtoExt.from_proto(obj.constraint)


@dataclass
class MPVariableProtoExt(MPVariableProto, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound
        objective_coefficient = obj.objective_coefficient
        is_integer = obj.is_integer
        name = obj.name

        print(type(obj.name))
        branching_priority = obj.branching_priority

        return MPVariableProtoExt(
            lower_bound,
            upper_bound,
            objective_coefficient,
            is_integer,
            name,
            branching_priority,
        )

@dataclass
class MPGeneralConstraintProtoExt(MPGeneralConstraintProto, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class MPQuadraticObjectiveExt(MPQuadraticObjective, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class PartialVariableAssignmentExt(PartialVariableAssignment, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        var_value = obj.var_value
        
        return PartialVariableAssignmentExt(
            var_index,
            var_value,
        )


@dataclass
class ReferenceMPVariableExt(ReferenceMPVariable, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class MPExpressionExt(MPExpression, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class ReferenceMPConstraintExt(ReferenceMPConstraint, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class MPModelProtoExt(MPModelProto, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class ReferenceMPModelExt(ReferenceMPModel, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class ExpressionMPModelExt(ExpressionMPModel, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()


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
class ExtendedMPModelExt(ExtendedMPModel, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()

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
class ReferenceMPModelRequestExt(ReferenceMPModelRequest, Container):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()

    @staticmethod
    def from_proto(obj:Any):
        model = ExtendedMPModelExt.from_proto(obj.model)

        return ReferenceMPModelRequestExt(
            model
        )



@dataclass
class ReferenceMPModelRequestStreem(HierarchyMixin, Container):

    model_requests: List[ReferenceMPModel]

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.populate_hierarchy()

    @staticmethod
    def from_proto(obj:Any):
        model_requests = from_list( ReferenceMPModelRequestExt.from_proto, obj)

        return ReferenceMPModelRequestStreem(
            model_requests
        )