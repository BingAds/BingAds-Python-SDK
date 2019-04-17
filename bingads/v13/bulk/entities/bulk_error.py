from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.bulk_object import _BulkObject
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping
from bingads.v13.internal.extensions import *


class BulkError(_BulkObject):
    """ Contains bulk file error details in a separate record that corresponds to the record of a :class:`.BulkEntity` derived instance.

    Properties of this class and of classes that it is derived from, correspond to error fields of the 'Error' records in a bulk file.
    For more information, see Bulk File Schema at https://go.microsoft.com/fwlink/?linkid=846127.

    *Example:*

    If you upload a :class:`.BulkCampaign` without setting the campaign name using :meth:`BulkServiceManager.upload_entities,
    and if you request errors to be returned in the results using the corresponding :attr:`SubmitUploadParameters.response_mode`,
    then the upload result file will contain a record that can be read with a :class:`.BulkFileReader` as an instance of :class:`.BulkError`.
    """

    def __init__(self):
        self._error = None
        self._number = None
        self._editorial_location = None
        self._editorial_term = None
        self._editorial_reason_code = None
        self._publisher_countries = None
        self._entity = None
        self._field_path = None

    @property
    def entity(self):
        return self._entity

    @entity.setter
    def entity(self, value):
        self._entity = value

    @property
    def error(self):
        """ The error code, for example 'CampaignServiceEditorialValidationError'.

        Corresponds to the 'Error' field in the bulk file.
        For more information, see Bing Ads Operation Error Codes at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: str
        """

        return self._error

    @property
    def number(self):
        """ The error number, for example '1042'.

        Corresponds to the 'Error Number' field in the bulk file.
        For more information, see Bing Ads Operation Error Codes at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: int
        """

        return self._number

    @property
    def editorial_location(self):
        """ The location of the entity property that resulted in the editorial error, for example 'AdDescription'.

        Corresponds to the 'Editorial Location' field in the bulk file.

        :rtype: str
        """

        return self._editorial_location

    @property
    def editorial_term(self):
        """ The term that resulted in the editorial error, for example 'bing'.

        Corresponds to the 'Editorial Term' field in the bulk file.

        :rtype: str
        """

        return self._editorial_term

    @property
    def editorial_reason_code(self):
        """ The term that resulted in the editorial error, for example '17'.

        Corresponds to the 'Editorial Reason Code' field in the bulk file.
        For more information, see Bing Ads Editorial Failure Reason Codes at https://go.microsoft.com/fwlink/?linkid=846127.

        :rtype: int
        """

        return self._editorial_reason_code


    @property
    def field_path(self):
        """ The term that resulted in the editorial error.

        Corresponds to the 'Field Path' field in the bulk file.

        :rtype: int
        """

        return self._field_path

    @property
    def publisher_countries(self):
        """ The publisher countries where editorial restriction is enforced, for example 'US'.

        Corresponds to the 'Publisher Countries' field in the bulk file.

        *Remarks:*

        In a bulk file, the list of publisher countries are delimited with a semicolon (;).

        :rtype: str
        """

        return self._publisher_countries

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Error,
            field_to_csv=lambda c: bulk_str(c.error),
            csv_to_field=lambda c, v: setattr(c, '_error', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ErrorNumber,
            field_to_csv=lambda c: bulk_str(c.number),
            csv_to_field=lambda c, v: setattr(c, '_number', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialLocation,
            field_to_csv=lambda c: bulk_str(c.editorial_location),
            csv_to_field=lambda c, v: setattr(c, '_editorial_location', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialReasonCode,
            field_to_csv=lambda c: bulk_str(c.editorial_reason_code),
            csv_to_field=lambda c, v: setattr(c, '_editorial_reason_code', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.EditorialTerm,
            field_to_csv=lambda c: bulk_str(c.editorial_term),
            csv_to_field=lambda c, v: setattr(c, '_editorial_term', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.PublisherCountries,
            field_to_csv=lambda c: bulk_str(c.publisher_countries),
            csv_to_field=lambda c, v: setattr(c, '_publisher_countries', v if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.FieldPath,
            field_to_csv=lambda c: bulk_str(c.field_path),
            csv_to_field=lambda c, v: setattr(c, '_field_path', v if v else None)
        ),
    ]

    def can_enclose_in_multiline_entity(self):
        return super(BulkError, self).can_enclose_in_multiline_entity()

    def enclose_in_multiline_entity(self):
        return super(BulkError, self).enclose_in_multiline_entity()

    def read_from_row_values(self, row_values):
        row_values.convert_to_entity(self, BulkError._MAPPINGS)

    def read_related_data_from_stream(self, stream_reader):
        return super(BulkError, self).read_related_data_from_stream(stream_reader)

    def write_to_row_values(self, row_values, exclude_readonly_data):
        self.entity.write_to_row_values(row_values, exclude_readonly_data)
        self.convert_to_values(row_values, BulkError._MAPPINGS)

    def write_to_stream(self, stream_writer, exclude_readonly_data):
        return super(BulkError, self).write_to_stream(stream_writer, exclude_readonly_data)
