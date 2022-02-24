import setuptools

with open("README.md", "r", encoding="utf-8") as file_handler:
    long_description = file_handler.read()

setuptools.setup(
    name="ezcode",                                  # This is the name of the package
    version="0.0.40",                               # The initial release version
    author="Zheng Gao",                             # Full name of the author
    description="Easy Algorithm & Data Structure",
    url="https://github.com/zheng-gao/ez_code",
    project_urls={
        "Bug Tracker": "https://github.com/zheng-gao/ez_code/issues",
    },
    long_description=long_description,              # Long description read from the the readme file
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                              # Information to filter the project on PyPi website
    python_requires=">=3.7",                        # Minimum version requirement of the package
    py_modules=["ezcode"],                          # Name of the python package
    package_dir={"": "src"},                        # Directory of the source code of the package
    packages=setuptools.find_packages(where="src"), # List of all python modules to be installed
    install_requires=[]                             # Install other dependencies if any
)
