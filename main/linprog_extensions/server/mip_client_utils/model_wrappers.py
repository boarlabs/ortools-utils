from operations_research import linear_solver_pb2

from mip_client_utils import MipVariableArray

import grpc
from operations_research import mip_pb2_grpc


class MipModel:
    def __init__(
        self,
    ):

        self.model_var_end_index = None

        self.varibale_pointers = dict()
        self.parameters = dict()
        self.constraint_pointers = dict()
        self.expressions = dict()
        self.mipmodels = dict()
        self.parent_mipmodel = None

    def append_variable_array(
        self,
        variable_array: MipVariableArray,
        tag=None,
    ):

        self.varibale_pointers[tag] = variable_array

        variable_array.add_mipmodel(self)

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

    def append_variable(self, variable_pointer, tag=None):
        if tag:

            self.varibale_pointers[tag] = variable_pointer

        variable_pointer.add_mipmodel(self)

    def build_variable(
        self,
        variable_pointer,
    ):
        # This method is for both Vairables and VariableArrays

        if hasattr(variable_pointer, "variable_pointer_list"):
            variable_index_list = list()

            for variable_pt in variable_pointer.variable_pointer_list:

                index = variable_pt.attach_mipmodel()
                variable_index_list.append(index)

            variable_pointer.attach_mipmodel(variable_index_list)

        else:
            variable_pointer.build_variable()
            self.model.variable.append(variable_pointer.variable)

            model_variable_end_index = len(self.model.variable) - 1

            _ = variable_pointer.attach_mipmodel(model_variable_end_index)

        return

    def update_variable(
        self,
        variable_pointer,
    ):

        self.model.variable[
            variable_pointer.mipmodel_var_index
        ].name = variable_pointer.variable.name
        self.model.variable[
            variable_pointer.mipmodel_var_index
        ].objective_coefficient = variable_pointer.variable.objective_coefficient
        self.model.variable[
            variable_pointer.mipmodel_var_index
        ].upper_bound = variable_pointer.variable.upper_bound
        self.model.variable[
            variable_pointer.mipmodel_var_index
        ].lower_bound = variable_pointer.variable.lower_bound
        self.model.variable[
            variable_pointer.mipmodel_var_index
        ].is_integer = variable_pointer.variable.is_integer
        return

    def append_parameter(self, parameter_pointer, tag=None):
        if tag:

            self.parameters[tag] = parameter_pointer

    def append_expression(self, expression, tag=None):
        if tag:
            self.expressions[tag] = expression

        expression.add_mipmodel(self)

        # okay so what needs to happen when an expression is attached to the mipmodel?
        # if the expression has lb/ub that will mean adding the constraints, but without it just setting the variables.
        #  setting the variables will be with attaching them with the mipmodel (if not already attahced)

    def build_expression(self, expression):
        expression.attach_mipmodel()
        return

    def append_expression_array(self, expression_array, tag=None):

        if tag:
            self.expressions[tag] = expression_array

        expression_array.add_mipmodel(self)
        return

    # def build_expression_array(self, expression_array):
    #     expression_array.attach_mipmodel()
    #     return

    def append_constraint(self, constraint_pointer, tag=None):
        if tag:

            self.constraint_pointers[tag] = constraint_pointer

        return

    def build_constraint(self, constraint_pointer):

        # the input can be a constraint pointer or a constraintPinterArray
        constraint_pointer.build_constraint()
        return

    def append_constraint_array(
        self,
        constraint_pointer_array,
        tag=None,
    ):

        if tag:
            self.constraint_pointers[tag] = constraint_pointer_array

        # constraint_pointer_array.set_coefficients()
        return

    def append_model(self, mipmodel, tag=None):

        # self.model.variable.extend(mipmodel.model.variable)
        # mipmodel.model_var_end_index = len(self.model.variable)

        # self.model.constraint.extend(mipmodel.model.constraint)

        self.mipmodels[tag] = mipmodel

        mipmodel.parent_mipmodel = self

        # Q: should we add variables of the child mipmodel to the parent directly or keep them under their own mipmodel?
        # self.varibale_pointers = dict()
        # self.paramter_pointers = dict()
        # self.constraint_pointers = dict()
        # self.expressions = dict()
        for key in mipmodel.varibale_pointers:
            mipmodel.varibale_pointers[key].add_mipmodel(self)

        # for key in mipmodel.parameters:
        #     mipmodel.parameters[key].add_mipmodel(self)

        for key in mipmodel.constraint_pointers:
            mipmodel.constraint_pointers[key].add_mipmodel(self)

        for key in mipmodel.expressions:
            mipmodel.expressions[key].add_mipmodel(self)

    def build_model(self):

        self.model_request = linear_solver_pb2.MPModelRequest()
        self.model = self.model_request.model

        for key in self.mipmodels:
            self.mipmodels[key].build_model()

        for key in self.varibale_pointers:
            self.build_variable(self.varibale_pointers[key])

        for key in self.constraint_pointers:
            self.build_constraint(self.constraint_pointers[key])

        for key in self.expressions:
            self.build_expression(self.expressions[key])

    def solve_model(
        self,
        maximize: bool = True,
        solver_type: str = None,
        target: str = "0.0.0.0:5050",
    ):

        if solver_type == "GLOP_LINEAR_PROGRAMMING":
            solver = linear_solver_pb2.MPModelRequest.SolverType.GLOP_LINEAR_PROGRAMMING

        self.model.maximize = maximize

        self.model_request.solver_type = solver

        options = [('grpc.max_receive_message_length', 1000 * 1024 * 1024)]

        with grpc.insecure_channel(target, options = options) as channel:
	        
            stub = mip_pb2_grpc.MPServiceStub(channel)
            self.model_solution = stub.MPModel(self.model_request)

        ck = 1
