
from context import operations_research

from server.mip_utils import(
    MipParameterPointer,
    MipVariablePointer,
    MipModel,
    MipConstraintPointer,
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

    print("test_mip_variable_pointer finish")

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
        name="test_constraint1",
    )




if __name__ == "__main__":
    test_parameter_pointer()

    test_mip_variable_pointer()