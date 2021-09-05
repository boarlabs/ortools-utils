
from context import operations_research

from operations_research.linprog_service_pb2_grpc import LinProgServiceServicer
import operations_research.linear_solver_pb2 as linear_solver_pb2

from ortools.linear_solver import pywraplp

from server.linprog_structs.operation_research_ext import(
    ReferenceMPModelRequestStreem,
)

import logging 

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)


class LinProgServer(LinProgServiceServicer):

    def MILPModel(self, request, context):

        ## toDo should set solver from the proto request
        solver = pywraplp.Solver.CreateSolver("GLOP")
        solver.LoadModelFromProto(input_model=request.model)
        _ = solver.Solve()

        response = linear_solver_pb2.MPSolutionResponse()
        _ = solver.FillSolutionResponseProto(response)

        return response


    def MILPReferenceModel(self, request_iterator, context):
        request_list = list()
        for request in request_iterator:
            request_list.append(request)

        logging.info('Request Recived with  %r models', len(request_list))

        request_stream_struct = ReferenceMPModelRequestStreem.from_proto(request_list)
        request_stream_struct.configure_references()
        request_stream_struct.build_final_mipmodel()
        request_stream_struct.solve_final_model()
        request_stream_struct.distribute_results()

        logging.info('Request Solved')

        for response in request_stream_struct.solution_responses:
            yield response

        # response = linear_solver_pb2.MPSolutionResponse()
        # return response
