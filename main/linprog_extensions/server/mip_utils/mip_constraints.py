from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional

from operations_research import linear_solver_pb2

from . import MipModel

from . import MipVariablePointer, MipVariableArray


class MipConstraintPointer:

    def __init__(
        self,
        variables: Optional[List[MipVariablePointer]] = list(),
        coefficient: Optional[List[float]] = list(),
        lower_bound: Optional[float] = float('-inf'),
        upper_bound: Optional[float] = float('inf'),
        name: Optional[str] = str(),
        is_lazy: Optional[bool] = False,
    ):

        self.variables = variables
        self.coefficient = coefficient
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.name = name
        self.is_lazy = is_lazy

        self.var_index = list()
        self.mipconstraint = None
        self._mipmodel = None
        return

    @property
    def mipmodel(self):
        return self._mipmodel

    @mipmodel.setter
    def mipmodel(self, mipmodel):
        self._mipmodel = mipmodel

    def build(self):

        self.var_index = self._get_variables_index()
        lower_bound, upper_bound = self.update_rhs_for_expressions()
        
        self.mipconstraint = linear_solver_pb2.MPConstraintProto(
            var_index=self.var_index,
            coefficient=self.coefficient,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            name=str(self.name),
            is_lazy=self.is_lazy,
        )

        self._mipmodel.model.constraint.append(self.mipconstraint)
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

    # def get_constraint(self):
    #     if not self.mipconstraint:
    #         self.build()
    #     return self.mipconstraint

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

        if not self.variables:
            ValueError("The constraint does not have any variables")

        for variable in self.variables:
            if isinstance(variable, MipVariablePointer):
                if not (variable.mipmodel == self.mipmodel):
                    ValueError(
                        "The variable pointer MipModel is not the same as the constraint MipModel"
                    )
                elif not variable.mipmodel_attached:
                    variable.build()
                
                var_index_list.append(variable.mipmodel_var_index)
                    
            elif hasattr(variable, "variable_list"):  # i.e. if it is an expresssion
                if not variable.mipmodel_attached:
                    variable.build()
                # getting the variable indices of an expression could be inside it,right?

                var_index = [
                    variable_pointer.mipmodel_var_index
                    for variable_pointer in variable.list_variable_coefficients()[0]
                ]
                var_index_list += var_index

        return var_index_list


#Not Ready
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

#Not Ready
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
