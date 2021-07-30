from __future__ import annotations
from main.linprog_extensions.server.struct_utils import hierarchy
# from main.linprog_extensions.server.struct_utils import component
from os import name
from typing import List, Any, TypeVar, Callable, Type, cast, Optional
from enum import Enum
from dataclasses import dataclass, MISSING, fields

from ..mip_utils import(
    MipModel,
    MipVariablePointer,
    MipParameterPointer,
    MipExpression,
    MipConstraintPointer,
)

from ..struct_utils import(
    Container,
    Content,
    HierarchyMixin,
    SimpleBase,
    Catalogue,
) 

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
class MPArrayWithConstantConstraintExt(Content, MPArrayWithConstantConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

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
class MPArrayConstraintExt(Content, MPArrayConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        resultant_var_index = obj.resultant_var_index

        return MPArrayConstraintExt(
            var_index,
            resultant_var_index,
        )


@dataclass
class MPAbsConstraintExt(Content, MPAbsConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index 
        resultant_var_index = obj.resultant_var_index

        return MPAbsConstraintExt(
            var_index,
            resultant_var_index,
        )


@dataclass
class MPQuadraticConstraintExt(Content, MPQuadraticConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

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
class MPSosConstraintExt(Content, MPSosConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

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
class MPConstraintProtoExt(Content, MPConstraintProto):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.mipconstraint = None
        return

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
    
    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=MPConstraintProto",
            f"parent={self._parent_component.name}"
        ]
        return
    
    def configure_mipmodel(self):

        self.mipconstraint = MipConstraintPointer(
            name = self.name,
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
            coefficient=self.coefficient,
            variables = [ self._parent_component.variable[index].mipvariable for index in self.var_index]
        ) 
        ## the parent component of MPConstraint is MPmodel which has MPVariable objects, which have mipvars
        return self.mipconstraint




@dataclass
class MPIndicatorConstraintExt(Content, MPIndicatorConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        var_value = obj.var_value
        constraint =  MPConstraintProtoExt.from_proto(obj.constraint)

        return MPIndicatorConstraintExt(
            var_index,
            var_value,
            constraint,
        )


@dataclass
class MPVariableProtoExt(Content, MPVariableProto):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.mipvariable = None
        return


    @staticmethod
    def from_proto(obj:Any): 
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound
        objective_coefficient = obj.objective_coefficient
        is_integer = obj.is_integer
        name = obj.name
        branching_priority = obj.branching_priority

        return MPVariableProtoExt(
            lower_bound,
            upper_bound,
            objective_coefficient,
            is_integer,
            name,
            branching_priority,
        )

    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=MPVariableProto",
            f"parent={self._parent_component.name}",
            f"model={self._parent_component.name}"
        ]
        return
    
    def configure_mipmodel(self):

        self.mipvariable = MipVariablePointer(
            name= self.name,
            is_integer= self.is_integer,
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
            objective_coefficient=MipParameterPointer(self.objective_coefficient)
        )

        return self.mipvariable

@dataclass
class MPGeneralConstraintProtoExt(Container, MPGeneralConstraintProto):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

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
class MPQuadraticObjectiveExt(Content, MPQuadraticObjective):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return


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
class PartialVariableAssignmentExt(Content, PartialVariableAssignment):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    @staticmethod
    def from_proto(obj:Any):
        var_index = obj.var_index
        var_value = obj.var_value
        
        return PartialVariableAssignmentExt(
            var_index,
            var_value,
        )


@dataclass
class ReferenceMPVariableExt(Content, ReferenceMPVariable):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.mipvariable = None
        return

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
      
    def add_tags(self):

        if isinstance(self._parent_component, ReferenceMPModelExt):
            model_name = self._parent_component.name 
        elif isinstance(self._parent_component, MPExpressionExt):
            model_name = self._parent_component._parent_component.name
        else:
            ValueError("the type of parent compoenet is not right!")

        self._tags = [
            f"name={self.reference_name}",
            "type=ReferenceMPVariable",
            f"parent={self._parent_component.name}",
            f"model={model_name}",
        ]
        return
    

    def configure_mipmodel(self):
        ## the returned object  could be A MipVariablePointer or a MipExpression
        ## the ReferenceVar itself could point to a concrete or reference var.

        if self.model_name:
            model_name = self.model_name
        elif isinstance(self._parent_component, MPExpressionExt):
            model_name = self._parent_component._parent_component.name
        elif isinstance(self._parent_component, ReferenceMPModelExt):
            model_name = self._parent_component.name
        else:
            ValueError( "ReferenceVariable parent component is not right!")

        component =  Catalogue.find_components(
            hierarchy_name = self._hierarchy.hierarchy_name,
            tag_list=[
                f"name={self.var_name}",
                f"model={model_name}",
            ]
        )
        assert(len(component) == 1)
        if not component:
            ValueError("component for the defined reference variable cannot be found")
        
        return component[0].mipvariable


@dataclass
class MPExpressionExt(Container, MPExpression):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.mipvariable = None
        return

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
    
    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=MPExpression",
            f"parent={self._parent_component.name}",
            f"model={self._parent_component.name}",
        ]
        return
    
    def configure_mipmodel(self):

        self.mipvariable = MipExpression(
            name=self.name,
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
            objective_coefficient=MipParameterPointer(self.objective_coefficient),
            coefficients=self.variable_coefficients,
            variable_list= [
                ref_variable.configure_mipmodel() for ref_variable in self.variables
            ],
        )
        return self.mipvariable


@dataclass
class ReferenceMPConstraintExt(Container, ReferenceMPConstraint):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    
    @staticmethod
    def from_proto(obj:Any):

        # ToDo: checkout the situation with this RefConstraints and how it includes Concrete variables
        lower_bound = obj.lower_bound
        upper_bound = obj.upper_bound
        name = obj.name
        variable_coefficients = obj.variable_coefficients
        variable_references = from_list(ReferenceMPVariableExt.from_proto, obj.variable_references)
        # variable_reference_names = obj.variable_reference_names
        # variables = from_list(MPVariableProtoExt.from_proto, obj.variables)
        # variable_names = obj.variable_names
        # var_coefficients = obj.var_coefficients
        # expressions = from_list(MPExpressionExt.from_proto, obj.expressions)
        # expression_names = obj.expression_names
        # expression_coefficients = obj.expression_coefficients

        return ReferenceMPConstraintExt(
            lower_bound,
            upper_bound,
            name,
            variable_coefficients,
            variable_references,
        ) 
    
    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=ReferenceMPConstraint",
        ]
        return
    

    def configure_mipmodel(self):
        return


@dataclass
class MPModelProtoExt(Container, MPModelProto):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.mipmodel = None
        return

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

    def __bool__(self):
        return bool(
            self.variable
        )

    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=MPModelProto",
        ]
        return

    def configure_mipmodel(self):

        ## there are a bunch of variables and constraints here,
        ## we need to refer them to each,
        self.mipmodel = MipModel(
            name=self.name,
            maximize=self.maximize,
        )

        for variable in self.variable:
            self.mipmodel.add_variable(
                variable.configure_mipmodel()
            )
        
        for constraint in self.constraint:
            self.mipmodel.add_constraint(
                constraint.configure_mipmodel()
            )

        return

@dataclass
class ReferenceMPModelExt(Container, ReferenceMPModel):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.relative_referecnes = False
        self.model_dependencies_configured = list()

        return
    
    def __bool__(self):
        return bool(
            self.variables or 
            self.reference_variables
        )

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
    
    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=ReferenceMPModel",
            f"model_dependencies={str(self.model_dependencies)}",
        ]
        return
    
    def configure_mipmodel(self):

        self.mipmodel = MipModel(
            name=self.name,
            maximize=self.maximize,
        )

        for variable in self.variables:
            self.mipmodel.add_variable(
                variable.configure_mipmodel()
            )
        
        for constraint in self.constraints:
            self.mipmodel.add_constraint(
                constraint.configure_mipmodel()
            )

        for model in self.model_dependencies_configured:
            self.mipmodel.add_model(model.mipmodel)
        
        ## So the question here is that what additional aspects/changes we should
        ## consider here for the Reference model. --> it all is about References outside the model
        ## which now their mipmodel has been added.(again what did happen when we added a mipmodel to another?)
        #### I guess the mipmodel references and connections will be established.
        ## is it enough for dealing with Reference variables?
        ## I think still we would need to replace a Refvar , with the actual Variable/Exp


        ## and then there is the story of Relative references.
        ## okay so we need to decide about the Relative references here.
        ## if they do exist, there is nothing we can do about them until 
        ## all models are configured, so we would need to come back for them
        ## figuring out which Refvar does or does not use of relative references at this point
        ## is also useless, so better just skipp on all of that 

        if self.relative_referecnes:
            return


        for expression in self.expressions:
            self.mipmodel.add_expression(
                expression.configure_mipmodel()
            )
        for reference_constraint in self.reference_constraints:
            self.mipmodel.add_constraint(
                reference_constraint.configure_mipmodel()
            )

        return


