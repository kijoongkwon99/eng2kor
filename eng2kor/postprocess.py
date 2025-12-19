
VOWELS = set([
    "아","야","어","여","오","요","우","유","으","이",
    "에","예","애","얘",

    "와","왜","외",
    "워","웨","위",
    "유","요",
])

CONSONANTS = set("ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ")
FINAL_OK = set("ㄴㄹㅁㅇ")  


def is_vowel(x):
    return x in VOWELS

def is_consonant(x):
    return x in CONSONANTS

def is_other(x):
    return not is_vowel(x) and not is_consonant(x)



PUNCTS = set("-.,:;?!()\"'")

def split_tokens(jamo: str):
    tokens = []
    buf = ""

    for ch in jamo:
        if ch == " ":
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(" ")
        elif ch in PUNCTS:
            if buf:
                tokens.append(buf)
                buf = ""
            tokens.append(ch)
        else:
            buf += ch

    if buf:
        tokens.append(buf)

    return tokens

def clean_word(word: str) -> str:
    chars = list(word)
    n = len(chars)
    if n == 0:
        return word

    new_chars = chars[:]  

    if is_consonant(chars[0]) and (n == 1 or not is_vowel(chars[1])):
        cho = CHO_MAP[chars[0]]
        jung = JUNG_MAP["으"]
        new_chars[0] = make_syllable(cho, jung, 0)  


    merged = []
    i = 0
    while i < n:
        cur = new_chars[i]

        if len(cur) == 1 and is_consonant(cur):
            if (
                i + 1 < n
                and len(new_chars[i+1]) == 1
                and is_consonant(new_chars[i+1])
                and new_chars[i+1] in FINAL_OK
            ):
                cho = CHO_MAP[cur]
                jung = JUNG_MAP["으"]
                merged.append(make_syllable(cho, jung, 0))
                i += 1
                continue

        merged.append(cur)
        i += 1

    new_chars = merged
    n = len(new_chars)


    last = new_chars[-1]

    if len(last) == 1 and is_consonant(last) and last not in FINAL_OK:
        cho = CHO_MAP[last]
        jung = JUNG_MAP["으"]
        new_chars[-1] = make_syllable(cho, jung, 0)

    return "".join(new_chars)


def clean_consonants(jamo: str) -> str:
    tokens = split_tokens(jamo)

    cleaned = []
    for tok in tokens:
        if tok == " " or tok in PUNCTS:
            cleaned.append(tok)
        else:
            cleaned.append(clean_word(tok))

    return "".join(cleaned)

CHO_MAP = {
    'ㄱ': 0, 'ㄴ': 2, 'ㄷ': 3, 'ㄹ': 5, 'ㅁ': 6,
    'ㅂ': 7, 'ㅅ': 9, 'ㅇ': 11, 'ㅈ': 12,
    'ㅊ': 14, 'ㅋ': 15, 'ㅌ': 16, 'ㅍ': 17, 'ㅎ': 18,
}

JUNG_MAP = {
    "아": 0,  "애": 1,  "야": 2,  "얘": 3,
    "어": 4,  "에": 5,  "여": 6,  "예": 7,
    "오": 8,  "와": 9,  "왜": 10, "외": 11,
    "요": 12, "우": 13, "워": 14, "웨": 15,
    "위": 16, "유": 17, "으": 18, "의": 19, "이": 20,
}


JONG_MAP = {
    '': 0,
    'ㄱ': 1, 'ㄴ': 4, 'ㄷ': 7, 'ㄹ': 8,
    'ㅁ': 16, 'ㅂ': 17, 'ㅅ': 19, 'ㅇ': 21,
    'ㅈ': 22, 'ㅊ': 23, 'ㅋ': 24,
    'ㅌ': 25, 'ㅍ': 26, 'ㅎ': 27,
}

def make_syllable(cho, jung, jong=0):
    return chr(0xAC00 + (cho*21 + jung)*28 + jong)

