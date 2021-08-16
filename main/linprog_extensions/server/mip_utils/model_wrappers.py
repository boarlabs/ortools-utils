from __future__ import annotations
from typing import List, Any, TypeVar, Callable, Type, cast, Optional

from operations_research.linear_solver_pb2 import(
    MPModelProto,
    MPSolutionResponse,
)

from operations_research.linear_extension_pb2 import(
    NamedValue,
)

from . import MipVariableArray

# import grpc
# from operations_research import mip_pb2_grpc


class MipModel:
    
    def __init__(
        self,
        name: Optional[str] = '',
        maximize: Optional[bool]= False,
    ): 
        self.name = name
        self.maximize= maximize
        # maybe later I can edit the init so that one could instantiate with vairables, etc., provided.
        self.varibale_pointers = list()
        self.parameters = list()
        self.constraint_pointers = list()
        self.expressions = list()
        self.mipmodels = list()

        self.parent_mipmodel = None
        self.model = MPModelProto()
        self.solution_response_vars = list()
        self.solution_response_exprs = list()
        # self.model_var_end_index = None
        # why we needed this? seems related to adding one mipmodel to another?
        return

    def add_parameter(
        self,
        parameter,
    ):     
        parameter.mipmodel = self
        self.parameters.append(parameter)
        return

    def add_variable(
        self,
        variable_pointer,
    ):
        variable_pointer.mipmodel = self
        self.varibale_pointers.append(variable_pointer)
        return

    def add_expression(
        self,
        expression,
    ):
        expression.mipmodel = self
        self.expressions.append(expression)
        # okay so what needs to happen when an expression is added to the mipmodel?
        # if the expression has lb/ub that will mean adding the constraints, but without it just setting the variables.
        #  setting the variables will be with attaching them with the mipmodel (if not already attahced)
        return

    def add_constraint(
        self,
        constraint_pointer,
    ):
        self.constraint_pointers.append(constraint_pointer)
        ## so here we just adding the tag, nothing more is needed??
        return

    def add_model(
        self,
        mipmodel,
    ):
        self.mipmodels.append(mipmodel)
        mipmodel.parent_mipmodel = self

        for variable in mipmodel.varibale_pointers:
            self.add_variable(variable)

        for parameter in mipmodel.parameters:
            self.add_parameter(parameter)

        for constraint in mipmodel.constraint_pointers:
            self.add_constraint(constraint)

        for expression in mipmodel.expressions:
            self.add_expression(expression)
        return

    def update_model(self,mipmodel):
        for variable in mipmodel.varibale_pointers:
            if not(variable in self.varibale_pointers):
                self.add_variable(variable)
            
        for parameter in mipmodel.parameters:
            if not (parameter in self.parameters):
                self.add_parameter(parameter)

        for constraint in mipmodel.constraint_pointers:
            if not (constraint in self.constraint_pointers):
                self.add_constraint(constraint)

        for expression in mipmodel.expressions:
            if not (expression in self.expressions):
                self.add_expression(expression)
        return

    def build_variable(
        self,
        variable_pointer,
    ):
        """
            This method is for both Vairables and VariableArrays
        """

        if hasattr(variable_pointer, "variable_pointer_list"):
            variable_index_list = list()
            for variable_pt in variable_pointer.variable_pointer_list:
                index = variable_pt.attach_mipmodel()
                variable_index_list.append(index)

            variable_pointer.attach_mipmodel(variable_index_list)
        else:
            variable_pointer.make_variable_proto()
            self.model.variable.append(variable_pointer.variable)
            model_variable_end_index = len(self.model.variable) - 1
            _ = variable_pointer.attach_mipmodel(model_variable_end_index)
        return

    def build(self):

        for variable in self.varibale_pointers:
            variable.build()
            # self.build_variable(variable)
        for constraint in self.constraint_pointers:
            constraint.build()
        for expression in self.expressions:
            expression.build()
        return


    def assemble_response(self):
        for variable in self.varibale_pointers:
            self.solution_response_vars.append( 
                NamedValue(
                    name = variable.name,
                    value = variable.return_response(),
                )
            )

        for expression in self.expressions:
            self.solution_response_exprs.append(
                NamedValue(
                    name = expression.name,
                    value = expression.return_response(),
                )
            )
        return

## so I want to create the LISTS of variables and Expressions for the MIPMODELS here


        
    # def update_variable(
    #     self,
    #     variable_pointer,
    # ):

    #     self.model.variable[
    #         variable_pointer.mipmodel_var_index
    #     ].name = variable_pointer.variable.name
    #     self.model.variable[
    #         variable_pointer.mipmodel_var_index
    #     ].objective_coefficient = variable_pointer.variable.objective_coefficient
    #     self.model.variable[
    #         variable_pointer.mipmodel_var_index
    #     ].upper_bound = variable_pointer.variable.upper_bound
    #     self.model.variable[
    #         variable_pointer.mipmodel_var_index
    #     ].lower_bound = variable_pointer.variable.lower_bound
    #     self.model.variable[
    #         variable_pointer.mipmodel_var_index
    #     ].is_integer = variable_pointer.variable.is_integer
    #     return

    # def append_variable_array(
    #     self,
    #     variable_array: MipVariableArray,
    #     tag=None,
    # ):

    #     self.varibale_pointers[tag] = variable_array
    #     variable_array.add_mipmodel(self)
        
    # def append_constraint_array(
    #     self,
    #     constraint_pointer_array,
    #     tag=None,
    # ):

    #     if tag:
    #         self.constraint_pointers[tag] = constraint_pointer_array

    #     # constraint_pointer_array.set_coefficients()
    #     return

    # def append_expression_array(self, expression_array, tag=None):

    #     if tag:
    #         self.expressions[tag] = expression_array

    #     expression_array.add_mipmodel(self)
    #     return

    # def build_expression_array(self, expression_array):
    #     expression_array.attach_mipmodel()
    #     return

    # def build_variable_array(
    #     self,
    #     variable_array: MipVariableArray,
    # ):
    #     variable_index_list = list()
    #     for variable_pointer in variable_array.variable_pointer_list:

    #         index = variable_pointer.attach_mipmodel(self)
    #         variable_index_list.append(index)
    #     # self.model.variable.extend(variable_array.variable_list)

    #     # model_variables_end_index = len(self.model.variable)

    #     variable_array.add_mipmodel(self, variable_index_list)


    # def solve_model(
    #     self,
    #     maximize: bool = True,
    #     solver_type: str = None,
    #     target: str = "0.0.0.0:5050",
    # ):

    #     if solver_type == "GLOP_LINEAR_PROGRAMMING":
    #         solver = linear_solver_pb2.MPModelRequest.SolverType.GLOP_LINEAR_PROGRAMMING

    #     self.model.maximize = maximize

    #     self.model_request.solver_type = solver

    #     options = [('grpc.max_receive_message_length', 1000 * 1024 * 1024)]

    #     with grpc.insecure_channel(target, options = options) as channel:
	        
    #         stub = mip_pb2_grpc.MPServiceStub(channel)
    #         self.model_solution = stub.MPModel(self.model_request)

    #     ck = 1
