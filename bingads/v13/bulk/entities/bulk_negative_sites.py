from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.entities.bulk_entity_identifier import _BulkEntityIdentifier
from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _DynamicColumnNameMapping
from bingads.v13.internal.bulk.entities.multi_record_bulk_entity import _MultiRecordBulkEntity
from bingads.v13.internal.extensions import bulk_str


class _BulkNegativeSite(_SingleRecordBulkEntity):
    """ This abstract base class for the bulk negative sites that are assigned individually to a campaign or ad group entity.

    *See also:*

    * :class:`.BulkAdGroupNegativeSite`
    * :class:`.BulkCampaignNegativeSite`
    """

    def __init__(self, identifier, website=None):
        super(_BulkNegativeSite, self).__init__()

        self._identifier = identifier
        self._website = website

    @property
    def website(self):
        """ The URL of a website on which you do not want your ads displayed.

        Corresponds to the 'Website' field in the bulk file.

        :rtype: str
        """

        return self._website

    @website.setter
    def website(self, website):
        self._website = website

    @property
    def status(self):
        """ The status of the negative site association.

        :rtype: str
        """

        return self._identifier.status

    @status.setter
    def status(self, value):
        self._identifier.status = value

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Website,
            field_to_csv=lambda c: c.website,
            csv_to_field=lambda c, v: setattr(c, 'website', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self._identifier.read_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkNegativeSite._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._identifier.write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, _BulkNegativeSite._MAPPINGS)

    @property
    def can_enclose_in_multiline_entity(self):
        return True

    def enclose_in_multiline_entity(self):
        return self.create_negative_sites_with_this_negative_site()

    def create_negative_sites_with_this_negative_site(self):
        raise NotImplementedError()

    def read_additional_data(self, stream_reader):
        super(_BulkNegativeSite, self).read_additional_data(stream_reader)


class BulkAdGroupNegativeSite(_BulkNegativeSite):
    """ Represents a negative site that is assigned to an ad group. Each negative site can be read or written in a bulk file.

    This class exposes properties that can be read and written as fields of the Ad Group Negative Site record in a bulk file.

    For more information, see Ad Group Negative Site at https://go.microsoft.com/fwlink/?linkid=846127.

    One :class:`.BulkAdGroupNegativeSites` exposes a read only list of :class:`.BulkAdGroupNegativeSite`. Each
    :class:`.BulkAdGroupNegativeSite` instance corresponds to one Ad Group Negative Site record in the bulk file. If you
    upload a :class:`.BulkAdGroupNegativeSites`, then you are effectively replacing any existing negative sites
    assigned to the ad group.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 status=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None,
                 website=None):
        super(BulkAdGroupNegativeSite, self).__init__(
            _BulkAdGroupNegativeSitesIdentifier(
                status=status,
                ad_group_id=ad_group_id,
                ad_group_name=ad_group_name,
                campaign_name=campaign_name,
            ),
            website=website
        )

    @property
    def ad_group_id(self):
        """ The identifier of the ad group that the negative site is assigned.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.ad_group_id

    @ad_group_id.setter
    def ad_group_id(self, value):
        self._identifier.ad_group_id = value

    @property
    def ad_group_name(self):
        """ The name of the ad group that the negative site is assigned.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._identifier.ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._identifier.ad_group_name = value

    @property
    def campaign_name(self):
        """ The name of the ad group that the negative site is assigned.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._identifier.campaign_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._identifier.campaign_name = value

    def create_negative_sites_with_this_negative_site(self):
        return BulkAdGroupNegativeSites(site=self)


