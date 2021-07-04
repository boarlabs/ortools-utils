import logging
import sys
import grpc

from context import operations_research

# from operations_research.python.linprog_service_pb2_grpc import(
#     LinProgServiceStub
# )
from linprog_service_pb2_grpc import(
    LinProgServiceStub
)

from basic_model_instantiation_from_proto import(
    instantiate_model
)




def create_stub(channel):
    stub = LinProgServiceStub(channel)
    return stub


def request_iterator(request):

    for item in request:
        yield item

def send_request(channel, request):
    stub = create_stub(channel)


    response = stub.MILPReferenceModel(request_iterator(request))

    logging.info("client received response")
    return  response





if __name__ == "__main__":

    # stub = create_stub()

    # model_requests = instantiate_model()


    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:50051'

    request = instantiate_model()

    with grpc.insecure_channel(target) as channel:
        response = send_request(channel, request)
