from linear_solver_pb2 import(
    MPModelProto,
    MPVariableProto,
    MPConstraintProto
)

from linear_extension_pb2 import(
    ExpressionMPModel,
    ReferenceMPVariable,
    MPExpression,
)


class Load:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        self.mipmodel = MPModelProto()


        ## Setup
        self.id = params["name"]
        self.objective_terms = {}

        self.mipmodel.name = self.id


        self.load =  params["load"]

        self.net_export = [
            MPVariableProto(
                lower_bound = -self.load[idx],
                upper_bound = -self.load[idx],
                name = "net_export["+ str(idx)+"]"
            ) for idx in interval_set
        ]

        [self.mipmodel.variable.add(var) for var in self.net_export]



class Generator:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        self.mipmodel = ExpressionMPModel()

        self.id = params["name"]
        self.objective_terms = {}

        self.mipmodel.name = self.id

        ## Parameters
        self.maxMW = params["maxMW"]
        self.minMW = params["minMW"]
        self.max_ramp = params["max_ramp"]
        self.marginal_cost = params["marginal_cost"]
        self.initial_commit = params["initial_commit"]

        ## Variables
        self.output = [
            MPVariableProto(
                lower_bound = 0,
                upper_bound = self.maxMW[idx],
                name = "output["+ str(idx)+"]",
            ) for idx in interval_set
        ] 
        # [self.mipmodel.variable.add(var) for var in self.output]
        for var in self.output: self.mipmodel.variable.add(var) 


        self.commit = [
            MPVariableProto(
                lower_bound = 0,
                upper_bound = 1,
                is_integer = True,
                name = f"commit[{idx}]",
            ) for idx in interval_set
        ] 

        for var in self.commit: self.mipmodel.variable.add(var)


        ## Expressions - this is where we define a common interface for model resource elements
        # Note in Optopy we have to have a generic and dynamic common interface for market products, different time indices, etc.
        # Will just use net_export as an interface for now
        # def _net_export(b,idx):
        #     return b.output[idx]
        # self.block.net_export = aml.Expression(interval_set, rule=_net_export)


        self.net_export = [ 
            MPExpression(
                name = f"net_export[{idx}]",
                variables = [
                    ReferenceMPVariable(
                        var_name = f"output[{idx}]",
                    )
                ],    
                variable_coefficients = [1],
            ) for idx in interval_set
        ]

        for item in self.ne_export: self.mipmodel.expressions.add(item) 


        ## Constraints
        # Note constraints should work with regular pyomo expression syntax
        # Should be able to reduce the amount of boilerplate here
        # def _output_commit_upper_bound(b,idx):
        #     return b.output[idx] - b.commit[idx] * b.maxMW <= 0
        # self.con_output_commit_upper_bound = aml.Constraint(interval_set, rule=_output_commit_upper_bound)


        self.con_output_commit_upper_bound = [
            MPConstraintProto(
                var_index= [idx, len(interval_set)+idx],
                coefficient = [1, -1*self.maxMW],
                upper_bound = 0,
                name = f"con_output_commit_upper_bound[{idx}]"
            ) for idx in range(len(interval_set))
        ]

        for item in  self.con_output_commit_upper_bound: self.mipmodel.constraint.add(item)
        # def _output_commit_lower_bound(b,idx):
        #     return b.commit[idx] * b.minMW - b.output[idx] <= 0
        # self.block.con_output_commit_lower_bound = aml.Constraint(interval_set, rule=_output_commit_lower_bound)
        # todo Add constraints/costs for ramping, min up, min down, startup/shutdown costs, etc.

        self.con_output_commit_lower_bound = [
            MPConstraintProto(
                var_index= [idx, len(interval_set)+idx],
                coefficient = [-1, 1*self.minMW],
                upper_bound = 0,
                name = f"con_output_commit_lower_bound[{idx}]"
            ) for idx in range(len(interval_set))
        ]


        self.mipmodel.constraint.extend(self.con_output_commit_lower_bound)
        

        ## Objective Terms
        # Unclear whether this expression object needs to be added to block/model - may be enough just to have it in the objective

        # def _interval_cost(b,idx):
        #     return b.marginal_cost * b.output[idx]
        # self.block.interval_cost = aml.Expression(interval_set, rule=_interval_cost)

        # def _total_cost(b):
        #     return sum(b.interval_cost[idx] for idx in interval_set)
        # self.block.total_cost = aml.Expression(rule=_total_cost)



        self.interval_cost = [
            MPExpression(
                name = f"interval_cost[{idx}]",
                variables = [
                    ReferenceMPVariable(
                        var_name = f"output[{idx}]",
                    )
                ],    
                variable_coefficients = [self.marginal_cost],
            ) for idx in interval_set
        ]
        
        self.mipmodel.expressions.extend(self.interval_cost)

        self.total_cost =  MPExpression(
            name = f"total_cost",
            variables = [
                ReferenceMPVariable(
                    var_name = f"interval_cost[{idx}]",
                ) for idx in interval_set
            ],    
            variable_coefficients = [1]*len(interval_set),
            objective_coefficient = 1
        )         
        
        
        self.mipmodel.expressions.add(self.total_cost)


        self.objective_terms["marginal_cost"] = self.total_cost
        




class Collection:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        ## Setup
        self.id = params["name"]
        self.objective_terms = {}

        self.block = aml.Block(concrete=True)

        # Need to reference interval set in coupling method, either need to add it to class or pass it to function.
        self.interval_set = interval_set

        self.component_element_ids = params["component_element_names"] # resources or other collections

        ## Parameters
        self.block.import_limit = params["import_limit"] # assume positive
        self.block.export_limit = params["export_limit"]

        ## Expressions/Variables
        # Should we define net_export as a variable and set equal later - allows to define upper and lower bounds here
        # or should it be an expression here, and we reconstruct constraints later whenever we add elements - i.e. the coupling aspect of the problem
        # It really depends on how the model is "constructed" - one option is to define everything as constructor functions that are called when the model is constructed, but order of construction matters here!
        # If we define as a variable, then we decouple them. 
        
        self.block.net_export = aml.Var(interval_set, bounds = (-self.block.import_limit,self.block.export_limit))

    def update_coupling_constraints(self):
        
        def _coupling_net_export(b,idx):
            sum_of_component_element_net_exports_idx = sum(getattr(b.parent_block(),component_element_id).net_export[idx] for component_element_id in self.component_element_ids)
            return b.net_export[idx] - sum_of_component_element_net_exports_idx == 0

        self.block.con_coupling_net_export = aml.Constraint(self.interval_set, rule=_coupling_net_export)