class BulkCampaignNegativeSite(_BulkNegativeSite):
    """ Represents a negative site that is assigned to an campaign. Each negative site can be read or written in a bulk file.

    This class exposes properties that can be read and written as fields of the Campaign Negative Site record in a bulk file.

    For more information, see Campaign Negative Site at https://go.microsoft.com/fwlink/?linkid=846127.

    One :class:`.BulkCampaignNegativeSites` exposes a read only list of :class:`.BulkCampaignNegativeSite`. Each
    :class:`.BulkCampaignNegativeSite` instance corresponds to one Campaign Negative Site record in the bulk file. If you
    upload a :class:`.BulkCampaignNegativeSites`, then you are effectively replacing any existing negative sites
    assigned to the campaign.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 status=None,
                 campaign_id=None,
                 campaign_name=None,
                 website=None):
        super(BulkCampaignNegativeSite, self).__init__(
            _BulkCampaignNegativeSitesIdentifier(
                status=status,
                campaign_id=campaign_id,
                campaign_name=campaign_name
            ),
            website=website
        )

    @property
    def campaign_id(self):
        """ The identifier of the campaign that the negative site is assigned.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._identifier.campaign_id = value

    @property
    def campaign_name(self):
        """ The name of the campaign that the negative site is assigned.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """
        return self._identifier.campaign_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._identifier.campaign_name = value

    def create_negative_sites_with_this_negative_site(self):
        return BulkCampaignNegativeSites(site=self)


