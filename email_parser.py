import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')


def extract_name_from_email(email):
    # Tokenize the email address
    tokens = word_tokenize(email)
    # Perform part-of-speech tagging
    tagged_tokens = pos_tag(tokens)

    # Extract proper nouns (NNP) and join them as the name
    name_tokens = [word for word, pos in tagged_tokens if pos == 'NNP']
    if name_tokens:
        return ' '.join(name_tokens)
    else:
        return None


extract_name_from_email('christopherrose@example.org')
