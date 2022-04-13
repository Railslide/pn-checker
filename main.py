import argparse
import datetime
import re


class PNValidityChecker:

    def verify(self, identity_number):
        try:
            self._validate(identity_number)
        except ValueError as e:
            print(f"{identity_number} is invalid") # TODO: log instead of printing?
            return False

        print(f"{identity_number} is valid")
        return True

    def _validate(self, identity_number):
        if not re.match(r"^\d{6,8}[-\+]?\d{4}$", identity_number):
            raise ValueError("Invalid format")

        digits_only = identity_number.replace("-", "").replace("+", "")
        ten_digits_number = digits_only[-10:]
        control_digit = int(ten_digits_number[-1])
        if control_digit != self._calculate_control_digit(ten_digits_number):
            raise ValueError("Invalid identity number")

        # This only work for humans @TODO
        if not self._check_is_valid_date_of_birth(identity_number, digits_only):
            raise ValueError("Invalid date of birth")

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

    def _check_is_valid_date_of_birth(self, identity_number, digits_only):
        # Slicing from the end of the string, so that it works for both 10 and 12 digits numbers
        month = int(digits_only[-4:-2])
        day = int(digits_only[-2:])
        year = int(digits_only[:-4])

        if "+" in identity_number:
            try:
                # Picking January 1 as we know for sut that it exists even if it's a leap year.
                # This is to avoid the corner case of 100+ year person born on February 29
                dummy_date = datetime.date(year, 1, 1)
                dummy_date.replace(year=dummy_date-100, month=month, day=day)
                return True
            except ValueError:
                return False
        try:
            datetime.date(year=year, month=month, day=day)
        except ValueError:
            return False

        return True

# @TODO: Log invalid numbers
# @TODO: Handle samordning number
# @TODO: Handle companies

def main():
    parser = argparse.ArgumentParser(description="Checks identity number validity")
    parser.add_argument(
        'identity_numbers',
        metavar='N',
        type=str,
        nargs='+',
        help ="A space separated list of identity numbers to be checked"
    )
    args = parser.parse_args()
    checker = PNValidityChecker()
    for number in args.identity_numbers:
        checker.verify(number)


if __name__ == "__main__":
    main()
