from setuptools import setup, find_namespace_packages

setup(
    name="gym_hnefatafl",
    version="0.0.1",
    packages=find_namespace_packages(),
    install_requires=["gym", "numpy", "scipy"],
)
