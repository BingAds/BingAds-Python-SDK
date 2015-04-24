from bingads.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.internal.bulk.string_table import _StringTable
from bingads.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.internal.bulk.entities.multi_record_bulk_entity import _MultiRecordBulkEntity
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY

from ..common import _ProductConditionHelper

from .common import *
from .common import _BulkCampaignAdExtensionAssociation
from .common import _BulkAdExtensionIdentifier


class _BulkProductAdExtensionIdentifier(_BulkAdExtensionIdentifier):
    def __init__(self,
                 name=None,
                 account_id=None,
                 ad_extension_id=None,
                 status=None,
                 version=None):
        super(_BulkProductAdExtensionIdentifier, self).__init__(
            account_id=account_id,
            ad_extension_id=ad_extension_id,
            status=status,
            version=version,
        )
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def __eq__(self, other):
        return isinstance(other, _BulkProductAdExtensionIdentifier) \
            and self._account_id == other.account_id \
            and self._ad_extension_id == other.ad_extension_id

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.name,
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        )
    ]

    def read_from_row_values(self, row_values):
        super(_BulkProductAdExtensionIdentifier, self).read_from_row_values(row_values)
        row_values.convert_to_entity(self, _BulkProductAdExtensionIdentifier._MAPPINGS)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        super(_BulkProductAdExtensionIdentifier, self).write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, _BulkProductAdExtensionIdentifier._MAPPINGS)

    def _create_entity_with_this_identifier(self):
        return BulkProductAdExtension(identifier=self)


