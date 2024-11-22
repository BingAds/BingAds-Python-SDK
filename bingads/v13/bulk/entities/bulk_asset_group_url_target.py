from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *

class BulkAssetGroupUrlTarget(_SingleRecordBulkEntity):
    """ Represents an asset group url target.

    This class exposes the property :attr:`asset_group_url_target` that can be read and written as fields of the asset group url target record
    in a bulk file.

    For more information, see Asset Group at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, status=None):
        super(BulkAssetGroupUrlTarget, self).__init__()

        self._status = status
        self._id = None
        self._asset_group_id = None
        self._target_condition1 = None
        self._target_condition2 = None
        self._target_condition3 = None
        self._target_condition_operator1 = None
        self._target_condition_operator2 = None
        self._target_condition_operator3 = None
        self._target_value1 = None
        self._target_value2 = None
        self._target_value3 = None

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def asset_group_id(self):
        return self._asset_group_id

    @asset_group_id.setter
    def asset_group_id(self, asset_group_id):
        self._asset_group_id = asset_group_id

    @property
    def target_condition1(self):
        return self._target_condition1

    @target_condition1.setter
    def target_condition1(self, target_condition1):
        self._target_condition1 = target_condition1

    @property
    def target_condition2(self):
        return self._target_condition2

    @target_condition2.setter
    def target_condition2(self, target_condition2):
        self._target_condition2 = target_condition2

    @property
    def target_condition3(self):
        return self._target_condition3

    @target_condition3.setter
    def target_condition3(self, target_condition3):
        self._target_condition3 = target_condition3

    @property
    def target_condition_operator1(self):
        return self._target_condition_operator1

    @target_condition_operator1.setter
    def target_condition_operator1(self, target_condition_operator1):
        self._target_condition_operator1 = target_condition_operator1

    @property
    def target_condition_operator2(self):
        return self._target_condition_operator2

    @target_condition_operator2.setter
    def target_condition_operator2(self, target_condition_operator2):
        self._target_condition_operator2 = target_condition_operator2

    @property
    def target_condition_operator3(self):
        return self._target_condition_operator3

    @target_condition_operator3.setter
    def target_condition_operator3(self, target_condition_operator3):
        self._target_condition_operator3 = target_condition_operator3

    @property
    def target_value1(self):
        return self._target_value1

    @target_value1.setter
    def target_value1(self, target_value1):
        self._target_value1 = target_value1

    @property
    def target_value2(self):
        return self._target_value2

    @target_value2.setter
    def target_value2(self, target_value2):
        self._target_value2 = target_value2

    @property
    def target_value3(self):
        return self._target_value3

    @target_value3.setter
    def target_value3(self, target_value3):
        self._target_value3 = target_value3

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.id),
            csv_to_field=lambda c, v: setattr(c, 'id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.asset_group_id),
            csv_to_field=lambda c, v: setattr(c, 'asset_group_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetCondition1,
            field_to_csv=lambda c: c.target_condition1,
            csv_to_field=lambda c, v: setattr(c, 'target_condition1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetCondition2,
            field_to_csv=lambda c: c.target_condition2,
            csv_to_field=lambda c, v: setattr(c, 'target_condition2', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetCondition3,
            field_to_csv=lambda c: c.target_condition3,
            csv_to_field=lambda c, v: setattr(c, 'target_condition3', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetConditionOperator1,
            field_to_csv=lambda c: c.target_condition_operator1,
            csv_to_field=lambda c, v: setattr(c, 'target_condition_operator1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetConditionOperator2,
            field_to_csv=lambda c: c.target_condition_operator2,
            csv_to_field=lambda c, v: setattr(c, 'target_condition_operator2', v)
        ),_SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetConditionOperator3,
            field_to_csv=lambda c: c.target_condition_operator3,
            csv_to_field=lambda c, v: setattr(c, 'target_condition_operator3', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetValue1,
            field_to_csv=lambda c: c.target_value1,
            csv_to_field=lambda c, v: setattr(c, 'target_value1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetValue2,
            field_to_csv=lambda c: c.target_value2,
            csv_to_field=lambda c, v: setattr(c, 'target_value2', v)
        ),_SimpleBulkMapping(
            header=_StringTable.AssetGroupTargetValue3,
            field_to_csv=lambda c: c.target_value3,
            csv_to_field=lambda c, v: setattr(c, 'target_value3', v)
        ),
    ]


    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkAssetGroupUrlTarget._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, BulkAssetGroupUrlTarget._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAssetGroupUrlTarget, self).read_additional_data(stream_reader)
