from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from optopy.io_processing.struct_utils import Component

from dataclasses import dataclass


@dataclass
class Content(Component):
    def __post_init__(self):

        super().__post_init__()

    @property
    def _children(self) -> List[Component]:
        return []

    def set_children(self):
        pass

    def operation(self) -> str:
        return "Operation Mp2"
