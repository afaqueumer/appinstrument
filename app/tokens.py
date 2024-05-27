import re


def get_token_count(text):
    # Use regular expression to split the text into tokens
    tokens = re.findall(r'\b\w+\b', text)
    return len(tokens)
