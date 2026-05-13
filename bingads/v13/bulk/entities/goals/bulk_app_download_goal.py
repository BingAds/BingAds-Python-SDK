from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.extensions import *
from .bulk_conversion_goal import BulkConversionGoal

class BulkAppDownloadGoal(BulkConversionGoal):
    """ Represents an AppDownload Goal that can be read or written in a bulk file.

    This class exposes the :attr:`app_download_goal` property that can be read and written as fields of the
    AppDownload Goal record in a bulk file.

    For more information, see AppDownload Goal at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 app_download_goal=None):
        super(BulkAppDownloadGoal, self).__init__(conversion_goal=app_download_goal)

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.AppPlatform,
            field_to_csv=lambda c: bulk_str(c.app_download_goal.AppPlatform),
            csv_to_field=lambda c, v: setattr(c.app_download_goal, 'AppPlatform', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AppStoreId,
            field_to_csv=lambda c: bulk_str(c.app_download_goal.AppStoreId),
            csv_to_field=lambda c, v: setattr(c.app_download_goal, 'AppStoreId', v)
        ),
    ]

    @property
    def app_download_goal(self):
        """ Defines an AppDownload Goal """

        return self._conversion_goal

    @app_download_goal.setter
    def app_download_goal(self, app_download_goal):
        self._conversion_goal = app_download_goal

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.app_download_goal, 'app_download_goal')
        super(BulkAppDownloadGoal, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAppDownloadGoal._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self.app_download_goal = _CAMPAIGN_OBJECT_FACTORY_V13.create('AppDownloadGoal')
        super(BulkAppDownloadGoal, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAppDownloadGoal._MAPPINGS)
