from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

import networkx as nx
import uuid

from .catalogue import Catalogue



class Hierarchy:

    def __init__(self, name):
        self.hierarchy_name = name
        self.graph = nx.Graph()
        return

    def register_component(self, component):

        Catalogue.add_component_to_catalogue(component, self.hierarchy_name)
        return


@dataclass
class HierarchyMixin:

    def __post_init__(self):

        hierarchy_name = self.__class__.__name__+ str(uuid.uuid4())
        self._hierarchy = Hierarchy(hierarchy_name)
        super().__post_init__()
        return

    def populate_hierarchy(self):
    
        for componenet in self._children:
            componenet.add_hierarchy(self._hierarchy)
        return
