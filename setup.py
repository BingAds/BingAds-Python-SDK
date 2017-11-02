try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '11.5.6'

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
]

setup(
    name='bingads',
    version=VERSION,
    description='A library to make working with the Bing Ads APIs and bulk services easy',
    long_description=readme + '\n\n' + history,
    author='Bing Ads SDK Team',
    author_email='bing_ads_sdk@microsoft.com',
    url='https://github.com/BingAds/BingAds-Python-SDK',
    packages=[
        'bingads',
        'bingads.internal',
        'bingads.v11.reporting',
        'bingads.v11',
        'bingads.v11.bulk',
        'bingads.v11.bulk.entities',
        'bingads.v11.bulk.entities.ad_extensions',
        'bingads.v11.bulk.entities.audiences',
        'bingads.v11.bulk.entities.target_criterions',
        'bingads.v11.bulk.entities.labels',
        'bingads.v11.internal',
        'bingads.v11.internal.bulk',
        'bingads.v11.internal.bulk.entities',
    ],
    include_package_data=True,
    install_requires=requirements,
    license='MIT',
    zip_safe=False,
    keywords='bingads',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
