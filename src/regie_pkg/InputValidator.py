from abc import ABC, abstractmethod
from typing import Tuple

# InputValidator interface
class InputValidator(ABC):
    @abstractmethod
    def is_valid(self, input_val: str) -> Tuple:
        '''return (str, bool) -> (error message, True if valid otherwise False)'''
        pass


class StudentIDInputValidator:
    def is_valid(self, input_val: str)-> Tuple:
        if input_val.strip().isdigit():
            return '', True
        return "Student ID must be an integer. Please try again.", False

class MenuChoiceInputValidator:
    __menu_options = ['1', '2', '3', '4', '5', '6', '7', '8']
    def is_valid(self, input_val: str)-> Tuple:
        if not input_val.strip().isdigit():
            return "Entered choice must be an integer. Please try again.", False
        elif input_val.strip() in self.__menu_options:
            return '', True
        else:
            return "Invalid choice, try again.", False

class CouseIDInputValidator:
    def is_valid(self, input_val: str)-> Tuple:
        if not input_val.strip().isdigit() or len(input_val) != 8:
            return "Course section/lab id must be an eight digit number. Please try again.", False
        return '', True

class ValidationExecutor:
    def __init__(self, input_validator: InputValidator=None):
        self.input_validator = input_validator

    def set_validator(self, input_validator: InputValidator):
        self.input_validator = input_validator
    
    def validate(self, input_val: str) -> Tuple:
        return self.input_validator.is_valid(input_val=input_val)

