from .preprocess import preprocess
from .mapper import IPA_TO_HANGUL
from .postprocess import postprocess_jamo_stream

def eng_to_ipa_with_punct(text: str) -> str:
    ipa_with_punct = preprocess(text)
    return ipa_with_punct    


def ipa_to_hangul(ipa: str) -> str:
    tokens = sorted(IPA_TO_HANGUL.keys(), key=len, reverse=True)

    result = ""
    i = 0

    while i < len(ipa):
        matched = False

        for t in tokens:
            if ipa.startswith(t, i):
                result += IPA_TO_HANGUL[t]
                i += len(t)
                matched = True
                break

        if not matched:
            ch = ipa[i]


            if ch.isspace():
                result += ch


            elif ch in "?!.,":  
                result += ch

            i += 1


    return postprocess_jamo_stream(result)


def eng_to_hangul(text: str) -> str:
    ipa = eng_to_ipa_with_punct(text)
    return ipa_to_hangul(ipa)