@dataclass
class ExpressionMPModelExt(Container, ExpressionMPModel):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.mipmodel = None
        return
    
    def __bool__(self):
        return bool(
            self.variable
        )

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
    
    def add_tags(self):
        self._tags = [
            f"name={self.name}",
            "type=ExpressionMPModel",
        ]
        return
    
    def configure_mipmodel(self):

        self.mipmodel = MipModel(
            name=self.name,
            maximize=self.maximize,
        )

        for variable in self.variable:
            self.mipmodel.add_variable(
                variable.configure_mipmodel()
            )
        
        for constraint in self.constraint:
            self.mipmodel.add_constraint(
                constraint.configure_mipmodel()
            )

        for expression in self.expressions:
            self.mipmodel.add_expression(
                expression.configure_mipmodel()
            )
        for reference_constraint in self.reference_constraints:
            self.mipmodel.add_constraint(
                reference_constraint.configure_mipmodel()
            )

        return

@dataclass
class ExtendedMPModelExt(Container, ExtendedMPModel):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.configured = False
        return

    @staticmethod
    def from_proto(obj:Any):
        concrete_model = MPModelProtoExt.from_proto(obj.concrete_model) if obj.concrete_model.ByteSize() != 0 else MPModelProtoExt()
        reference_model = ReferenceMPModelExt.from_proto(obj.reference_model) if obj.reference_model.ByteSize() != 0 else ReferenceMPModelExt()
        expression_model = ExpressionMPModelExt.from_proto(obj.expression_model) if obj.expression_model.ByteSize() != 0 else ExpressionMPModelExt()

        return ExtendedMPModelExt(
           concrete_model,
           reference_model,
           expression_model
        )
    
    def configure_mip_independent(self):

        if self.reference_model:
            return
        
        if self.concrete_model:
            self.concrete_model.configure_mipmodel()
        
        if self.expression_model:
            self.expression_model.configure_mipmodel()
        
        self.configured = True
        return
    
    def configure_mip_dependent(self):
        
        list_model_dependencies = self.reference_model.model_dependencies
        if list_model_dependencies:
            for model_name in list_model_dependencies:
                ## find model based on the model name:
                ## 
                if not isinstance(model_name, str):
                    continue

                if model_name == 'parent':
                    self.reference_model.relative_referecnes = True
                    continue
                
                model = Catalogue.find_components(
                    hierarchy_name=self._hierarchy.hierarchy_name,
                    tags=[f"name={model_name}"],
                )

                # ToDo: Is there anyways that I won't have to use this Find function,
                #  at least not in this expensive form?
                assert(len(model)==1)

                if not(model[0]._parent_component.configured):
                    return
                
                list_model_dependencies.remove(model_name)
                self.reference_model.model_dependencies_configured.append(model[0])

        ## okay so at this point, all the model dependencies should be met:

        self.reference_model.configure_mipmodel()
        self.configured = True
        return
