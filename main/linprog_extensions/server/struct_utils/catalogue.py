from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


from dataclasses import dataclass

# @dataclass
class Catalogue:
    catalogue_items_dict = dict()

    def __new__(cls, component, hierarchy_name,  *args, **kwargs):
        # component_item = cls.components_dict.get(component_id)
        hierarchy_catalogue = cls.catalogue_items_dict.get(hierarchy_name)

        # if not component_item:
        #     component_item = super().__new__(cls)
        #     cls.components_dict[component_id] = component_item
        # return component_item
        if not hierarchy_catalogue:
            hierarchy_catalogue = dict()
            cls.catalogue_items_dict[hierarchy_name] = hierarchy_catalogue
            catalogue_item = None
        else:
            catalogue_item = hierarchy_catalogue.get(component._uid)

        if not catalogue_item:
            catalogue_item = super().__new__(cls)
            cls.catalogue_items_dict[hierarchy_name][component._uid] = catalogue_item

        return catalogue_item

    def __init__(self,  component, hirarchy_name):

        if not hasattr(self, "initted"):
            self.id = component._uid
            self.component_name = component.name if hasattr(component, "name") else ""
            # self.component_class_name = (
            #     component.class_name if hasattr(component, "class_name") else ""
            # )
            self.component = component
            self.initted = True

    @classmethod
    def list_components(cls, hierarchy_name):

        # return cls.components_dict
        return cls.catalogue_items_dict[hierarchy_name]


    @classmethod
    def get_component(cls, hierarchy_name, component_id):

        # return cls.components_dict[component_id]
        return cls.catalogue_items_dict[hierarchy_name][component_id]


    @staticmethod
    def add_component_to_catalogue(component, hierarchy_name):
        # assert(isinstance(component,Component))
        Catalogue(component, hierarchy_name)

    @classmethod
    def find_components(cls, hierarchy_name, component_name=None, component_class_name=None):

        # if component_name:
            # for key, item in cls.components_dict.items():
            #     if item.component_name == component_name:
            #         return {key: item.component}

            # return {}
        if component_name:

            for key, item in cls.catalogue_items_dict[hierarchy_name].items():
                if component_name in item.component_name:
                    return {key: item.component}

            return {}


    @classmethod
    def purge(cls, hierarchy_name):

        # cls.components_dict = dict()
        cls.catalogue_items_dict[hierarchy_name] = dict()
        return
