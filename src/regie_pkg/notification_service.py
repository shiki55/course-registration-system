"""
This module provides a NotificationService class that
allows for the use of different notification strategies.
"""

from .email import NotificationStrategy


class NotificationService:
    """
    A class for sending notifications using a specified notification strategy.

    This class uses the strategy design pattern to allow the notification strategy
    to be changed easily and flexibly.

    Parameters:
    - NotificationStrategy (NotificationStrategy, optional): The notification strategy to
                                                             use for sending notifications.
                                                             Defaults to None.

    Attributes:
    - notif_strategy (NotificationStrategy): The notification strategy being used by the NotificationService.

    Methods:
    - send_notification: Send a notification
    """
    def __init__(self, notification_strategy: NotificationStrategy=None):
        self.notification_strategy = notification_strategy
    def send_notification(self):
        """Send a notification."""
        return self.notification_strategy.send()