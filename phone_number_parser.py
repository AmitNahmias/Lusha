import phonenumbers
import pycountry
from functools import lru_cache

from logger import setup_logger

LOGGER = setup_logger(__name__)


def parse_phone_number(phone_number: str, region: str) -> str | None:
    try:
        # Parsing the phone number
        parsed_number = phonenumbers.parse(phone_number)
        return f"{parsed_number.country_code}{parsed_number.national_number}"

    except phonenumbers.phonenumberutil.NumberParseException:
        country_code = _get_country_code(country_name=region)
        if country_code:
            try:
                parsed_number = phonenumbers.parse(phone_number, region=country_code)
                return f"{parsed_number.country_code}{parsed_number.national_number}"
            except phonenumbers.phonenumberutil.NumberParseException:
                pass

        return None


@lru_cache
def _get_country_code(country_name: str) -> str:
    """
    Gets country name or code and returns matched country code.

    :param country_name: The country to search for.
    :return: The matched country code.
    """
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2
    except LookupError as lookup_error:
        # LOGGER.exception(lookup_error)
        # LOGGER.error(f"Country '{country_name}' not found.")
        return None
