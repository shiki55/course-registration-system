import os, sys, inspect
import unittest
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.student import Student
from regie_pkg.notification_service import NotificationService
from regie_pkg.email import Email

class TestNotificationService(unittest.TestCase):
    def setUp(self): # ran before each method w/ prefix "test_"
        email = Email(
            sender="bisping@uchicago.edu",
            to="smith@uchicago.edu",
            cc=[],
            subject="approval request",
            body="I am requesting an approval to enroll in CS123"
        )
        self.notif_service1 = NotificationService(notification_strategy=email)

    def test_notification_service(self):
        expected = {
            "sender": "bisping@uchicago.edu",
            "to":"smith@uchicago.edu",
            "cc": [],
            "subject":"approval request",
            "body":"I am requesting an approval to enroll in CS123"
            }
        self.assertEqual(self.notif_service1.send_notification(), expected)


if __name__ == '__main__':
    unittest.main()