@dataclass
class ReferenceMPModelRequestExt(Container, ReferenceMPModelRequest):

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    @staticmethod
    def from_proto(obj:Any):
        model = ExtendedMPModelExt.from_proto(obj.model)

        return ReferenceMPModelRequestExt(
            model
        )


@dataclass
class ReferenceMPModelRequestStreem(HierarchyMixin, Container, SimpleBase):

    model_requests: List[ReferenceMPModelRequestExt]

    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.collect_tags()
        self.populate_hierarchy()
        return

    @staticmethod
    def from_proto(obj:Any):
        model_requests = from_list( ReferenceMPModelRequestExt.from_proto, obj)

        return ReferenceMPModelRequestStreem(
            model_requests
        )
    

    def configure_references(self):

        ## the goal to establish the logic for Order of Construction.
        ## There is two notes to consider 
        ## 1- all concrete models should be built before the reference Ones
            ## What if we call the build_model concurently on all list ietms?
            ## some of them will have to wait till the others are finished?
        non_configured = self.model_requests

        for model_request in self.model_requests:
            model_request.model.configure_mip_independent()
            if model_request.model.configured:
                non_configured.remove(model_request)

        
        for model_request in self.model_requests:
            model_request.model.configure_mip_dependent()
        
        index = 0
        while non_configured:
            if index >=  len(non_configured):
                index = 0
            non_configured[index].model.configure_mip_dependent()
            if model_request.model.configured:
                non_configured.remove(model_request)
            else:
                index += 1
            
        return