def process_vowel(cur, next_):
    if not is_vowel(cur):
        return None
    if not is_consonant(next_):
        return None
    
    # if is_vowel(next_next):
    #     return cur

    cho = CHO_MAP['ㅇ']
    jung = JUNG_MAP[cur]
    jong = JONG_MAP.get(next_, 0) if next_ and is_consonant(next_) else 0

    return make_syllable(cho, jung, jong)

def process_consonant(cur, next_):
    is_full = False
    no_skip = False
    if not is_consonant(cur):
        return None, None, None

    if is_vowel(next_):
        cho = CHO_MAP[cur]
        jung = JUNG_MAP[next_]
        return make_syllable(cho, jung, 0), is_full, no_skip

    if isinstance(next_, str) and len(next_) == 1:
        is_full = True
        code = ord(next_)
        if 0xAC00 <= code <= 0xD7A3:
            cho_old, jung_old, jong_old = decompose_syllable(next_)

            if cho_old == CHO_MAP["ㅇ"]:
                cho_new = CHO_MAP[cur]
                merged = make_syllable(cho_new, jung_old, jong_old)
                return merged, is_full, no_skip


            no_skip= False
            cho_new = CHO_MAP[cur]
            jung_new = JUNG_MAP["으"]
            new_syll = make_syllable(cho_new, jung_new, 0)
            return new_syll, is_full, no_skip

    return None, None, None


def decompose_syllable(syllable):
    code = ord(syllable) - 0xAC00
    jong = code % 28
    jung = ((code - jong) // 28) % 21
    cho = ((code - jong) // 28) // 21
    return cho, jung, jong


def process_candidate(result_candidate, cur, next_):
    if is_vowel(next_):
        return None

    if len(result_candidate) != 1:
        return None

    cho, jung, jong = decompose_syllable(result_candidate)

    if cur not in JONG_MAP:
        return None

    jong_new = JONG_MAP[cur]


    new_syllable = make_syllable(cho, jung, jong_new)

    return new_syllable

def postprocess_word(jamo_word: str) -> str:
    result = ""
    result_candidate = None

    n = len(jamo_word)
    skip_flag = False

    for i in range(n):

        if skip_flag:
            skip_flag = False
            continue

        cur = jamo_word[i]
        # prev = jamo_word[i-1] if i > 0 else None
        next_ = jamo_word[i+1] if i < n-1 else None
        next_next = jamo_word[i+2] if i < n-2 else None


        # print(f"cur      :{cur}")
        # print(f"candidate:{result_candidate}")
        if is_consonant(cur):
            if result_candidate:
                syll = process_candidate(result_candidate, cur, next_)
                if syll:
                    result += syll
                    result_candidate = None
                    continue
                else:
                    result += result_candidate
                    result_candidate = None
                    syll, is_full, no_skip = process_consonant(cur, next_)
                    if syll:
                        if is_full:
                            result += syll
                        else:
                            result_candidate = syll
                        if no_skip:
                            continue
                        else: 
                            skip_flag = True
                        continue

            else:
                syll, is_full, no_skip = process_consonant(cur, next_)
                if syll:
                    if is_full:
                        result += syll
                    else:
                        result_candidate = syll
                        if no_skip:
                            continue
                        else: 
                            skip_flag = True
                    continue

        if result_candidate:
            result += result_candidate
            result_candidate = None

        if is_vowel(cur):
            if not is_consonant(next_):
                result += cur
                continue
            elif is_vowel(next_next):
                result += cur
                continue
            else:
                syll = process_vowel(cur, next_)
                if syll:
                    result += syll
                    skip_flag = True
                    continue

        if is_other(cur):
            if result_candidate:
                result += result_candidate
                result_candidate = None
            result += cur
            continue

    if result_candidate:
        result += result_candidate

    return result


def postprocess_jamo_stream(jamo: str) -> str:
    jamo = clean_consonants(jamo)
    words = jamo.split(" ")
    processed_words = [postprocess_word(w) for w in words]

    return " ".join(processed_words)
