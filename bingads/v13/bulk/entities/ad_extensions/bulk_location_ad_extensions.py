from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from .common import *
from .common import _BulkAdExtensionBase
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAccountAdExtensionAssociation

_LocationAdExtension = type(_CAMPAIGN_OBJECT_FACTORY_V13.create('LocationAdExtension'))


class BulkLocationAdExtension(_BulkAdExtensionBase):
    """ Represents an location ad extension.

    This class exposes the :attr:`location_ad_extension` property that can be read and written
    as fields of the Location Ad Extension record in a bulk file.

    For more information, see Location Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, account_id=None, ad_extension=None):
        if ad_extension and not isinstance(ad_extension, _LocationAdExtension):
            raise ValueError('The type of ad_extension is: {0}, should be: {1}'.format(
                type(ad_extension),
                'LocationAdExtension'
            ))
        super(BulkLocationAdExtension, self).__init__(
            account_id=account_id,
            ad_extension=ad_extension
        )

    @property
    def location_ad_extension(self):
        """ The location ad extension.

        see Location Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_extension

    @location_ad_extension.setter
    def location_ad_extension(self, value):
        self._ad_extension = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.BusinessName,
            field_to_csv=lambda c: c.location_ad_extension.CompanyName,
            csv_to_field=lambda c, v: setattr(c.location_ad_extension, 'CompanyName', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PhoneNumber,
            field_to_csv=lambda c: bulk_optional_str(c.location_ad_extension.PhoneNumber, c.location_ad_extension.Id),
            csv_to_field=lambda c, v: setattr(c.location_ad_extension, 'PhoneNumber', v if v else '')
        ),
        _SimpleBulkMapping(
            header=_StringTable.GeoCodeStatus,
            field_to_csv=lambda c: bulk_str(c.location_ad_extension.GeoCodeStatus),
            csv_to_field=lambda c, v: csv_to_field_enum(c.location_ad_extension, v, 'GeoCodeStatus', BusinessGeoCodeStatus)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AddressLine1,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(
                c,
                lambda x: x.StreetAddress
            ),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'StreetAddress', v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.AddressLine2,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(
                c,
                lambda x: bulk_optional_str(x.StreetAddress2, c.location_ad_extension.Id)
            ),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'StreetAddress2', v if v else '')
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.City,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(c, lambda x: x.CityName),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'CityName', v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.ProvinceName,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(c, lambda x: x.ProvinceName),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'ProvinceName', v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.StateOrProvince,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(c, lambda x: x.ProvinceCode),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'ProvinceCode', v)
            )
        ),

        _SimpleBulkMapping(
            header=_StringTable.PostalCode,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(c, lambda x: x.PostalCode),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'PostalCode', v)
            )
        ),

        _SimpleBulkMapping(
            header=_StringTable.CountryCode,
            field_to_csv=lambda c: BulkLocationAdExtension.get_address_part(c, lambda x: x.CountryCode),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_address_part(
                c,
                lambda x: setattr(x, 'CountryCode', v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Latitude,
            field_to_csv=lambda c: BulkLocationAdExtension.get_geo_point_part(
                c,
                lambda x: bulk_str(
                    float(x.LatitudeInMicroDegrees) / 1000000.0
                )
                if x.LatitudeInMicroDegrees is not None else None
            ),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_geo_point_part(
                c,
                lambda x, latitude: setattr(x, 'LatitudeInMicroDegrees', int(round(float(latitude) * 1000000))),
                v
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Longitude,
            field_to_csv=lambda c: BulkLocationAdExtension.get_geo_point_part(
                c,
                lambda x: bulk_str(
                    float(x.LongitudeInMicroDegrees) / 1000000.0
                )
                if x.LongitudeInMicroDegrees is not None else None
            ),
            csv_to_field=lambda c, v: BulkLocationAdExtension.set_geo_point_part(
                c,
                lambda x, longitude: setattr(x, 'LongitudeInMicroDegrees', int(round(float(longitude) * 1000000))),
                v
            )
        ),
    ]

    @staticmethod
    def get_address_part(bulk_ad_extension, get_func):
        if bulk_ad_extension.location_ad_extension.Address is not None:
            return get_func(bulk_ad_extension.location_ad_extension.Address)
        else:
            return None

    @staticmethod
    def set_address_part(bulk_ad_extension, set_func):
        if bulk_ad_extension.location_ad_extension.Address is None:
            bulk_ad_extension.location_ad_extension.Address = _CAMPAIGN_OBJECT_FACTORY_V13.create('Address')
        set_func(bulk_ad_extension.location_ad_extension.Address)

    @staticmethod
    def get_geo_point_part(bulk_ad_extension, get_func):
        if bulk_ad_extension.location_ad_extension.GeoPoint is not None:
            return get_func(bulk_ad_extension.location_ad_extension.GeoPoint)
        else:
            return None

    @staticmethod
    def set_geo_point_part(bulk_ad_extension, set_func, value):
        if not value:
            return
        if bulk_ad_extension.location_ad_extension.GeoPoint is None:
            bulk_ad_extension.location_ad_extension.GeoPoint = _CAMPAIGN_OBJECT_FACTORY_V13.create('GeoPoint')
        set_func(bulk_ad_extension.location_ad_extension.GeoPoint, value)

    def process_mappings_from_row_values(self, row_values):
        self.location_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V13.create('LocationAdExtension')
        self.location_ad_extension.Type = 'LocationAdExtension'
        if row_values[_StringTable.Latitude] or row_values[_StringTable.Longitude]:
            self.location_ad_extension.GeoPoint = _CAMPAIGN_OBJECT_FACTORY_V13.create('GeoPoint')
        super(BulkLocationAdExtension, self).process_mappings_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkLocationAdExtension._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.location_ad_extension, 'location_ad_extension')
        super(BulkLocationAdExtension, self).process_mappings_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkLocationAdExtension._MAPPINGS)


class BulkAccountLocationAdExtension(_BulkAccountAdExtensionAssociation):
    """ Represents an account level location ad extension.

    This class exposes properties that can be read and written
    as fields of the Account Location Ad Extension record in a bulk file.

    For more information, see Account Location Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkCampaignLocationAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level location ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Location Ad Extension record in a bulk file.

    For more information, see Campaign Location Ad Extension at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass