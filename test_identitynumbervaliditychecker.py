import unittest
from identity_number_checker import IdentityNumberValidityChecker


class IdentityNumberValidityCheckerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.validity_checker = IdentityNumberValidityChecker()

    def test_calculate_control_digit(self):
        control_digit = self.validity_checker._calculate_control_digit("8112189876")
        expected = 6
        assert control_digit == expected, f"Expected control digit was {expected}, actual was {control_digit}"

    def test_identify_number_type_person(self):
        number_type = self.validity_checker._identify_number_type("201701102384")
        assert number_type == "personnummer", f"Expected type was personnummer, actual was {number_type}"

    def test_identify_number_type_samordningsnummer(self):
        number_type = self.validity_checker._identify_number_type("190910799824")
        assert number_type == "samordningsnummer", f"Expected type was samordningsnummer, actual was {number_type}"

    def test_identify_number_type_company(self):
        number_type = self.validity_checker._identify_number_type("5566143185")
        assert number_type == "organisationsnummer",\
            f"Expected type was organisationsnummer, actual was {number_type}"

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

    def test_valid_samordningsnummer(self):
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
