from bingads.internal.bulk.entities.multi_record_bulk_entity import _MultiRecordBulkEntity
from bingads.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.internal.bulk.entities.bulk_entity_identifier import _BulkEntityIdentifier
from bingads.internal.bulk.mappings import _SimpleBulkMapping, _DynamicColumnNameMapping
from bingads.internal.bulk.string_table import _StringTable
from bingads.internal.extensions import *
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY


class _BulkTargetIdentifier(_BulkEntityIdentifier):
    def __init__(self,
                 target_bid_type,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        self._target_bid_type = target_bid_type
        self._status = status
        self._target_id = target_id
        self._entity_id = entity_id
        self._entity_name = entity_name
        self._parent_entity_name = parent_entity_name

    def __eq__(self, other):
        return type(self) == type(other) \
            and self.entity_id == other.entity_id \
            and self.entity_name == other.entity_name \
            and self.parent_entity_name == other.parent_entity_name

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: bulk_str(c.status),
            csv_to_field=lambda c, v: setattr(c, '_status', v if v else None),
        ),
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.target_id),
            csv_to_field=lambda c, v: setattr(c, '_target_id', int(v) if v else None),
        ),
        _SimpleBulkMapping(
            header=_StringTable.ParentId,
            field_to_csv=lambda c: bulk_str(c.entity_id),
            csv_to_field=lambda c, v: setattr(c, '_entity_id', int(v) if v else None),
        ),
        _DynamicColumnNameMapping(
            header_func=lambda c: c.entity_column_name,
            field_to_csv=lambda c: c.entity_name,
            csv_to_field=lambda c, v: setattr(c, '_entity_name', v),
        ),
    ]

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.convert_to_values(row_values, _BulkTargetIdentifier._MAPPINGS)

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, _BulkTargetIdentifier._MAPPINGS)

    @property
    def is_delete_row(self):
        return self.status == 'Deleted'

    def _create_entity_with_this_identifier(self):
        raise NotImplementedError()

    @property
    def entity_column_name(self):
        raise NotImplementedError()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def target_id(self):
        return self._target_id

    @target_id.setter
    def target_id(self, value):
        self._target_id = value

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = value

    @property
    def entity_name(self):
        return self._entity_name

    @entity_name.setter
    def entity_name(self, value):
        self._entity_name = value

    @property
    def parent_entity_name(self):
        return self._parent_entity_name

    @parent_entity_name.setter
    def parent_entity_name(self, value):
        self._parent_entity_name = value

    @property
    def target_bid_type(self):
        return self._target_bid_type


class _BulkCampaignTargetIdentifier(_BulkTargetIdentifier):
    @property
    def entity_column_name(self):
        return _StringTable.Campaign

    def _create_entity_with_this_identifier(self):
        return BulkCampaignTarget(identifier=self)

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


class _BulkAdGroupTargetIdentifier(_BulkTargetIdentifier):
    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Campaign,
            field_to_csv=lambda c: bulk_str(c.parent_entity_name),
            csv_to_field=lambda c, v: setattr(c, '_parent_entity_name', v)
        )
    ]

    def __eq__(self, other):
        return super(_BulkAdGroupTargetIdentifier, self).__eq__(other) and self.campaign_name == other.campaign_name

    def write_to_row_values(self, row_values, exclude_readonly_data):
        super(_BulkAdGroupTargetIdentifier, self).write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, _BulkAdGroupTargetIdentifier._MAPPINGS)

    def read_from_row_values(self, row_values):
        super(_BulkAdGroupTargetIdentifier, self).read_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkAdGroupTargetIdentifier._MAPPINGS)

    @property
    def entity_column_name(self):
        return _StringTable.AdGroup

    def _create_entity_with_this_identifier(self):
        return BulkAdGroupTarget(identifier=self)

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
        return self._parent_entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._parent_entity_name = value


