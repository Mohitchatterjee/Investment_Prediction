from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME = 'requirements.txt'


def get_requirements():
    with open(REQUIREMENT_FILE_NAME) as file:
        file_list = file.readlines()
        file_list=[requirement_name.replace('\n','') for requirement_name in file_list]
        if '-e .' in file_list:
            file_list.remove('-e .')
        return file_list


setup(
    name='Investment_Prediction',
    version='0.1',
    author='Mohit Chatterjee',
    author_email='chatterjeemohit160@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements() 
)