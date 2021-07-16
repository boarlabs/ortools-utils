
from context import operations_research

from server.mip_utils import(
    MipParameterPointer,
    MipVariablePointer,
    MipModel,
    MipConstraintPointer,
    MipExpression,
)




def test_parameter_pointer():

    # okay so why we need a parameter pointer. can't we just use a list as a wrapper?
    # what about Enum? does that provide a similar functionality? 

    param1 = MipParameterPointer(name='test_param', value= 23)
    param2 = param1
    param2.value = 34
    assert( param1.value ==34)

    param3 = MipParameterPointer()
    param1.add_value(param3)
    assert(param1.value == 34)

    param4 = MipParameterPointer(name ='test_param4', value =1)
    param1.add_value(param4)
    assert(param1.value == 35)

    param5 = MipParameterPointer(42)

    assert(param5.value ==42)
    return


def test_mip_variable_pointer():

    var1 = MipVariablePointer(name="test_var1")

    assert(var1.name =="test_var1")
    assert(var1.lower_bound == float("-inf"))
    assert(var1.upper_bound == float("inf"))
    assert(isinstance(var1.objective_coefficient,MipParameterPointer))
    assert(var1.objective_coefficient.name == "")
    var1.make_variable_proto()

    mipmodel1 = MipModel()
    var1.mipmodel = mipmodel1
    var1.build()

    assert(var1.mipmodel_var_index == 0)
    assert(mipmodel1.model.variable[0].name == "test_var1")

    var1.add_objective_coefficient(
        MipParameterPointer()
    )
    var1.build()
    ## NOTE: A New Variable is added here to the model
    assert(mipmodel1.model.variable[1].objective_coefficient == 0)

    var1.add_objective_coefficient(
        MipParameterPointer(name="test_cost1", value=12)
    )
    var1.build()
    ## NOTE: A New Variable is added here to the model
    assert(mipmodel1.model.variable[2].objective_coefficient == 12)

    return


def test_mip_constraint():
    
    var1= MipVariablePointer(
        name="test_var1",
    )
    var2= MipVariablePointer(
        name = "test_var2"
    )

    constr1 = MipConstraintPointer(
        variables=[var1, var2],
        coefficient =[1,2],
        name="test_constraint1",
        upper_bound= 4
    )

    mipmodel1 = MipModel()

    var1.mipmodel = mipmodel1
    # var2.mipmodel = mipmodel1
    constr1.build()

    assert(constr1.mipconstraint.var_index[0] == 0)
    assert(constr1.mipconstraint.coefficient[0] ==1)
    assert(mipmodel1.model.variable[0].name == "test_var1")


      
    var3= MipVariablePointer(
        name="test_var3",
    )
    var4= MipVariablePointer(
        name = "test_var4"
    )

    constr1 = MipConstraintPointer(
        variables=[var3, var4],
        coefficient =[3,4],
        name="test_constraint2",
        upper_bound= 4
    )

    mipmodel1 = MipModel()

    constr1.mipmodel = mipmodel1
    constr1.build()

    assert(constr1.mipconstraint.var_index[0] == 0)
    assert(constr1.mipconstraint.coefficient[0] ==3)
    assert(mipmodel1.model.variable[0].name == "test_var3")

    return


def test_mip_expression():

    var1 = MipVariablePointer(
        name = "test_var1"
    )
    var2 = MipVariablePointer(
        name="test_var2"
    )
    param1 = MipParameterPointer(34)
    exp1 = MipExpression(
        name = "test_expr1",
        variable_list=[var1, var2, param1],
        coefficients = [1,2, 3],
        lower_bound= 0 
    )
    mipmodel1 = MipModel()
    exp1.mipmodel = mipmodel1
    # unlike constraint, here we cannot just asssign a mipmodel to expr, and it'll
    ## figure out for the vars, maybe add it later
    var1.mipmodel = mipmodel1
    var2.mipmodel = mipmodel1

    exp1.build()

    assert(mipmodel1.model.constraint[0].var_index[0]==0)
    assert(len(mipmodel1.model.variable)==2)
    assert(mipmodel1.model.variable[1].name=="test_var2")
    assert(mipmodel1.model.constraint[0].lower_bound == -102)

    ### okay so still remains testing of expressions with expressions

    var3 = MipVariablePointer(
        name = "test_var3"
    )
    var4 = MipVariablePointer(
        name="test_var4"
    )
    var5= MipVariablePointer(
        name="test_var5"
    )
    param2 = MipParameterPointer(34)
    param3 = MipParameterPointer(3)

    exp2 = MipExpression(
        name = "test_expr2",
        variable_list=[var3, var4, param2],
        coefficients = [1,2, 3],
        lower_bound= 0 
    )
    mipmodel2 = MipModel()
    exp2.mipmodel = mipmodel2
    var3.mipmodel = mipmodel2
    var4.mipmodel = mipmodel2
    var5.mipmodel = mipmodel2
    exp3 = MipExpression(
        name = "test_expr3",
        variable_list=[exp2, var5, param3],
        coefficients = [1,2, 1],
        lower_bound= 0 
    )
    exp3.mipmodel = mipmodel2
    exp3.build()

    assert(mipmodel2.model.constraint[1].lower_bound == -105)

    return


if __name__ == "__main__":
    test_parameter_pointer()

    test_mip_variable_pointer()

    test_mip_constraint()

    test_mip_expression()