class _BulkNegativeSites(_MultiRecordBulkEntity):
    """ This abstract base class for the bulk negative sites that assigned in sets to a campaign or ad group entity. """

    def __init__(self, status=None, site=None, identifier=None):
        super(_BulkNegativeSites, self).__init__()

        self._bulk_negative_sites = []
        self._first_row_identifier = None
        self._has_delete_all_row = None

        self._site = site
        self._identifier = identifier

        if self._site and self._identifier:
            raise ValueError('Conflicting keyword arguments of site and identifier provided')

        if self._site:
            if not isinstance(self._site, self.site_class):
                raise ValueError('Negative site object provided is not of type: {0}'.format(self.site_class.__name__))
            self._bulk_negative_sites.append(self._site)
            self._identifier = self._site._identifier

        if self._identifier:
            if not isinstance(self._identifier, self.identifier_class):
                raise ValueError(
                    'Negative site object provided is not of type: {0}'.format(self.identifier_class.__name__))
            self._first_row_identifier = self._identifier
            self._has_delete_all_row = self._identifier.is_delete_row

        self._status = status

    @property
    def status(self):
        """ The status of the negative site association.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def negative_sites(self):
        return self._bulk_negative_sites

    @property
    def child_entities(self):
        return self.negative_sites

    def _create_identifier(self):
        raise NotImplementedError()

    def _validate_properties_not_null(self):
        raise NotImplementedError()

    def write_to_stream(self, row_writer, exclude_readonly_data):
        self._validate_properties_not_null()

        delete_row = self._create_identifier()
        delete_row._status = 'Deleted'
        row_writer.write_object_row(delete_row, exclude_readonly_data)

        if self._status == 'Deleted':
            return

        for site in self.convert_api_to_bulk_negative_sites():
            site.write_to_stream(row_writer, exclude_readonly_data)

    def convert_api_to_bulk_negative_sites(self):
        raise NotImplementedError()

    def reconstruct_api_objects(self):
        raise NotImplementedError()

    @property
    def site_class(self):
        raise NotImplementedError()

    @property
    def identifier_class(self):
        raise NotImplementedError()

    def read_related_data_from_stream(self, stream_reader):
        has_more_rows = True
        while has_more_rows:
            site_success, site = stream_reader.try_read(
                self.site_class,
                lambda x: x._identifier == self._first_row_identifier
            )
            if site_success:
                self._bulk_negative_sites.append(site)
            else:
                identifier_success, identifier = stream_reader.try_read(
                    self.identifier_class,
                    lambda x: x == self._first_row_identifier
                )
                if identifier_success:
                    if identifier.is_delete_row:
                        self._has_delete_all_row = True
                else:
                    has_more_rows = False

        self.reconstruct_api_objects()
        self._status = 'Active' if self._bulk_negative_sites else 'Deleted'

    @property
    def all_children_are_present(self):
        return self._has_delete_all_row


class BulkAdGroupNegativeSites(_BulkNegativeSites):
    """ Represents one or more negative sites that are assigned to an ad group. Each negative site can be read or written in a bulk file.

    This class exposes properties that can be read and written as fields of the Ad Group Negative Site record in a bulk file.

    For more information, see Ad Group Negative Site at https://go.microsoft.com/fwlink/?linkid=846127.

    One :class:`.BulkAdGroupNegativeSites` has one or more :class:`.BulkAdGroupNegativeSite`. Each :class:`.BulkAdGroupNegativeSite` instance
    corresponds to one Ad Group Negative Site record in the bulk file. If you upload a :class:`.BulkAdGroupNegativeSites`,
    then you are effectively replacing any existing negative sites assigned to the ad group.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 ad_group_negative_sites=None,
                 ad_group_name=None,
                 campaign_name=None,
                 status=None,
                 site=None,
                 identifier=None):
        super(BulkAdGroupNegativeSites, self).__init__(
            status=status,
            site=site,
            identifier=identifier,
        )

        self._ad_group_negative_sites = ad_group_negative_sites
        self._ad_group_name = ad_group_name
        self._campaign_name = campaign_name

        if self._identifier:
            self.set_data_from_identifier(self._identifier)

    @property
    def ad_group_negative_sites(self):
        """ The AdGroupNegativeSites Data Object of the Campaign Management Service.

        subset of AdGroupNegativeSites properties are available in the Ad Group Negative Site record.
        For more information, see Ad Group Negative Site at https://go.microsoft.com/fwlink/?linkid=846127.
        """

        return self._ad_group_negative_sites

    @ad_group_negative_sites.setter
    def ad_group_negative_sites(self, ad_group_negative_sites):
        self._ad_group_negative_sites = ad_group_negative_sites

    @property
    def ad_group_name(self):
        """ The name of the ad group that the negative site is assigned.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, ad_group_name):
        self._ad_group_name = ad_group_name

    @property
    def campaign_name(self):
        """ The name of the campaign that the negative site is assigned.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    def set_data_from_identifier(self, identifier):
        self._ad_group_negative_sites = _CAMPAIGN_OBJECT_FACTORY_V13.create('AdGroupNegativeSites')
        self._ad_group_negative_sites.AdGroupId = identifier.ad_group_id
        self._ad_group_name = identifier.ad_group_name
        self._campaign_name = identifier.campaign_name

    def convert_api_to_bulk_negative_sites(self):
        self._validate_list_not_null_or_empty(
            self._ad_group_negative_sites.NegativeSites,
            self._ad_group_negative_sites.NegativeSites.string,
            'ad_group_negative_sites.negative_sites'
        )

        def convert_api_to_bulk_negative_site(website):
            bulk_ad_group_negative_site = BulkAdGroupNegativeSite()
            bulk_ad_group_negative_site.ad_group_id = self._ad_group_negative_sites.AdGroupId
            bulk_ad_group_negative_site.ad_group_name = self._ad_group_name
            bulk_ad_group_negative_site.campaign_name = self._campaign_name
            bulk_ad_group_negative_site._website = website
            return bulk_ad_group_negative_site

        return map(convert_api_to_bulk_negative_site, self._ad_group_negative_sites.NegativeSites.string)

    def reconstruct_api_objects(self):
        self._ad_group_negative_sites.NegativeSites.string = list(map(lambda x: x.website, self.negative_sites))

    def _create_identifier(self):
        return _BulkAdGroupNegativeSitesIdentifier(
            ad_group_id=self._ad_group_negative_sites.AdGroupId,
            ad_group_name=self._ad_group_name,
            campaign_name=self.campaign_name
        )

    def _validate_properties_not_null(self):
        self._validate_property_not_null(self._ad_group_negative_sites, 'ad_group_negative_sites')

    @property
    def identifier_class(self):
        return _BulkAdGroupNegativeSitesIdentifier

    @property
    def site_class(self):
        return BulkAdGroupNegativeSite


