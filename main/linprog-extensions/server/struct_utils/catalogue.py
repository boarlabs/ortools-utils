from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List

class Catalogue:
    catalogue_items_dict = dict()
    catalogue_items_list = dict()
    catalogue_tag_list = dict()

    def __new__(cls, component, hierarchy_name,  *args, **kwargs):

        hierarchy_catalogue = cls.catalogue_items_dict.get(hierarchy_name)
        hierarchy_items_list = cls.catalogue_items_list.get(hierarchy_name)
        # hierarchy_tag_list = cls.catalogue_tag_list.get(hierarchy_name)

        if not hierarchy_catalogue:
            hierarchy_catalogue = dict()
            hierarchy_items_list = list()
            # hierarchy_tag_list = list()
            cls.catalogue_items_dict[hierarchy_name] = hierarchy_catalogue
            cls.catalogue_items_list[hierarchy_name] = hierarchy_items_list
            # cls.catalogue_tag_list[hierarchy_name] = hierarchy_tag_list

            catalogue_item = None
        else:
            catalogue_item = hierarchy_catalogue.get(component._uid)

        if not catalogue_item:
            catalogue_item = super().__new__(cls)
            cls.catalogue_items_dict[hierarchy_name][component._uid] = catalogue_item
            hierarchy_items_list.append(catalogue_item)
            # hierarchy_tag_list.append(component._tags)

        return catalogue_item

    def __init__(self,  component, hirarchy_name):

        if not hasattr(self, "initted"):
            self.initted = True
            self.id = component._uid
            self.component_name = component.name if hasattr(component, "name") else ""
            # self.component_class_name = (
            #     component.class_name if hasattr(component, "class_name") else ""
            # )
            self.component = component
            self.tags = component._tags
        return

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
    def find_components(
        cls,
        hierarchy_name: str,
        component_name: str = None,
        # component_class_name: str = None,
        tag_list: list = None,
    ):
        matching_components = list()

        def tag_list_generator(hierarchy_name, search_tags):
            for item in cls.catalogue_items_list[hierarchy_name]:
                yield item.tags, search_tags, cls.catalogue_items_list[hierarchy_name].index(item)
        
        def find_matching_tags(args):
            tag_list = args[0]
            search_tags = args[1]
            catalogue_item_index = args[2]
            search_tags_set = set(search_tags)
            tag_list_set = set(tag_list)
            if (tag_list_set.intersection(search_tags_set) == search_tags_set):
                return cls.catalogue_items_list[hierarchy_name][catalogue_item_index].component
           

        if component_name:
            for key, item in cls.catalogue_items_dict[hierarchy_name].items():
                if component_name in item.component_name:
                    matching_components =  item.component
        
        if tag_list:
            matching_components =  list(
                filter(
                    None.__ne__,
                    map(
                        find_matching_tags,
                        tag_list_generator(hierarchy_name, tag_list),
                    ),
                )
            )

        return matching_components




        

        


    @classmethod
    def purge(cls, hierarchy):

        hierarchy_name = hierarchy._hierarchy.hierarchy_name
        _ = cls.catalogue_items_dict.pop(hierarchy_name)
        return
