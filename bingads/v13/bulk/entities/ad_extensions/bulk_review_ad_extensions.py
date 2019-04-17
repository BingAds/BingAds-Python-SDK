from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import _BulkAdExtensionBase
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

from bingads.v13.internal.extensions import *

_ReviewAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('ReviewAdExtension'))


class BulkReviewAdExtension(_BulkAdExtensionBase):
    """ Represents a review ad extension.

    This class exposes the :attr:`review_ad_extension` property that can be read and written
    as fields of the Review Ad Extension record in a bulk file.

    For more information, see Review Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _ReviewAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'ReviewAdExtension'
            ))
        super(BulkReviewAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def review_ad_extension(self):
        """ The review ad extension.

        see Review Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @review_ad_extension.setter
    def review_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Text,
            field_to_csv=lambda c: c.review_ad_extension.Text,
            csv_to_field=lambda c, v: setattr(c.review_ad_extension, 'Text', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.IsExact,
            field_to_csv=lambda c: bulk_str(c.review_ad_extension.IsExact),
            csv_to_field=lambda c, v: setattr(c.review_ad_extension, 'IsExact',
                                              v.lower() == 'true' if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Source,
            field_to_csv=lambda c: c.review_ad_extension.Source,
            csv_to_field=lambda c, v: setattr(c.review_ad_extension, 'Source', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Url,
            field_to_csv=lambda c: c.review_ad_extension.Url,
            csv_to_field=lambda c, v: setattr(c.review_ad_extension, 'Url', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.review_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('ReviewAdExtension')
        self.review_ad_extension.Type = 'ReviewAdExtension'
        super(BulkReviewAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkReviewAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.review_ad_extension, 'review_ad_extension')
        super(BulkReviewAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkReviewAdExtension._MAPPINGS)


class BulkAccountReviewAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level review ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Review Ad Extension record in a bulk file.

    For more information, see Account Review Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkCampaignReviewAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level review ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Review Ad Extension record in a bulk file.

    For more information, see Campaign Review Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass

class BulkAdGroupReviewAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level Review ad extension.

    This class exposes properties that can be read and written
    as fields of the Ad Group Review Ad Extension record in a bulk file.

    For more information, see Ad Group Review Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
