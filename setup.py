# File: setup.py
# File Created: Friday, 11th October 2024 3:10:15 pm
# Author: Philippe Hawi (philippe.hawi@outlook.com)

from setuptools import setup

description = (
    "Graphical User Interface (GUI) for the Probabilistic Learning on Manifolds (PLoM) Python package"
)

dependencies = [
    "numpy",
    "matplotlib",
    "scipy"
]

setup(
    name='plomGUI',
    version='0.1',
    description=description,
    url="https://github.com/philippehawi/PLoM-GUI",
    author="Philippe Hawi",
    author_email="philippe.hawi@outlook.com",
    license="MIT",
    py_modules=['plom_gui'],
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'plom-gui=plom_gui:launch_gui',
        ],
    },
)