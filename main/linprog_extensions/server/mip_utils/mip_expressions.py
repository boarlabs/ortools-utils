from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Union


from . import (
    MipVariablePointer,
    MipVariableArray,
    MipConstraintPointer,
    MipParameterPointer,
    MipModel,
)


class MipExpression:
    """
    The MIP proto does not have a expression class, so this is by default a pointer.
    No need to distinguish like we did for variable, and variable pointer.
    An expression can be thought of a variable with  a set of linear equality constraints
    or a pointer to a set of variables that provides the same interface of a variable (pointer).
    So when we define a constraint over an expression, that is in fact placed over a set of variables,
    (with their given coefficients of course), and when we define an objective coefficient for
    an expression it is transfered to it's composing variables (pointers).
    Important: We need to remember that we might have multiple expressions that have different comositions of
    the same variables, But each variable can only have one coefficient in the objective
    """

    def __init__(
        self,
        variable_list: List[Union[MipVariablePointer, MipExpression]],
        coefficients: List[float],
        index_name: Optional[str] = None,
        objective_coefficient: Optional[Union[MipParameterPointer, float]] = None,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
        mipmodel: Optional[MipModel] = None,
    ):

        """
        The paramters here can actually be a parametterPointer or a regular number
        We are dealing with variable pointers, so we need to pay attention how the actual
        variables are cprrectly affected.
        """

        assert len(coefficients) == len(variable_list)

        self.index_name = index_name
        self.variable_list = variable_list
        self.variable_coefficients = coefficients

        self.objective_coefficient = objective_coefficient
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self._mipmodel = None
        # Here we will need to pay attention to  the decision of how to set the mipmodel of the expression,
        # depending on if the variables have already a mipmodel are not

        self.constraint_pointers = list()

        self.mipmodel_attached = False
        # we will have up to two constraints for the lower bound and upper bound limits

        if lower_bound:
            self.add_constraint_pointer(lower_bound=lower_bound)

        if upper_bound:
            self.add_constraint_pointer(upper_bound=upper_bound)

        if objective_coefficient:
            self.add_objective_coefficient(self, objective_coefficient, 1)

        return

    @property
    def mipmodel(self):
        return self._mipmodel

    @mipmodel.setter
    def mipmodel(self, mipmodel):
        self._mipmodel = mipmodel
    
    def list_variable_coefficients(self):

        variables, coefficients = self._list_variable_coefficients_recursive(self)
        return variables, coefficients

    def _list_variable_coefficients_recursive(self, expression: None):

        var_list = list()
        coef_list = list()

        if hasattr(expression, "variable_list"):
            index = 0
            for variable in expression.variable_list:
                variables, coefficients = self._list_variable_coefficients_recursive(
                    variable
                )
                var_list += variables
                coef_list += [
                    expression.variable_coefficients[index] * coefficient
                    for coefficient in coefficients
                ]
                index += 1

        else:

            if isinstance(expression, MipVariablePointer):
                var_list.append(expression)
                coef_list = [1]

        return var_list, coef_list

    def recursive_rhs_calculator(
        self, expression_term, coefficient, lower_bound, upper_bound
    ):

        updated_lb = lower_bound
        updated_ub = upper_bound

        if hasattr(expression_term, "variable_list"):
            for index in range(len(expression_term.variable_list)):
                updated_lb, updated_ub = self.recursive_rhs_calculator(
                    expression_term.variable_list[index],
                    expression_term.variable_coefficients[index],
                    updated_lb,
                    updated_ub,
                )
        else:

            if isinstance(expression_term, MipParameterPointer):

                if updated_lb:
                    updated_lb += -coefficient * expression_term.value

                if updated_ub:
                    updated_ub += -coefficient * expression_term.value

        return updated_lb, updated_ub

    def adjust_right_handside_for_paramters(self, lower_bound, upper_bound):

        updated_lb = lower_bound
        updated_ub = upper_bound

        for index in range(len(self.variable_list)):

            updated_lb, updated_ub = self.recursive_rhs_calculator(
                self.variable_list[index],
                self.variable_coefficients[index],
                updated_lb,
                updated_ub,
            )

        return updated_lb, updated_ub

    def add_constraint_pointer(
        self,
        lower_bound: float = None,
        upper_bound: float = None,
    ):
        # here need to account for having some of the variables to be expressions.

        variables, coefficients = self.list_variable_coefficients()
        lower_bound, upper_bound = self.adjust_right_handside_for_paramters(
            lower_bound, upper_bound
        )

        constraint_pointer = MipConstraintPointer(
            variables=variables,
            coefficient=coefficients,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            name=None,
        )

        self.constraint_pointers.append(constraint_pointer)
        return

    def add_objective_coefficient(
        self, expression, objective_coefficient, variable_coefficient
    ):

        if hasattr(expression, "variable_list"):

            for index in range(len(expression.variable_list)):

                self.add_objective_coefficient(
                    expression.variable_list[index],
                    objective_coefficient,
                    expression.variable_coefficients[index] * variable_coefficient,
                )

                index += 1

        else:

            if isinstance(objective_coefficient, MipParameterPointer):

                variable_objective_coefficient = MipParameterPointer(
                    parameter_name=objective_coefficient.name,
                    parameter_value=variable_coefficient * objective_coefficient.value,
                )
            else:

                variable_objective_coefficient = (
                    variable_coefficient * objective_coefficient
                )

            expression.add_objective_coefficient(variable_objective_coefficient)

        return

    # def set_expression(
    #     self,
    #     objective_coefficient: Optional[Union[MipParameterPointer, float]] ,
    #     lower_bound:Optional[Union[MipParameterPointer, float]] ,
    #     upper_bound:Optional[Union[MipParameterPointer, float]] ,
    # ):

    #     pass

    def build(self):

        """
        okay so this is supposed to be similar to that of the variable.
        if we want to set some parameter of the expression we do it here.
        Also it would Set it's variables, and Constraints.
        It would need to have the mipmodel defined already in order to set the constraints
        (for constraints, we donot need to set the mipmodel seperately if the variables have a model.
        similarly here is the variables (or the constraints) have a mip model, we donot need to define a model.
        If they don't we can define a mipmodel for the constraints and the variables.

        """
        # so when we set the expression, the variable_pointers  are already updated, and and constraint_pointers are defined.
        # here we only need to SET them in the mipmodel. This means update the objective coefficients for variables and attach the constraints.
        # and what about the expressions?

        def check_variable_attached_to_expression_mipmodel(variable_pointer, mipmodel):

            if hasattr(variable_pointer, "variable_list"):

                if mipmodel != variable_pointer.mipmodel:
                    ValueError(
                        "The expression MipModel is not the same as the given MipModel"
                    )

                for variable in variable_pointer.variable_list:
                    check_variable_attached_to_expression_mipmodel(variable, mipmodel)

            elif hasattr(variable_pointer, "attach_mipmodel"):

                if not variable_pointer.mipmodel:
                    variable_pointer.attach_mipmodel(mipmodel)

                elif variable_pointer.mipmodel != mipmodel:
                    ValueError(
                        "The variable pointer MipModel is not the same as the constraint MipModel"
                    )

                elif variable_pointer.mipmodel == mipmodel:
                    ## i.e the variable is already set and is attached to the mipmodel

                    variable_pointer.reattach_mipmodel()

        if not self.mipmodel:
            self._add_mipmodel_from_variables()

        for variable_pointer in self.variable_list:

            check_variable_attached_to_expression_mipmodel(
                variable_pointer, self.mipmodel
            )

        for constraint_pointer in self.constraint_pointers:
            constraint_pointer.build_constraint()

        self.mipmodel_attached = True

        # what else needs to happen when we want to Build the actual expression?
        # similar to variablepointer and constraint_pointer,  need to add for the case we want to change the parameters of the expression

    ## still need to think about the case when we add a Mipmodel to another model, what will/should happen to it's variable_pointers of the old/new mipmodels

    def _add_mipmodel_from_variables(self):

        """
        so here the assumption is that we have not specified the mipmodel for the
        expression explicitly, but we have variables that are attached to some mipmodel.
        Q; whatif the variables or the expression does not have a mipmodel?


        """

        mipmodel_list = [variable.mipmodel for variable in self.variable_list]
        mipmodel = next(item for item in mipmodel_list if item is not None)
        assert mipmodel != None
        self.add_mipmodel(mipmodel)

        return mipmodel

    




class MipExpressionArray:
    def __init__(
        self,
        index_names: Optional[List[str]] = None,
        expression_list: Optional[List[MipExpression]] = None,
        variable_list: Optional[List[MipVariableArray]] = None,
        coefficients: Optional[List[List[float]]] = None,
        objective_coefficients: Optional[
            List[Union[MipParameterPointer, float]]
        ] = None,
        lower_bounds: Optional[List[Union[MipParameterPointer, float]]] = None,
        upper_bounds: Optional[List[Union[MipParameterPointer, float]]] = None,
        mipmodel: Optional[MipModel] = None,
    ):

        """
        this is  to create an array of expressions from a list of variableArrays
        Right now I just want to use this as a thin wrapper for the  Single MipExpression.
        So I will leave the constructing the  expressionArrays from variable_arrays directly to later.
        """

        self.index_names = index_names

        self.expression_list = expression_list

    def attach_mipmodel(self):

        for expression in self.expression_list:

            expression.attach_mipmodel()

    def add_mipmodel(self, mipmodel):

        for expression in self.expression_list:

            expression.add_mipmodel(mipmodel)
