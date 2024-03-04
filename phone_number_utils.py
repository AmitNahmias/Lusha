import phonenumbers

from country_code_utils import get_country_code


def parse_phone_number(phone_number: str, region: str, api_mode=False) -> str | None:
    """
    Parsing phone number to unified structure with Google's API.

    :param phone_number: Input phone number.
    :param region: Location/country code if there is.
    :param api_mode: In api mode the function will try to 'clean' the number if she can.
    :return: Phone number.
    """
    try:
        # Parsing the phone number
        parsed_number = phonenumbers.parse(phone_number)
        return f"{parsed_number.country_code}{parsed_number.national_number}"

    except phonenumbers.phonenumberutil.NumberParseException:
        # Converting location to country code, for example United States to US
        country_code = get_country_code(country_name=region)

        if country_code:
            try:
                # If basic parsing failed trying with the location
                parsed_number = phonenumbers.parse(phone_number, region=country_code)
                return f"{parsed_number.country_code}{parsed_number.national_number}"
            except phonenumbers.phonenumberutil.NumberParseException:
                pass

    return phone_number if api_mode else None
