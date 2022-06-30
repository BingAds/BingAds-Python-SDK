import time
from bingads.exceptions import TimeoutException
from suds.client import WebFault
from suds.cache import Cache


class DictCache(dict, Cache):
    # .get and .clear work as intended
    purge = dict.__delitem__

    def put(self, id_, obj):
        self[id_] = obj
        return obj
    

class _TimeHelper(object):
    """
    Time helper class to handle timeout
    """
    MIN_TIMEOUT_VALUE = 1000

    @staticmethod
    def get_current_time():
        return time.time()

    @staticmethod
    def get_current_time_milliseconds():
        return int(round(time.time()) * 1000)

    @staticmethod
    def get_remaining_time_milliseconds(start_time_milliseconds, total_timeout):
        return None if total_timeout is None else total_timeout - (_TimeHelper.get_current_time_milliseconds() - start_time_milliseconds)

    @staticmethod
    def get_remaining_time_milliseconds_with_min_value(start_time_milliseconds, total_timeout):
        if total_timeout is None:
            return None
        remaining_time = total_timeout - (_TimeHelper.get_current_time_milliseconds() - start_time_milliseconds)
        return remaining_time if remaining_time > 0 else _TimeHelper.MIN_TIMEOUT_VALUE


class _PollingBlocker(object):
    INITIAL_STATUS_CHECK_INTERVAL_IN_MS = 1000
    NUMBER_OF_INITIAL_STATUS_CHECKS = 5

    def __init__(self, poll_interval_in_milliseconds, timeout_in_milliseconds=None):
        self._poll_interval_in_milliseconds = poll_interval_in_milliseconds
        self._status_update_count = 0
        self._timeout_stamp = None if timeout_in_milliseconds is None else \
            int(round(time.time()) * 1000) + timeout_in_milliseconds

    def wait(self):
        self._status_update_count += 1
        if self._timeout_stamp is not None and int(round(time.time()) * 1000) > self._timeout_stamp:
            raise TimeoutException('Timeout at polling.')
        if self._status_update_count >= _PollingBlocker.NUMBER_OF_INITIAL_STATUS_CHECKS:
            time.sleep(self._poll_interval_in_milliseconds / 1000.0)
        else:
            time.sleep(_PollingBlocker.INITIAL_STATUS_CHECK_INTERVAL_IN_MS / 1000.0)


ratelimit_retry_duration=[15, 20, 25, 30]
def errorcode_of_exception(ex):
    if isinstance(ex, WebFault):
        if hasattr(ex.fault, 'detail') \
                and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
                and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
                and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
            ad_api_errors = ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
            if type(ad_api_errors) == list:
                return ad_api_errors[0].Code
            else:
                return ad_api_errors.Code
    return -1


def operation_errorcode_of_exception(ex):
    if isinstance(ex, WebFault):
        if hasattr(ex.fault, 'detail') \
                and hasattr(ex.fault.detail, 'ApiFaultDetail') \
                and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
                and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
            operation_error = ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
            if type(operation_error) == list:
                return operation_error[0].ErrorCode
            else:
                return operation_error.ErrorCode
    return ""