import argparse
import datetime
import re


class IdentityNumberValidationError(Exception):
    pass


class IdentityNumberValidityChecker:
    """Validity checker for identity numbers"""

    def verify(self, identity_number):
        """
        Verify if an identity number is valid

        :param self:
        :param identity_number: (str) a string representing an identity number
        :return: (bool) whether an identity number is valid
        """
        try:
            self._validate(identity_number)
        except IdentityNumberValidationError:
            print(f"{identity_number} is invalid")
            return False

        print(f"{identity_number} is valid")
        return True

    def _validate(self, identity_number):
        """
        Validate an identity number

        :param identity_number: (str) a string representing an identity number
        :return: None
        :raises: IdentityNumberValidationError if validation fails
        """
        if not re.match(r"^(\d{6}[-+]?|\d{8}-?)\d{4}$", identity_number):
            raise IdentityNumberValidationError("Invalid format")

        digits_only = identity_number.replace("-", "").replace("+", "")
        ten_digits_number = digits_only[-10:]

        control_digit = int(ten_digits_number[-1])
        if control_digit != self._calculate_control_digit(ten_digits_number):
            raise IdentityNumberValidationError("Invalid identity number")

        date_part = digits_only[:-4]
        number_type = self._identify_number_type(digits_only)
        if number_type == "organisationsnummer":
            return
        elif number_type == "samordningsnummer":
            actual_day_of_birth = int(date_part[-2:]) - 60
            date_part = f"{date_part[:-2]}{actual_day_of_birth}"

        hundred_plus_year_old = "+" in identity_number
        if not self._check_is_valid_date_of_birth(date_part, hundred_plus_year_old):
            raise IdentityNumberValidationError("Invalid date of birth")

    @staticmethod
    def _calculate_control_digit(identity_number):
        """
        Calculate control digit for an identity number using Luhn algorythm

        :param identity_number: (str) a string representing an identity number
        :return: (int) the calculated control digit
        """
        total_sum = 0
        for index, digit_string in enumerate(identity_number[:-1]):
            digit = int(digit_string)
            if index % 2 == 0:
                digit = 2 * digit
                if digit > 9:
                    digit = digit - 9
            total_sum += digit
        return (10 - (total_sum % 10)) % 10

    @staticmethod
    def _identify_number_type(identity_number):
        """
        Identify the type of identity number

        :param identity_number: (str) a string representing an identity number
        :return: (str) identity number type (i.e personnummer, organisationnumer, or samordningsnummer)
        """
        # Slicing from the end of the string, so that it works for both YYMMDDXXXX and YYYYMMDDXXXX
        date_string = identity_number[:-4]
        month = int(date_string[-4:-2])
        day = int(date_string[-2:])

        if month >= 20:
            return "organisationsnummer"
        if 61 <= day <= 91:
            return "samordningsnummer"

        return "personnummer"

    @staticmethod
    def _check_is_valid_date_of_birth(date_string, is_100_plus_short_date=False):
        """
        Check if the provided date of birth is a valid date

        :param date_string: (str) date of birth either as YYYYMMDD or YYMMDD
        :param is_100_plus_short_date: (bool) whether the date is for a 100+ years old person and in the YYMMDD format
        :return: (bool) whether the date of birth is a valid one
        :raises: IdentityNumberValidationError if date is not valid
        """
        if len(date_string) == 8:
            date_fmt = "%Y%m%d"
        elif len(date_string) == 6:
            date_fmt = "%y%m%d"
        else:
            return False

        try:
            if is_100_plus_short_date:
                if date_string.endswith("0229"):
                    # Picking January 1 as we know for sut that it exists even if it's not a leap year.
                    # This is to avoid the corner case of 100+ year person born on February 29
                    year = int(date_string[:2])
                    first_day_of_year_of_birth = datetime.datetime(year=year, month=1, day=1)
                    datetime.datetime(year=first_day_of_year_of_birth.year-100, month=2, day=29)
                    return True

                closest_date = datetime.datetime.strptime(date_string, date_fmt)
                closest_date.replace(year=closest_date.year-100)
                return True

            datetime.datetime.strptime(date_string, date_fmt)
        except ValueError:
            raise IdentityNumberValidationError("Invalid date of birth")

        return True


def main():
    parser = argparse.ArgumentParser(description="Checks identity number validity")
    parser.add_argument(
        'identity_numbers',
        metavar='N',
        type=str,
        nargs='+',
        help="One or more identity numbers to be checked, space separated."
    )
    args = parser.parse_args()
    checker = IdentityNumberValidityChecker()
    for number in args.identity_numbers:
        checker.verify(number)


if __name__ == "__main__":
    main()
