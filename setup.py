try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '9.3.3'

with open('README.rst', 'r') as f:
    readme = f.read()
with open('HISTORY.rst', 'r') as f:
    history = f.read().replace('.. :changelog:', '')

requirements = [
    'suds-jurko==0.6.0',
    'future',
    'six',
    'requests',
    'enum34',
    'chardet',
]

setup(
    name='bingads',
    version=VERSION,
    description='A library to make working with the Bing Ads APIs and bulk services easy',
    long_description=readme + '\n\n' + history,
    author='Bing Ads SDK Team',
    author_email='bing_ads_sdk@microsoft.com',
    url='https://github.com/bing-ads-sdk/BingAds-Python-SDK',
    packages=[
        'bingads',
        'bingads.bulk',
        'bingads.bulk.entities',
        'bingads.bulk.entities.ad_extensions',
        'bingads.bulk.entities.targets',
        'bingads.internal',
        'bingads.internal.bulk',
        'bingads.internal.bulk.entities',
    ],
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='bingads',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
