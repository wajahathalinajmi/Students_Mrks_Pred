from setuptools import setup,find_packages

hypen_e = "-e ."
with open("D:/Student_Mrks_pred/requirements.txt") as f:
    requirements = f.read().splitlines()

if hypen_e in requirements:
    requirements.remove(hypen_e)

setup(
    name="STDNT_MRKS_PRED",
    version="0.0.1",
    author="WAJAHATH ALI",
    packages=find_packages(),
    install_requires = requirements,
)