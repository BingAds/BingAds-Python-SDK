from bingads.v10.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v10.internal.bulk.string_table import _StringTable
from bingads.v10.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
#from bingads.internal.extensions import bulk_device_preference_str, parse_device_preference
from bingads.v10.internal.bulk.entities.multi_record_bulk_entity import _MultiRecordBulkEntity
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V10
from bingads.internal.extensions import *

from .common import *
from .common import _BulkAdExtensionIdentifier
from .common import _BulkAdGroupAdExtensionAssociation
from .common import _BulkCampaignAdExtensionAssociation


class _SiteLinkAdExtensionIdentifier(_BulkAdExtensionIdentifier):
    def __init__(self,
                 account_id=None,
                 ad_extension_id=None,
                 status=None,
                 version=None):
        super(_SiteLinkAdExtensionIdentifier, self).__init__(
            account_id=account_id,
            ad_extension_id=ad_extension_id,
            status=status,
            version=version,
        )

    def __eq__(self, other):
        return isinstance(other, _SiteLinkAdExtensionIdentifier) \
            and self._account_id == other.account_id \
            and self._ad_extension_id == other.ad_extension_id

    def _create_entity_with_this_identifier(self):
        return BulkSiteLinkAdExtension(identifier=self)


class BulkAdGroupSiteLinkAdExtension(_BulkAdGroupAdExtensionAssociation):
    """ Represents an ad group level sitelink ad extension.

    This class exposes properties that can be read and written
    as fields of the AdGroup Sitelink Ad Extension record in a bulk file.

    For more information, see AdGroup Sitelink Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620262.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """
    pass


class BulkCampaignSiteLinkAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents an campaign level sitelink ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Sitelink Ad Extension record in a bulk file.

    For more information, see Campaign Sitelink Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620251.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass


class BulkSiteLink(_SingleRecordBulkEntity):
    """ Represents a sitelink.

    This class exposes the <see cref="BulkSiteLink.SiteLink"/> property that can be read and written
    as fields of the Sitelink Ad Extension record in a bulk file.

    For more information, see Sitelink Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620236.

    The Sitelink Ad Extension record includes the distinct properties of the :class:`.BulkSiteLink` class, combined with
    the common properties of the :class:`.BulkSiteLinkAdExtension` class.

    One :class:`BulkSiteLinkAdExtension` has one or more :class:`BulkSiteLink`. :class:`.BulkSiteLink` instance
    corresponds to one Sitelink Ad Extension record in the bulk file. If you upload a :class:`.BulkSiteLinkAdExtension`,
    then you are effectively replacing any existing site links for the sitelink ad extension.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_extension_id=None,
                 account_id=None,
                 status=None,
                 version=None,
                 order=None,
                 site_link=None, ):
        super(BulkSiteLink, self).__init__()

        self._identifier = _SiteLinkAdExtensionIdentifier(
            ad_extension_id=ad_extension_id,
            account_id=account_id,
            status=status,
            version=version,
        )
        self._order = order
        self._site_link = site_link

    @property
    def order(self):
        """ The order of the sitelink displayed to a search user in the ad.

        :rtype: int
        """

        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def site_link(self):
        """ The sitelink.

        See SiteLink at: https://msdn.microsoft.com/en-US/library/jj134381.aspx
        """

        return self._site_link

    @site_link.setter
    def site_link(self, value):
        self._site_link = value

    @property
    def ad_extension_id(self):
        """ The identifier of the ad extension.

        Corresponds to the 'Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.ad_extension_id

    @ad_extension_id.setter
    def ad_extension_id(self, value):
        self._identifier._ad_extension_id = value

    @property
    def account_id(self):
        """ The ad extension's parent account identifier.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.account_id

    @account_id.setter
    def account_id(self, value):
        self._identifier._account_id = value

    @property
    def status(self):
        """ The status of the ad extension.

        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._identifier.status

    @status.setter
    def status(self, value):
        self._identifier._status = value

    @property
    def version(self):
        """ The version of the ad extension.

        Corresponds to the 'Version' field in the bulk file.

        :rtype: int
        """

        return self._identifier.version

    @version.setter
    def version(self, value):
        self._identifier._version = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkExtensionOrder,
            field_to_csv=lambda c: bulk_str(c.order),
            csv_to_field=lambda c, v: setattr(c, 'order', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDisplayText,
            field_to_csv=lambda c: c.site_link.DisplayText,
            csv_to_field=lambda c, v: setattr(c.site_link, 'DisplayText', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDestinationUrl,
            field_to_csv=lambda c: c.site_link.DestinationUrl,
            csv_to_field=lambda c, v: setattr(c.site_link, 'DestinationUrl', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDescription1,
            field_to_csv=lambda c: c.site_link.Description1,
            csv_to_field=lambda c, v: setattr(c.site_link, 'Description1', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.SiteLinkDescription2,
            field_to_csv=lambda c: c.site_link.Description2,
            csv_to_field=lambda c, v: setattr(c.site_link, 'Description2', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.DevicePreference,
            field_to_csv=lambda c: bulk_device_preference_str(c.site_link.DevicePreference),
            csv_to_field=lambda c, v: setattr(
                c.site_link,
                'DevicePreference',
                parse_device_preference(v)
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.site_link.FinalUrls),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.site_link.FinalUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FinalMobileUrl,
            field_to_csv=lambda c: field_to_csv_Urls(c.site_link.FinalMobileUrls),
            csv_to_field=lambda c, v: csv_to_field_Urls(c.site_link.FinalMobileUrls, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrackingTemplate,
            field_to_csv=lambda c: bulk_str(c.site_link.TrackingUrlTemplate),
            csv_to_field=lambda c, v: setattr(c.site_link, 'TrackingUrlTemplate', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.CustomParameter,
            field_to_csv=lambda c: field_to_csv_UrlCustomParameters(c.site_link),
            csv_to_field=lambda c, v: csv_to_field_UrlCustomParameters(c.site_link, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: field_to_csv_SchedulingStartDate(c.site_link.Scheduling),
            csv_to_field=lambda c, v: csv_to_field_Date(c.site_link.Scheduling, 'StartDate', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: field_to_csv_SchedulingEndDate(c.site_link.Scheduling),
            csv_to_field = lambda c, v: csv_to_field_Date(c.site_link.Scheduling, 'EndDate', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.AdSchedule,
            field_to_csv=lambda c: field_to_csv_AdSchedule(c.site_link.Scheduling),
            csv_to_field=lambda c, v: csv_to_field_AdSchedule(c.site_link.Scheduling, v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.UseSearcherTimeZone,
            field_to_csv=lambda c: field_to_csv_UseSearcherTimeZone(c.site_link.Scheduling),
            csv_to_field=lambda c, v: setattr(c.site_link.Scheduling, 'UseSearcherTimeZone', parse_bool(v))
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._site_link = _CAMPAIGN_OBJECT_FACTORY_V10.create('SiteLink')
        self._identifier.read_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkSiteLink._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._site_link, 'site_link')
        self._identifier.write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkSiteLink._MAPPINGS)

    @property
    def can_enclose_in_multiline_entity(self):
        return True

    def enclose_in_multiline_entity(self):
        return BulkSiteLinkAdExtension(bulk_site_link=self)

    def read_additional_data(self, stream_reader):
        super(BulkSiteLink, self).read_additional_data(stream_reader)


class BulkSiteLinkAdExtension(_MultiRecordBulkEntity):
    """
    Represents a sitelink ad extension.

    This class exposes the :attr:`BulkSiteLinkAdExtension.SiteLinksAdExtension` property that can be read and written
    as fields of the Sitelink Ad Extension record in a bulk file.

    For more information, see Sitelink Ad Extension at http://go.microsoft.com/fwlink/?LinkID=620236.

    The Sitelink Ad Extension record includes the distinct properties of the :class:`.BulkSiteLink` class, combined with
    the common properties of the :class:`.BulkSiteLinkAdExtension` class,

    One :class:`.BulkSiteLinkAdExtension` has one or more :class:`.BulkSiteLink`. Each :class:`.BulkSiteLink` instance
    corresponds to one Sitelink Ad Extension record in the bulk file. If you upload a :class:`.BulkSiteLinkAdExtension`,
    then you are effectively replacing any existing site links for the sitelink ad extension.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 account_id=None,
                 site_links_ad_extension=None,
                 bulk_site_link=None,
                 identifier=None,):
        super(BulkSiteLinkAdExtension, self).__init__()

        self._account_id = account_id
        self._site_links_ad_extension = site_links_ad_extension
        self._bulk_site_links = []
        self._bulk_site_link = bulk_site_link
        self._identifier = identifier

        if self._bulk_site_link and self._identifier:
            raise ValueError('Conflicting arguments of bulk site link and site link identifier provided.')

        if self._bulk_site_link:
            if not isinstance(self._bulk_site_link, BulkSiteLink):
                raise ValueError('Site link object provided is not of type: {0}.'.format(BulkSiteLink.__name__))
            self._identifier = self._bulk_site_link._identifier

        if self._identifier:
            if not isinstance(self._identifier, _SiteLinkAdExtensionIdentifier):
                raise ValueError(
                    'Site link identifier object provided is not of type: {0}.'.format(_SiteLinkAdExtensionIdentifier.__name__)
                )
            self._has_delete_all_row = self._identifier.is_delete_row

            self._site_links_ad_extension = _CAMPAIGN_OBJECT_FACTORY_V10.create('SiteLinksAdExtension')
            self._site_links_ad_extension.Type = 'SiteLinksAdExtension'
            self._site_links_ad_extension.Id = self._identifier.ad_extension_id
            self._site_links_ad_extension.Status = self._identifier.status
            self._site_links_ad_extension.Version = self._identifier.version

            self.account_id = self._identifier.account_id
        if self._bulk_site_link:
            self._bulk_site_links.append(self._bulk_site_link)

    @property
    def account_id(self):
        """ The ad extension's parent account identifier.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def site_links_ad_extension(self):
        """ Defines an ad extension that specifies one or more sitelinks to add to a text add.

        :rtype: SiteLinksAdExtension
        """

        return self._site_links_ad_extension

    @site_links_ad_extension.setter
    def site_links_ad_extension(self, value):
        self._site_links_ad_extension = value

    @property
    def site_links(self):
        """ The list of :class:`BulkSiteLink` are represented by multiple Sitelink Ad Extension records in the file.

        :rtype: list[BulkSiteLink]
        """
        return self._bulk_site_links

    @property
    def child_entities(self):
        return self.site_links

    def write_to_stream(self, row_writer, exclude_readonly_data):
        self._validate_property_not_null(self._site_links_ad_extension, 'site_links_ad_extension')

        if self.site_links_ad_extension.Status != 'Deleted':
            self._validate_list_not_null_or_empty(
                self._site_links_ad_extension.SiteLinks,
                self._site_links_ad_extension.SiteLinks.SiteLink,
                'site_links_ad_extension.SiteLinks'
            )
        if self.site_links_ad_extension.Id is None:
            raise ValueError('SiteLinkAdExtension.Id must not be null. Please set it to a positive or negative Id.')

        delete_row = _SiteLinkAdExtensionIdentifier(
            status='Deleted',
            account_id=self.account_id,
            ad_extension_id=self.site_links_ad_extension.Id
        )
        row_writer.write_object_row(delete_row, exclude_readonly_data)

        if self.site_links_ad_extension.Status == 'Deleted':
            return

        for bulk_site_link in self.convert_raw_to_bulk_site_links():
            bulk_site_link.write_to_stream(row_writer, exclude_readonly_data)

    def read_related_data_from_stream(self, stream_reader):
        has_more_rows = True

        while has_more_rows:
            site_link_success, site_link = stream_reader.try_read(
                BulkSiteLink,
                lambda x: x._identifier == self._identifier
            )

            if site_link_success:
                self._bulk_site_links.append(site_link)
            else:
                identifier_success, identifier = stream_reader.try_read(
                    _SiteLinkAdExtensionIdentifier,
                    lambda x: x == self._identifier
                )

                if identifier_success:
                    if identifier.is_delete_row:
                        self._has_delete_all_row = True
                else:
                    has_more_rows = False

        if self._bulk_site_links:
            self.site_links_ad_extension.SiteLinks.SiteLink = \
                [bulk_site_link.site_link for bulk_site_link in sorted(self._bulk_site_links, key=lambda link: link.order)]
            self.site_links_ad_extension.Status = 'Active'
            self.site_links_ad_extension.Version = self._bulk_site_links[0].version  # consider if need to check the versions.
        else:
            self.site_links_ad_extension.Status = 'Deleted'

    def convert_raw_to_bulk_site_links(self):
        for index, site_link in enumerate(self.site_links_ad_extension.SiteLinks.SiteLink):
            bulk_site_link = BulkSiteLink(
                account_id=self.account_id,
                ad_extension_id=self.site_links_ad_extension.Id,
                order=index + 1,
                version=self.site_links_ad_extension.Version,
                site_link=site_link,
            )
            yield bulk_site_link

    @property
    def all_children_are_present(self):
        return self._has_delete_all_row
