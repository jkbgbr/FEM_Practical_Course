import numpy as np
from typing import Tuple


class IDMixin:
    """
    This mixin class provides a unique ID for each element and keeps track of the IDs in a class variable ID_counter.

    The unique IDs are required to identify the elements and nodes in the global stiffness matrix and force vector and
    so to be able to use the assemble_* functions.

    If you implemented a new element or node class, you must inherit from this class and call

    super().__init__(__class__.__name__)  # Call the IDMixin constructor to set the ID

    """
    ID_counter = {}  # class variable to keep track of the ID of the element and node

    def __init__(self, class_name: str):
        IDMixin.register_class(class_name)
        _id = IDMixin.ID_counter.get(class_name)  # set the ID of the element or node
        if _id is None:
            raise ValueError(f"IDMixin: Class {class_name} not found in ID_counter.")
        self.ID = _id
        IDMixin.ID_counter[class_name] += 1  # increment the ID counter for the next element or node

    @classmethod
    def register_class(cls, class_name: str):
        """
        Register a new class in the ID_counter dictionary.
        This is useful if you implement a new element or node class that should have unique IDs.

        :param class_name: Name of the class to register
        """
        if class_name not in cls.ID_counter:
            cls.ID_counter[class_name] = 0

    @classmethod
    def reset(cls):
        """
        Resets the IDs of the elements and nodes to 0.
        This is useful for testing purposes to ensure that the IDs are consistent across tests.

        :return:
        """
        cls.ID_counter = {}
