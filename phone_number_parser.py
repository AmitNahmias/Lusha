import phonenumbers

from country_code_parser import get_country_code


def parse_phone_number(phone_number: str, region: str) -> str | None:
    try:
        # Parsing the phone number
        parsed_number = phonenumbers.parse(phone_number)
        return f"{parsed_number.country_code}{parsed_number.national_number}"

    except phonenumbers.phonenumberutil.NumberParseException:
        country_code = get_country_code(country_name=region)
        if country_code:
            try:
                parsed_number = phonenumbers.parse(phone_number, region=country_code)
                return f"{parsed_number.country_code}{parsed_number.national_number}"
            except phonenumbers.phonenumberutil.NumberParseException:
                pass
        return None


