from setuptools import setup, find_packages

setup(
    name='project_name',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'flask',
    ],
    entry_points={
        'console_scripts': [
            'project_name=project_name.__main__:main',
        ],
    },
    author='Rye',
    author_email='rye@grcand.me',
    description='A framework for Scanning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/project_name',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
