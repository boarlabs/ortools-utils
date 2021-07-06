
from dataclasses import dataclass
from os import name

from context import operations_research

from server.linprog_structs.operations_research import(
    ReferenceMPModel,
    MPVariableProto,
    ReferenceMPModelRequest,
    ExtendedMPModel,
)

from operations_research.linear_extension_pb2 import(
    ReferenceMPModel as ReferenceMPModel_pb2,
    ExtendedMPModel as ExtendedMPModel_pb2
)

from operations_research.linear_solver_pb2 import(
    MPVariableProto as MPVariableProto_pb2,
    MPModelProto as MPModelProto_pb2

)

from server.linprog_structs.operation_research_ext import(
    ExtendedMPModelExt,
)


from google.protobuf.json_format import ParseDict, MessageToDict



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

    return 




def test_normal_betterproto_creation():

    data1 = ReferenceMPModel()

    data1.name = "test_model"
    data1.variables.append(
        MPVariableProto(name="test_var1")
    )

    data2 = ExtendedMPModel()

    data2.reference_model = data1

    obj_to_dict = data2.to_dict()
    assert( isinstance(obj_to_dict, dict) )

    # test serialize

    serialized = bytes(data2)


    data3  = ExtendedMPModelExt().parse(serialized)

    obj_to_dict2 = data3.to_dict()


    return




def test_normal_betterproto_creation_alternative():

    data1 = ReferenceMPModel(
        name="test_model",
        variables = [MPVariableProto(name="test_var1")]

    )


    data2 = ExtendedMPModel(
        reference_model=data1
    )


    obj_to_dict = data2.to_dict()
    assert( isinstance(obj_to_dict, dict) )

    # test serialize

    serialized = bytes(data2)


    data3  = ExtendedMPModelExt().parse(serialized)

    obj_to_dict2 = data3.to_dict()

    data4 = ExtendedMPModelExt().from_dict(obj_to_dict2)

    obj_to_dict3 = data4.to_dict()


    return



def test_standard_proto_to_better_proto():

    data1 = ExtendedMPModel_pb2()

    conc_model =MPModelProto_pb2()

    conc_model.name = "test_model3"

    conc_model.variable.append(
        MPVariableProto_pb2(
            name = "test_variable_1"
        )
    )

    data1.concrete_model.CopyFrom(conc_model)


    data2 = ExtendedMPModelExt.from_proto(data1)

    obj_to_dict = data2.to_dict()
    assert( isinstance(obj_to_dict, dict) )

    # test serialize

    serialized = bytes(data2)


    data3  = ExtendedMPModelExt().parse(serialized)

    obj_to_dict2 = data3.to_dict()
    return



def test_proto_to_dict_to_proto():

    data1 = ExtendedMPModel_pb2()
    conc_model =MPModelProto_pb2()
    conc_model.name = "test_model3"
    conc_model.variable.append(
        MPVariableProto_pb2(
            name = "test_variable_1"
        )
    )
    data1.concrete_model.CopyFrom(conc_model)

    obj_to_dict1 = MessageToDict(data1)
    
    data2 = ExtendedMPModelExt().from_dict(obj_to_dict1)
    obj_to_dict2 = data2.to_dict()

    return





if __name__ == "__main__":
    # test1()
    # test2()

    # test_standard_proto_to_better_proto()

    # test_normal_betterproto_creation()
    
    # test_normal_betterproto_creation_alternative()


    test_proto_to_dict_to_proto()