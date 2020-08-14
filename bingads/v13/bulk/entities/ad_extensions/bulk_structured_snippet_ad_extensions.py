from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *

_StructuredSnippetAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('StructuredSnippetAdExtension'))


class BulkStructuredSnippetAdExtension(_BulkAdExtensionBase):
    """ Represents a structured snippet ad extension.

    This class exposes the :attr:`structured_snippet_ad_extension` property that can be read and written
    as fields of the Structured Snippet Ad Extension record in a bulk file.

    For more information, see Structured Snippet Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _StructuredSnippetAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'StructuredSnippetAdExtension'
            ))
        super(BulkStructuredSnippetAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def structured_snippet_ad_extension(self):
        """ The structured snippet ad extension.

        see Structured Snippet Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127
        """

        return self._ad_extension

    @structured_snippet_ad_extension.setter
    def structured_snippet_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.StructuredSnippetHeader,
            field_to_csv=lambda c: c.structured_snippet_ad_extension.Header,
            csv_to_field=lambda c, v: setattr(c.structured_snippet_ad_extension, 'Header', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StructuredSnippetValues,
            field_to_csv=lambda c: field_to_csv_delimited_strings(c.structured_snippet_ad_extension.Values),
            csv_to_field=lambda c, v: csv_to_field_delimited_strings(c.structured_snippet_ad_extension.Values, v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.structured_snippet_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('StructuredSnippetAdExtension')
        self.structured_snippet_ad_extension.Type = 'StructuredSnippetAdExtension'
        super(BulkStructuredSnippetAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkStructuredSnippetAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.structured_snippet_ad_extension, 'structured_snippet_ad_extension')
        super(BulkStructuredSnippetAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkStructuredSnippetAdExtension._MAPPINGS)


class BulkAccountStructuredSnippetAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level structured snippet ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Structured Snippet Ad Extension record in a bulk file.

    For more information, see Account Structured Snippet Extension at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkCampaignStructuredSnippetAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level structured snippet ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Structured Snippet Ad Extension record in a bulk file.

    For more information, see Campaign Structured Snippet Extension at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupStructuredSnippetAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level structured snippet ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Structured Snippet Ad Extension record in a bulk file.

    For more information, see Ad Group Structured Snippet Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
