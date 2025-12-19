# preprocessing.py

import re
from phonemizer import phonemize

PUNCTS = set("-.,:;?!()\"'")

def split_with_punct(text: str):
    """
    문장을 '단어 또는 연속문자'와 '구두점'으로 분리.
    결과는 리스트 형태로 (word, punct) 튜플로 저장.
    """
    tokens = []
    i = 0
    n = len(text)

    while i < n:
        ch = text[i]

        if ch in PUNCTS:
            tokens.append((None, ch))
            i += 1
            continue

        # 단어 읽기
        j = i
        while j < n and text[j] not in PUNCTS:
            j += 1

        tokens.append((text[i:j], None))
        i = j

    return tokens


def phonemize_word(word: str):
    """단어만 phonemize. 빈 문자열이면 그대로."""
    if word is None or word.strip() == "":
        return word

    return phonemize(
        word,
        language='en-us',
        backend='espeak',
        strip=True,
    )


def preprocess(text: str):
    # -----------------------
    # 1) punctuation 분리
    # -----------------------
    tokens = split_with_punct(text)

    # -----------------------
    # 2) 단어만 phonemize
    # -----------------------
    processed = []
    for word, punct in tokens:
        if punct is not None:
            processed.append(punct)
        else:
            processed.append(phonemize_word(word))

    # -----------------------
    # 3) 토큰 재결합
    # -----------------------
    result = []
    for idx, item in enumerate(processed):
        # 단어 뒤에는 공백 유지 (punct는 붙인다)
        if item in PUNCTS:
            # punctuation → 앞 단어에 바로 붙임
            if len(result) == 0:
                result.append(item)
            else:
                result[-1] = result[-1] + item
        else:
            # 단어
            if len(result) > 0:
                result.append(" " + item)
            else:
                result.append(item)

    return "".join(result)


if __name__ == "__main__":
    text = "world"

    print(f"INPUT: {text}")
    print(f"OUT:   {preprocess(text)}")