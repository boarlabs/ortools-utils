

from operations_research.linprog_service_pb2_grpc import LinProgServiceServicer
import operations_research.linear_solver_pb2 as linear_solver_pb2

from ortools.linear_solver import pywraplp


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

        print(len(request_list))


        response = linear_solver_pb2.MPSolutionResponse()
        return response
