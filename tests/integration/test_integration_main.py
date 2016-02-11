
from django.test import  TransactionTestCase
from django.contrib.auth.models import User


class UserItengrationTest(TransactionTestCase):
    reset_sequences = True
    def test_user_pk(self):
        user = User.objects.create(first_name="test")
        self.assertEqual(user.pk,1)