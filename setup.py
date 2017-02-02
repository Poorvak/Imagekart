"""Setup modeule."""
from setuptools import setup

DESCRIPTION = """All Image related processing for resizing and enhancement."""
VERSION = "0.0.1"
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.md').read()
except Exception:
    pass

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

KEYWORDS = ["Enhancer", "Image Optimization", "AWS", "Intelligent-Resizer", "Resizer"]

with open("requirements.txt") as fil:
    INSTALL_REQUIRES = fil.read().splitlines()


setup(
    name='Imagekart',
    packages=['Imagekart'],
    version=VERSION,
    author=u"Poorvak Kapoor",
    author_email="poorvak.kapoor@cube26.com",
    url="https://github.com/Poorvak/Imagekart.git",
    license="MIT",
    keywords=KEYWORDS,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
)
