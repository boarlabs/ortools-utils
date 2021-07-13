from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

from operations_research import linear_solver_pb2

from . import MipModel

from . import MipVariablePointer, MipVariableArray


class MipConstraintPointer:
    def __init__(
        self,
        var_index: Optional[List[int]] = None,
        variables: Optional[List[MipVariablePointer]] = None,
        coefficient: Optional[List[float]] = None,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
        name: Optional[str] = None,
        is_lazy: Optional[bool] = None,
        mipmodel: Optional[MipModel] = None,
    ):

        self.var_index = var_index
        self.variables = variables
        self.coefficient = coefficient
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.name = name
        self.is_lazy = is_lazy

        self.mipconstraint = None

        self.mipmodel = None

        if mipmodel:
            self.add_mipmodel(mipmodel)

    def build_constraint(self):

        if self.variables:
            self.var_index = self._get_variables_index()

        lower_bound, upper_bound = self.update_rhs_for_expressions()

        assert self.var_index != None

        self.mipconstraint = linear_solver_pb2.MPConstraintProto(
            var_index=self.var_index,
            coefficient=self.coefficient,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            name=str(self.name),
            is_lazy=self.is_lazy,
        )

        self._add_constraint_to_mipmodel()
        return

    def update_rhs_for_expressions(self):
        lower_bound = self.lower_bound
        upper_bound = self.upper_bound

        for term in self.variables:

            if hasattr(term, "variable_list"):

                lower_bound, upper_bound = term.adjust_right_handside_for_paramters(
                    lower_bound,
                    upper_bound,
                )

        return lower_bound, upper_bound

    def get_constraint(self):
        if not self.mipconstraint:
            self.build_constraint()
        return self.mipconstraint

    def _get_variables_index(self):
        """
        A constraint includes coefficients and indices of variables (that are tied to a model).
        A constraint-pointer however, includes variables (or variable pointers) that are not tied to any model, and we could initialize
        a constraint-pointer that is not tied to any model.
        In order to generate a constraint that is tied to a model, we need to define a model for the constraint.
        We can add a MipModel to a constraint-pointer manually or as part of getting the indicies of the variables.

        """
        var_index_list = list()

        if not self.mipmodel:
            mipmodel_list = [
                variable.mipmodel
                for variable in self.variables
                if isinstance(variable, MipVariablePointer)
            ]
            mipmodel = next(item for item in mipmodel_list if item is not None)
            assert mipmodel != None
            self.add_mipmodel(mipmodel)

        for variable in self.variables:
            if isinstance(variable, MipVariablePointer):

                if not variable.mipmodel_attached:
                    var_index = variable.attach_mipmodel(self.mipmodel)
                    var_index_list.append(var_index)
                elif (variable.mipmodel_attached) and (
                    variable.mipmodel != self.mipmodel
                ):

                    ValueError(
                        "The variable pointer MipModel is not the same as the constraint MipModel"
                    )
                    # ToDo should make this a warning and change the mipmodel of the variable.
                    # Can  a variable pointer have multiple mipmodels?
                else:  # i.e. if the variable.mipmodel exist and it is the same as the constraint mipmodel
                    var_index = variable.mipmodel_var_index
                    var_index_list.append(var_index)

            elif hasattr(variable, "variable_list"):  # i.e. if it is an expresssion

                if not variable.mipmodel_attached:
                    variable.attach_mipmodel()

                var_index = [
                    variable_pointer.mipmodel_var_index
                    for variable_pointer in variable.list_variable_coefficients()[0]
                ]
                var_index_list += var_index

            else:  # i.e. if the variable is variableproto
                var_index = self.mipmodel.append_variable(variable)
                var_index_list.append(var_index)

        return var_index_list

    def add_mipmodel(self, mipmodel: MipModel):
        self.mipmodel = mipmodel

    def _add_constraint_to_mipmodel(self):

        self.mipmodel.model.constraint.append(self.mipconstraint)


class MipConstraintArrayVariable:

    """
    A MipConstraintPointerArrayVariable is a single constraint defined over  a list of MipVariableArray.
    The key goal here is to ease the defenition of constraints.


    """

    def __init__(
        self,
        variables_list: List[MipVariableArray],
        variables_coefficients_list: Optional[List[list]] = None,
        mipmodel: Optional[MipModel] = None,
        constraint_lower_bound: Optional[float] = None,
        constraint_upper_bound: Optional[float] = None,
        index_name: Optional[str] = None,
    ):

        # self.mip_constraint_pointer = None
        # self.variable_arrays = variables_list
        # self.variables_coefficients_list = variables_coefficients_list
        # self.constraint_lower_bound = constraint_lower_bound
        # self.constraint_upper_bound = constraint_upper_bound
        # self.index_name = index_name

        self.mip_constraint_pointer = MipConstraintPointer(
            variables=[
                variable_pointer
                for variable_array in variables_list
                for variable_pointer in variable_array.variable_pointer_list
            ],
            coefficient=[
                item for sublist in variables_coefficients_list for item in sublist
            ],
            lower_bound=constraint_lower_bound,
            upper_bound=constraint_upper_bound,
            name=index_name,
            is_lazy=False,
        )

        ck = 1

    def build_constraint(
        self,
        variables_coefficients_list=None,
    ):
        # toDO need to update both this and that of the mipconstraint so that similar to the variables we can update and set paramters simultaniouslt
        self.mip_constraint_pointer.build_constraint()

        # okay so before we wanted to have a constraint that is attached to a model but now we define a pointer
        # mipmodel= self._assert_variables_attached_to_mipmodel(mipmodel =mipmodel, array_variable_list=variables_list )

    def add_mipmodel(self, mipmodel):

        self.mip_constraint_pointer.add_mipmodel(mipmodel)
        return

    def _assert_variables_attached_to_mipmodel(self, mipmodel, array_variable_list):

        if not mipmodel:
            mipmodel = array_variable_list[0].mipmodel

        for variable_array in array_variable_list:
            if variable_array.mipmodel != mipmodel:
                mipmodel.append_variable_array(variable_array)
                # varriable_array.mipmodel=mipmodel
        for variable_array in array_variable_list:
            assert variable_array.mipmodel == mipmodel

        ck = 1

        return mipmodel


class MipConstraintArray:
    def __init__(
        self,
        mip_constraint_list: Optional[List[MipConstraintArrayVariable]] = None,
        variables_list: Optional[List[MipVariableArray]] = None,
        variables_coefficients_list: Optional[List[List[list]]] = None,
        mipmodel: Optional[MipModel] = None,
        constraint_lower_bounds: Optional[List[float]] = None,
        constraint_upper_bounds: Optional[List[float]] = None,
        index_names: Optional[List[str]] = None,
    ):

        # here for now we construct the Constraint_array only from the single constraint. I leave the construct from the paramters direcly to later

        self.mip_constraintpointer_list = mip_constraint_list

        self.index_names = index_names

    def build_constraint(self):

        for constraint_pointer in self.mip_constraintpointer_list:
            constraint_pointer.build_constraint()

        return

    def add_mipmodel(self, mipmodel):

        self.mipmodel = mipmodel

        for constraint_pointer in self.mip_constraintpointer_list:
            constraint_pointer.add_mipmodel(mipmodel)

        return
