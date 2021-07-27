
# from dataclasses import dataclass
# from google.protobuf.json_format import ParseDict, MessageToDict

from context import operations_research

from server.struct_utils import Catalogue

from server.linprog_structs.operation_research_ext import(
    ReferenceMPModelRequestStreem,
)


from build_reference_model.basic_model_instantiation_from_proto import instantiate_model

class TestReturnRef:

    def __init__(self) -> None:
        
        self.name = ""
        self.value = None
    
    def set_value(self, value):
        self.value = value

        return self.value

class SecondTestClass:

    def __init__(self):
        self.received_value = None
    
    def get_value(self, value):
        self.received_value = value
        return

def test_build_concrete_models():

    model_requests = instantiate_model()
    request_stream_struct = ReferenceMPModelRequestStreem.from_proto(model_requests)
    request_stream_struct.configure_references()

    return


def test_reference_functions():
    a = TestReturnRef()
    b = SecondTestClass()
    
    c=[65]
    b.get_value(
        a.set_value(c)
    )

    c[0] =32
    a.set_value(c)

    print(b.received_value)
    return

if __name__ == "__main__":

    test_build_concrete_models() 
    # test_reference_functions()

   


    ck=1