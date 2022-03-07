from .Email import NotificationStrategy


class NotificationService:
    '''strategy design pattern'''
    def __init__(self, NotificationStrategy: NotificationStrategy=None):
        self.notif_strategy = NotificationStrategy
    def send_notification(self):
        return self.notif_strategy.send()