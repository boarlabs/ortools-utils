from dataclasses import dataclass
# from main.linprog_extensions.server.struct_utils import component
from os import name
from google.protobuf.json_format import ParseDict, MessageToDict

from context import operations_research

from server.struct_utils.catalogue import Catalogue

from server.linprog_structs.operation_research_ext import(
    ExtendedMPModelExt,
    MPModelProtoExt,
    ReferenceMPModelExt,
    ReferenceMPModelRequestStreem,
)


from build_reference_model.basic_model_instantiation_from_proto import instantiate_model

def test_adding_tags():


    model_requests = instantiate_model()
    request_stream_struct = ReferenceMPModelRequestStreem.from_proto(model_requests)

    component = Catalogue.find_components(
        hierarchy_name = request_stream_struct._hierarchy.hierarchy_name,
        tag_list=["name=output[1]", "type=MPVariableProto", "parent=gen_name_0"]
    )
    return





    







if __name__ == "__main__":
    
    test_adding_tags()