from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass, field
import uuid
import copy
from datetime import datetime

from optopy.io_processing.struct_utils import Catalogue

from optopy.io_processing.structs.quicktype_mini_funcs import from_list


@dataclass
class Component(ABC):
    # name: str = field(default_factory=str)
    # parent: str = field(default_factory=str)
    # class_name: str = field(default_factory=str)
    # creates a whole lot of trouble when combined with non-optional fileds of elements

    def __post_init__(self):
        # super().__post_init__()
        # self.name = None
        # self.parent = None
        # self.class_name = None
        # if an element has name/etc it will be called before this post-init, so this one will make it None        
        self._parent_component_ = None
        self._uid = uuid.uuid4()

        # Catalogue.add_component_to_catalogue(self)

    @property
    def _parent_component(self) -> Component:
        return self._parent_component_

    @_parent_component.setter
    def _parent_component(self, parent_component: Component):
        self._parent_component_ = parent_component

    def add(self, component: Component) -> None:
        pass

    def remove(self, component: Component) -> None:
        pass

    def is_composite(self) -> bool:
        return False

    @property
    def _children(self) -> List[Component]:
        pass

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
    



    def to_flat_dict(self) -> dict:
        result = list()
        attributes = self.get_public_attributes()

        for _, atrib in attributes.items():

            if isinstance(atrib, Component):
                result += atrib.to_flat_dict()
            elif isinstance(atrib, list):
                for list_item in atrib:
                    if isinstance(list_item, Component):
                        result += list_item.to_flat_dict()
        
        if (hasattr(self, "name") and hasattr(self, "class_name")):
        # if (self.name and self.class_name):
            object_dict = dict()
            object_dict["name"] = self.name
            object_dict["class_name"] = self.class_name

            try:
                object_dict["class_dependencies"]  = self.class_dependencies.to_dict()

            except:
                pass


            # if self.parent:
            if hasattr(self, "parent"):
                object_dict["parent"] = self.parent
            elif self._parent_component_:
                if hasattr(self._parent_component_, "name"):
                    object_dict["parent"] = self._parent_component_.name
                else:
                    object_dict["parent"] = None


            else:
                ValueError(" could not find the object's parent element")
            
            args = dict()

            for key, atrib in attributes.items():

                if key in ["name", "class_name", "parent", "class_dependencies"]:
                    continue
                
                elif isinstance(atrib, list):
                    if len(atrib) == 0:
                        args[key] = atrib
                        continue
                    
                    if isinstance(atrib[0], Component):
                        if atrib[0].is_composite():
                            continue
                        # else:
                        #     args[key] = [content_item.to_dict() for content_item in atrib]
                    else:
                        if hasattr(atrib[0], "to_dict"):
                            args[key] =[item.to_dict() for  item in atrib]
                            
                        else:
                            args[key] = atrib

                elif not (isinstance(atrib, Component)):

                    if hasattr(atrib, "to_dict"):
                        args[key] = atrib.to_dict()
                    else:
                        if atrib is not None:
                            args[key] = atrib
                
                elif (isinstance(atrib, Component)) and not (atrib.is_composite()):
                    # args[key] = atrib.to_dict()
                    ValueError("This should not happen!")
                
            
            object_dict["args"] = args
            result.append(object_dict)    

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
