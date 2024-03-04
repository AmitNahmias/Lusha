from functools import lru_cache

import phonenumbers
import pycountry

from logger import setup_logger

LOGGER = setup_logger(__name__)


def parse_country_code(phone_number: str, location: str) -> str | None:
    """
    Parse country code from input number or based the given location.

    :param location: Input location, could be country name or code.
    :param phone_number: Input phone number.
    :return: The country code.
    """
    try:
        parsed_number = phonenumbers.parse(phone_number)
        country_code: str = phonenumbers.region_code_for_country_code(parsed_number.country_code)

    except phonenumbers.phonenumberutil.NumberParseException:
        country_code = get_country_code(location)

    return country_code


@lru_cache(maxsize=500)
def get_country_code(country_name: str) -> str | None:
    """
    Gets country name or code and returns matched country code.

    :param country_name: The country to search for.
    :return: The matched country code.
    """
    if country_name:
        try:
            country_code = pycountry.countries.lookup(country_name.strip())
            # LOGGER.info(f'Found {country_code.alpha_2 =} for {country_name =}')
            return country_code.alpha_2
        except LookupError:
            LOGGER.warning(f"There is no country code for '{country_name}'.")


parse_country_code('003-574-4213', 'SE')
