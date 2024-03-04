import re
from typing import List

import spacy

from logger import setup_logger

WORDS_TO_EXCLUDE = \
    [
        "Miss", "Ms", "Mrs", "Mr", "Dr", "Prof", "Eng",
        "Doc", "PhD", "MD", "DDS", "JD", "DVM", ".",
        "Sr", "Hon", "Jr",
        "RN",  # Registered Nurse
        "CPA",  # Certified Public Accountant
        "Esq",  # Esquire
        "MBA",  # Master of Business Administration
        "MA",  # Master of Arts
        "MSc",  # Master of Science
        "BSc",  # Bachelor of Science
        "BA",  # Bachelor of Arts
        "LLB",  # Bachelor of Laws
        "LLM",  # Master of Laws
        "PharmD",  # Doctor of Pharmacy
    ]

# Load the English language model
NLP = spacy.load("en_core_web_sm")


def _remove_titles_and_emojis(text: str) -> str:
    # Remove emojis
    text_without_emojis = ''.join(c for c in text if ord(c) < 128)

    # Remove titles
    for title in WORDS_TO_EXCLUDE:
        text_without_emojis = text_without_emojis.replace(title, '')

    return text_without_emojis.strip().replace('  ', ' ')


def extract_name(text: str) -> str:
    """
    Gets a text and extract name if exists.

    :param text: Input text.
    :return: Name.
    """
    # Remove emojis from the text
    text = _remove_titles_and_emojis(text)

    if len(text.split()) > 2:  # more than two words --> more than name
        # Process the text with spaCy
        doc = NLP(text)

        # Extract entities labeled as PERSON
        names: List = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]

        # If no PERSON entity found, return None
        if not names:
            LOGGER.warning(f'Did not find name inside {text =}')
            return None
    else:  # only the name --> reduce using in spacy
        names: List = [text]

    # Sort the cleaned names alphabetically
    # Also enforced camel case name to keep on unified name structure, for example Amit Nahmias and not Amit nahmias
    result_name = ' '.join(sorted(names[0].strip().split(), key=str.lower)).title()
    return result_name
