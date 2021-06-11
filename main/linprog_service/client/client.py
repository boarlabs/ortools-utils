import sys
import json
import logging
import grpc
from google.protobuf.json_format import ParseDict, MessageToDict

import linear_solver_pb2
from linprog_service_pb2_grpc import(
    LinProgServiceStub
)

def create_stub(channel):
    stub = LinProgServiceStub(channel)
    return stub



def send_request(channel, request):
    stub = create_stub(channel)
    response = stub.MILPModel(request)
    return  response


def create_request():

    model_request= linear_solver_pb2.MPModelRequest()

    model = model_request.model

    objective_coefficients = [10.0, 6.0, 4.0]
    variable_names = ["x1", "x2", "x3"]
    constraint_names = ["c1", "c2", "c3"]
    constraint_upbound = [100.0, 600.0, 300.0]
    constraint_coefficients = [[1.0, 1.0, 1.0], [10.0, 4.0, 5.0], [2.0, 2.0, 6.0]]

    # Set up variables
    num_var = len(variable_names)
    for i in range(num_var):
        variable = model.variable.add()
        variable.name = variable_names[i]
        variable.objective_coefficient = objective_coefficients[i]
        variable.lower_bound = 0.0 
        variable.is_integer = False  

    model.maximize = True

    # Set up constraints
    num_cons = len(constraint_names)
    for i in range(num_cons):
        constraint = model.constraint.add()
        constraint.name = constraint_names[i]
        constraint.upper_bound = constraint_upbound[i]
        # dealing with the constraint coefficient 
        for j in range(num_var):
            constraint.coefficient.append(constraint_coefficients[i][j])
            constraint.var_index.append(j)
    # Set up solver 
    model_request.solver_type  = linear_solver_pb2.MPModelRequest.SolverType.GLOP_LINEAR_PROGRAMMING

    return model_request

 


def read_solution(model_solution):
    print("The values of the variables:")
    variable_names = ["x1", "x2", "x3"]
    for j in range(3):
        print('Variable %s : %f' %(variable_names[j], model_solution.variable_value[j]))
    print("The objective value : %f" %(model_solution.objective_value))
    return 



if __name__ == '__main__':

    logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = '0.0.0.0:50051'

    request = create_request()

    with grpc.insecure_channel(target) as channel:
        response = send_request(channel, request)
    
    read_solution(response)