class _BulkTargetBid(_SingleRecordBulkEntity):
    """ This base class provides properties that are shared by all bulk target bid classes.

    For example :class:`.BulkAdGroupDayTimeTargetBid`.
    """
    def __init__(self,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        super(_BulkTargetBid, self).__init__()
        self._identifier = self._identifier_type(
            target_bid_type=type(self),
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def process_mappings_from_row_values(self, row_values):
        self._prepare_process_mapping_from_row_values()
        self._identifier.read_from_row_values(row_values)
        row_values.convert_to_entity(self, type(self)._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._identifier.write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, type(self)._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(_BulkTargetBid, self).read_additional_data(stream_reader)

    @property
    def can_enclose_in_multiline_entity(self):
        return True

    def enclose_in_multiline_entity(self):
        if isinstance(self, _BulkTargetBidCampaignMixin):
            return BulkCampaignTarget(bulk_target_bid=self)
        elif isinstance(self, _BulkTargetBidAdGroupMixin):
            return BulkAdGroupTarget(bulk_target_bid=self)
        else:
            raise Exception(
                'BulkTargetBid class: {0}, should be extended with either {1} or {2}'.format(
                    type(self).__name__,
                    _BulkTargetBidCampaignMixin.__name__,
                    _BulkTargetBidAdGroupMixin.__name__
                )
            )

    def _prepare_process_mapping_from_row_values(self):
        raise NotImplementedError()

    @property
    def _identifier_type(self):
        if isinstance(self, _BulkTargetBidCampaignMixin):
            return _BulkCampaignTargetIdentifier
        elif isinstance(self, _BulkTargetBidAdGroupMixin):
            return _BulkAdGroupTargetIdentifier
        else:
            raise Exception(
                'BulkTargetBid class: {0}, should be extended with either {1} or {2}'.format(
                    type(self).__name__,
                    _BulkTargetBidCampaignMixin.__name__,
                    _BulkTargetBidAdGroupMixin.__name__
                )
            )

    @property
    def status(self):
        """ The status of the target bid.

        The value is Active if the target bid is available in the target.
        The value is Deleted if the target bid is deleted from the target, or should be deleted in a subsequent upload operation.
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._identifier.status

    @status.setter
    def status(self, value):
        self._identifier.status = value

    @property
    def target_id(self):
        """ The identifier of the target that contains this target bid.

        Corresponds to the 'Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.target_id

    @target_id.setter
    def target_id(self, value):
        self._identifier.target_id = value

    @property
    def entity_id(self):
        return self._identifier.entity_id

    @entity_id.setter
    def entity_id(self, value):
        self._identifier.entity_id = value

    @property
    def entity_name(self):
        return self._identifier.entity_name

    @entity_name.setter
    def entity_name(self, value):
        self._identifier.entity_name = value

    @property
    def parent_entity_name(self):
        return self._identifier.parent_entity_name

    @parent_entity_name.setter
    def parent_entity_name(self, value):
        self._identifier.parent_entity_name = value


class _BulkTargetBidCampaignMixin(object):
    @property
    def campaign_id(self):
        """ The identifier of the campaign that the target is associated.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.campaign_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._identifier.campaign_id = value

    @property
    def campaign_name(self):
        """ The name of the campaign that the target is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._identifier.campaign_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._identifier.campaign_name = value


class _BulkTargetBidAdGroupMixin(object):
    @property
    def ad_group_id(self):
        """ The identifier of the ad group that the target is associated.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._identifier.ad_group_id

    @ad_group_id.setter
    def ad_group_id(self, value):
        self._identifier.ad_group_id = value

    @property
    def ad_group_name(self):
        """ The name of the ad group that target is associated.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._identifier.ad_group_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._identifier.ad_group_name = value

    @property
    def campaign_name(self):
        """ The name of the ad group that target is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._identifier.campaign_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._identifier.campaign_name = value


class _BulkSubTarget(_MultiRecordBulkEntity):
    """ This base class provides properties that are shared by all bulk sub target classes. """

    def __init__(self,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        super(_BulkSubTarget, self).__init__()
        self._target_id = target_id
        self._status = status
        self._entity_id = entity_id
        self._entity_name = entity_name
        self._parent_entity_name = parent_entity_name
        self._bids = []
        self._identifier = None
        self._has_delete_all_row = False
        self._is_being_written_as_part_of_parent_target = False

    def set_bids(self, bids):
        for bid in bids:
            self._bids.append(bid)
        self._convert_bulk_entities_to_target()
        self.status = 'Active' if self._bids else 'Deleted'

    def set_identifier(self, identifier):
        self._identifier = identifier
        self._has_delete_all_row = identifier.is_delete_row
        self.entity_id = identifier.entity_id
        self.target_id = identifier.target_id
        self.entity_name = identifier.entity_name
        self.parent_entity_name = identifier.parent_entity_name

    def _create_identifier_before_write(self):
        identifier = self._create_bid()._identifier
        identifier.status = 'Deleted'
        identifier.target_id = self.target_id
        identifier.entity_id = self.entity_id
        identifier.entity_name = self.entity_name
        identifier.parent_entity_name = self.parent_entity_name
        return identifier

    def write_to_stream(self, row_writer, exclude_readonly_data):

        if (not self.is_being_written_as_part_of_parent_target) and (not self.status == 'Deleted'):
            self._validate_properties()
            # as suds accepts empty sub targets, we accept it either.
            self._validate_bids()

        identifier = self._create_identifier_before_write()
        identifier.write_to_stream(row_writer, exclude_readonly_data)
        if self.status == 'Deleted':
            return
        for bulk_entity in self._convert_target_to_bulk_entities():
            bulk_entity.write_to_stream(row_writer, exclude_readonly_data)

    def read_related_data_from_stream(self, stream_reader):
        pass

    def _create_and_populate_bid(self):
        bid = self._create_bid()
        bid.status = self.status
        bid.target_id = self.target_id
        bid.entity_id = self.entity_id
        bid.entity_name = self.entity_name
        bid.parent_entity_name = self.parent_entity_name
        return bid

    @property
    def bids(self):
        """ The list of target bids corresponding the this sub target type.

        :rtype: list
        """

        return self._bids

    @property
    def child_entities(self):
        return self._bids

    @property
    def all_children_are_present(self):
        return self._has_delete_all_row

    @property
    def is_being_written_as_part_of_parent_target(self):
        return self._is_being_written_as_part_of_parent_target

    @is_being_written_as_part_of_parent_target.setter
    def is_being_written_as_part_of_parent_target(self, value):
        self._is_being_written_as_part_of_parent_target = value

    def _create_bid(self):
        raise NotImplementedError()

    def _validate_properties(self):
        raise NotImplementedError()

    def _validate_bids(self):
        raise NotImplementedError()

    def _convert_target_to_bulk_entities(self):
        raise NotImplementedError()

    def _convert_bulk_entities_to_target(self):
        raise NotImplementedError()

    @property
    def status(self):
        """ The status of the target.

        The value is Active if the target is available in the customer's shared library.
        The value is Deleted if the target is deleted from the customer's shared library, or should be deleted in a subsequent upload operation.
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def target_id(self):
        """ The identifier of the target.

        Corresponds to the 'Id' field in the bulk file.

        :rtype: int
        """

        return self._target_id

    @target_id.setter
    def target_id(self, value):
        self._target_id = value

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = value

    @property
    def entity_name(self):
        return self._entity_name

    @entity_name.setter
    def entity_name(self, value):
        self._entity_name = value

    @property
    def parent_entity_name(self):
        return self._parent_entity_name

    @parent_entity_name.setter
    def parent_entity_name(self, value):
        self._parent_entity_name = value


class _BulkSubTargetCampaignMixin(object):
    @property
    def campaign_id(self):
        """ The identifier of the campaign that the target is associated.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._entity_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._entity_id = value

    @property
    def campaign_name(self):
        """ The name of the campaign that the target is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._entity_name = value


class _BulkSubTargetAdGroupMixin(object):
    @property
    def ad_group_id(self):
        """ The identifier of the ad group that the target is associated.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._entity_id

    @ad_group_id.setter
    def ad_group_id(self, value):
        self._entity_id = value

    @property
    def ad_group_name(self):
        """ The name of the ad group that the target is associated.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._entity_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._entity_name = value

    @property
    def campaign_name(self):
        """ The name of the ad group that target is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """
        return self._parent_entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._parent_entity_name = value


class _BulkTarget(_MultiRecordBulkEntity):
    """ This abstract base class provides properties that are shared by all bulk target classes.

    For example :class:`.BulkAdGroupDayTimeTarget`.
    """

    def __init__(self,
                 target=None,
                 status=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None,
                 bulk_target_bid=None,
                 identifier=None, ):
        super(_BulkTarget, self).__init__()
        self._target = target
        self._status = status
        self._entity_id = entity_id
        self._entity_name = entity_name
        self._parent_entity_name = parent_entity_name

        self._bids = []
        self._deleted_rows = []
        self._original_identifier = None
        if isinstance(self, BulkCampaignTarget):
            self._age_target = BulkCampaignAgeTarget()
            self._day_time_target = BulkCampaignDayTimeTarget()
            self._device_os_target = BulkCampaignDeviceOsTarget()
            self._gender_target = BulkCampaignGenderTarget()
            self._radius_target = BulkCampaignRadiusTarget()
            self._location_target = BulkCampaignLocationTarget()
            self._negative_location_target = BulkCampaignNegativeLocationTarget()
        elif isinstance(self, BulkAdGroupTarget):
            self._age_target = BulkAdGroupAgeTarget()
            self._day_time_target = BulkAdGroupDayTimeTarget()
            self._device_os_target = BulkAdGroupDeviceOsTarget()
            self._gender_target = BulkAdGroupGenderTarget()
            self._radius_target = BulkAdGroupRadiusTarget()
            self._location_target = BulkAdGroupLocationTarget()
            self._negative_location_target = BulkAdGroupNegativeLocationTarget()
        else:
            raise ValueError('Can only initialize with BulkAdGroupTarget or BulkCampaignTarget.')
        self._sub_targets = [
            self._age_target,
            self._day_time_target,
            self._device_os_target,
            self._gender_target,
            self._radius_target,
            self._location_target,
            self._negative_location_target,
        ]

        if bulk_target_bid is not None and identifier is not None:
            raise ValueError('cannot provide both bulk_target_bid and identifier')
        self._identifier = identifier
        if bulk_target_bid is not None:
            self._bids.append(bulk_target_bid)
            self._identifier = bulk_target_bid._identifier
        if self._identifier is not None:
            self._original_identifier = self._identifier
            self._target = _CAMPAIGN_OBJECT_FACTORY.create('Target2')
            self._target.Id = self._identifier.target_id
            self._entity_id = self._identifier.entity_id
            self._entity_name = self._identifier.entity_name
            self._parent_entity_name = self._identifier.parent_entity_name
            if self._identifier.is_delete_row:
                self._deleted_rows.append(self._identifier)

    def write_to_stream(self, row_writer, exclude_readonly_data):
        if self.status != 'Deleted':
            self._validate_property_not_null(self.target, 'target')
        if self.target is not None:
            self.age_target.age_target = self.target.Age
            self.day_time_target.day_time_target = self.target.DayTime
            self.device_os_target.device_os_target = self.target.DeviceOS
            self.gender_target.gender_target = self.target.Gender
            self.radius_target.location_target = self.target.Location
            self.location_target.location_target = self.target.Location
            self.negative_location_target.location_target = self.target.Location

        self.set_default_identifier(self.age_target)
        self.set_default_identifier(self.day_time_target)
        self.set_default_identifier(self.device_os_target)
        self.set_default_identifier(self.gender_target)
        self.set_default_identifier(self.radius_target)
        self.set_default_identifier(self.location_target)
        self.set_default_identifier(self.negative_location_target)

        self.age_target.is_being_written_as_part_of_parent_target = True
        self.day_time_target.is_being_written_as_part_of_parent_target = True
        self.device_os_target.is_being_written_as_part_of_parent_target = True
        self.gender_target.is_being_written_as_part_of_parent_target = True
        self.radius_target.is_being_written_as_part_of_parent_target = True
        self.location_target.is_being_written_as_part_of_parent_target = True
        self.negative_location_target.is_being_written_as_part_of_parent_target = True

        for sub_target in self.sub_targets:
            sub_target.write_to_stream(row_writer, exclude_readonly_data)

    def read_related_data_from_stream(self, stream_reader):
        has_more_rows = True
        while has_more_rows:
            bulk_target_bid_success, bulk_target_bid = stream_reader.try_read(
                _BulkTargetBid,
                lambda x: x._identifier == self._original_identifier
            )
            if bulk_target_bid_success:
                self._bids.append(bulk_target_bid)
            else:
                identifier_success, identifier = stream_reader.try_read(
                    _BulkTargetIdentifier,
                    lambda x: x == self._original_identifier and x.is_delete_row
                )
                if identifier_success:
                    self._deleted_rows.append(identifier)
                else:
                    has_more_rows = False
            if self.target.Id is None and bulk_target_bid is not None and bulk_target_bid.target_id is not None:
                self.target.Id = bulk_target_bid.target_id
        self.status = 'Active' if self._bids else 'Deleted'

        location = _CAMPAIGN_OBJECT_FACTORY.create('LocationTarget2')
        self.radius_target.location_target = location
        self.location_target.location_target = location
        self.negative_location_target.location_target = location

        self.populate_child_target_bids(self.age_target)
        self.populate_child_target_bids(self.day_time_target)
        self.populate_child_target_bids(self.device_os_target)
        self.populate_child_target_bids(self.gender_target)
        self.populate_child_target_bids(self.radius_target)
        self.populate_child_target_bids(self.location_target)
        self.populate_child_target_bids(self.negative_location_target)

        self.populate_child_target_identities(self.age_target)
        self.populate_child_target_identities(self.day_time_target)
        self.populate_child_target_identities(self.device_os_target)
        self.populate_child_target_identities(self.gender_target)
        self.populate_child_target_identities(self.radius_target)
        self.populate_child_target_identities(self.location_target)
        self.populate_child_target_identities(self.negative_location_target)

        self.target.Age = self.age_target.age_target
        self.target.DayTime = self.day_time_target.day_time_target
        self.target.DeviceOS = self.device_os_target.device_os_target
        self.target.Gender = self.gender_target.gender_target
        self.target.Location = location

    @property
    def all_children_are_present(self):
        return all(sub_target.all_children_are_present for sub_target in self.sub_targets)

    @property
    def child_entities(self):
        return self._sub_targets

    def set_default_identifier(self, bulk_sub_target):
        bulk_target_bid_type = type(bulk_sub_target._create_bid())
        if isinstance(self, BulkCampaignTarget):
            identifier = _BulkCampaignTargetIdentifier(target_bid_type=bulk_target_bid_type)
        elif isinstance(self, BulkAdGroupTarget):
            identifier = _BulkAdGroupTargetIdentifier(target_bid_type=bulk_target_bid_type)
        else:
            raise ValueError('Can only initialize with BulkAdGroupTarget or BulkCampaignTarget.')
        identifier.entity_id = self.entity_id
        if self.target is not None:
            identifier.target_id = self.target.Id
        identifier.entity_name = self.entity_name
        identifier.parent_entity_name = self.parent_entity_name
        if self.status == 'Deleted':
            bulk_sub_target.status = 'Deleted'
        bulk_sub_target.set_identifier(identifier)

    def populate_child_target_bids(self, bulk_sub_target):
        bulk_target_bid_type = type(bulk_sub_target._create_bid())
        bids = [bid for bid in self._bids if type(bid) == bulk_target_bid_type]
        if bids:
            bulk_sub_target.set_bids(bids)
        else:
            bulk_sub_target.status = 'Deleted'

    def populate_child_target_identities(self, bulk_sub_target):
        bulk_target_bid_type = type(bulk_sub_target._create_bid())
        identifiers = [identifier for identifier in self._deleted_rows if
                       identifier.target_bid_type == bulk_target_bid_type]
        if identifiers:
            for identifier in identifiers:
                bulk_sub_target.set_identifier(identifier)
        else:
            self.set_default_identifier(bulk_sub_target)

    @property
    def target(self):
        """ The associated target.

        :rtype: Target2
        """

        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def status(self):
        """ The status of the target.

        The value is Active if the target is available in the customer's shared library.
        The value is Deleted if the target is deleted from the customer's shared library, or should be deleted in a subsequent upload operation.
        Corresponds to the 'Status' field in the bulk file.

        :rtype: str
        """

        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def entity_id(self):
        return self._entity_id

    @entity_id.setter
    def entity_id(self, value):
        self._entity_id = value

    @property
    def entity_name(self):
        return self._entity_name

    @entity_name.setter
    def entity_name(self, value):
        self._entity_name = value

    @property
    def parent_entity_name(self):
        return self._parent_entity_name

    @parent_entity_name.setter
    def parent_entity_name(self, value):
        self._parent_entity_name = value

    @property
    def age_target(self):
        """ The :class:`.BulkAgeTarget` contains multiple :class:`.BulkAgeTargetBid`.

        :rtype: _BulkAgeTarget
        """

        return self._age_target

    @property
    def day_time_target(self):
        """ The :class:`.BulkDayTimeTarget` contains multiple :class:`.BulkDayTimeTargetBid`.

        :rtype: _BulkDayTimeTarget
        """

        return self._day_time_target

    @property
    def device_os_target(self):
        """ The :class:`.BulkDeviceOsTarget` contains multiple :class:`.BulkDeviceOsTargetBid`.

        :rtype: _BulkDeviceOsTarget
        """

        return self._device_os_target

    @property
    def gender_target(self):
        """ The :class:`.BulkGenderTarget` contains multiple :class:`.BulkGenderTargetBid`.

        :rtype: _BulkGenderTarget
        """

        return self._gender_target

    @property
    def radius_target(self):
        """ The :class:`.BulkRadiusTarget` contains multiple :class:`.BulkRadiusTargetBid`.

        :rtype: _BulkRadiusTarget
        """

        return self._radius_target

    @property
    def location_target(self):
        """ The :class:`.BulkLocationTarget` contains multiple :class:`.BulkLocationTargetBid`.

        :rtype: _BulkLocationTarget
        """

        return self._location_target

    @property
    def negative_location_target(self):
        """ The :class:`.BulkNegativeLocationTarget` contains multiple :class:`.BulkNegativeLocationTargetBid`.

        :rtype: _BulkNegativeLocationTarget
        """

        return self._negative_location_target

    @property
    def sub_targets(self):
        """ The list of sub targets.

        The target contains can include

        * :class:`.LocationTarget`
        * :class:`.AgeTarget`
        * :class:`.GenderTarget`
        * :class:`.DayTimeTarget`
        * :class:`.DeviceOsTarget`
        * :class:`.NegativeLocationTarget`
        * :class:`.RadiusTarget`

        :rtype: list[_BulkSubTarget]
        """

        return self._sub_targets


class BulkAdGroupTarget(_BulkTarget):
    """ Represents a target that is associated with an ad group.

    The target contains one or more sub targets,
    including age, gender, day and time, device OS, and location. Each target can be read or written in a bulk file.

    *Remarks:*

    When requesting downloaded entities of type *BulkAdGroupTarget*, the results will include
    Ad Group Age Target, Ad Group DayTime Target, Ad Group DeviceOS Target, Ad Group Gender Target, Ad Group Location Target,
    Ad Group Negative Location Target, and Ad Group Radius Target records.
    For more information, see Bulk File Schema at http://go.microsoft.com/fwlink/?LinkID=511639.

    For upload you must set the *Target2* property, which will effectively replace any existing bids for the corresponding target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """
    def __init__(self,
                 target=None,
                 status=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None,
                 bulk_target_bid=None,
                 identifier=None, ):
        super(BulkAdGroupTarget, self).__init__(
            target=target,
            status=status,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
            bulk_target_bid=bulk_target_bid,
            identifier=identifier,
        )

    @property
    def ad_group_id(self):
        """ The identifier of the ad group that the target is associated.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._entity_id

    @ad_group_id.setter
    def ad_group_id(self, value):
        self._entity_id = value

    @property
    def ad_group_name(self):
        """ The name of the ad group that the target is associated.

        Corresponds to the 'Ad Group' field in the bulk file.

        :rtype: str
        """

        return self._entity_name

    @ad_group_name.setter
    def ad_group_name(self, value):
        self._entity_name = value

    @property
    def campaign_name(self):
        """ The name of the ad group that target is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """
        return self._parent_entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._parent_entity_name = value


class BulkCampaignTarget(_BulkTarget):
    """ Represents a target that is associated with a campaign.

    The target contains one or more sub targets,
    including age, gender, day and time, device OS, and location. Each target can be read or written in a bulk file.

    *Remarks:*

    When requesting downloaded entities of type *BulkCampaignTarget*, the results will include
    Ad Group Age Target, Ad Group DayTime Target, Ad Group DeviceOS Target, Ad Group Gender Target, Ad Group Location Target,
    Ad Group Negative Location Target, and Ad Group Radius Target records.
    For more information, see Bulk File Schema at http://go.microsoft.com/fwlink/?LinkID=511639.

    For upload you must set the *Target2* property, which will effectively replace any existing bids for the corresponding target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """
    def __init__(self,
                 target=None,
                 status=None,
                 campaign_id=None,
                 campaign_name=None,
                 bulk_target_bid=None,
                 identifier=None, ):
        super(BulkCampaignTarget, self).__init__(
            target=target,
            status=status,
            entity_id=campaign_id,
            entity_name=campaign_name,
            bulk_target_bid=bulk_target_bid,
            identifier=identifier,
        )

    @property
    def campaign_id(self):
        """ The identifier of the campaign that the target is associated.

        Corresponds to the 'Parent Id' field in the bulk file.

        :rtype: int
        """

        return self._entity_id

    @campaign_id.setter
    def campaign_id(self, value):
        self._entity_id = value

    @property
    def campaign_name(self):
        """ The name of the campaign that the target is associated.

        Corresponds to the 'Campaign' field in the bulk file.

        :rtype: str
        """

        return self._entity_name

    @campaign_name.setter
    def campaign_name(self, value):
        self._entity_name = value


# age target


class _BulkAgeTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk age target bid classes. """

    def __init__(self,
                 age_target_bid=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._age_target_bid = age_target_bid
        super(_BulkAgeTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: c.age_target_bid.Age,
            csv_to_field=lambda c, v: setattr(c.age_target_bid, 'Age', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.age_target_bid.BidAdjustment),
            csv_to_field=lambda c, v: setattr(c.age_target_bid, 'BidAdjustment', int(v))
        ),
    ]

    def _prepare_process_mapping_from_row_values(self):
        self.age_target_bid = _CAMPAIGN_OBJECT_FACTORY.create('AgeTargetBid')

    @property
    def age_target_bid(self):
        """ Defines a list of age ranges to target with bid adjustments.

        :rtype: AgeTargetBid
        """

        return self._age_target_bid

    @age_target_bid.setter
    def age_target_bid(self, value):
        self._age_target_bid = value


class BulkAdGroupAgeTargetBid(_BulkAgeTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one age target bid within an age target that is associated with an ad group.

    This class exposes the :attr:`age_target_bid` property that can be read and written as fields of the Ad Group Age Target record in a bulk file.

    For more information, see Ad Group Age Target at http://go.microsoft.com/fwlink/?LinkID=511546.

    *Remarks:*

    One :class:`.BulkAdGroupAgeTarget` exposes a read only list of :class:`.BulkAdGroupAgeTargetBid`.
    Each :class:`.BulkAdGroupAgeTargetBid` instance corresponds to one Ad Group Age Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupAgeTarget`, then you are effectively replacing any existing bids for the corresponding age target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 age_target_bid=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkAgeTargetBid.__init__(
            self,
            age_target_bid=age_target_bid,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignAgeTargetBid(_BulkAgeTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one age target bid within an age target that is associated with a campaign.

    This class exposes the :attr:`.age_target_bid` property that can be read and written as fields of the Campaign Age Target record in a bulk file.
    For more information, see Campaign Age Target at http://go.microsoft.com/fwlink/?LinkID=511530.

    *Remarks:*

    One :class:`.BulkCampaignAgeTarget` exposes a read only list of :class:`.BulkCampaignAgeTargetBid`.
    Each :class:`.BulkCampaignAgeTargetBid` instance corresponds to one Campaign Age Target record in the bulk file.
    If you upload a :class:`.BulkCampaignAgeTarget`, then you are effectively replacing any existing bids for the corresponding age target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 age_target_bid=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkAgeTargetBid.__init__(
            self,
            age_target_bid=age_target_bid,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkAgeTarget(_BulkSubTarget):
    """ This base class provides properties that are shared by all bulk age target classes. """

    def __init__(self,
                 age_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        self._age_target = age_target
        super(_BulkAgeTarget, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def _create_bid(self):
        raise NotImplementedError()

    def _validate_properties(self):
        self._validate_property_not_null(self.age_target, 'age_target')

    def _validate_bids(self):
        if self.age_target is not None:
            self._validate_list_not_null_or_empty(self.age_target.Bids, self.age_target.Bids.AgeTargetBid,
                                                  'age_target.Bids')

    def _convert_target_to_bulk_entities(self):
        if self.age_target is None or self.age_target.Bids is None:
            return
        for bid in self.age_target.Bids.AgeTargetBid:
            bulk_bid = self._create_and_populate_bid()
            bulk_bid.age_target_bid = bid
            yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.age_target = _CAMPAIGN_OBJECT_FACTORY.create('AgeTarget')
        for bid in self.child_entities:
            self.age_target.Bids.AgeTargetBid.append(bid.age_target_bid)

    @property
    def age_target(self):
        """ Defines a list of age ranges to target with bid adjustments.

        :rtype: AgeTarget
        """

        return self._age_target

    @age_target.setter
    def age_target(self, value):
        self._age_target = value


class BulkAdGroupAgeTarget(_BulkAgeTarget, _BulkSubTargetAdGroupMixin):
    """ Represents an age target that is associated with an ad group.

    This class exposes the :attr:`AgeTarget` property that can be read and written as fields of the Ad Group Age Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkAdGroupAgeTarget` exposes a read only list of :class:`.BulkAdGroupAgeTargetBid`.
    Each :class:`.BulkAdGroupAgeTargetBid` instance corresponds to one Ad Group Age Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupAgeTarget`, then you are effectively replacing any existing bids for the corresponding age target.

    For more information, see Ad Group Age Target at http://go.microsoft.com/fwlink/?LinkID=511546.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 age_target=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkAgeTarget.__init__(
            self,
            age_target=age_target,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupAgeTargetBid()


class BulkCampaignAgeTarget(_BulkAgeTarget, _BulkSubTargetCampaignMixin):
    """ Represents an age target that is associated with a campaign.

    The age target contains one or more age target bids.
    This class exposes the :attr:`AgeTarget` property that can be read and written as fields of the Campaign Age Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkCampaignAgeTarget` exposes a read only list of :class:`.BulkCampaignAgeTargetBid`.
    Each :class:`.BulkCampaignAgeTargetBid` instance corresponds to one Campaign Age Target record in the bulk file.
    If you upload a :class:`BulkCampaignAgeTarget`, then you are effectively replacing any existing bids for the corresponding age target.

    For more information, see Campaign Age Target at http://go.microsoft.com/fwlink/?LinkID=511530.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 age_target=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkAgeTarget.__init__(
            self,
            age_target=age_target,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignAgeTargetBid()


class _BulkDayTimeTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk day and time target bid classes. """

    def __init__(self,
                 day_time_target_bid=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._day_time_target_bid = day_time_target_bid
        super(_BulkDayTimeTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.day_time_target_bid.Day),
            csv_to_field=lambda c, v: setattr(c.day_time_target_bid, 'Day', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.FromHour,
            field_to_csv=lambda c: bulk_str(c.day_time_target_bid.FromHour),
            csv_to_field=lambda c, v: setattr(c.day_time_target_bid, 'FromHour', int(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.ToHour,
            field_to_csv=lambda c: bulk_str(c.day_time_target_bid.ToHour),
            csv_to_field=lambda c, v: setattr(c.day_time_target_bid, 'ToHour', int(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.FromMinute,
            field_to_csv=lambda c: minute_bulk_str(c.day_time_target_bid.FromMinute),
            csv_to_field=lambda c, v: setattr(c.day_time_target_bid, 'FromMinute', parse_minute(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.ToMinute,
            field_to_csv=lambda c: minute_bulk_str(c.day_time_target_bid.ToMinute),
            csv_to_field=lambda c, v: setattr(c.day_time_target_bid, 'ToMinute', parse_minute(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.day_time_target_bid.BidAdjustment),
            csv_to_field=lambda c, v: setattr(c.day_time_target_bid, 'BidAdjustment', int(v))
        )
    ]

    @property
    def day_time_target_bid(self):
        """ Defines a specific day of the week and time range to target.

        :rtype: DayTimeTargetBid
        """

        return self._day_time_target_bid

    @day_time_target_bid.setter
    def day_time_target_bid(self, value):
        self._day_time_target_bid = value

    def _prepare_process_mapping_from_row_values(self):
        self._day_time_target_bid = _CAMPAIGN_OBJECT_FACTORY.create('DayTimeTargetBid')


class BulkAdGroupDayTimeTargetBid(_BulkDayTimeTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one day and time target bid within a day and time target that is associated with an ad group.

    This class exposes the :attr:`day_time_target_bid` property that can be read and written as fields of the Ad Group DayTime Target record in a bulk file.

    For more information, see Ad Group DayTime Target at http://go.microsoft.com/fwlink/?LinkID=512015.

    *Remarks*

    One :class:`.BulkAdGroupDayTimeTarget` exposes a read only list of :class:`.BulkAdGroupDayTimeTargetBid`.
    Each :class:`.BulkAdGroupDayTimeTargetBid` instance corresponds to one Ad Group DayTime Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupDayTimeTarget`, then you are effectively replacing any existing bids for the corresponding day and time target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 day_time_target_bid=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkDayTimeTargetBid.__init__(
            self,
            day_time_target_bid=day_time_target_bid,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignDayTimeTargetBid(_BulkDayTimeTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one day and time target bid within a day and time target that is associated with an campaign.

    This class exposes the :attr:`day_time_target_bid` property that can be read and written as fields of the Campaign DayTime Target record in a bulk file.

    For more information, see Campaign DayTime Target at http://go.microsoft.com/fwlink/?LinkID=512016.

    *Remarks*

    One :class:`.BulkCampaignDayTimeTarget` exposes a read only list of :class:`.BulkCampaignDayTimeTargetBid`.
    Each :class:`.BulkCampaignDayTimeTargetBid` instance corresponds to one Campaign DayTime Target record in the bulk file.
    If you upload a :class:`.BulkCampaignDayTimeTarget`, then you are effectively replacing any existing bids for the corresponding day and time target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 day_time_target_bid=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkDayTimeTargetBid.__init__(
            self,
            day_time_target_bid=day_time_target_bid,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkDayTimeTarget(_BulkSubTarget):
    """ This base class provides properties that are shared by all bulk day and time target classes. """

    def __init__(self,
                 day_time_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        self._day_time_target = day_time_target
        super(_BulkDayTimeTarget, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def _create_bid(self):
        raise NotImplementedError()

    def _validate_properties(self):
        self._validate_property_not_null(self.day_time_target, 'day_time_target')

    def _validate_bids(self):
        if self.day_time_target is not None:
            self._validate_list_not_null_or_empty(self.day_time_target.Bids, self.day_time_target.Bids.DayTimeTargetBid,
                                                  'day_time_target.Bids')

    def _convert_target_to_bulk_entities(self):
        if self.day_time_target is None or self.day_time_target.Bids is None:
            return
        for bid in self.day_time_target.Bids.DayTimeTargetBid:
            bulk_bid = self._create_and_populate_bid()
            bulk_bid.day_time_target_bid = bid
            yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.day_time_target = _CAMPAIGN_OBJECT_FACTORY.create('DayTimeTarget')
        for bid in self.child_entities:
            self.day_time_target.Bids.DayTimeTargetBid.append(bid.day_time_target_bid)

    @property
    def day_time_target(self):
        """ Defines a list of days of the week and time ranges to target with bid adjustments.

        :rtype: DayTimeTarget
        """

        return self._day_time_target

    @day_time_target.setter
    def day_time_target(self, value):
        self._day_time_target = value


class BulkAdGroupDayTimeTarget(_BulkDayTimeTarget, _BulkSubTargetAdGroupMixin):
    """ Represents a day and time target that is associated with an ad group.

    This class exposes the :attr:`day_time_target` property that can be read and written as fields of the Ad Group DayTime Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkAdGroupDayTimeTarget` exposes a read only list of :class:`.BulkAdGroupDayTimeTargetBid`.
    Each :class:`.BulkAdGroupDayTimeTargetBid` instance corresponds to one Ad Group DayTime Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupDayTimeTarget`, then you are effectively replacing any existing bids for the corresponding day and time target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 day_time_target=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkDayTimeTarget.__init__(
            self,
            day_time_target=day_time_target,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupDayTimeTargetBid()


class BulkCampaignDayTimeTarget(_BulkDayTimeTarget, _BulkSubTargetCampaignMixin):
    """ Represents a day and time target that is associated with a campaign.

    This class exposes the :attr:`day_time_target` property that can be read and written as fields of the Campaign DayTime Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkCampaignDayTimeTarget` exposes a read only list of :class:`.BulkCampaignDayTimeTargetBid`.
    Each :class:`.BulkCampaignDayTimeTargetBid` instance corresponds to one Campaign DayTime Target record in the bulk file.
    If you upload a :class:`.BulkCampaignDayTimeTarget`, then you are effectively replacing any existing bids for the corresponding day and time target.

    For more information, see Campaign DayTime Target at http://go.microsoft.com/fwlink/?LinkID=512016.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 day_time_target=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkDayTimeTarget.__init__(
            self,
            day_time_target=day_time_target,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignDayTimeTargetBid()


class _BulkDeviceOsTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk device OS target bid classes. """

    def __init__(self,
                 device_os_target_bid=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._device_os_target_bid = device_os_target_bid
        super(_BulkDeviceOsTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.device_os_target_bid.DeviceName),
            csv_to_field=lambda c, v: setattr(c.device_os_target_bid, 'DeviceName', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.OsNames,
            field_to_csv=lambda c: ';'.join(
                c.device_os_target_bid.OSNames.string) if c.device_os_target_bid.OSNames.string else None,
            csv_to_field=lambda c, v: setattr(
                c.device_os_target_bid.OSNames,
                'string',
                list(filter(None, v.split(';'))) if v else [],
            ),
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.device_os_target_bid.BidAdjustment),
            csv_to_field=lambda c, v: setattr(c.device_os_target_bid, 'BidAdjustment', int(v))
        ),
    ]

    @property
    def device_os_target_bid(self):
        """ Defines a specific device to target.

        :rtype: DeviceOSTargetBid
        """

        return self._device_os_target_bid

    @device_os_target_bid.setter
    def device_os_target_bid(self, value):
        self._device_os_target_bid = value

    def _prepare_process_mapping_from_row_values(self):
        self._device_os_target_bid = _CAMPAIGN_OBJECT_FACTORY.create('DeviceOSTargetBid')


class BulkAdGroupDeviceOsTargetBid(_BulkDeviceOsTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one device OS target bid within a device OS target that is associated with an ad group.

    This class exposes the :attr:`device_os_target_bid` property that can be read and written as fields of the Ad Group DeviceOS Target record in a bulk file.

    For more information, see Ad Group DeviceOS Target at http://go.microsoft.com/fwlink/?LinkID=511529.

    *Remarks:*

    One :class:`.BulkAdGroupDeviceOsTarget` exposes a read only list of :class:`.BulkAdGroupDeviceOsTargetBid`.
    Each :class:`BulkAdGroupDeviceOsTargetBid` instance corresponds to one Ad Group DeviceOS Target record in the bulk file.
    If you upload a :class:`BulkAdGroupDeviceOsTarget`, then you are effectively replacing any existing bids for the corresponding device OS target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 device_os_target_bid=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkDeviceOsTargetBid.__init__(
            self,
            device_os_target_bid=device_os_target_bid,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignDeviceOsTargetBid(_BulkDeviceOsTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one device OS target bid within a device OS target that is associated with a campaign.

    This class exposes the :attr:`device_os_target_bid` property that can be read and written as fields of the Campaign DeviceOS Target record in a bulk file.

    For more information, see Campaign DeviceOS Target at http://go.microsoft.com/fwlink/?LinkID=511529.

    *Remarks:*

    One :class:`.BulkCampaignDeviceOsTarget` exposes a read only list of :class:`.BulkCampaignDeviceOsTargetBid`.
    Each :class:`.BulkCampaignDeviceOsTargetBid` instance corresponds to one Campaign DeviceOS Target record in the bulk file.
    If you upload a :class:`.BulkCampaignDeviceOsTarget`, then you are effectively replacing any existing bids for the corresponding device OS target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 device_os_target_bid=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkDeviceOsTargetBid.__init__(
            self,
            device_os_target_bid=device_os_target_bid,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkDeviceOsTarget(_BulkSubTarget):
    """ This base class provides properties that are shared by all bulk device OS target classes. """

    def __init__(self,
                 device_os_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        self._device_os_target = device_os_target
        super(_BulkDeviceOsTarget, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def _create_bid(self):
        raise NotImplementedError()

    def _validate_properties(self):
        self._validate_property_not_null(self.device_os_target, 'device_os_target')

    def _validate_bids(self):
        if self.device_os_target is not None:
            self._validate_list_not_null_or_empty(
                self.device_os_target.Bids,
                self.device_os_target.Bids.DeviceOSTargetBid,
                'device_os_target.Bids'
            )

    def _convert_target_to_bulk_entities(self):
        if self.device_os_target is None or self.device_os_target.Bids is None:
            return
        for bid in self.device_os_target.Bids.DeviceOSTargetBid:
            bulk_bid = self._create_and_populate_bid()
            bulk_bid.device_os_target_bid = bid
            yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.device_os_target = _CAMPAIGN_OBJECT_FACTORY.create('DeviceOSTarget')
        for bid in self.child_entities:
            self.device_os_target.Bids.DeviceOSTargetBid.append(bid.device_os_target_bid)

    @property
    def device_os_target(self):
        """ Defines a list of devices to target with bid adjustments.

        :rtype: DeviceOSTarget
        """

        return self._device_os_target

    @device_os_target.setter
    def device_os_target(self, value):
        self._device_os_target = value


class BulkAdGroupDeviceOsTarget(_BulkDeviceOsTarget, _BulkSubTargetAdGroupMixin):
    """ Represents a device OS target that is associated with an ad group.

    This class exposes the :attr:`device_os_target` property that can be read and written as fields of the Ad Group DeviceOS Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkAdGroupDeviceOsTarget` exposes a read only list of :class`.BulkAdGroupDeviceOsTargetBid`.
    Each :class:`.BulkAdGroupDeviceOsTargetBid` instance corresponds to one Ad Group DeviceOS Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupDeviceOsTarget`, then you are effectively replacing any existing bids for the corresponding device OS target.

    For more information, see Ad Group DeviceOS Target at http://go.microsoft.com/fwlink/?LinkID=511529.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 device_os_target=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkDeviceOsTarget.__init__(
            self,
            device_os_target=device_os_target,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupDeviceOsTargetBid()


class BulkCampaignDeviceOsTarget(_BulkDeviceOsTarget, _BulkSubTargetCampaignMixin):
    """ Represents a device OS target that is associated with a campaign.

    This class exposes the :attr:`device_os_target` property that can be read and written as fields of the Campaign DeviceOS Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkCampaignDeviceOsTarget` exposes a read only list of :class:`.BulkCampaignDeviceOsTargetBid`.
    Each :class:`.`BulkCampaignDeviceOsTargetBid` instance corresponds to one Campaign DeviceOS Target record in the bulk file.
    If you upload a :class:`.BulkCampaignDeviceOsTarget`, then you are effectively replacing any existing bids for the corresponding device OS target

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`.
    """

    def __init__(self,
                 device_os_target=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkDeviceOsTarget.__init__(
            self,
            device_os_target=device_os_target,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignDeviceOsTargetBid()


class _BulkGenderTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk gender target bid classes. """

    def __init__(self,
                 gender_target_bid=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._gender_target_bid = gender_target_bid
        super(_BulkGenderTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.gender_target_bid.Gender),
            csv_to_field=lambda c, v: setattr(c.gender_target_bid, 'Gender', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.gender_target_bid.BidAdjustment),
            csv_to_field=lambda c, v: setattr(c.gender_target_bid, 'BidAdjustment', int(v))
        )
    ]

    @property
    def gender_target_bid(self):
        """ Defines a specific gender target.

        :rtype: GenderTargetBid
        """

        return self._gender_target_bid

    @gender_target_bid.setter
    def gender_target_bid(self, value):
        self._gender_target_bid = value

    def _prepare_process_mapping_from_row_values(self):
        self._gender_target_bid = _CAMPAIGN_OBJECT_FACTORY.create('GenderTargetBid')


class BulkAdGroupGenderTargetBid(_BulkGenderTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one gender target bid within a gender target that is associated with an ad group.

    This class exposes the :attr:`gender_target_bid` property that can be read and written as fields of the Ad Group Gender Target record in a bulk file.

    For more information, see Ad Group Gender Target at http://go.microsoft.com/fwlink/?LinkID=511544.

    *Remarks:*

    One :class:`.BulkAdGroupGenderTarget` exposes a read only list of :class:`.BulkAdGroupGenderTargetBid`.
    Each :class`.BulkAdGroupGenderTargetBid` instance corresponds to one Ad Group Gender Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupGenderTarget`, then you are effectively replacing any existing bids for the corresponding gender target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 gender_target_bid=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkGenderTargetBid.__init__(
            self,
            gender_target_bid=gender_target_bid,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignGenderTargetBid(_BulkGenderTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one gender target bid within a gender target that is associated with a campaign.

    This class exposes the :attr:`gender_target_bid` property that can be read and written as fields of the Campaign Gender Target record in a bulk file.

    For more information, see Campaign Gender Target at http://go.microsoft.com/fwlink/?LinkID=511528.

    *Remarks:*
    One :class:`.BulkCampaignGenderTarget` exposes a read only list of :class:`.BulkCampaignGenderTargetBid`.
    Each :class:`.BulkCampaignGenderTargetBid` instance corresponds to one Campaign Gender Target record in the bulk file.
    If you upload a :class:`.BulkCampaignGenderTarget`, then you are effectively replacing any existing bids for the corresponding gender target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 gender_target_bid=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkGenderTargetBid.__init__(
            self,
            gender_target_bid=gender_target_bid,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkGenderTarget(_BulkSubTarget):
    """ This base class provides properties that are shared by all bulk gender target classes. """

    def __init__(self,
                 gender_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None, ):
        self._gender_target = gender_target
        super(_BulkGenderTarget, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def _create_bid(self):
        raise NotImplementedError()

    def _validate_properties(self):
        self._validate_property_not_null(self.gender_target, 'gender_target')

    def _validate_bids(self):
        if self.gender_target is not None:
            self._validate_list_not_null_or_empty(
                self.gender_target.Bids,
                self.gender_target.Bids.GenderTargetBid,
                'gender_target.Bids'
            )

    def _convert_target_to_bulk_entities(self):
        if self.gender_target is None or self.gender_target.Bids is None:
            return
        for bid in self.gender_target.Bids.GenderTargetBid:
            bulk_bid = self._create_and_populate_bid()
            bulk_bid.gender_target_bid = bid
            yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.gender_target = _CAMPAIGN_OBJECT_FACTORY.create('GenderTarget')
        for bid in self.child_entities:
            self.gender_target.Bids.GenderTargetBid.append(bid.gender_target_bid)

    @property
    def gender_target(self):
        """ Defines a list of genders to target with bid adjustments.

        :rtype: GenderTarget
        """

        return self._gender_target

    @gender_target.setter
    def gender_target(self, value):
        self._gender_target = value


class BulkAdGroupGenderTarget(_BulkGenderTarget, _BulkSubTargetAdGroupMixin):
    """ Represents a gender target that is associated with an ad group.

    This class exposes the :attr:`gender_target` property that can be read and written as fields of the Ad Group Gender Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkAdGroupGenderTarget` exposes a read only list of :class:`.BulkAdGroupGenderTargetBid`.
    Each :class:`.BulkAdGroupGenderTargetBid` instance corresponds to one Ad Group Gender Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupGenderTarget`, then you are effectively replacing any existing bids for the corresponding gender target.

    For more information, see Ad Group Gender Target at http://go.microsoft.com/fwlink/?LinkID=511544.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 gender_target=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkGenderTarget.__init__(
            self,
            gender_target=gender_target,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupGenderTargetBid()


class BulkCampaignGenderTarget(_BulkGenderTarget, _BulkSubTargetCampaignMixin):
    """ Represents a gender target that is associated with an campaign.

    This class exposes the :attr:`gender_target` property that can be read and written as fields of the Campaign Gender Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkCampaignGenderTarget` exposes a read only list of :class:`.BulkCampaignGenderTargetBid`.
    Each :class:`.BulkCampaignGenderTargetBid` instance corresponds to one Campaign Gender Target record in the bulk file.
    If you upload a :class:`.BulkCampaignGenderTarget`, then you are effectively replacing any existing bids for the corresponding gender target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 gender_target=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkGenderTarget.__init__(
            self,
            gender_target=gender_target,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignGenderTargetBid()


class _BulkRadiusTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk radius target bid classes. """

    def __init__(self,
                 radius_target_bid=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._radius_target_bid = radius_target_bid
        self._intent_option = None
        super(_BulkRadiusTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.RadiusTargetId,
            field_to_csv=lambda c: bulk_str(c.radius_target_bid.Id),
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'Id', int(v) if v else None),
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.radius_target_bid.Name,
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'Name', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.Radius,
            field_to_csv=lambda c: bulk_str(c.radius_target_bid.Radius),
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'Radius', float(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.Unit,
            field_to_csv=lambda c: c.radius_target_bid.RadiusUnit,
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'RadiusUnit', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.Latitude,
            field_to_csv=lambda c: bulk_str(c.radius_target_bid.LatitudeDegrees),
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'LatitudeDegrees', float(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.Longitude,
            field_to_csv=lambda c: bulk_str(c.radius_target_bid.LongitudeDegrees),
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'LongitudeDegrees', float(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.radius_target_bid.BidAdjustment),
            csv_to_field=lambda c, v: setattr(c.radius_target_bid, 'BidAdjustment', int(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.PhysicalIntent,
            field_to_csv=lambda c: bulk_str(c.intent_option),
            csv_to_field=lambda c, v: setattr(c, '_intent_option', v if v else None),
        ),
    ]

    @property
    def radius_target_bid(self):
        """ Defines a specific geographical radius to target.

        :rtype: RadiusTargetBid2
        """

        return self._radius_target_bid

    @radius_target_bid.setter
    def radius_target_bid(self, value):
        self._radius_target_bid = value

    @property
    def intent_option(self):
        """  Defines the possible intent options for location targeting.

        :rtype: str
        """

        return self._intent_option

    def _prepare_process_mapping_from_row_values(self):
        self._radius_target_bid = _CAMPAIGN_OBJECT_FACTORY.create('RadiusTargetBid2')


class BulkAdGroupRadiusTargetBid(_BulkRadiusTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one radius target bid within a radius target that is associated with an ad group.

    This class exposes the :attr:`radius_target_bid` property that can be read and written as fields of the Ad Group Radius Target record in a bulk file.

    For more information, see Ad Group Radius Target at http://go.microsoft.com/fwlink/?LinkID=511543.

    *Remarks:*

    One :class:`.BulkAdGroupRadiusTarget` exposes a read only list of :class:`.BulkAdGroupRadiusTargetBid`.
    Each :class:`.BulkAdGroupRadiusTargetBid` instance corresponds to one Ad Group Radius Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupRadiusTarget`, then you are effectively replacing any existing bids for the corresponding radius target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 radius_target_bid=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkRadiusTargetBid.__init__(
            self,
            radius_target_bid=radius_target_bid,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignRadiusTargetBid(_BulkRadiusTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one radius target bid within a radius target that is associated with a campaign.

    This class exposes the :attr:`radius_target_bid` property that can be read and written as fields of the Campaign Radius Target record in a bulk file.

    For more information, see Campaign Radius Target at http://go.microsoft.com/fwlink/?LinkID=511527.

    *Remarks:*

    One :class:`.BulkCampaignRadiusTarget` exposes a read only list of :class:`.BulkCampaignRadiusTargetBid`.
    Each :class:`.BulkCampaignRadiusTargetBid` instance corresponds to one Campaign Radius Target record in the bulk file.
    If you upload a :class:`.BulkCampaignRadiusTarget`, then you are effectively replacing any existing bids for the corresponding radius target.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 radius_target_bid=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkRadiusTargetBid.__init__(
            self,
            radius_target_bid=radius_target_bid,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkTargetWithLocation(_BulkSubTarget):
    """ This base class provides properties that are shared by all bulk entities mapped to the API LocationTarget2 object. """

    def __init__(self,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        super(_BulkTargetWithLocation, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )
        self._location_target = None

    @property
    def location_target(self):
        return self._location_target

    @location_target.setter
    def location_target(self, value):
        self._location_target = value

    def ensure_location_target(self):
        if self.location_target is None:
            self.location_target = _CAMPAIGN_OBJECT_FACTORY.create('LocationTarget2')


class _BulkRadiusTarget(_BulkTargetWithLocation):
    """ This base class provides properties that are shared by all bulk radius target classes. """

    def __init__(self,
                 radius_target=None,
                 intent_option=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        super(_BulkRadiusTarget, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )
        if radius_target is not None:
            self.radius_target = radius_target
        if intent_option is not None:
            self.intent_option = intent_option

    def _validate_properties(self):
        self._validate_property_not_null(self.radius_target, 'radius_target')

    def _validate_bids(self):
        if self.radius_target is not None:
            self._validate_list_not_null_or_empty(
                self.radius_target.Bids,
                self.radius_target.Bids.RadiusTargetBid2,
                'radius_target.Bids'
            )

    def _convert_target_to_bulk_entities(self):
        if self.radius_target is None or self.radius_target.Bids is None:
            return
        for bid in self.radius_target.Bids.RadiusTargetBid2:
            bulk_bid = self._create_and_populate_bid()
            bulk_bid.radius_target_bid = bid
            bulk_bid._intent_option = self.location_target.IntentOption
            yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.ensure_location_target()
        for bid in self.child_entities:
            self.radius_target.Bids.RadiusTargetBid2.append(bid.radius_target_bid)
        if self.child_entities:
            bid = self.child_entities[0]
            if bid.intent_option is not None:
                self.location_target.IntentOption = bid.intent_option

    @property
    def radius_target(self):
        """ Defines a list of geographical radius targets with bid adjustments.

        :rtype: RadiusTarget2
        """

        if self.location_target is None:
            return None
        return self.location_target.RadiusTarget

    @radius_target.setter
    def radius_target(self, value):
        self.ensure_location_target()
        self.location_target.RadiusTarget = value

    @property
    def intent_option(self):
        """ Defines the possible intent options for location targeting.

        :rtype: str
        """

        if self.location_target is None:
            return None
        return self.location_target.IntentOption

    @intent_option.setter
    def intent_option(self, value):
        self.ensure_location_target()
        self.location_target.IntentOption = value


class BulkCampaignRadiusTarget(_BulkRadiusTarget, _BulkSubTargetCampaignMixin):
    """ Represents a radius target that is associated with a campaign.

    This class exposes the :attr:`radius_target` property that can be read and written as fields of the Campaign Radius Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkCampaignRadiusTarget` exposes a read only list of :class:`.BulkCampaignRadiusTargetBid`.
    Each :class:`.BulkCampaignRadiusTargetBid` instance corresponds to one Campaign Radius Target record in the bulk file.
    If you upload a :class`.BulkCampaignRadiusTarget`, then you are effectively replacing any existing bids for the corresponding radius target.

    For more information, see Campaign Radius Target at http://go.microsoft.com/fwlink/?LinkID=511527.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 radius_target=None,
                 intent_option=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkRadiusTarget.__init__(
            self,
            radius_target=radius_target,
            intent_option=intent_option,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignRadiusTargetBid()


class BulkAdGroupRadiusTarget(_BulkRadiusTarget, _BulkSubTargetAdGroupMixin):
    """ Represents a radius target that is associated with an ad group.

    This class exposes the :attr:`radius_target` property that can be read and written as fields of the Ad Group Radius Target record in a bulk file.

    *Remarks:*

    One :class:`.BulkAdGroupRadiusTarget` exposes a read only list of :class:`.BulkAdGroupRadiusTargetBid`.
    Each :class:`.BulkAdGroupRadiusTargetBid` instance corresponds to one Ad Group Radius Target record in the bulk file.
    If you upload a :class:`.BulkAdGroupRadiusTarget`, then you are effectively replacing any existing bids for the corresponding radius target.

    For more information, see Ad Group Radius Target at http://go.microsoft.com/fwlink/?LinkID=511543.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 radius_target=None,
                 intent_option=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkRadiusTarget.__init__(
            self,
            radius_target=radius_target,
            intent_option=intent_option,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupRadiusTargetBid()


class _BulkLocationTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk location target bid classes. """

    def __init__(self,
                 location=None,
                 location_type=None,
                 bid_adjustment=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._location = location
        self._location_type = location_type
        self._bid_adjustment = bid_adjustment
        self._intent_option = None
        super(_BulkLocationTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.location),
            csv_to_field=lambda c, v: setattr(c, '_location', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.SubType,
            field_to_csv=lambda c: location_target_type_bulk_str(c.location_type),
            csv_to_field=lambda c, v: setattr(c, '_location_type', parse_location_target_type(v)),
        ),
        _SimpleBulkMapping(
            header=_StringTable.PhysicalIntent,
            field_to_csv=lambda c: bulk_str(c.intent_option),
            csv_to_field=lambda c, v: setattr(c, '_intent_option', v if v else None),
        ),
        _SimpleBulkMapping(
            header=_StringTable.BidAdjustment,
            field_to_csv=lambda c: bulk_str(c.bid_adjustment),
            csv_to_field=lambda c, v: setattr(c, '_bid_adjustment', int(v))
        )
    ]

    def _prepare_process_mapping_from_row_values(self):
        pass

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def location_type(self):
        return self._location_type

    @location_type.setter
    def location_type(self, value):
        self._location_type = value

    @property
    def intent_option(self):
        """ Defines the possible intent options for location targeting.

        :rtype: str
        """

        return self._intent_option

    @property
    def bid_adjustment(self):
        """ The percentage adjustment to the base bid.

        :rtype: int
        """

        return self._bid_adjustment

    @bid_adjustment.setter
    def bid_adjustment(self, value):
        self._bid_adjustment = value


class BulkAdGroupLocationTargetBid(_BulkLocationTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one sub location target bid within a location target that is associated with an ad group.

    This class exposes properties that can be read and written as fields of the Ad Group Location Target record in a bulk file.

    For more information, see Ad Group Location Target at http://go.microsoft.com/fwlink/?LinkID=511541.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 location=None,
                 location_type=None,
                 bid_adjustment=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None):
        _BulkLocationTargetBid.__init__(
            self,
            location=location,
            location_type=location_type,
            bid_adjustment=bid_adjustment,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignLocationTargetBid(_BulkLocationTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one sub location target bid within a location target that is associated with a campaign.

    This class exposes properties that can be read and written as fields of the Campaign Location Target record in a bulk file.

    For more information, see Campaign Location Target at http://go.microsoft.com/fwlink/?LinkID=511525.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 location=None,
                 location_type=None,
                 bid_adjustment=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None):
        _BulkLocationTargetBid.__init__(
            self,
            location=location,
            location_type=location_type,
            bid_adjustment=bid_adjustment,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkLocationTargetWithStringLocation(_BulkTargetWithLocation):
    """ This base class provides properties that are shared by all bulk location target classes. """

    LOCATION_TYPES = ['City', 'MetroArea', 'State', 'Country', 'PostalCode']

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        super(_BulkLocationTargetWithStringLocation, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )
        if city_target is not None:
            self.city_target = city_target
        if metro_area_target is not None:
            self.metro_area_target = metro_area_target
        if state_target is not None:
            self.state_target = state_target
        if country_target is not None:
            self.country_target = country_target
        if postal_code_target is not None:
            self.postal_code_target = postal_code_target

    def _validate_properties(self):
        self._validate_property_not_null(self.location_target, 'location_target')

    def _validate_bids(self):
        if self.location_target is not None:
            if not (
                any(self.city_target.Bids.CityTargetBid) or
                any(self.metro_area_target.Bids.MetroAreaTargetBid) or
                any(self.state_target.Bids.StateTargetBid) or
                any(self.country_target.Bids.CountryTargetBid) or
                any(self.postal_code_target.Bids.PostalCodeTargetBid)
            ):
                raise ValueError('Sub target bid in Location Target cannot all be empty')

    @property
    def city_target(self):
        """ Defines a list of cities to target with bid adjustments.

        :rtype: CityTarget
        """

        if self.location_target is None:
            return None
        return self.location_target.CityTarget

    @city_target.setter
    def city_target(self, value):
        self.ensure_location_target()
        self.location_target.CityTarget = value

    @property
    def metro_area_target(self):
        """ Defines a list of metro areas to target with bid adjustments.

        :rtype: MetroAreaTarget
        """

        if self.location_target is None:
            return None
        return self.location_target.MetroAreaTarget

    @metro_area_target.setter
    def metro_area_target(self, value):
        self.ensure_location_target()
        self.location_target.MetroAreaTarget = value

    @property
    def state_target(self):
        """ Defines a list of states to target with bid adjustments.

        :rtype: StateTarget
        """

        if self.location_target is None:
            return None
        return self.location_target.StateTarget

    @state_target.setter
    def state_target(self, value):
        self.ensure_location_target()
        self.location_target.StateTarget = value

    @property
    def country_target(self):
        """ Defines a list of countries to target with bid adjustments.

        :rtype: CountryTarget
        """

        if self.location_target is None:
            return None
        return self.location_target.CountryTarget

    @country_target.setter
    def country_target(self, value):
        self.ensure_location_target()
        self.location_target.CountryTarget = value

    @property
    def postal_code_target(self):
        """ Defines a list of postal codes to target with bid adjustments.

        :rtype: PostalCodeTarget
        """

        if self.location_target is None:
            return None
        return self.location_target.PostalCodeTarget

    @postal_code_target.setter
    def postal_code_target(self, value):
        self.ensure_location_target()
        self.location_target.PostalCodeTarget = value


class _BulkLocationTarget(_BulkLocationTargetWithStringLocation):
    """ A base class for all bulk location target classes. """

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        super(_BulkLocationTarget, self).__init__(
            city_target=city_target,
            metro_area_target=metro_area_target,
            state_target=state_target,
            country_target=country_target,
            postal_code_target=postal_code_target,
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def _convert_target_to_bulk_entities(self):
        for location_type in self.LOCATION_TYPES:
            if location_type == 'City':
                if self.city_target is None or self.city_target.Bids is None:
                    continue
                for bid in self.city_target.Bids.CityTargetBid:
                    if bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.City
                    bulk_bid.location_type = location_type
                    bulk_bid.bid_adjustment = bid.BidAdjustment
                    bulk_bid._intent_option = self.location_target.IntentOption
                    yield bulk_bid
            elif location_type == 'MetroArea':
                if self.metro_area_target is None or self.metro_area_target.Bids is None:
                    continue
                for bid in self.metro_area_target.Bids.MetroAreaTargetBid:
                    if bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.MetroArea
                    bulk_bid.location_type = location_type
                    bulk_bid.bid_adjustment = bid.BidAdjustment
                    bulk_bid._intent_option = self.location_target.IntentOption
                    yield bulk_bid
            elif location_type == 'State':
                if self.state_target is None or self.state_target.Bids is None:
                    continue
                for bid in self.state_target.Bids.StateTargetBid:
                    if bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.State
                    bulk_bid.location_type = location_type
                    bulk_bid.bid_adjustment = bid.BidAdjustment
                    bulk_bid._intent_option = self.location_target.IntentOption
                    yield bulk_bid
            elif location_type == 'Country':
                if self.country_target is None or self.country_target.Bids is None:
                    continue
                for bid in self.country_target.Bids.CountryTargetBid:
                    if bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.CountryAndRegion
                    bulk_bid.location_type = location_type
                    bulk_bid.bid_adjustment = bid.BidAdjustment
                    bulk_bid._intent_option = self.location_target.IntentOption
                    yield bulk_bid
            elif location_type == 'PostalCode':
                if self.postal_code_target is None or self.postal_code_target.Bids is None:
                    continue
                for bid in self.postal_code_target.Bids.PostalCodeTargetBid:
                    if bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.PostalCode
                    bulk_bid.location_type = location_type
                    bulk_bid.bid_adjustment = bid.BidAdjustment
                    bulk_bid._intent_option = self.location_target.IntentOption
                    yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.ensure_location_target()
        for bulk_bid in self.child_entities:
            if bulk_bid.location_type == 'City':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('CityTargetBid')
                bid.City = bulk_bid.location
                bid.BidAdjustment = bulk_bid.bid_adjustment
                bid.IsExcluded = False
                self.city_target.Bids.CityTargetBid.append(bid)
            elif bulk_bid.location_type == 'MetroArea':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('MetroAreaTargetBid')
                bid.MetroArea = bulk_bid.location
                bid.BidAdjustment = bulk_bid.bid_adjustment
                bid.IsExcluded = False
                self.metro_area_target.Bids.MetroAreaTargetBid.append(bid)
            elif bulk_bid.location_type == 'State':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('StateTargetBid')
                bid.State = bulk_bid.location
                bid.BidAdjustment = bulk_bid.bid_adjustment
                bid.IsExcluded = False
                self.state_target.Bids.StateTargetBid.append(bid)
            elif bulk_bid.location_type == 'Country':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('CountryTargetBid')
                bid.CountryAndRegion = bulk_bid.location
                bid.BidAdjustment = bulk_bid.bid_adjustment
                bid.IsExcluded = False
                self.country_target.Bids.CountryTargetBid.append(bid)
            elif bulk_bid.location_type == 'PostalCode':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('PostalCodeTargetBid')
                bid.PostalCode = bulk_bid.location
                bid.BidAdjustment = bulk_bid.bid_adjustment
                bid.IsExcluded = False
                self.postal_code_target.Bids.PostalCodeTargetBid.append(bid)
        if self.child_entities:
            bid = self.child_entities[0]
            if bid.intent_option is not None:
                self.location_target.IntentOption = bid.intent_option


class BulkCampaignLocationTarget(_BulkLocationTarget, _BulkSubTargetCampaignMixin):
    """ Represents a geographical location target that is associated with a campaign.

    This class exposes the :attr:`city_target`, :attr:`metro_area_target`, :attr:`state_target`,
    :attr:`country_target`, and :attr:`postal_code_target`.
    Each sub type can be read and written as fields of the Campaign Location Target record in a bulk file.

    For more information, see Campaign Location Target at http://go.microsoft.com/fwlink/?LinkID=511525.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkLocationTarget.__init__(
            self,
            city_target=city_target,
            metro_area_target=metro_area_target,
            state_target=state_target,
            country_target=country_target,
            postal_code_target=postal_code_target,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignLocationTargetBid()


class BulkAdGroupLocationTarget(_BulkLocationTarget, _BulkSubTargetAdGroupMixin):
    """ Represents a geographical location target that is associated with an ad group.

    This class exposes the :attr:`city_target`, :attr:`metro_area_target`, :attr:`state_target`,
    :attr:`country_target`, and :attr:`postal_code_target`.
    Each sub type can be read and written as fields of the Ad Group Location Target record in a bulk file.

    For more information, see Ad Group Location Target at http://go.microsoft.com/fwlink/?LinkID=511541.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkLocationTarget.__init__(
            self,
            city_target=city_target,
            metro_area_target=metro_area_target,
            state_target=state_target,
            country_target=country_target,
            postal_code_target=postal_code_target,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupLocationTargetBid()


class _BulkNegativeLocationTargetBid(_BulkTargetBid):
    """ This base class provides properties that are shared by all bulk negative location target bid classes. """

    def __init__(self,
                 location=None,
                 location_type=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        self._location = location
        self._location_type = location_type
        super(_BulkNegativeLocationTargetBid, self).__init__(
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name
        )

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Target,
            field_to_csv=lambda c: bulk_str(c.location),
            csv_to_field=lambda c, v: setattr(c, '_location', v),
        ),
        _SimpleBulkMapping(
            header=_StringTable.SubType,
            field_to_csv=lambda c: location_target_type_bulk_str(c.location_type),
            csv_to_field=lambda c, v: setattr(c, '_location_type', parse_location_target_type(v)),
        ),
    ]

    def _prepare_process_mapping_from_row_values(self):
        pass

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def location_type(self):
        return self._location_type

    @location_type.setter
    def location_type(self, value):
        self._location_type = value


class BulkAdGroupNegativeLocationTargetBid(_BulkNegativeLocationTargetBid, _BulkTargetBidAdGroupMixin):
    """ Represents one sub location negative target bid within a negative location target that is associated with an ad group.

    This class exposes properties that can be read and written as fields of the Ad Group Negative Location Target record in a bulk file.

    For more information, see Ad Group Negative Location Target at http://go.microsoft.com/fwlink/?LinkID=511542.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 location=None,
                 location_type=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None):
        _BulkNegativeLocationTargetBid.__init__(
            self,
            location=location,
            location_type=location_type,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )


class BulkCampaignNegativeLocationTargetBid(_BulkNegativeLocationTargetBid, _BulkTargetBidCampaignMixin):
    """ Represents one sub location negative target bid within a negative location target that is associated with a campaign.

    This class exposes properties that can be read and written as fields of the Campaign Negative Location Target record in a bulk file.

    For more information, see Campaign Negative Location Target at http://go.microsoft.com/fwlink/?LinkID=511526.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """
    def __init__(self,
                 location=None,
                 location_type=None,
                 bid_adjustment=None,
                 intent_option=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None):
        _BulkNegativeLocationTargetBid.__init__(
            self,
            location=location,
            location_type=location_type,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )


class _BulkNegativeLocationTarget(_BulkLocationTargetWithStringLocation):
    """ A base class for all bulk negative location target classes.

    For example :class:`.BulkAdGroupNegativeLocationTarget`.
    """

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 entity_id=None,
                 entity_name=None,
                 parent_entity_name=None):
        super(_BulkNegativeLocationTarget, self).__init__(
            city_target=city_target,
            metro_area_target=metro_area_target,
            state_target=state_target,
            country_target=country_target,
            postal_code_target=postal_code_target,
            status=status,
            target_id=target_id,
            entity_id=entity_id,
            entity_name=entity_name,
            parent_entity_name=parent_entity_name,
        )

    def _convert_target_to_bulk_entities(self):
        for location_type in self.LOCATION_TYPES:
            if location_type == 'City':
                if self.city_target is None or self.city_target.Bids is None:
                    continue
                for bid in self.city_target.Bids.CityTargetBid:
                    if not bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.City
                    bulk_bid.location_type = location_type
                    yield bulk_bid
            elif location_type == 'MetroArea':
                if self.metro_area_target is None or self.metro_area_target.Bids is None:
                    continue
                for bid in self.metro_area_target.Bids.MetroAreaTargetBid:
                    if not bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.MetroArea
                    bulk_bid.location_type = location_type
                    yield bulk_bid
            elif location_type == 'State':
                if self.state_target is None or self.state_target.Bids is None:
                    continue
                for bid in self.state_target.Bids.StateTargetBid:
                    if not bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.State
                    bulk_bid.location_type = location_type
                    yield bulk_bid
            elif location_type == 'Country':
                if self.country_target is None or self.country_target.Bids is None:
                    continue
                for bid in self.country_target.Bids.CountryTargetBid:
                    if not bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.CountryAndRegion
                    bulk_bid.location_type = location_type
                    yield bulk_bid
            elif location_type == 'PostalCode':
                if self.postal_code_target is None or self.postal_code_target.Bids is None:
                    continue
                for bid in self.postal_code_target.Bids.PostalCodeTargetBid:
                    if not bid.IsExcluded:
                        continue
                    bulk_bid = self._create_and_populate_bid()
                    bulk_bid.location = bid.PostalCode
                    bulk_bid.location_type = location_type
                    yield bulk_bid

    def _convert_bulk_entities_to_target(self):
        self.ensure_location_target()
        for bulk_bid in self.child_entities:
            if bulk_bid.location_type == 'City':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('CityTargetBid')
                bid.City = bulk_bid.location
                bid.IsExcluded = True
                self.city_target.Bids.CityTargetBid.append(bid)
            elif bulk_bid.location_type == 'MetroArea':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('MetroAreaTargetBid')
                bid.MetroArea = bulk_bid.location
                bid.IsExcluded = True
                self.metro_area_target.Bids.MetroAreaTargetBid.append(bid)
            elif bulk_bid.location_type == 'State':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('StateTargetBid')
                bid.State = bulk_bid.location
                bid.IsExcluded = True
                self.state_target.Bids.StateTargetBid.append(bid)
            elif bulk_bid.location_type == 'Country':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('CountryTargetBid')
                bid.CountryAndRegion = bulk_bid.location
                bid.IsExcluded = True
                self.country_target.Bids.CountryTargetBid.append(bid)
            elif bulk_bid.location_type == 'PostalCode':
                bid = _CAMPAIGN_OBJECT_FACTORY.create('PostalCodeTargetBid')
                bid.PostalCode = bulk_bid.location
                bid.IsExcluded = True
                self.postal_code_target.Bids.PostalCodeTargetBid.append(bid)


class BulkCampaignNegativeLocationTarget(_BulkNegativeLocationTarget, _BulkSubTargetCampaignMixin):
    """ Represents a negative geographical location target that is associated with a campaign.

    This class exposes the :attr:`city_target`, :attr:`metro_area_target`, :attr:`state_target`,
    :attr:`country_target`, and :attr:`postal_code_target`.
    Each sub type can be read and written as fields of the Campaign Location Target record in a bulk file.

    For more information, see Campaign Negative Location Target at http://go.microsoft.com/fwlink/?LinkID=511526.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 campaign_id=None,
                 campaign_name=None, ):
        _BulkNegativeLocationTarget.__init__(
            self,
            city_target=city_target,
            metro_area_target=metro_area_target,
            state_target=state_target,
            country_target=country_target,
            postal_code_target=postal_code_target,
            status=status,
            target_id=target_id,
            entity_id=campaign_id,
            entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkCampaignNegativeLocationTargetBid()


class BulkAdGroupNegativeLocationTarget(_BulkNegativeLocationTarget, _BulkSubTargetAdGroupMixin):
    """ Represents a negative geographical location target that is associated with an ad group.

    This class exposes the :attr:`city_target`, :attr:`metro_area_target`, :attr:`state_target`,
    :attr:`country_target`, and :attr:`postal_code_target`.
    Each sub type can be read and written as fields of the Ad Group Location Target record in a bulk file.

    For more information, see Ad Group Negative Location Target at http://go.microsoft.com/fwlink/?LinkID=511542.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 city_target=None,
                 metro_area_target=None,
                 state_target=None,
                 country_target=None,
                 postal_code_target=None,
                 status=None,
                 target_id=None,
                 ad_group_id=None,
                 ad_group_name=None,
                 campaign_name=None, ):
        _BulkNegativeLocationTarget.__init__(
            self,
            city_target=city_target,
            metro_area_target=metro_area_target,
            state_target=state_target,
            country_target=country_target,
            postal_code_target=postal_code_target,
            status=status,
            target_id=target_id,
            entity_id=ad_group_id,
            entity_name=ad_group_name,
            parent_entity_name=campaign_name,
        )

    def _create_bid(self):
        return BulkAdGroupNegativeLocationTargetBid()
