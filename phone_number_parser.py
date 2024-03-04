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
def _get_country_code(country_name: str) -> str | None:
    """
    Gets country name or code and returns matched country code.

    :param country_name: The country to search for.
    :return: The matched country code.
    """
    if country_name:
        try:
            country = pycountry.countries.lookup(country_name.strip())
            return country.alpha_2
        except LookupError:
            LOGGER.warning(f"There is no country code for '{country_name}'.")