class BulkProductConditionCollection(_SingleRecordBulkEntity):
    """ Represents the product condition collection for a product ad extension.

    Each product condition collection can be read or written in a bulk file.

    This class exposes the :attr:`product_condition_collection` property that can be read and written
    as fields of the Product Ad Extension record in a bulk file.

    For more information, see Product Ad Extension at http://go.microsoft.com/fwlink/?LinkID=511516.

    The Product Ad Extension record includes the distinct properties of the :class:`.BulkProductConditionCollection` class, combined with
    the common properties of the :class:`.BulkProductAdExtension` class, for example :attr:`account_id` and :class:`.ProductAdExtension`.

    One :class:`.BulkProductAdExtension` has one or more :class:`.BulkProductConditionCollection`. Each :class:`.BulkProductConditionCollection` instance
    corresponds to one Product Ad Extension record in the bulk file. If you upload a :class:`.BulkProductAdExtension`,
    then you are effectively replacing any existing site links for the product ad extension.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 account_id=None,
                 ad_extension_id=None,
                 version=None,
                 status=None,
                 store_id=None,
                 name=None,
                 product_condition_collection=None):
        super(BulkProductConditionCollection, self).__init__()
        self._identifier = _BulkProductAdExtensionIdentifier(
            account_id=account_id,
            ad_extension_id=ad_extension_id,
            version=version,
            status=status,
        )

        self._product_condition_collection = product_condition_collection
        self._name = name
        self._store_id = store_id
        self._store_name = None

    @property
    def name(self):
        """ The name of the ad extension.

        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def store_id(self):
        """ The product ad extension's store identifier.

        :rtype: int
        """

        return self._store_id

    @store_id.setter
    def store_id(self, value):
        self._store_id = value

    @property
    def product_condition_collection(self):
        """ The collection of product conditions for a product ad extension.

        see ProductConditionCollection in https://msdn.microsoft.com/en-US/library/bing-ads-campaign-management-productconditioncollection.aspx
        """

        return self._product_condition_collection

    @product_condition_collection.setter
    def product_condition_collection(self, value):
        self._product_condition_collection = value

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

    @property
    def store_name(self):
        """ The product ad extension's store name.

        Corresponds to the 'Store Name' field in the bulk file.

        :rtype: str
        """

        return self._store_name

    _MAPPINGS = [
        _ComplexBulkMapping(
            lambda entity, row_values: _ProductConditionHelper.add_row_values_from_conditions(
                entity.product_condition_collection.Conditions.ProductCondition,
                row_values
            ),
            lambda row_values, entity: _ProductConditionHelper.add_conditions_from_row_values(
                row_values,
                entity.product_condition_collection.Conditions.ProductCondition
            )
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.name,
            csv_to_field=lambda c, v: setattr(c, 'name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BingMerchantCenterId,
            field_to_csv=lambda c: bulk_str(c.store_id),
            csv_to_field=lambda c, v: setattr(c, 'store_id', int(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.BingMerchantCenterName,
            field_to_csv=lambda c: bulk_str(c.store_name),
            csv_to_field=lambda c, v: setattr(c, '_store_name', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.product_condition_collection = _CAMPAIGN_OBJECT_FACTORY.create('ProductConditionCollection')
        self._identifier.read_from_row_values(row_values)
        row_values.convert_to_entity(self, BulkProductConditionCollection._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self.product_condition_collection, 'product_condition_collection')
        self._validate_property_not_null(
            self.product_condition_collection.Conditions,
            'product_condition_collection.Conditions'
        )
        self._identifier.write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkProductConditionCollection._MAPPINGS)

    def can_enclose_in_multiline_entity(self):
        return True

    def enclose_in_multiline_entity(self):
        return BulkProductAdExtension(product_collection=self)

    def read_additional_data(self, stream_reader):
        super(BulkProductConditionCollection, self).read_additional_data(stream_reader)


class BulkProductAdExtension(_MultiRecordBulkEntity):
    """ Represents a product ad extension.

    This class exposes the :attr:`product_ad_extension` property that can be read and written
    as fields of the Product Ad Extension record in a bulk file.

    For more information, see Product Ad Extension at http://go.microsoft.com/fwlink/?LinkID=511516.

    The Product Ad Extension record includes the distinct properties of the :class:`.BulkProductConditionCollection` class, combined with
    the common properties of the :class:`.BulkProductAdExtension` class, for example :attr:`account_id` and :class:`.ProductAdExtension`.

    One :class:`.BulkProductAdExtension` has one or more :class:`.BulkProductConditionCollection`. Each :class:`.BulkProductConditionCollection` instance
    corresponds to one Product Ad Extension record in the bulk file. If you upload a :class:`.BulkProductAdExtension`,
    then you are effectively replacing any existing product conditions for the product ad extension.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self,
                 account_id=None,
                 product_ad_extension=None,
                 product_collection=None,
                 identifier=None):
        super(BulkProductAdExtension, self).__init__()
        self._account_id = account_id
        self._product_ad_extension = product_ad_extension
        self._product_condition_collections = []
        self._product_collection = product_collection
        self._identifier = identifier

        if self._product_collection and self._identifier:
            raise ValueError('Conflicting arguments of product_collection and identifier provided.')
        if self._product_collection:
            if not isinstance(self._product_collection, BulkProductConditionCollection):
                raise ValueError(
                    'Product collection object provided is not of type: {0}.'.format(
                        BulkProductConditionCollection.__name__
                    )
                )
            self._identifier = self._product_collection._identifier
        if self._identifier:
            if not isinstance(self._identifier, _BulkProductAdExtensionIdentifier):
                raise ValueError(
                    'Product ad extension identifier object provided is not of type: {0}'.format(
                        _BulkProductAdExtensionIdentifier.__name__
                    )
                )
            self._has_delete_all_row = self._identifier.is_delete_row

            self._product_ad_extension = _CAMPAIGN_OBJECT_FACTORY.create('ProductAdExtension')
            self._product_ad_extension.Type = 'ProductAdExtension'
            self._product_ad_extension.Id = self._identifier.ad_extension_id
            self._product_ad_extension.Status = self._identifier.status
            self._product_ad_extension.Version = self._identifier.version
            self._product_ad_extension.Name = self._identifier.name

            self.account_id = self._identifier.account_id
        if self._product_collection:
            self._add_product_collection(self._product_collection)

    @property
    def account_id(self):
        """ The ad extension's parent account identifier.

        Corresponds to the 'Parent Id' field in the bulk file.

        :type: int
        """

        return self._account_id

    @account_id.setter
    def account_id(self, value):
        self._account_id = value

    @property
    def product_ad_extension(self):
        """ The product ad extension.

        see ProductAdExtension from: https://msdn.microsoft.com/en-us/library/jj721706(v=msads.90).aspx
        """

        return self._product_ad_extension

    @product_ad_extension.setter
    def product_ad_extension(self, value):
        self._product_ad_extension = value

    @property
    def product_condition_collections(self):
        """ The list of :class:`BulkProductConditionCollection` are represented by multiple Product Ad Extension records in the file.

        :rtype: list[BulkProductConditionCollection]
        """
        return self._product_condition_collections

    @property
    def child_entities(self):
        return self._product_condition_collections

    def _add_product_collection(self, product_collection):
        """

        :param product_collection:
        :type product_collection: BulkProductConditionCollection
        :return:
        """
        self.product_condition_collections.append(product_collection)
        self.product_ad_extension.StoreId = product_collection.store_id
        self.product_ad_extension.StoreName = product_collection.store_name

    def write_to_stream(self, row_writer, exclude_readonly_data):
        self._validate_property_not_null(self._product_ad_extension, 'product_ad_extension')
        self._validate_property_not_null(
            self._product_ad_extension.ProductSelection,
            'product_ad_extension.ProductSelection'
        )
        delete_all_row = _BulkProductAdExtensionIdentifier(
            account_id=self.account_id,
            ad_extension_id=self.product_ad_extension.Id,
            name=self.product_ad_extension.Name,
            version=self.product_ad_extension.Version,
            status='Deleted',
        )
        row_writer.write_object_row(delete_all_row, exclude_readonly_data)
        for bulk_product_collection in self._convert_raw_to_bulk_product_condition_collections():
            bulk_product_collection.write_to_stream(row_writer, exclude_readonly_data)

    def read_related_data_from_stream(self, stream_reader):
        has_more_rows = True
        while has_more_rows:
            product_collection_success, product_collection = stream_reader.try_read(
                BulkProductConditionCollection,
                lambda x: x._identifier == self._identifier
            )
            if product_collection_success:
                self.product_condition_collections.append(product_collection)
            else:
                identifier_success, identifier = stream_reader.try_read(
                    _BulkProductAdExtensionIdentifier,
                    lambda x: x == self._identifier
                )

                if identifier_success:
                    if identifier.is_delete_row:
                        self._has_delete_all_row = True
                else:
                    has_more_rows = False
        self.product_ad_extension.ProductSelection.ProductConditionCollection = \
            [pc.product_condition_collection for pc in self.product_condition_collections]
        if self.product_condition_collections:
            self.product_ad_extension.Status = 'Active'
            self.product_ad_extension.StoreId = self.product_condition_collections[0].store_id
            self.product_ad_extension.StoreName = self.product_condition_collections[0].store_name
        else:
            self.product_ad_extension.Status = 'Deleted'

    def _convert_raw_to_bulk_product_condition_collections(self):
        for product_collection in self.product_ad_extension.ProductSelection.ProductConditionCollection:
            collection = BulkProductConditionCollection(
                account_id=self.account_id,
                ad_extension_id=self.product_ad_extension.Id,
                version=self.product_ad_extension.Version,
                name=self.product_ad_extension.Name,
                store_id=self.product_ad_extension.StoreId,
                product_condition_collection=product_collection
            )
            yield collection

    @property
    def all_children_are_present(self):
        return self._has_delete_all_row


class BulkCampaignProductAdExtension(_BulkCampaignAdExtensionAssociation):
    """ Represents a campaign level product ad extension.

    This class exposes properties that can be read and written
    as fields of the Campaign Product Ad Extension record in a bulk file.

    For more information, see Campaign Product Ad Extension at http://go.microsoft.com/fwlink/?LinkID=511535.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    pass
