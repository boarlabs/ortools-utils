from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Any

from networkx.algorithms import components

from context import operations_research

from server.linprog_structs.operations_research import(
    MPVariableProto,
)
# import  server

from server.struct_utils import Component, Container, Content, HierarchyMixin, Catalogue

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)

@dataclass
class SomeBaseClass:

    def __post_init__(self):
        return

@dataclass
class Settings2(Content, SomeBaseClass):
  
      
    def __post_init__(self):
        super().__post_init__()
        self.set_children()

        return
    
    def add_tags(self):
        return ['tag1','tag4']


@dataclass
class Settings(Content, SomeBaseClass):
    horizon: float = None
    length: float = None
      
    def __post_init__(self):
        super().__post_init__()
        self.set_children()

        return
    
    def add_tags(self):
        return ['tag1','tag2']

    @staticmethod
    def from_dict(obj: Any):
        assert isinstance(obj, dict)
        horizon = from_float(obj.get("horizon"))
        length = from_float(obj.get("length"))
        return Settings(horizon, length)

@dataclass
class Input(HierarchyMixin, Container, SomeBaseClass):
    settings: Settings = None
    settings2: Settings2 = None
        
    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        self.populate_hierarchy()

        return
## The Tags of The Top Level Class are not actually used, Since the top level of hierarchy (single object)
## is not added to the Catalogue
    def add_tags(self):
        return ['tag1','tag2']
          
    @staticmethod
    def from_dict(obj: Any):
        assert isinstance(obj, dict)
        settings = Settings.from_dict(obj.get("settings"))
        settings2 = Settings2()
        
        return Input(settings, settings2)

def test_component_and_post_inits():

    input ={
        "settings":{
            "horizon": 4.3,
            "length": 1.2
        }
    }

    data_obj = Input.from_dict(input)
    assert( data_obj.settings.horizon == 4.3 )
    print(data_obj._children)

    return

def test_catalogue_utils():

    input ={
        "settings":{
            "horizon": 4.3,
            "length": 1.2
        }
    }

    data_obj = Input.from_dict(input)
    components = Catalogue.catalogue_items_dict

    component = Catalogue.find_components(data_obj._hierarchy.hierarchy_name, tag_list=["tag1"])
    return



if __name__ == "__main__":
    # test_component_and_post_inits()

    test_catalogue_utils()