from setuptools import setup, find_packages

setup(
    name="fscli",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        "console_scripts": [
            "fscli = fscli.fscli:main",
        ],
    },
    author="FonalityCode",
    author_email="admin@ivantana.xyz",
    description="A CLI tool for filesystem operations and forensic analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Fonality-code/fscli-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
