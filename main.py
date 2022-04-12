import re


class PNValidityChecker:
    def __init__(self):
        pass # TODO: Remove?

    def verify(self, identity_number):
        try:
            self._validate(identity_number)
        except ValueError as e:
            print(e) # TODO: log instead of printing?
            return False

        return True

    def _validate(self, identity_number):
        if not re.match(r"^\d{6,8}[-\+]?\d{4}$", identity_number):
            raise ValueError("Invalid format")

        digits_only = identity_number.replace("-", "").replace("+", "")
        ten_digits_number = digits_only[-10:]

        control_digit = int(ten_digits_number[-1])
        if control_digit != self._calculate_control_digit(ten_digits_number):
            raise ValueError("Invalid identity number")

    def _calculate_control_digit(self, identity_number):
        total_sum = 0
        for index, digit_string in enumerate(identity_number[:-1]):
            digit = int(digit_string)
            if index % 2 == 0:
                digit = 2 * digit
                if digit > 9:
                    digit = digit - 9
            total_sum += digit
        return (10 - (total_sum % 10)) % 10
