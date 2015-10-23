===================
Bing Ads Python SDK
===================

.. image:: https://img.shields.io/pypi/v/bingads.svg
        :target: https://pypi.python.org/pypi/bingads

.. image:: https://img.shields.io/pypi/dm/bingads.svg
        :target: https://pypi.python.org/pypi/bingads


You can develop Bing Ads applications with any programming language that supports web services. The Bing Ads Python Software Development Kit (SDK) Version 10.4 enhances the experience of developing Bing Ads applications
with the Python programming language. The SDK includes a proxy to all Bing Ads API web services and abstracts low level details of authentication with OAuth. You can use the high level BulkServiceManager and ReportingServiceManager interfaces to abstract and execute operations in the low level Bulk and Reporting services. For example instead of calling SubmitGenerateReport and PollGenerateReport to download a report, you download a report using one method with the ReportingServiceManager class.
For more information, see `Bing Ads Client Libraries`_ on MSDN.

Getting Started
---------------

To get started developing Bing Ads applications with Python,
install the SDK and either start with the `examples`_ or follow one of the application walkthroughs on MSDN.
For more information, see `Getting Started Using Python with Bing Ads Services`_.

External Dependencies
---------------------

    - `suds-jurko`_
    - `requests`_
    - `chardet`_
    - `future`_
    - `six`_
    - `enum34`_

.. _Bing Ads Client Libraries: https://msdn.microsoft.com/en-US/library/bing-ads-client-libraries.aspx
.. _examples: https://github.com/bing-ads-sdk/BingAds-Python-SDK/tree/master/examples
.. _Getting Started Using Python with Bing Ads Services: https://msdn.microsoft.com/en-US/library/bing-ads-overview-getting-started-python-with-web-services.aspx

.. _suds-jurko: http://pypi.python.org/pypi/suds-jurko
.. _requests: http://pypi.python.org/pypi/requests
.. _chardet: http://pypi.python.org/pypi/chardet
.. _future: http://pypi.python.org/pypi/future
.. _six: http://pypi.python.org/pypi/six
.. _enum34: http://pypi.python.org/pypi/enum34
