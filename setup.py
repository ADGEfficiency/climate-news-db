from setuptools import setup, find_packages


setup(
    name='climate-news-db',
    version='0.3',
    packages=find_packages(),
    install_requires=['Click'],
    entry_points={
        'console_scripts': [
            'dbcollect=climatedb.collect:cli'
        ],
    }
)
