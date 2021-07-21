
# from dataclasses import dataclass
# from google.protobuf.json_format import ParseDict, MessageToDict

from context import operations_research

from server.struct_utils import Catalogue

from server.linprog_structs.operation_research_ext import(
    ReferenceMPModelRequestStreem,
)


from build_reference_model.basic_model_instantiation_from_proto import instantiate_model



def test_build_concrete_models():

    model_requests = instantiate_model()
    
    request_stream_struct = ReferenceMPModelRequestStreem.from_proto(model_requests)

    request_stream_struct.build_models()

    return





if __name__ == "__main__":
    
    test_build_concrete_models()