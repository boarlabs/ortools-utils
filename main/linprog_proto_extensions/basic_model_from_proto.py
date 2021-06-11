from linear_solver_pb2 import(
    MPModelProto,
    MPVariableProto
)

# class NumVarExtension:



class Load:
    def __init__(
        self,
        interval_set,
        params: dict,
        ):
        super().__init__()

        ## Setup
        self.id = params["name"]
        self.objective_terms = {}

        self.mipmodel = MPModelProto()

        self.load =  params["load"]


        ## Expressions
        def _net_export(b,idx):
            return -b.load[idx]

        self.net_export = [
            MPVariableProto(
                lower_bound = -self.load[idx],
                upper_bound = -self.load[idx],
                name = "net_export_"+ str(idx)
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

        self.mipmodel = MPModelProto()

        self.id = params["name"]
        self.objective_terms = {}

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
                name = "output_"+ str(idx)
            ) for idx in interval_set
        ] 
        [self.mipmodel.variable.add(var) for var in self.output]


        self.commit = [
            MPVariableProto(
                lower_bound = 0,
                upper_bound = 1,
                is_integer = True,
                name = "commit_"+ str(idx)
            ) for idx in interval_set
        ] 
        [self.mipmodel.variable.add(var) for var in self.commit]

        
        


        ## Expressions - this is where we define a common interface for model resource elements
        # Note in Optopy we have to have a generic and dynamic common interface for market products, different time indices, etc.
        # Will just use net_export as an interface for now
        def _net_export(b,idx):
            return b.output[idx]
        
        self.block.net_export = aml.Expression(interval_set, rule=_net_export)

        ## Constraints
        # Note constraints should work with regular pyomo expression syntax
        # Should be able to reduce the amount of boilerplate here

        def _output_commit_upper_bound(b,idx):
            return b.output[idx] - b.commit[idx] * b.maxMW <= 0

        self.block.con_output_commit_upper_bound = aml.Constraint(interval_set, rule=_output_commit_upper_bound)

        def _output_commit_lower_bound(b,idx):
            return b.commit[idx] * b.minMW - b.output[idx] <= 0

        self.block.con_output_commit_lower_bound = aml.Constraint(interval_set, rule=_output_commit_lower_bound)

        # todo Add constraints/costs for ramping, min up, min down, startup/shutdown costs, etc.

        ## Objective Terms
        # Unclear whether this expression object needs to be added to block/model - may be enough just to have it in the objective

        def _interval_cost(b,idx):
            return b.marginal_cost * b.output[idx]

        self.block.interval_cost = aml.Expression(interval_set, rule=_interval_cost)
        
        def _total_cost(b):
            return sum(b.interval_cost[idx] for idx in interval_set)

        self.block.total_cost = aml.Expression(rule=_total_cost)

        self.objective_terms["marginal_cost"] = self.block.total_cost
        
