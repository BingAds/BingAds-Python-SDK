from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity


class UnknownBulkEntity(_SingleRecordBulkEntity):
    """ Reserved to support new record types that may be added to the Bulk schema. """

    def __init__(self):
        super(UnknownBulkEntity, self).__init__()
        self._values = None

    @property
    def values(self):
        """ The forward compatibility map of fields and values.

        :rtype: dict | None
        """

        return self._values

    def process_mappings_from_row_values(self, row_values):
        self._values = row_values.to_dict()

    def process_mappings_to_row_values(self, row_values):
        for (key, value) in self._values.items():
            row_values[key] = value

    def read_additional_data(self, stream_reader):
        super(UnknownBulkEntity, self).read_additional_data(stream_reader)
