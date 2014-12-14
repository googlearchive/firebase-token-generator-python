try:
    basestring
except NameError:  # Python 3
    basestring = str
from firebase_token_generator import create_token
import unittest

class TestTokenGenerator(unittest.TestCase):

    def test_smoke_test(self):
        token = create_token("barfoo", {"uid": "foo"})
        self.assertIsInstance(token, basestring)

    def test_malformed_key(self):
        with self.assertRaises(ValueError):
            token = create_token(1234567890, {"uid": "foo"})

    def test_no_uid(self):
        with self.assertRaises(ValueError):
            token = create_token("barfoo", {"blah": 5})

    def test_invalid_uid(self):
        with self.assertRaises(ValueError):
            token = create_token("barfoo", {"uid": 5, "blah": 5})

    def test_uid_max_length(self):
        #length:                                        10        20        30        40        50        60        70        80        90       100       110       120       130       140       150       160       170       180       190       200       210       220       230       240       250   256
        token = create_token("barfoo", {"uid": "1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456"})
        self.assertIsInstance(token, basestring)

    def test_uid_too_long(self):
        with self.assertRaises(ValueError):
            #length:                                        10        20        30        40        50        60        70        80        90       100       110       120       130       140       150       160       170       180       190       200       210       220       230       240       250    257
            token = create_token("barfoo", {"uid": "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567"})

    def test_uid_min_length(self):
        token = create_token("barfoo", {"uid": ""})
        self.assertIsInstance(token, basestring)

    def test_token_too_long(self):
        with self.assertRaises(RuntimeError):
            create_token("barfoo", {"uid": "blah", "long_var": "123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345612345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234561234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456"})

    def test_no_uid_with_admin(self):
        token = create_token("barfoo", None, {"admin": True})
        self.assertIsInstance(token, basestring)
        token = create_token("barfoo", {}, {"admin": True})
        self.assertIsInstance(token, basestring)
        token = create_token("barfoo", {"foo": "bar"}, {"admin": True})
        self.assertIsInstance(token, basestring)

    def test_invalid_uid_with_admin(self):
        with self.assertRaises(ValueError):
            token = create_token("barfoo", {"uid": 1}, {"admin": True})
        with self.assertRaises(ValueError):
            token = create_token("barfoo", {"uid": None}, {"admin": True})
        with self.assertRaises(ValueError):
            token = create_token("barfoo", "foo", {"admin": True})

if __name__ == '__main__':
    unittest.main()
