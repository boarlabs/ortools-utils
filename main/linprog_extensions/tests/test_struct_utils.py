from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import List, Any

from context import operations_research
# import  server

from server.struct_utils import Component, Container, Content

def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)

@dataclass
class Settings(Content):
    horizon: float
    length: float
      
    def __post_init__(self):
        super().__post_init__()
        return

    @staticmethod
    def from_dict(obj: Any):
        assert isinstance(obj, dict)
        horizon = from_float(obj.get("horizon"))
        length = from_float(obj.get("length"))
        return Settings(horizon, length)

@dataclass
class Input(Container):
    settings: Settings
        
    def __post_init__(self):
        super().__post_init__()
        self.set_children()
        return

    @staticmethod
    def from_dict(obj: Any):
        assert isinstance(obj, dict)
        settings = Settings.from_dict(obj.get("settings"))
        
        return Input(settings)

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


if __name__ == "__main__":
    test_component_and_post_inits()