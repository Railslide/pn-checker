import unittest
from main import PNValidityChecker


class PNValidityCheckerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.validity_checker = PNValidityChecker()

    def test_calculate_control_digit(self):
        control_digit = self.validity_checker._calculate_control_digit("8112189876")
        expected = 6
        assert control_digit == expected, f"Expected control digit was {expected}, actual was {control_digit}"

    def test_identify_number_type_person(self):
        assert self.validity_checker._identify_number_type("20170110") == "personnummer"

    def test_identify_number_type_samordningnummer(self):
        number_type = self.validity_checker._identify_number_type("19091079")
        assert number_type == "samordningnummer", f"{number_type}"

    def test_identify_number_type_company(self):
        assert self.validity_checker._identify_number_type("556614") == "company"

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
            assert self.validity_checker.verify(pn) is True, \
                f"Validity check for {pn} failed. Expected: True, actual: False"

    def test_valid_company_number(self):
        valid_numbers = (
            "556614-3185",
            "16556601-6399",
            "262000-1111",
            "857202-7566",
        )

        for n in valid_numbers:
            assert self.validity_checker.verify(n) is True, \
                f"Validity check for {n} failed. Expected: True, actual: False"

    def test_valid_samordningnummer(self):
        number = "190910799824"

        assert self.validity_checker.verify(number) is True, \
            f"Validity check for {number} failed. Expected: True, actual: False"

    def test_invalid_personnumer(self):
        invalid_numbers = (
            "201701272394",
            "190302299813",
            "030229+9813",
            "18900118+9811"
        )
        for pn in invalid_numbers:
            assert self.validity_checker.verify(pn) is False, \
                f"Validity check for {pn} failed. Expected: False, actual: True"
