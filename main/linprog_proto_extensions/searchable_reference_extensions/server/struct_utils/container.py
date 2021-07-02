from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
import copy

from optopy.io_processing.struct_utils import Component
from dataclasses import dataclass, field


@dataclass
class Container(Component):
    def __post_init__(self):

        super().__post_init__()
        self._children_ = []

    @property
    def _children(self) -> List[Component]:
        return self._children_

    def add(self, component: Component) -> None:
        self._children_.append(component)
        component._parent_component = self

    def remove(self, component: Component) -> None:
        self._children_.remove(component)
        component._parent_component = None

    def is_composite(self) -> bool:
        return True

    # def get_children(self) ->List[Component]:
    #     return self._children

    def set_children(self) -> List[Component]:

        component_vars_copy = self.get_public_attributes(very_deep_copy=True)
        component_vars = self.get_public_attributes()

        for key, item in component_vars_copy.items():

            # if not key == '_children_':
            if isinstance(component_vars[key], list):
                [
                    self.add(sub_item)
                    for sub_item in component_vars[key]
                    if isinstance(sub_item, Component)
                ]

            elif isinstance(item, Component):
                self.add(component_vars[key])


    def operation(self) -> str:

        results = []
        for child in self._children_:
            results.append(child.operation())
        return f"Branch({'+'.join(results)})"

