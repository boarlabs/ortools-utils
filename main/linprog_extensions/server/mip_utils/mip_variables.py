from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from operations_research import linear_solver_pb2


class MipParameterPointer:

    def __init__(
        self,
        value: float = None,
        name: str = str(),
    ):
        self._value = value
        self.name = name
        self._mipmodel = None
        return

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        return
    
    @property
    def mipmodel(self):
        return self._mipmodel

    @mipmodel.setter
    def mipmodel(self, mipmodel):
        self._mipmodel = mipmodel

    def add_value(
        self,
        parameter: MipParameterPointer,
    ):
        assert(isinstance(parameter, MipParameterPointer))
        parameter_value = parameter.value
        if not parameter_value:
            parameter_value = 0

        if not self._value:
            self._value = 0
         
        self._value += parameter_value
        return

    def build(self):
        value = self._value
        if not value:
            value = 0 

        return value

class MipVariablePointer:
    def __init__(
        self,
        name: Optional[str] = str(),
        is_integer: Optional[bool] = False,
        objective_coefficient: Optional[MipParameterPointer] = MipParameterPointer(),
        lower_bound: Optional[float] = float('-inf'),
        upper_bound: Optional[float] = float('inf'),
    ):

        ## why I have put the objective coefficient and lb, and ub as parameters???
        ## maybe we want a variable that we can objective coefficient at any time?
        ## do we need a parameter for that?
        assert(isinstance(objective_coefficient, MipParameterPointer))
        assert(isinstance(lower_bound, float))
        assert(isinstance(upper_bound, float))
        assert(isinstance(is_integer, bool))
        assert(isinstance(name, str))


        self.name = name
        self.is_integer = is_integer
        self.objective_coefficient = objective_coefficient
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.variable = None
        self._mipmodel = None
        self.mipmodel_var_index = None
        self.mipmodel_attached = False
        self.variable_response = None
        return

    @property
    def mipmodel(self):
        return self._mipmodel

    @mipmodel.setter
    def mipmodel(self, mipmodel):
        self._mipmodel = mipmodel

    def make_variable_proto(self):

        # def get_value(obj):
        #     try:
        #         value = obj.value
        #     except:
        #         value = obj
        #     return value

        self.variable = linear_solver_pb2.MPVariableProto(
            name=self.name,
            is_integer=self.is_integer,
            objective_coefficient= self.objective_coefficient.build(),
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
        )

        return

    def build(self):
        ## Note: right now everytime we build the variable pointer, a new variable is added to the model
        ## would be good to ifx this; but I think I don't need this right now
        self.make_variable_proto()
        self._mipmodel.model.variable.append(self.variable)
        self.mipmodel_var_index = len(self._mipmodel.model.variable) - 1
        self.mipmodel_attached = True
        return

    def add_objective_coefficient(
        self,
        objective_coefficient: Optional[MipParameterPointer],
    ):
        # if not self.objective_coefficient.value:
        #     self.objective_coefficient = objective_coefficient
        # if isinstance(self.objective_coefficient, MipParameterPointer):
        self.objective_coefficient.add_value(objective_coefficient)
        
        # elif isinstance(objective_coefficient, MipParameterPointer):
            # objective_coefficient.add_value(self.objective_coefficient)
            # self.objective_coefficient = objective_coefficient
        # else:
            # self.objective_coefficient += objective_coefficient
        return

    def extract_response(self, response):
        self.variable_response = response.variable_value[self.mipmodel_var_index]
        return



    # def attach_mipmodel(
    #     self,
    #     var_index: int = None,
    # ):
    #     """
    #         since we can have a variable that is not attached to any MPmodels, the VariablePointer can also be "Built"
    #         without having the mipmodel (note this is not the case for the MPconstraint and thus MipConstraintPointer).
    #         So here when we attach/append a  variable to a MipModel.
    #         This method can be called in two ways, either by MipVariablePointer and giving a MipModel, or by a mipmodel and giving a MipVariablePointer
    #     """

    #     assert (not self.mipmodel_attached)
    #     if  not self._mipmodel:  
    #         ValueError("A MipModelPointer instance is not defined for the MipVairablePointer instance")

    #     ## not sure if the mechanism of creating the loop between this MipVariable and MipModel is the best
    #     ##  or most straight forward, but it did seem interesting to me at the time.        
    #     ## so how does this work? 
    #     ## 1- The VariablePointer method build_variable is called directly from variablepointer.
    #     ## or the build_variableArray method of the mipmodel
    #     ## in that case the var_index would not be provided.
    #     ## this is not the preffered way though.

    #     if not var_index: 
    #         # i.e. the mipVariableArray is calling the method/ or the build_variableArray method of the mipmodel
    #         ## so at this point we just need to make sure that a MipModelPointer is defined for the variable 
    #         ## and that the variable is not already attached to it.
    #         ## then we pass the VariablePointer to the MipModelPointer, to add it(which again will call this method with the index
    #         self.make_variable_proto()
    #         self._mipmodel.build_variable(self)

    #     ## 2- when the mipmodel is calling the method 
    #     ## at this time the variable associated with VariablePointer is added to the model of the Modelpointer
    #     ## we provide the model index to this pointer
    #     self.mipmodel_var_index = var_index
    #     self.mipmodel_attached = True
    #     return self.mipmodel_var_index


## Not Ready
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
