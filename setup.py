import json
from pathlib import Path
from setuptools import setup, find_packages


def build_long_description():
    long_description=""
    docs = Path(__file__).parent / "docs"
    for md in sorted(docs.glob("*.md")):
        with open(md, mode="r", encoding="utf-8") as f:
            long_description += f.read()
    return long_description


setup(
    name="ezcode",
    version="0.1.4",
    author="Zheng Gao",
    author_email="mail.zheng.gao@gmail.com",
    description="Easy Algorithm & Data Structure",
    url="https://github.com/zheng-gao/ez_code",
    project_urls={"Bug Tracker": "https://github.com/zheng-gao/ez_code/issues"},
    long_description=build_long_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                            # Information to filter the project on PyPi website
    python_requires=">=3.7",                      # Minimum version requirement of the package
    py_modules=["ezcode"],                        # Name of the python package
    package_dir={"": "src"},                      # Directory of the source code of the package
    packages=find_packages(where="src"),          # List of all python modules to be installed
    install_requires=[]                           # Install other dependencies if any
)
