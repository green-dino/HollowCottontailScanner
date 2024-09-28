from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='HollowCottonTail',
    version='0.1',
    packages=find_packages(),
    install_requires=requirements,
    author='Rye',
    author_email='rye@grcand.me',
    description='A framework for Scanning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/green-dino/HollowCottontailScanner ',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
