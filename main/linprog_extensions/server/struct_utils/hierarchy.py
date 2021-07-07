from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

import uuid
from .catalogue import Catalogue

import networkx as nx


class Hierarchy:

    def __init__(self, name):
        self.hierarchy_name = name
        self.graph = nx.Graph()

        # self.add_hirarchy()
        # super().__post_init__()

    def register_component(self, component):
        # self.catalogue_item=  Catalogue( component,self.hirarchy_name)
        Catalogue.add_component_to_catalogue(component, self.hierarchy_name)
        return


@dataclass
class HierarchyMixin:

    def __post_init__(self):

        self._hierarchy = Hierarchy(self.__class__.__name__+ str(uuid.uuid4()))
        super().__post_init__()
        return

    def populate_hierarchy(self):

        for componenet in self._children:
            componenet.add_hierarchy(self._hierarchy)
        return
