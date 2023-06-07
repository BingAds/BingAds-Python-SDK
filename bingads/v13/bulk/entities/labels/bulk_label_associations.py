from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class _BulkLabelAssociation(_SingleRecordBulkEntity):
    """ Represents a label association that can be read or written in a bulk file.

    This class exposes the :attr:`label_association` property that can be read and written as fields of the Keyword record in a bulk file.
    Properties of this class and of classes that it is derived from, correspond to fields of the Keyword record in a bulk file.
    For more information, see Keyword at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(_BulkLabelAssociation, self).__init__()
        self._label_association = label_association
        self._status = status

    @property
    def label_association(self):
        """ The LabelAssociation Data Object of the Campaign Management Service.

        A subset of Label properties are available in the Ad Group record.
        """

        return self._label_association

    @label_association.setter
    def label_association(self, value):
        self._label_association = value

    @property
    def status(self):
        """ the status of bulk record
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(
                c,
                'status',
                v if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: c.label_association.LabelId,
            csv_to_field=lambda c, v: setattr(
                c.label_association,
                'LabelId',
                int(v) if v else None
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: c.label_association.EntityId,
            csv_to_field=lambda c, v: setattr(
                c.label_association,
                'EntityId',
                int(v) if v else None
            )
        ),

    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._label_association, 'label_association')
        self.convert_to_values(row_values, _BulkLabelAssociation._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        self._label_association = _CAMPAIGN_OBJECT_FACTORY_V13.create('LabelAssociation')
        row_values.convert_to_entity(self, _BulkLabelAssociation._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(_BulkLabelAssociation, self).read_additional_data(stream_reader)


class BulkCampaignLabel(_BulkLabelAssociation):
    """ Represents a campaign label.

    Defines an association record between a Campaign and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see Campaign Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None, campaign=None):
        super(BulkCampaignLabel, self).__init__(label_association, status)
        self._campaign = campaign

    @property
    def campaign(self):
        """ The campaign name of the Campaign Management Service.

        A subset of Label properties are available in the Ad Group record.
        """

        return self._campaign

    @campaign.setter
    def campaign(self, value):
        self._campaign = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign,
            csv_to_field=lambda c, v: setattr(
                c,
                'campaign',
                v
            )
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkCampaignLabel, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkCampaignLabel._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkCampaignLabel, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkCampaignLabel._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkCampaignLabel, self).read_additional_data(stream_reader)


class BulkAdGroupLabel(_BulkLabelAssociation):
    """ Represents a AdGroup label.

    Defines an association record between a AdGroup and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see AdGroup Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None, campaign=None, ad_group=None):
        super(BulkAdGroupLabel, self).__init__(label_association, status)
        self._campaign = campaign
        self._ad_group = ad_group

    @property
    def campaign(self):
        """ The campaign name of the Campaign Management Service.

        A subset of Label properties are available in the Ad Group record.
        """

        return self._campaign

    @campaign.setter
    def campaign(self, value):
        self._campaign = value

    @property
    def ad_group(self):
        """ The ad group name of the Campaign Management Service.

        A subset of Label properties are available in the Ad Group record.
        """

        return self._campaign

    @ad_group.setter
    def ad_group(self, value):
        self._ad_group = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign,
            csv_to_field=lambda c, v: setattr(
                c,
                'campaign',
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdGroup,
            field_to_csv=lambda c: c.ad_group,
            csv_to_field=lambda c, v: setattr(
                c,
                'ad_group',
                v
            )
        )
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupLabel, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupLabel._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupLabel, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupLabel._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupLabel, self).read_additional_data(stream_reader)


class BulkKeywordLabel(_BulkLabelAssociation):
    """ Represents a Keyword label.

    Defines an association record between a Keyword and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see Keyword Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkKeywordLabel, self).__init__(label_association, status)


class BulkAppInstallAdLabel(_BulkLabelAssociation):
    """ Represents a AppInstallAd label.

    Defines an association record between a AppInstallAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see AppInstallAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkAppInstallAdLabel, self).__init__(label_association, status)


class BulkDynamicSearchAdLabel(_BulkLabelAssociation):
    """ Represents a DynamicSearchAd label.

    Defines an association record between a DynamicSearchAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see DynamicSearchAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkDynamicSearchAdLabel, self).__init__(label_association, status)


class BulkExpandedTextAdLabel(_BulkLabelAssociation):
    """ Represents a ExpandedTextAd label.

    Defines an association record between a ExpandedTextAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see ExpandedTextAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkExpandedTextAdLabel, self).__init__(label_association, status)


class BulkProductAdLabel(_BulkLabelAssociation):
    """ Represents a ProductAd label.

    Defines an association record between a ProductAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see ProductAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkProductAdLabel, self).__init__(label_association, status)


class BulkTextAdLabel(_BulkLabelAssociation):
    """ Represents a TextAd label.

    Defines an association record between a TextAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see TextAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkTextAdLabel, self).__init__(label_association, status)

class BulkResponsiveAdLabel(_BulkLabelAssociation):
    """ Represents a ResponsiveAd label.

    Defines an association record between a ResponsiveAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see ResponsiveAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkResponsiveAdLabel, self).__init__(label_association, status)

class BulkResponsiveSearchAdLabel(_BulkLabelAssociation):
    """ Represents a ResponsiveSearchAd label.

    Defines an association record between a ResponsiveSearchAd and a Label that can be uploaded and downloaded in a bulk file.

    For more information, see ResponsiveSearchAd Label at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, label_association=None, status=None):
        super(BulkResponsiveSearchAdLabel, self).__init__(label_association, status)