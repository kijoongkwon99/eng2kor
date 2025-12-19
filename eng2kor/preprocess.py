# preprocessing.py

import re
from phonemizer import phonemize

PUNCTS = set("-.,:;?!()\"'")

def split_with_punct(text: str):
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if ch in PUNCTS:
            tokens.append((None, ch))
            i += 1
            continue

        j = i
        while j < n and text[j] not in PUNCTS:
            j += 1

        tokens.append((text[i:j], None))
        i = j

    return tokens


def phonemize_word(word: str):
    if word is None or word.strip() == "":
        return word

    return phonemize(
        word,
        language='en-us',
        backend='espeak',
        strip=True,
    )


def preprocess(text: str):
    tokens = split_with_punct(text)
    processed = []
    for word, punct in tokens:
        if punct is not None:
            processed.append(punct)
        else:
            processed.append(phonemize_word(word))

    result = []
    for idx, item in enumerate(processed):
        if item in PUNCTS:
            if len(result) == 0:
                result.append(item)
            else:
                result[-1] = result[-1] + item
        else:
            if len(result) > 0:
                result.append(" " + item)
            else:
                result.append(item)

    return "".join(result)


if __name__ == "__main__":
    text = "world"

    print(f"INPUT: {text}")
    print(f"OUT:   {preprocess(text)}")