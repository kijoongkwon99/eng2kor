# -----------------------------
# 0. 공통 분류
# -----------------------------
VOWELS = set([
    # 단모음
    "아","야","어","여","오","요","우","유","으","이",
    "에","예","애","얘",

    # 합성모음
    "와","왜","외",
    "워","웨","위",
    "유","요",

    # r-colored (미국식)
    # "얼","아르","오르",

    # 이중모음 매핑
    # "아이","아우","오이","에이",
])

CONSONANTS = set("ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ")
FINAL_OK = set("ㄴㄹㅁㅇ")   # 받침 허용 자음


def is_vowel(x):
    return x in VOWELS

def is_consonant(x):
    return x in CONSONANTS

def is_other(x):
    return not is_vowel(x) and not is_consonant(x)



PUNCTS = set("-.,:;?!()\"'")

def split_tokens(jamo: str):
    """
    공백, 구두점, 단어를 모두 개별 토큰으로 분리
    예: 'hi,' → ['hi', ',']
        'hello world!' → ['hello', ' ', 'world', '!']
    """
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




# -----------------------------
# 1. 단어 단위 자음 보정(clean)
# -----------------------------
def clean_word(word: str) -> str:
    """
    규칙:
    1) 맨 앞 글자가 자음이고, 두 번째 글자가 모음이 아니면 -> '자음+으' (완성음절)
    2) 마지막 글자가 자음이고 FINAL_OK에 없으면 -> 마지막 뒤에 '으' (완성음절)
    3) 자음 + 자음 이고 뒤 자음이 FINAL_OK이면 -> 앞 자음+='으' (완성음절)
    """

    chars = list(word)
    n = len(chars)
    if n == 0:
        return word

    new_chars = chars[:]  # 복사

    # ---------- 규칙 1 ----------
    if is_consonant(chars[0]) and (n == 1 or not is_vowel(chars[1])):
        cho = CHO_MAP[chars[0]]
        jung = JUNG_MAP["으"]
        new_chars[0] = make_syllable(cho, jung, 0)  # 완성형 ‘그, 느, 드…’

    # ---------- 규칙 3 ----------
    merged = []
    i = 0
    while i < n:
        cur = new_chars[i]

        # 현재 글자가 '완성형 음절'인지 '자음 한 글자'인지 구분 필요
        if len(cur) == 1 and is_consonant(cur):
            # cur은 자음 1글자
            if (
                i + 1 < n
                and len(new_chars[i+1]) == 1
                and is_consonant(new_chars[i+1])
                and new_chars[i+1] in FINAL_OK
            ):
                # cur + '으' -> 완성음절
                cho = CHO_MAP[cur]
                jung = JUNG_MAP["으"]
                merged.append(make_syllable(cho, jung, 0))
                i += 1
                continue

        merged.append(cur)
        i += 1

    new_chars = merged
    n = len(new_chars)

    # ---------- 규칙 2 ----------
    last = new_chars[-1]

    if len(last) == 1 and is_consonant(last) and last not in FINAL_OK:
        # last + '으' → 완성음절
        cho = CHO_MAP[last]
        jung = JUNG_MAP["으"]
        new_chars[-1] = make_syllable(cho, jung, 0)

    return "".join(new_chars)



# -----------------------------
# 2. 문장 단위로 clean 적용
# -----------------------------
def clean_consonants(jamo: str) -> str:
    tokens = split_tokens(jamo)

    cleaned = []
    for tok in tokens:
        # 구두점 or 공백은 그대로 유지
        if tok == " " or tok in PUNCTS:
            cleaned.append(tok)
        else:
            cleaned.append(clean_word(tok))

    return "".join(cleaned)



