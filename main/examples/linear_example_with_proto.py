# import grpc 
# import mip_pb2
# import mip_pb2_grpc

from absl import app
from absl import flags

import linear_solver_pb2
import sys

from ortools.linear_solver import pywraplp


def create_model_request(model_request):
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

    return 


def read_solution(model_solution):
    print("The values of the variables:")
    variable_names = ["x1", "x2", "x3"]
    for j in range(3):
        print('Variable %s : %f' %(variable_names[j], model_solution.variable_value[j]))
    print("The objective value : %f" %(model_solution.objective_value))
    return 





def main():
    # """Optimize the bus driver allocation in two passes."""
    # print('----------- first pass: minimize the number of drivers')
    # num_drivers = bus_driver_scheduling(True, -1)
    # if num_drivers == -1:
    #     print('no solution found, skipping the final step')
    # else:
    #     print('----------- second pass: minimize the sum of working times')
    #     bus_driver_scheduling(False, num_drivers)

    model_request= linear_solver_pb2.MPModelRequest()
    response = linear_solver_pb2.MPSolutionResponse()
    create_model_request(model_request)

    solver = pywraplp.Solver.CreateSolver("GLOP")
    solver.LoadModelFromProto(input_model=model_request.model)

    ## These are not meant for getting reposne!
    # pywraplp.Solver.SolveWithProto(model_request, response)
    # r = solver.LoadSolutionFromProto(response)
    # r = solver.LoadModelFromProto(response)
    # r= solver.ExportModelToProto(response)


    result_status = solver.Solve()

    r = solver.FillSolutionResponseProto(response)

    assert result_status == pywraplp.Solver.OPTIMAL

    print(result_status)
    read_solution(response)



if __name__ == '__main__':
    # app.run(main)
    main()



