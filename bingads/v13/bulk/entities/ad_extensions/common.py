from bingads.v13.internal.bulk.entities.bulk_entity_identifier import _BulkEntityIdentifier
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.extensions import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
Date = _CAMPAIGN_OBJECT_FACTORY_V13.create('Date')

class _BulkAdExtensionBase(_SingleRecordBulkEntity):
    """ This class provides properties that are shared by all bulk ad extension classes.

    *See also:*

    * :class:`.BulkCallAdExtension`
    * :class:`.BulkImageAdExtension`
    * :class:`.BulkLocationAdExtension`
    * :class:`.BulkSiteLinkAdExtension`
    """

    def __init__(self, account_id=None, ad_extension=None):
        super(_BulkAdExtensionBase, self).__init__()

        self._account_id = account_id
        self._ad_extension = ad_extension

    @property
    def account_id(self):
        """ The ad extension's parent account identifier.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c._ad_extension.Status),
            csv_to_field=lambda c, v: csv_to_field_enum(c._ad_extension, v, 'Status', AdExtensionStatus)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c._ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c._ad_extension, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Version,
            field_to_csv=lambda c: bulk_str(c._ad_extension.Version),
            csv_to_field=lambda c, v: setattr(c._ad_extension, 'Version', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: field_to_csv_SchedulingDate(c._ad_extension.Scheduling.StartDate, c._ad_extension.Id) if c._ad_extension.Scheduling else None,
            csv_to_field=lambda c, v: csv_to_field_Date(c._ad_extension.Scheduling, 'StartDate', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: field_to_csv_SchedulingDate(c._ad_extension.Scheduling.EndDate, c._ad_extension.Id) if c._ad_extension.Scheduling else None,
            csv_to_field = lambda c, v: csv_to_field_Date(c._ad_extension.Scheduling, 'EndDate', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdSchedule,
            field_to_csv=lambda c: field_to_csv_AdSchedule(c._ad_extension.Scheduling, c._ad_extension.Id),
            csv_to_field=lambda c, v: csv_to_field_AdSchedule(c._ad_extension.Scheduling, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.UseSearcherTimeZone,
            field_to_csv=lambda c: field_to_csv_UseSearcherTimeZone(c._ad_extension.Scheduling.UseSearcherTimeZone, c._ad_extension.Id) if c._ad_extension.Scheduling else None,
            csv_to_field=lambda c, v: setattr(c._ad_extension.Scheduling, 'UseSearcherTimeZone', parse_bool(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.DevicePreference,
            field_to_csv=lambda c: bulk_device_preference_str(c._ad_extension.DevicePreference),
            csv_to_field=lambda c, v: setattr(c._ad_extension, 'DevicePreference', parse_device_preference(v))
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _BulkAdExtensionBase._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, _BulkAdExtensionBase._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(_BulkAdExtensionBase, self).read_additional_data(stream_reader)


class _BulkAdExtensionAssociation(_SingleRecordBulkEntity):
    """ This class provides properties that are shared by all bulk ad extension association classes.

    For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.
    """

    def __init__(self,
                 ad_extension_id_to_entity_id_association=None,
                 status=None,
                 editorial_status=None):
        super(_BulkAdExtensionAssociation, self).__init__()

        self._status = status
        self._ad_extension_id_to_entity_id_association = ad_extension_id_to_entity_id_association
        self._editorial_status = editorial_status
        self._performance_data = None

    @property
    def ad_extension_id_to_entity_id_association(self):
        """ Defines an association relationship between an ad extension and a supported entity, for example a campaign or ad group.

        :rtype: AdExtensionIdToEntityIdAssociation
        """

        return self._ad_extension_id_to_entity_id_association

    @ad_extension_id_to_entity_id_association.setter
    def ad_extension_id_to_entity_id_association(self, value):
        self._ad_extension_id_to_entity_id_association = value

    @property
    def status(self):
        """ The status of the ad extension association.

        The value is Active if the EntityId and AdExtensionId are associated. The value is Deleted if the association is removed.
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def editorial_status(self):
        """ The editorial status of the ad extension and associated entity.

        For more information, see AdExtensionEditorialStatus at https://go.microsoft.com/fwlink/?linkid=846127.
        Corresponds to the 'Editorial Status' field in the bulk file.

        :rtype: str
        """

        return self._editorial_status

    @editorial_status.setter
    def editorial_status(self, editorial_status):
        self._editorial_status = editorial_status

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.ad_extension_id_to_entity_id_association.AdExtensionId),
            csv_to_field=lambda c, v: setattr(c.ad_extension_id_to_entity_id_association, 'AdExtensionId', int(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, '_status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.ad_extension_id_to_entity_id_association.EntityId),
            csv_to_field=lambda c, v: setattr(c.ad_extension_id_to_entity_id_association, 'EntityId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialStatus,
            field_to_csv=lambda c: c.editorial_status,
            csv_to_field=lambda c, v: setattr(c, '_editorial_status', v if v else None)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._ad_extension_id_to_entity_id_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdExtensionIdToEntityIdAssociation')
        row_values.convert_to_entity(self, _BulkAdExtensionAssociation._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(
            self._ad_extension_id_to_entity_id_association,
            'ad_extension_id_to_entity_id_association'
        )
        self.convert_to_values(row_values, _BulkAdExtensionAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(_BulkAdExtensionAssociation, self).read_additional_data(stream_reader)


class _BulkAccountAdExtensionAssociation(_BulkAdExtensionAssociation):
    """ This abstract class provides properties that are shared by all bulk account ad extension association classes. """

    def __init__(self,
                 ad_extension_id_to_entity_id_association=None,
                 status=None,
                 editorial_status=None):
        super(_BulkAccountAdExtensionAssociation, self).__init__(
            ad_extension_id_to_entity_id_association,
            status,
            editorial_status,
        )


class _BulkCampaignAdExtensionAssociation(_BulkAdExtensionAssociation):
    """ This abstract class provides properties that are shared by all bulk campaign ad extension association classes. """

    def __init__(self,
                 ad_extension_id_to_entity_id_association=None,
                 status=None,
                 editorial_status=None):
        super(_BulkCampaignAdExtensionAssociation, self).__init__(
            ad_extension_id_to_entity_id_association,
            status,
            editorial_status,
        )
        self._campaign_name = None

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, '_campaign_name', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        super(_BulkCampaignAdExtensionAssociation, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkCampaignAdExtensionAssociation._MAPPINGS)

    @property
    def campaign_name(self):
        """ The name of the campaign containing the ad group that the ad extension is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name


class _BulkAdGroupAdExtensionAssociation(_BulkAdExtensionAssociation):
    """ This abstract class provides properties that are shared by all bulk ad group ad extension association classes. """

    def __init__(self,
                 ad_extension_id_to_entity_id_association=None,
                 status=None,
                 editorial_status=None):
        super(_BulkAdGroupAdExtensionAssociation, self).__init__(
            ad_extension_id_to_entity_id_association,
            status,
            editorial_status,
        )
        self._ad_group_name = None
        self._campaign_name = None

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group_name,
            csv_to_field=lambda c, v: setattr(c, '_ad_group_name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, '_campaign_name', v)
        )
    ]

    def process_mappings_from_row_values(self, row_values):
        super(_BulkAdGroupAdExtensionAssociation, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkAdGroupAdExtensionAssociation._MAPPINGS)

    @property
    def ad_group_name(self):
        """ The name of the ad group that the ad extension is associated.

        Corresponds to the 'AdGroup' field in the bulk file.

        :rtype str
        """

        return self._ad_group_name

    @property
    def campaign_name(self):
        """ The name of the campaign containing the ad group that the ad extension is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name


class _BulkAdExtensionIdentifier(_BulkEntityIdentifier):
    def __init__(self,
                 account_id=None,
                 ad_extension_id=None,
                 status=None,
                 version=None):
        super(_BulkAdExtensionIdentifier, self).__init__()

        self._account_id = account_id
        self._ad_extension_id = ad_extension_id
        self._status = status
        self._version = version

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, account_id):
        self._account_id = account_id

    @property
    def ad_extension_id(self):
        return self._ad_extension_id

    @ad_extension_id.setter
    def ad_extension_id(self, ad_extension_id):
        self._ad_extension_id = ad_extension_id

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, 'status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.ad_extension_id),
            csv_to_field=lambda c, v: setattr(c, 'ad_extension_id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Version,
            field_to_csv=lambda c: bulk_str(c.version),
            csv_to_field=lambda c, v: setattr(c, 'version', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.account_id),
            csv_to_field=lambda c, v: setattr(c, 'account_id', int(v) if v else None)
        ),
    ]

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _BulkAdExtensionIdentifier._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, _BulkAdExtensionIdentifier._MAPPINGS)

    def __eq__(self, other):
        raise NotImplementedError()

    @property
    def is_delete_row(self):
        return self._status == 'Deleted'
