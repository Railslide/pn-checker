import argparse
import datetime
import re


class IdentityNumberValidationError(Exception):
    pass


class PNValidityChecker:

    def verify(self, identity_number):
        try:
            self._validate(identity_number)
        except IdentityNumberValidationError as e:
            print(e)
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
            raise IdentityNumberValidationError("Invalid identity number")

        date_part = digits_only[:-4]
        number_type = self._identify_number_type(date_part)
        if number_type == "company":
            return
        elif number_type == "samordningnummer":
            actual_day_of_birth = int(date_part[-2:]) - 60
            date_part = f"{date_part[:-2]}{actual_day_of_birth}"

        if not self._check_is_valid_date_of_birth(date_part, True):
            raise IdentityNumberValidationError("Invalid date of birth")

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

    def _identify_number_type(self, date_string):
        # Slicing from the end of the string, so that it works for both YYMMDD and YYYYMMDD
        month = int(date_string[-4:-2])
        day = int(date_string[-2:])

        if month >= 20:
            return "company"
        if 61 <= day <= 91:
            return "samordningnummer"

        return "personnummer"

    def _check_is_valid_date_of_birth(self, date_string, is_100_plus_short_date=False):
        if len(date_string) == 8:
            date_fmt = "%Y%m%d"
        elif len(date_string) == 6:
            date_fmt = "%y%m%d"
        else:
            return False
        try:
            datetime.datetime.strptime(date_string, date_fmt)
        except ValueError:
            raise IdentityNumberValidationError("Invalid date of birth")

        return True
        # if is_100_plus_short_date and  date_string.endswith("0229"):
        #    date_string = f"{date_string[:2]}0101"
        # if "+" in identity_number:
        #     try:
        #         # Picking January 1 as we know for sut that it exists even if it's a leap year.
        #         # This is to avoid the corner case of 100+ year person born on February 29
        #         import pdb; pdb.set_trace()
        #         dummy_date = datetime.date(year, 1, 1).strftime("%Y%d%m")
        #         dummy_date.replace(year=dummy_date.year-100, month=month, day=day)
        #         return True
        #     except ValueError:
        #         return False
        # try:
        #     datetime.date(year=year, month=month, day=day)
        # except ValueError:
        #     print(year, month, day)
        #     return False
        #
        # return True

# @TODO: Log invalid numbers


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
