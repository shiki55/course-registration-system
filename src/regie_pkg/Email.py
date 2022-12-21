from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    """
    An abstract base class for notification strategies.

    This class defines the interface for sending notifications using
    different strategies, such as email or SMS.
    Subclasses of this class must implement the `send` method.
    """
    @abstractmethod
    def send(self):
        """
        Sends a notification using the specified strategy.

        This method should be implemented by subclasses to send a
        notification using the strategy specific to that subclass.
        """

class Email(NotificationStrategy):
    """
    A class representing an email notification strategy.

    This class implements the `send` method of the NotificationStrategy
    class to send an email notification. It takes in the sender, recipient,
    subject, and body of the email, as well as an optional list of CC recipients.
    """
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
        """Send an email"""

        return {
            "sender": self.__sender,
            "to": self.__to,
            "cc": self.__cc,
            "subject": self.__subject,
            "body": self.__body,
        }