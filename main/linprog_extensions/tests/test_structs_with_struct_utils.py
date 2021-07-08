from context import operations_research

# from server.linprog_structs.operations_research import(
#     ReferenceMPModel,
#     MPVariableProto,
#     ReferenceMPModelRequest,
#     ExtendedMPModel,
# )


from operations_research.linear_extension_pb2 import(
    # ReferenceMPModel as ReferenceMPModel_pb2,
    ExtendedMPModel as ExtendedMPModel_pb2,
    ReferenceMPModelRequest as ReferenceMPModelRequest_pb2
)

from operations_research.linear_solver_pb2 import(
    MPVariableProto as MPVariableProto_pb2,
    MPModelProto as MPModelProto_pb2,
)

from server.linprog_structs.operation_research_ext import(
    # ExtendedMPModelExt,
    ReferenceMPModelRequestExt,
    ReferenceMPModelRequestStreem,
)




def test_betterproto_structs_with_struct_utils():

    ## first we need to create some proto message for requests

    extended_model_one = ExtendedMPModel_pb2()
    conc_model_one = MPModelProto_pb2()
    conc_model_one.name = "test_conc_model_one"
    conc_model_one.variable.add()
    conc_model_one.variable[0].name = "test_var_onne"
    
    extended_model_one.concrete_model.CopyFrom(conc_model_one)
    request_one = ReferenceMPModelRequest_pb2( model = extended_model_one)

    # another request
    extended_model_two = ExtendedMPModel_pb2()
    conc_model_two = MPModelProto_pb2()
    conc_model_two.name = "test_conc_model_two"
    extended_model_two.concrete_model.CopyFrom(conc_model_two)
    request_two = ReferenceMPModelRequest_pb2( model = extended_model_two)


    # okay now test if we can create a single betterproto from above

    request_python_one = ReferenceMPModelRequestExt.from_proto(request_one)

    all_request_hierarchy = ReferenceMPModelRequestStreem.from_proto([request_one, request_two])

    




    print("test finish")


if __name__ == "__main__":

    test_betterproto_structs_with_struct_utils()
