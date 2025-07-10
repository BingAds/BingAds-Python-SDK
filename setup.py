try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = '13.0.25b4'

with open('README.rst', 'r') as f:
    readme = f.read()
with open('HISTORY.rst', 'r') as f:
    history = f.read().replace('.. :changelog:', '')

requirements = [
    'requests',
    'enum34;python_version<"3.9"',
    'pydantic>=2.0.0',
    'pydantic-core>=2.0.1',
    'typing-extensions>=4.0.0'
]

setup(
    name='msads',
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
        'openapi_client',
        'openapi_client.api',
        'openapi_client.models',
        'openapi_client.models.bulk',
        'openapi_client.models.campaign',
        'openapi_client.models.reporting',
        'openapi_client.models.customer',
        'openapi_client.models.billing',
        'openapi_client.models.adinsight',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
)
