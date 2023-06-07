from abc import ABCMeta, abstractmethod, abstractproperty

from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.bulk import EntityWriteException


class _BulkObject(metaclass=ABCMeta):
    """ The abstract base class for all bulk objects that can be read and written in a file that conforms to the Bing Ad Bulk File Schema.

    For more information about the Bulk File Schema, see https://go.microsoft.com/fwlink/?linkid=846127.
    """

    @abstractmethod
    def read_from_row_values(self, row_values):
        """ Read object data from a single row.

        *Example:*

        * SingleLineBulkEntity: reads entity fields.
        * BulkError: reads error fields.
        * BulkEntityIdentifier: reads identifier fields (Id, status etc.).

        :param row_values:
        :type row_values: _RowValues
        """

        raise NotImplementedError()

    @abstractmethod
    def write_to_row_values(self, row_values, exclude_readonly_data):
        """ Writes object data to a single row.

        *Example:*

        * SingleLineBulkEntity: writes entity fields.
        * BulkEntityIdentifier: writes identifier fields (Id, status etc.)

        :param row_values:
        :type row_values: _RowValues
        """

        raise NotImplementedError()

    @abstractmethod
    def read_related_data_from_stream(self, stream_reader):
        """ Reads object data from consecutive rows.

        *Example:*

        * SingleLineBulkEntity: reads entity errors.
        * MultilineBulkEntity: reads child entities.

        :param stream_reader:
        :type stream_reader: _BulkStreamReader
        """

        pass

    @abstractmethod
    def write_to_stream(self, row_writer, exclude_readonly_data):
        """ Writes object data to consecutive rows.

        *Example:*

        * SingleLineBulkEntity: writes entity.
        * MultilineBulkEntity: writes child entities.
        * BulkEntityIdentifier: writes identifier information (Id, status etc.)

        :param row_writer:
        :type row_writer: :class:`._BulkObjectWriter`
        """

        raise NotImplementedError()

    @abstractproperty
    def can_enclose_in_multiline_entity(self):
        """ Returns true if the entity is part of multiline entity, false otherwise.

        *Example:*

        * BulkSiteLinkAdExtension: returns true
        * BulkCampaignTarget: returns true
        * BulkAdGroup: returns false
        * BulkKeyword: returns false

        :rtype: bool
        """
        return False

    @abstractmethod
    def enclose_in_multiline_entity(self):
        """ Creates a multiline entity containing this entity

        *Example:*

        * BulkSiteLink: returns BulkSiteLinkAdExtension containing this BulkSiteLink
        * BulkCampaignAgeTargetBid: return BulkCampaignTarget containing this BulkCampaignAgeTargetBid

        :return: the wrapping multi-line entity
        :rtype: :class:`._MultiRecordBulkEntity`
        """
        raise NotImplementedError()

    def convert_to_values(self, row_values, mappings):
        for mapping in mappings:
            try:
                mapping.convert_to_csv(self, row_values)
            except Exception as ex:
                raise self._create_entity_write_error(mapping, ex)

    def _create_entity_write_error(self, mapping, ex):
        entity_type = str(type(self))
        if isinstance(mapping, _SimpleBulkMapping):
            message = "Couldn't write column {0} of {1} entity: {2}".format(mapping.header, entity_type, ex)
        else:
            message = "Couldn't write {0} entity: {1}".format(entity_type, ex)
        message += " See InnerException for error details."
        return EntityWriteException(message=message, inner_exception=ex)
