# eng2kor  
A lightweight, rule-based English-to-Hangul phoneme converter using **phonemizer (IPA)** from **espeak-ng** as the backend.

## Overview  
**eng2kor** converts English words and full sentences into approximate Korean Hangul pronunciations.  
This project does **not** rely on dictionary lookup; instead, it uses a **rule-based phoneme transformation pipeline**, allowing it to generate plausible Hangul outputs even for:

- Words not found in English dictionaries  
- Informal spellings  
- maintaining punctuations

The phoneme conversion internally utilizes **espeak-ng** through the `phonemizer` library.

---

## Requirements
```
python >=3.11
phonemizer>=3.0.0
```


## Quick Start


```
conda create -n "eng2kor" python=3.11
cd eng2kor
pip install git+https://github.com/kijoongkwon99/eng2kor.git

```
```python
from eng2kor import eng_to_hangul
print(eng_to_hangul("Hello, world!"))
# 허로, 우얼드!

```
---

## How to Use

### Example

```python
from eng2kor import eng_to_hangul

print(eng_to_hangul("This tool is not perfect, but it was designed to minimize unexpected edge cases and ensure stable behavior."))
print(eng_to_hangul("It was created to serve as a plug-and-play module for TTS systems or as a lightweight normalizer component during model training."))
print(eng_to_hangul("Since the tool prioritizes reflecting the original English phonetics, the output may differ from intuitive Korean pronunciations."))
```

### Output example

```
디스 튤 이즈 나트 퍼펰트, 버트 이트 우어즈 디자인드 터 미니마이즈 어넼펰티드 에지 케이시즈 앤드 엔시울 스테이벌 비헤이비얼.
이트 우어즈 크리에이리드 터 서브 애즈 어 프러그 앤드 프레이 마지율 폴 티티에스 시스텀즈 올 애즈 어 라이투에이트 노르머라잊얼 컴포넌트 두르링 마덜 트레이닝.
신스 더 튤 프라이오리타이지즈 리프렠팅 디 얼리지이널 잉그리시 퍼네맄스, 디 아웉푸트 메이 딮얼 프럼 인튜이티브 코리안 프러넌시에이시언즈.
```

The system follows:  
**English → IPA → Jamo → Assembled Hangul**,  
providing stable and consistent phonetic results.

---
