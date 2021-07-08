from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
import uuid
import copy
from datetime import datetime

from .catalogue import Catalogue



@dataclass
class Component(ABC):

    def __post_init__(self):
        # super().__init__()
        self._parent_component_ = None
        self._uid = uuid.uuid4()


    @property
    def _parent_component(self) -> Component:
        return self._parent_component_


    @_parent_component.setter
    def _parent_component(self, parent_component: Component):
        self._parent_component_ = parent_component

    
    @property
    def _children(self) -> List[Component]:
        pass


    # def add(self, component: Component) -> None:
    #     pass
    # def remove(self, component: Component) -> None:
    #     pass

    def is_composite(self) -> bool:
        return False


    def ls(self) -> List[Component]:
        return self._children


    def set_children(self):
        pass


    @abstractmethod
    def operation(self) -> str:
        pass


    def to_dict(self) -> dict:
        result: dict = {}

        attributes = self.get_public_attributes()

        for key, atrib in attributes.items():

            if hasattr(atrib, "to_dict"):
                result[key] = atrib.to_dict()
            elif isinstance(atrib, list):

                item_result = list()
                for item in atrib:
                    if  hasattr(item, "to_dict"):
                        item_result.append(item.to_dict())
                    elif isinstance(item, datetime):
                        if item.tzinfo is not None:
                            ts = item.replace(tzinfo=None)
                        else:
                            ts = item
                        item_result.append(ts.isoformat("T") + "Z")
                    else:
                        item_result.append(item)

                result[key] = item_result
            
            elif isinstance(atrib, datetime):
                if atrib.tzinfo is not None:
                    ts = atrib.replace(tzinfo=None)
                else:
                    ts = atrib
                result[key] =  ts.isoformat("T") + "Z"

            else:
                if atrib is not None:
                    result[key] = atrib

        return result
    

    def get_public_attributes(self, very_deep_copy=False):
        component_vars = {
            k: v
            for k, v in vars(self).items()
            if not (k.startswith("_") or callable(v))
        }

        # component_vars=vars(self)
        # # component_vars_copy=component_vars.copy()  ## it does not work why??
        # # component_vars_list= list(component_vars.values())
        # # component_vars_copy=component_vars_list[:]
        # component_vars_copy = copy.deepcopy(component_vars)

        if very_deep_copy:
            return copy.deepcopy(component_vars)
        else:
            return component_vars

    def add_hierarchy(self, hierarchy):

        self._hierarchy = hierarchy
        hierarchy.register_component(self)
        for componenet in self._children:
            componenet.add_hierarchy(hierarchy)
