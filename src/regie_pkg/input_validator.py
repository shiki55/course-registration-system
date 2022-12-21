"""
This module contains classes for input validation.

The InputValidator class is an abstract base class that defines the interface for input validation.
Concrete implementations of InputValidator include StudentIDInputValidator,
MenuChoiceInputValidator, and CourseIDInputValidator.
"""

from abc import ABC, abstractmethod
from typing import Tuple

# InputValidator interface
class InputValidator(ABC):
    """
    Abstract base class for input validators.
    All input validators must implement the `is_valid` method.
    """
    @abstractmethod
    def is_valid(self, input_val: str) -> Tuple[str, bool]:
        """
        Check if the given input value is valid.

        Parameters:
            input_val (str): The input value to be validated.

        Returns:
            Tuple[str, bool]: A tuple containing an error message (if any)
                              and a boolean indicating whether the input value is valid.
        """


class StudentIDInputValidator(InputValidator):
    """Input validator for student IDs. Student IDs must be integers."""
    def is_valid(self, input_val: str)-> Tuple[str, bool]:
        if input_val.strip().isdigit():
            return '', True
        return "Student ID must be an integer. Please try again.", False

class MenuChoiceInputValidator(InputValidator):
    """
    Input validator for menu choices.
    Menu choices must be integers and must be one of the valid options.
    """
    __menu_options = ['1', '2', '3', '4', '5', '6', '7', '8']
    def is_valid(self, input_val: str)-> Tuple[str, bool]:
        if not input_val.strip().isdigit():
            return "Entered choice must be an integer. Please try again.", False
        elif input_val.strip() in self.__menu_options:
            return '', True
        else:
            return "Invalid choice, try again.", False

class CouseIDInputValidator(InputValidator):
    """Input validator for course IDs. Course IDs must be eight-digit integers."""
    def is_valid(self, input_val: str)-> Tuple[str, bool]:
        if not input_val.strip().isdigit() or len(input_val) != 8:
            return "Course section/lab id must be an eight digit number. Please try again.", False
        return '', True

class ValidationExecutor:
    """Class for executing input validation using an `InputValidator`."""
    def __init__(self, input_validator: InputValidator=None):
        self.input_validator = input_validator

    def set_validator(self, input_validator: InputValidator):
        """Set the `InputValidator`."""
        self.input_validator = input_validator

    def validate(self, input_val: str) -> Tuple[str, bool]:
        """Validate the given input"""
        return self.input_validator.is_valid(input_val=input_val)
