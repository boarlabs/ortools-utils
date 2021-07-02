from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from operations_research import linear_solver_pb2




class MipParameterPointer:
    def __init__(self, parameter_name=None, parameter_value=None):
        # self._value = list()
        self._value = parameter_value
        self._name = parameter_name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, parameter):
        self._value = parameter
        return

    def add_value(self, parameter: Union[MipParameterPointer, float]):

        try:
            self._value += parameter.value
        except:
            self._value += paramter

        return

    # def __getattr__(self, name=None):
    #     return self.obj

    # def set_value(self, obj):


class Reference:
    def __init__(self, parameter):

        self.param = parameter

    def get(self):
        return self.param

    def set(self, parameter):
        self.param = parameter


class MipVariablePointer:
    def __init__(
        self,
        name: MipParameterPointer = None,
        is_integer: bool = False,
        objective_coefficient: MipParameterPointer = None,
        lower_bound: MipParameterPointer = None,
        upper_bound: MipParameterPointer = None,
    ):
        self.variable = None
        self.name = name
        self.is_integer = is_integer
        self.objective_coefficient = objective_coefficient
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.mipmodel = None
        self.mipmodel_var_index = None
        self.mipmodel_attached = False

    def get_variable(self):
        if not self.variable:
            self.build_variable()
        return self.variable

    def build_variable(
        self,
        name: str = None,
        is_integer: bool = False,
        objective_coefficient: float = None,
        lower_bound: float = None,
        upper_bound: float = None,
    ):
        def get_value(obj):
            try:
                value = obj.value
            except:
                value = obj
            return value

        self.variable = linear_solver_pb2.MPVariableProto(
            name=str(name) if name else str(get_value(self.name)),
            is_integer=is_integer if is_integer else self.is_integer,
            objective_coefficient=objective_coefficient
            if objective_coefficient
            else get_value(self.objective_coefficient),
            lower_bound=lower_bound if lower_bound else get_value(self.lower_bound),
            upper_bound=upper_bound if upper_bound else get_value(self.upper_bound),
        )

        return

    def attach_mipmodel(
        self,
        # mipmodel,
        var_index=None,
    ):
        """
        since we can have a variable that is not attached to any MPmodels, the VariablePointer can also be "Set"
        without having the mipmodel (note this is not the case for the MPconstraint and thus MipConstraintPointer).

        So here when we attach/append a  variable to a MipModel.


        This method can be called in two ways, either by variable and giving a mipmodel, or by a mipmodel.


        """

        # if not self.mipmodel_attached:
        #     if not var_index:
        #         self.mipmodel = mipmodel
        #         if not self.variable:
        #             self.set_variable()
        #         mipmodel.append_variable(self)
        #         # self.mipmodel_var_index= var_index

        #     else:
        #         self.mipmodel=mipmodel
        #         self.mipmodel_var_index = var_index
        # else:
        #     assert( self.mipmodel == mipmodel)
        #     self.mipmodel_var_index = var_index

        # return self.mipmodel_var_index

        if var_index:  # (i.e. the mipmodel is calling the method )

            if self.mipmodel:  # i.e. if a mipmodel is added to this variableP before
                assert not self.mipmodel_attached
                # assert( self.mipmodel == mipmodel)
                self.mipmodel_var_index = var_index

            else:
                # self.mipmodel = mipmodel
                # self.mipmodel_var_index = var_index
                ValueError("The mipmodel is not defined for the mipvairable")

        else:  # i.e. the mipVariableArray is calling the method/ or the build_variableArray method of the mipmodel

            if self.mipmodel:
                assert not self.mipmodel_attached
                # assert( self.mipmodel == mipmodel)
            else:
                # self.mipmodel = mipmodel
                ValueError("The mipmodel is not defined for the mipvairable")

            self.build_variable()
            self.mipmodel.build_variable(self)

        self.mipmodel_attached = True
        return self.mipmodel_var_index

    def add_mipmodel(self, mipmodel):
        self.mipmodel = mipmodel
        return

    def reattach_mipmodel(self):

        self.build_variable()
        self.mipmodel.update_variable(self)
        return

    def add_objective_coefficient(
        self,
        objective_coefficient: Optional[Union[MipParameterPointer, float]],
    ):

        if self.objective_coefficient:
            # this is mainly needed for the case where multiple expressions point to the same variablePointer
            # Q: Does the variable needs to know which expressions are pointing to it though?
            if isinstance(self.objective_coefficient, MipParameterPointer):
                self.objective_coefficient.add_value(objective_coefficient)

            elif isinstance(objective_coefficient, MipParameterPointer):

                objective_coefficient.add_value(self.objective_coefficient)
                self.objective_coefficient = objective_coefficient
            else:
                self.objective_coefficient += objective_coefficient

        else:
            self.objective_coefficient = objective_coefficient

        self.build_variable(objective_coefficient=self.objective_coefficient)


