# -*- coding: utf-8 -*-
import mock

from django.core.management import call_command
from django.test import TestCase

from django.core.management.base import CommandError

from django.contrib.auth.models import User

TEST_USER_EMAIL = 'test_user@test.com'
REFERRER_EMAIL = 'test_user_no_staff@test.com'


class ResendWelcomeEmailTest(TestCase):
    fixtures = ['users']

    @mock.patch('seqr.utils.communication_utils.send_welcome_email')
    def test_command(self, mock_send_welcome_email):
        call_command('resend_welcome_email', '--email-address={}'.format(TEST_USER_EMAIL),
                     '--referrer={}'.format(REFERRER_EMAIL))
        user = User.objects.get(email=TEST_USER_EMAIL)
        referrer = User.objects.get(email=REFERRER_EMAIL)
        mock_send_welcome_email.assert_called_with(user, referrer)

    def test_command_exceptions(self):
        with self.assertRaises(CommandError) as ce:
            call_command('resend_welcome_email', '--email-address={}'.format(TEST_USER_EMAIL))
        self.assertEqual(ce.exception.message, 'Error: argument -r/--referrer is required')

        with self.assertRaises(CommandError) as ce:
            call_command('resend_welcome_email', '--referrer={}'.format(REFERRER_EMAIL))
        self.assertEqual(ce.exception.message, 'Error: argument -e/--email-address is required')
