
# from main.linprog_proto_extensions.searchable_reference_extensions.server.linear_solver_pb2 import MPVariableProto
from os import name
from lib.operations_research import(
    ReferenceMPModel,
    MPVariableProto,
    ReferenceMPModelRequest,
)

from linear_extension_pb2 import(
    ReferenceMPModel as ReferenceMPModel_pb2,
    ExtendedMPModel as ExtendedMPModel_pb2
)

from linear_solver_pb2 import(
    MPVariableProto as MPVariableProto_pb2,
    MPModelProto as MPModelProto_pb2
)


def test1():

    data1 = ReferenceMPModel()

    data1.name = "test_model"
    data1.variables.append(
        MPVariableProto(name="test_var1")
    )

    ck=1

    data2= ReferenceMPModel_pb2()

    data2.name = "test_model2"
    
    data2.variables.extend([
        MPVariableProto_pb2(name="test_var2")
    ])

    variable =  MPVariableProto_pb2(name="test_var2")


    data1.variables.append(variable)

def test2():


    data1 = ExtendedMPModel_pb2()

    conc_model =MPModelProto_pb2()

    conc_model.name = "test_model3"

    data1.concrete_model.CopyFrom(conc_model)


    data2 = ReferenceMPModelRequest( model = data1)

    ck=2




if __name__ == "__main__":
    # test1()


    test2()

