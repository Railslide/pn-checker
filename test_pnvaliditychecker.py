import unittest
from main import PNValidityChecker

class SubvenvTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.validity_checker = PNValidityChecker()

    def test_calculate_control_digit(self):
        control_digit = self.validity_checker._calculate_control_digit("8112189876")
        expected = 6
        assert control_digit == expected, f"Expected control digit was {expected}, received was {control_digit}"

    def test_valid_personnummer(self):
        valid_personnumer = (
            "201701102384",
            "141206-2380",
            "20080903-2386",
            "7101169295",
            "198107249289",
            "19021214-9819",
            "190910199827",
            "191006089807",
            "192109099180",
            "4607137454",
            "194510168885",
            "900118+9811",
            "189102279800",
            "189912299816",
        )

        for pn in valid_personnumer:
            assert self.validity_checker.verify(pn) is True, pn

