# eng2kor  
A lightweight, rule-based English-to-Hangul phoneme converter using **phonemizer (IPA)** and **espeak-ng** as the backend.

## Overview  
**eng2kor** converts English words and full sentences into approximate Korean Hangul pronunciations.  
This project does **not** rely on dictionary lookup; instead, it uses a **rule-based phoneme transformation pipeline**, allowing it to generate plausible Hangul outputs even for:

- Words not found in English dictionaries  
- Informal spellings  
- Proper nouns and coined terms  
- Domain-specific or uncommon vocabulary  

The phoneme conversion internally utilizes **espeak-ng** through the `phonemizer` library.

---

## Requirements

### Python Dependencies
Defined in `requirements.txt`:

```
phonemizer>=3.0.0
```

### System Dependency  
Because the IPA conversion pipeline uses espeak-ng:

- **Ubuntu / Debian**
  ```
  sudo apt-get install espeak-ng
  ```

- **macOS (Homebrew)**
  ```
  brew install espeak-ng
  ```

- **Windows**
  Download and install from:  
  https://github.com/espeak-ng/espeak-ng/releases

---

## Installation

Clone the repository:

```
git clone https://github.com/kijoongkwon99/eng2kor
cd eng2kor
```

Install the package:

```
pip install -e .
```

(Optional) Install dependencies manually:

```
pip install -r requirements.txt
```

---

## How to Use

### Basic Example

```python
from eng2kor import eng_to_hangul

print(eng_to_hangul("hello world"))
print(eng_to_hangul("transformer"))
print(eng_to_hangul("Starbucks"))
```

### Expected Output (approximate)

```
헬로 월드
트랜스포머
스타벅스
```

The system follows:  
**English → IPA → Jamo → Assembled Hangul**,  
providing stable and consistent phonetic results.

---

## Features

- Rule-based English-to-Hangul pronunciation conversion  
- Works even for non-dictionary English words  
- Full sentence support  
- Uses espeak-ng backend through phonemizer  
- Lightweight and suitable for NLP preprocessing pipelines  

---
