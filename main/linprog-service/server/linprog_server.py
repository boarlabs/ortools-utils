from linprog_service_pb2_grpc import LinProgServiceServicer
import linear_solver_pb2

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