# -----------------------------
# 3. vowel 기반 음절 생성 (너의 기존 함수)
# -----------------------------

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
    """
    cur: 자음 1개
    next_: 다음 글자
        - 모음 → cur + 모음 → 음절 생성
        - 완성형 음절(중성+종성) → cur을 초성으로 replace 후 이어서 음절 생성
        - 그 외 → None
    """
    is_full = False
    no_skip = False
    if not is_consonant(cur):
        return None, None, None

    # -------------------------
    # Case 1: next_가 모음일 때
    # -------------------------
    if is_vowel(next_):
        cho = CHO_MAP[cur]
        jung = JUNG_MAP[next_]
        return make_syllable(cho, jung, 0), is_full, no_skip

    # -------------------------
    # Case 2: next_가 완성형 한 글자 음절일 때
    #   → 초성 교체(cur로)
    # -------------------------
    if isinstance(next_, str) and len(next_) == 1:
        is_full = True
        code = ord(next_)
        if 0xAC00 <= code <= 0xD7A3:
            cho_old, jung_old, jong_old = decompose_syllable(next_)

            # 2-1) 초성이 'ㅇ'이면 merge
            if cho_old == CHO_MAP["ㅇ"]:
                cho_new = CHO_MAP[cur]
                merged = make_syllable(cho_new, jung_old, jong_old)
                return merged, is_full, no_skip

            # 2-2) 초성이 ㅇ이 아닐 때 → cur + 'ㅡ' 로 새 음절 생성
            no_skip= False
            cho_new = CHO_MAP[cur]
            jung_new = JUNG_MAP["으"]
            new_syll = make_syllable(cho_new, jung_new, 0)
            return new_syll, is_full, no_skip


    # -------------------------
    # Case 3: next_가 자음 또는 기타 → None
    # -------------------------
    return None, None, None


def decompose_syllable(syllable):
    """완성형 한글 -> (초성index, 중성index, 종성index) 반환"""
    code = ord(syllable) - 0xAC00
    jong = code % 28
    jung = ((code - jong) // 28) % 21
    cho = ((code - jong) // 28) // 21
    return cho, jung, jong


def process_candidate(result_candidate, cur, next_):
    """
    result_candidate: 초성+중성만 있는 완성형 음절
    cur : 종성 후보 자음
    next_: 다음 글자

    next_가 모음이면 → 종성 붙이면 안되므로 None
    next_가 모음이 아니면 → cur을 종성으로 붙여 새 음절 생성
    """
    # print(f"process_candidate")
    # print(f"input_candidate :{result_candidate}")
    # print(f"cur             :{cur}")
    # print(f"next            :{next_}")
    # print(f"is_vowel(next_) :{is_vowel(next_)}")
    # 1) next_가 모음이면 종성 절대 금지
    if is_vowel(next_):
        return None

    # 2) result_candidate가 완성형 음절이 맞는지 확인
    if len(result_candidate) != 1:
        return None

    # 3) 기존 음절 분해
    cho, jung, jong = decompose_syllable(result_candidate)

    # 4) 현재 cur 자음을 JONG_MAP에 넣어 종성 index 찾기
    if cur not in JONG_MAP:
        return None

    jong_new = JONG_MAP[cur]

    # 5) 새 음절 조합
    new_syllable = make_syllable(cho, jung, jong_new)

    return new_syllable



# -----------------------------
# 4. 최종 postprocess
# -----------------------------
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
        # -----------------------------------
        # 자음 처리
        # -----------------------------------
        if is_consonant(cur):

            # case 1: candidate가 이미 존재할 때
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

            # case 2: candidate가 없을 때
            else:
                # print(f"no candidate consonat cur : {cur}")
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

        # -----------------------------------
        # 모음 처리
        # -----------------------------------
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

        # -----------------------------------
        # 기타 처리
        # -----------------------------------
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
    # print("input jamo:", jamo)

    # 1) 자음 보정 (단어 단위)
    jamo = clean_consonants(jamo)
    # print("cleaned:", jamo)

    # 2) 단어 단위 후처리
    words = jamo.split(" ")
    processed_words = [postprocess_word(w) for w in words]

    return " ".join(processed_words)
