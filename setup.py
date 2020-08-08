from setuptools import setup, find_packages


setup(
    name='climate-news-db',
    version='0.1',
    packages=find_packages(),
    install_requires=['Click'],
    entry_points={
        'console_scripts': [
            'collect=collect_urls:cli',
            'parse=parse_urls:main'
        ],
    }
)
