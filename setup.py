import io
import os
import setuptools

with io.open("./README.md", mode="rt") as f:
    long_description = f.read()

about = {}
root_path = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(root_path, "msvdd_bloc", "about.py")) as f:
    exec(f.read(), about)


setuptools.setup(
    name="msvdd_bloc",
    version=about["__version__"],
    description=about["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=about["__url__"],
    maintainer=about["__maintainer__"],
    maintainer_email=about["__maintainer_email__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4>=4.7.0",
        "Faker>=2.0.0",
        "ftfy>=5.6",
        "glom>=19.0.0",
        "marshmallow>=3.0.0",
        "matplotlib>=3.0.0",
        "pandas>=0.25.0",
        "probablepeople>=0.5.4",
        "python-crfsuite>=0.9.6",
        "requests>=2.20.0",
        "spacy>=2.1,<2.2",
        "textacy>=0.9.0",
        "tika>=1.19",
        "toolz>=0.10.0",
        "usaddress>=0.5.10",
        "watermark>=1.8.0",
        "yapdfminer>=1.2.0",
    ],
)
