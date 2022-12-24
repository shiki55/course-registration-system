import os, sys, inspect
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.notification_service import NotificationService
from regie_pkg.email import Email

class TestNotificationService:
    """A class for testing the NotificationService and Email classes"""

    def test_notification_service(self):
        """Test the send_notification method of the NotificationService class with email."""

        email = Email(
            sender="bisping@uchicago.edu",
            to="smith@uchicago.edu",
            cc=[],
            subject="approval request",
            body="I am requesting an approval to enroll in CS123"
        )
        notif_service =  NotificationService(notification_strategy=email)
        expected = {
            "sender": "bisping@uchicago.edu",
            "to":"smith@uchicago.edu",
            "cc": [],
            "subject":"approval request",
            "body":"I am requesting an approval to enroll in CS123"
            }
        assert notif_service.send_notification() == expected
