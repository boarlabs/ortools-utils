
from context import operations_research

from server.mip_utils import(
    MipParameterPointer,
)




def test_paramter_pointer():

    # okay so why we need a parameter pointer. can't we just use a list as a wrapper?
    # what about Enum? does that provide a similar functionality? 

    a = MipParameterPointer(name='test_param', value= 23)
    b = a
    b.value = 34
    assert( a.value ==34)
    print("def test_paramter_pointer finish")
    return


def test_mip_variable_pointer():

    pass


if __name__ == "__main__":
    test_paramter_pointer()