class MipVariableArray:
    def __init__(
        self,
        index_names: Optional[List[str]] = None,
        objective_coefficients: Optional[List[float]] = None,
        lower_bounds: Optional[List[float]] = None,
        upper_bounds: Optional[List[float]] = None,
        is_integer: bool = False,
    ):
        len_variable_array = None
        if index_names:
            len_variable_array = len(index_names)
        if objective_coefficients:
            if len_variable_array:
                assert len_variable_array == len(objective_coefficients)
            else:
                len_variable_array = len(objective_coefficients)
        if lower_bounds:
            if len_variable_array:
                assert len_variable_array == len(lower_bounds)
            else:
                len_variable_array = len(lower_bounds)
        if upper_bounds:
            if len_variable_array:
                assert len_variable_array == len(upper_bounds)
            else:
                len_variable_array = len(upper_bounds)
        if not len_variable_array:
            ValueError("Not Sufficient paramters for varriable array")

        self.variable_pointer_list = [
            MipVariablePointer(
                name=index_names[i],
                is_integer=is_integer,
                objective_coefficient=objective_coefficients[i]
                if objective_coefficients
                else None,
                lower_bound=lower_bounds[i] if lower_bounds else None,
                upper_bound=upper_bounds[i] if upper_bounds else None,
            )
            for i in range(len_variable_array)
        ]

        self.model_variables_index_list = list()
        self.mipmodel = None

    def add_mipmodel(self, mipmodel):
        self.mipmmodel = mipmodel

        for vairable_pointer in self.variable_pointer_list:

            vairable_pointer.add_mipmodel(mipmodel)

        return

    def attach_mipmodel(self, mipmodel=None, model_index_list=None):
        # if not self.mipmodel:
        #     if not model_index_list:
        #         self.mipmodel= mipmodel
        #         self.mipmodel.build_variable(self)
        #     else:
        #         self.mipmodel = mipmodel
        #         self.model_variables_index_list = model_index_list
        # else:
        #     assert(self.mipmodel == mipmodel)
        self.model_variables_index_list = model_index_list

        return

    def build_variable(
        self,
        index_names: Optional[List[str]],
        objective_coefficients: Optional[List[float]],
        lower_bounds: Optional[List[float]],
        upper_bounds: Optional[List[float]],
    ):

        if index_names:
            assert len(self.variable_pointer_list) == len(index_names)
        if objective_coefficients:
            assert len(self.variable_pointer_list) == len(objective_coefficients)
        if lower_bounds:
            assert len(self.variable_pointer_list) == len(lower_bounds)
        if upper_bounds:
            assert len(self.variable_pointer_list) == len(upper_bounds)

        index = 0
        for variable_pointer in self.variable_pointer_list:
            variable_pointer.build_variable(
                name=index_names[index] if index_names else None,
                objective_coefficient=objective_coefficients[index]
                if objective_coefficients
                else None,
                lower_bound=lower_bounds[index] if lower_bounds else None,
                upper_bound=upper_bounds[index] if upper_bounds else None,
            )

            index += 1

    def add_objective_coefficients(self, objective_coefficients: list):

        assert len(self.variable_pointer_list) == len(objective_coefficients)

        for i in range(len(objective_coefficients)):
            self.variable_pointer_list[i].build_variable(
                objective_coefficient=objective_coefficients[i]
            )
