from setuptools import setup, find_namespace_packages

setup(
    name="gym_hnefatafl",
    version="0.1.0",
    packages=find_namespace_packages(),
    install_requires=["gym", "numpy", "scipy"],
)