class BulkCampaignNegativeSites(_BulkNegativeSites):
    """ Represents one or more negative sites that are assigned to an campaign. Each negative site can be read or written in a bulk file.

    This class exposes properties that can be read and written as fields of the Campaign Negative Site record in a bulk file.

    For more information, see Campaign Negative Site at https://go.microsoft.com/fwlink/?linkid=846127.

    One :class:`.BulkCampaignNegativeSites` has one or more :class:`.BulkCampaignNegativeSite`. Each :class:`.BulkCampaignNegativeSite` instance
    corresponds to one Campaign Negative Site record in the bulk file. If you upload a :class:`.BulkCampaignNegativeSites`,
    then you are effectively replacing any existing negative sites assigned to the campaign.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 campaign_negative_sites=None,
                 campaign_name=None,
                 status=None,
                 site=None,
                 identifier=None):
        super(BulkCampaignNegativeSites, self).__init__(
            status=status,
            site=site,
            identifier=identifier
        )

        self._campaign_negative_sites = campaign_negative_sites
        self._campaign_name = campaign_name

        if self._identifier:
            self.set_data_from_identifier(self._identifier)

    @property
    def campaign_negative_sites(self):
        """ The CampaignNegativeSites Data Object of the Campaign Management Service.

        A subset of CampaignNegativeSites properties are available in the Campaign Negative Site record.
        For more information, see Campaign Negative Site at https://go.microsoft.com/fwlink/?linkid=846127.

        """

        return self._campaign_negative_sites

    @campaign_negative_sites.setter
    def campaign_negative_sites(self, campaign_negative_sites):
        self._campaign_negative_sites = campaign_negative_sites

    @property
    def campaign_name(self):
        """ The name of the campaign that the negative site is assigned.

        Corresponds to the 'Campaign' field in the bulk file.
        :rtype: str
        """

        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    def set_data_from_identifier(self, identifier):
        self._campaign_negative_sites = _CAMPAIGN_OBJECT_FACTORY_V13.create('CampaignNegativeSites')
        self.campaign_negative_sites.CampaignId = identifier.campaign_id
        self._campaign_name = identifier.campaign_name

    def convert_api_to_bulk_negative_sites(self):
        self._validate_list_not_null_or_empty(
            self._campaign_negative_sites.NegativeSites,
            self._campaign_negative_sites.NegativeSites.string,
            'campaign_negative_sites.negative_sites'
        )

        def convert_api_to_bulk_negative_site(website):
            bulk_campaign_negative_site = BulkCampaignNegativeSite()
            bulk_campaign_negative_site.campaign_id = self._campaign_negative_sites.CampaignId
            bulk_campaign_negative_site.campaign_name = self._campaign_name
            bulk_campaign_negative_site._website = website
            return bulk_campaign_negative_site

        return map(convert_api_to_bulk_negative_site, self._campaign_negative_sites.NegativeSites.string)

    def reconstruct_api_objects(self):
        self._campaign_negative_sites.NegativeSites.string = list(map(lambda x: x.website, self.negative_sites))

    def _create_identifier(self):
        return _BulkCampaignNegativeSitesIdentifier(
            campaign_id=self._campaign_negative_sites.CampaignId,
            campaign_name=self._campaign_name
        )

    def _validate_properties_not_null(self):
        self._validate_property_not_null(self._campaign_negative_sites, 'campaign_negative_sites')

    @property
    def identifier_class(self):
        return _BulkCampaignNegativeSitesIdentifier

    @property
    def site_class(self):
        return BulkCampaignNegativeSite


class _BulkNegativeSiteIdentifier(_BulkEntityIdentifier):
    def __init__(self, status=None, entity_id=None, entity_name=None):
        self._status = status
        self._entity_id = entity_id
        self._entity_name = entity_name

    @property
    def status(self):
        return self._status

    @property
    def entity_id(self):
        return self._entity_id

    @property
    def entity_name(self):
        return self._entity_name

    @property
    def _parent_column_name(self):
        raise NotImplementedError()

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c._status),
            csv_to_field=lambda c, v: setattr(c, '_status', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: None if c._entity_id == 0 else bulk_str(c._entity_id),
            csv_to_field=lambda c, v: setattr(c, '_entity_id', int(v) if v else 0)
        ),
        _DynamicColumnNameMapping(
            header_func=lambda c: c._parent_column_name,
            field_to_csv=lambda c: c._entity_name,
            csv_to_field=lambda c, v: setattr(c, '_entity_name', v)
        )
    ]

    @property
    def is_delete_row(self):
        return self._status == 'Deleted'

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _BulkNegativeSiteIdentifier._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, _BulkNegativeSiteIdentifier._MAPPINGS)


class _BulkCampaignNegativeSitesIdentifier(_BulkNegativeSiteIdentifier):
    def __init__(self, status=None, campaign_id=None, campaign_name=None):
        super(_BulkCampaignNegativeSitesIdentifier, self).__init__(
            status,
            campaign_id,
            campaign_name,
        )

    def __eq__(self, other):
        is_name_not_empty = (
            self.campaign_name is not None and
            len(self.campaign_name) > 0
        )
        return (
            type(self) == type(other) and
            (
                self.campaign_id == other.campaign_id or
                (
                    is_name_not_empty and
                    self.campaign_name == other.campaign_name
                )
            )
        )

    @property
    def campaign_id(self):
        return self._entity_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._entity_id = value

    @property
    def campaign_name(self):
        return self._entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._entity_name = value

    def _create_entity_with_this_identifier(self):
        return BulkCampaignNegativeSites(identifier=self)

    @property
    def _parent_column_name(self):
        return _StringTable.Campaign


class _BulkAdGroupNegativeSitesIdentifier(_BulkNegativeSiteIdentifier):
    def __init__(self,
                 status=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None):
        super(_BulkAdGroupNegativeSitesIdentifier, self).__init__(
            status,
            ad_group_id,
            ad_group_name,
        )
        self._campaign_name = campaign_name

    def __eq__(self, other):
        is_name_not_empty = (
            self.campaign_name is not None and
            len(self.campaign_name) > 0 and
            self.ad_group_name is not None and
            len(self.ad_group_name) > 0
        )
        return (
            type(self) == type(other) and
            (
                self.ad_group_id == other.ad_group_id or
                (
                    is_name_not_empty and
                    self.campaign_name == other.campaign_name and
                    self.ad_group_name == other.ad_group_name
                )
            )
        )

    @property
    def ad_group_id(self):
        return self._entity_id

    @ad_group_id.setter
    def ad_group_id(self, value):
        self._entity_id = value

    @property
    def ad_group_name(self):
        return self._entity_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._entity_name = value

    @property
    def campaign_name(self):
        return self._campaign_name

    @campaign_name.setter
    def campaign_name(self, campaign_name):
        self._campaign_name = campaign_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: c.campaign_name,
            csv_to_field=lambda c, v: setattr(c, 'campaign_name', v)
        ),
    ]

    def read_from_row_values(self, row_values):
        super(_BulkAdGroupNegativeSitesIdentifier, self).read_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkAdGroupNegativeSitesIdentifier._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        super(_BulkAdGroupNegativeSitesIdentifier, self).write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, _BulkAdGroupNegativeSitesIdentifier._MAPPINGS)

    def _create_entity_with_this_identifier(self):
        return BulkAdGroupNegativeSites(identifier=self)

    @property
    def _parent_column_name(self):
        return _StringTable.AdGroup
