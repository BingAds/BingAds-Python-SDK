from bingads.v13.bulk.entities import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13
from bingads.v13.bulk.entities.bulk_ad_group_criterion import BulkAdGroupCriterion
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable

_HotelGroup = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('HotelGroup'))

class BulkAdGroupHotelListingGroup(BulkAdGroupCriterion):
    """ Represents an Ad Group Hotel Group that can be read or written in a bulk file.

    This class exposes the :attr:`ad_group_criterion` property that can be read and written as fields of the
    Ad Group Hotel Group record in a bulk file.

    For more information, see Ad Group Product Scope at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_name=None,
                 ad_group_name=None,
                 ad_group_criterion=None
                 ):
        super(BulkAdGroupHotelListingGroup, self).__init__(campaign_name, ad_group_name, ad_group_criterion)

    @classmethod
    def _get_listing_type(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
            hasattr(entity.ad_group_criterion.Criterion, 'ListingType'):
            return entity.ad_group_criterion.Criterion.ListingType
        return None

    @classmethod
    def _get_parent_criterion_id(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
            hasattr(entity.ad_group_criterion.Criterion, 'ParentCriterionId'):
            return bulk_str(entity.ad_group_criterion.Criterion.ParentCriterionId)
        return None

    @classmethod
    def _get_listing_operand(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
            hasattr(entity.ad_group_criterion.Criterion, 'Listing') and \
            entity.ad_group_criterion.Criterion.Listing is not None and \
            hasattr(entity.ad_group_criterion.Criterion.Listing, 'Operand'):
            return entity.ad_group_criterion.Criterion.Listing.Operand
        return None

    @classmethod
    def _get_listing_attribute(cls, entity):
        if entity.ad_group_criterion.Criterion is not None and \
            hasattr(entity.ad_group_criterion.Criterion, 'Listing') and \
            entity.ad_group_criterion.Criterion.Listing is not None and \
            hasattr(entity.ad_group_criterion.Criterion.Listing, 'Attribute'):
            return entity.ad_group_criterion.Criterion.Listing.Attribute
        return None

    _MAPPINGS = [
        _SimpleBulkMapping(
            _StringTable.SubType,
            field_to_csv=lambda c: BulkAdGroupHotelListingGroup._get_listing_type(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion, 'ListingType', v)
        ),
        _SimpleBulkMapping(
            _StringTable.ParentAdGroupCriterionId,
            field_to_csv=lambda c: BulkAdGroupHotelListingGroup._get_parent_criterion_id(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion, 'ParentCriterionId',
                                              int(v) if v else None)
        ),
        _SimpleBulkMapping(
            _StringTable.HotelAttribute,
            field_to_csv=lambda c: BulkAdGroupHotelListingGroup._get_listing_operand(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion.Listing, 'Operand', v)
        ),
        _SimpleBulkMapping(
            _StringTable.HotelAttributeValue,
            field_to_csv=lambda c: BulkAdGroupHotelListingGroup._get_listing_attribute(c),
            csv_to_field=lambda c, v: setattr(c.ad_group_criterion.Criterion.Listing, 'Attribute', v)
        ),
    ]

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        super(BulkAdGroupHotelListingGroup, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkAdGroupHotelListingGroup._MAPPINGS)

    def process_mappings_from_row_values(self, row_values):
        super(BulkAdGroupHotelListingGroup, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkAdGroupHotelListingGroup._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkAdGroupHotelListingGroup, self).read_additional_data(stream_reader)

    def create_criterion(self):
        hotel_group = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelGroup')
        hotel_group.Listing = _CAMPAIGN_OBJECT_FACTORY_V13.create('HotelListing')
        hotel_group.Type = 'HotelGroup'
        return hotel_group
