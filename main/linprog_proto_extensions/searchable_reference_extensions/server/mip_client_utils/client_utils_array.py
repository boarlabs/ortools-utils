import grpc
from operations_research import mip_pb2
from operations_research import mip_pb2_grpc
from operations_research import linear_solver_pb2


class VariableArray:
    model_last_index = 0

    def __new__(cls, ort_model, index, *args, **kwargs):

        model_last_index = cls.model_last_index

        variable_array = super().__new__(cls)

        variable_array.model_var_index = model_last_index

        cls.model_last_index = model_last_index + len(index)

        return variable_array

    def __init__(
        self,
        ort_model,
        index: list,
        domain: str,
        lower_bound: list = None,
        upper_bound: list = None,
    ):
        self.ort_model = ort_model
        self.index = index
        # self.model_index= model_last_index +1

        for i in range(len(index)):

            variable = self.ort_model.variable.add()
            variable.name = index[i]
            # variable.objective_coefficient = objective_coefficients[i]

            if lower_bound:
                variable.lower_bound = lower_bound[i]

            if upper_bound:
                variable.upper_bound = upper_bound[i]

            if not domain == "Integer":
                variable.is_integer = False
            else:
                variable.is_integer = True

        ck = 1

    def add_objective_coefficients(self, coefficients: list):

        for i in range(len(self.index)):
            variable = self.ort_model.variable[self.model_var_index + i]
            variable.objective_coefficient = coefficients[i]
            ck = 1


class ConstraintArray:
    def __init__(
        self,
        ort_model,
        constraint_variables_list: list,
        constraint_variable_coefficients_list: list,
        constraint_lower_bounds_list: list = None,
        constraint_upper_bounds_list: list = None,
        constraint_index_list: list = None,
    ):

        self.ort_model = ort_model

        if constraint_index_list:
            num_cons = len(constraint_index_list)
        else:
            num_cons = len(constraint_variable_coefficients_list[0])

        for constraint_index in range(num_cons):

            constraint = self.ort_model.constraint.add()

            if constraint_index_list:
                constraint.name = constraint_index_list[constraint_index]
            if constraint_lower_bounds_list:
                constraint.lower_bound = constraint_lower_bounds_list[constraint_index]

            if constraint_upper_bounds_list:
                constraint.upper_bound = constraint_upper_bounds_list[constraint_index]

            # dealing with the constraint coefficient
            for constraint_variable_index in range(len(constraint_variables_list)):

                for variable_index in range(
                    len(constraint_variables_list[constraint_variable_index].index)
                ):

                    constraint.coefficient.append(
                        constraint_variable_coefficients_list[
                            constraint_variable_index
                        ][constraint_index][variable_index]
                    )

                    constraint.var_index.append(
                        constraint_variables_list[
                            constraint_variable_index
                        ].model_var_index
                        + variable_index
                    )


class ExpressionArray(VariableArray):
    def __init__(
        self,
        ort_model,
        index,
        expression_variable_list,
        variable_coefficient_list,
    ):

        super().__init__(ort_model=ort_model, index=index, domain="REAL")

        constaint = ConstraintArray(
            ort_model=ort_model,
            constraint_variables_list=[self] + expression_variable_list,
            constraint_variable_coefficients_list=[[[-1] * len(index)]]
            + variable_coefficient_list,
            constraint_lower_bounds_list=[0] * len(index),
            constraint_upper_bounds_list=[0] * len(index),
        )
