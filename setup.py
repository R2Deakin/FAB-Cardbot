from setuptools import setup, find_packages

setup(
    name='holocron',
    version='0.0.1',
    description='SW:Destiby Discord bot',
    author='Aaron Chapman',
    author_email='aaronchpmn@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
        'discord.py',
        'fuzzywuzzy',
        'python-Levenshtein',
    ],
)
