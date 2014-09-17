from setuptools import setup, find_packages

VERSION = 0.1

setup(
    name="spaceship-build",
    version=VERSION,
    description="A game where you build spaceships",
    url="https://github.com/deontologician/spaceship-build",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)