import setuptools

with open("README.md", mode="r", encoding="utf-8") as fh:
    long_description = fh.read()

required_packages = [
    "phonemizer>=3.0.0",
]

setuptools.setup(
    name="eng2kor",   # repository 이름과 동일하게 설정
    version="0.1.0",
    author="kijoongkwon",
    author_email="kijoongkwon@kaist.ac.kr",
    description="A lightweight English-to-Hangul converter using IPA phonemization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kijoongkwon99/eng2kor",
    install_requires=required_packages,
    packages=setuptools.find_packages(),   # eng2kor/eng2kor 자동 탐색
    include_package_data=True,
    package_data={
        "eng2kor": [
            # 필요시 여기에 리소스 파일 추가
        ]
    },
    python_requires=">=3.11",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
