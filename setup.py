import setuptools

with open("README.md", "r") as fobj:
    long_description = fobj.read()


setuptools.setup(
    name="pastebin-cli",
    version="0.1.0",
    author="Álvaro Justen",
    author_email="alvarojusten@gmail.com",
    description="Command-line interface for pastebin.com API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/turicas/pastebin-cli",
    packages=setuptools.find_packages(),
    py_modules=["pastebin"],
    install_requires=[],
    entry_points={"console_scripts": ["pastebin = pastebin:main"]},
    classifiers=["Programming Language :: Python :: 3",],
    python_requires=">=3.5",
)
