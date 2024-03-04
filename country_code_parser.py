import phonenumbers


def parse_country_code(phone_number: str) -> str:
    """
    Parse country code from input number.

    :param phone_number: Input phone number.
    :return: The country code.
    """
    try:
        parsed_number = phonenumbers.parse(phone_number)
        return phonenumbers.region_code_for_country_code(parsed_number.country_code)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        return None
