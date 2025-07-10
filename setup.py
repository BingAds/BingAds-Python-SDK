try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '13.0.25'

with open('README.rst', 'r') as f:
    readme = f.read()
with open('HISTORY.rst', 'r') as f:
    history = f.read().replace('.. :changelog:', '')

requirements = [
    'suds-community>=1.1.0',
    'requests',
    'enum34;python_version<"3.9"',
]

setup(
    name='bingads',
    version=VERSION,
    description='A library to make working with the Bing Ads APIs and bulk services easy',
    long_description=readme,
    author='Bing Ads SDK Team',
    author_email='bing_ads_sdk@microsoft.com',
    url='https://github.com/BingAds/BingAds-Python-SDK',
    packages=[
        'bingads',
        'bingads.internal',
        'bingads.v13',
        'bingads.v13.bulk',
        'bingads.v13.bulk.entities',
        'bingads.v13.bulk.entities.ad_extensions',
        'bingads.v13.bulk.entities.audiences',
        'bingads.v13.bulk.entities.feeds',
        'bingads.v13.bulk.entities.target_criterions',
        'bingads.v13.bulk.entities.labels',
        'bingads.v13.bulk.entities.goals',
        'bingads.v13.internal',
        'bingads.v13.internal.bulk',
        'bingads.v13.internal.bulk.entities',
        'bingads.v13.internal.reporting',
        'bingads.v13.reporting',
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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)
