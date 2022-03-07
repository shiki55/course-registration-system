from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    @abstractmethod
    def send(self):
        pass

class Email(NotificationStrategy):
    def __init__(self, sender, to, subject, body, cc=None):
        self.__sender = sender
        self.__to = to
        if cc is None:
            self.__cc = []
        else:
            self.__cc = cc 
        self.__subject = subject
        self.__body = body

    def send(self):
        '''email send implementation'''
        
        return {
            "sender": self.__sender,
            "to": self.__to,
            "cc": self.__cc,
            "subject": self.__subject,
            "body": self.__body,
        }