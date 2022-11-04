# from pathlib import Path
from setuptools import setup, find_packages


# def read_long_description(file_path):
#     print(file_path)
#     long_description = None
#     with open(file_path, "r", encoding="utf-8") as file_handler:
#         long_description = file_handler.read()
#     return long_description


setup(
    name="ezcode",
    version="0.0.104",
    author="Zheng Gao",
    author_email="mail.zheng.gao@gmail.com",
    description="Easy Algorithm & Data Structure",
    url="https://github.com/zheng-gao/ez_code",
    project_urls={"Bug Tracker": "https://github.com/zheng-gao/ez_code/issues"},
    # long_description=(Path(__file__).parent / "readme.md").read_text(encoding="utf-8"),
    # long_description_content_type="text/markdown",
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
