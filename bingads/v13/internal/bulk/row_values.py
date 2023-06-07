from .csv_headers import _CsvHeaders
from .mappings import _SimpleBulkMapping
from bingads.v13.bulk import EntityReadException


class _RowValues:
    def __init__(self, mappings=None, columns=None):
        self._mappings = mappings
        self._columns = columns
        if self.mappings is None:
            self._mappings = _CsvHeaders.get_mappings()
        if self.columns is None:
            self._columns = [None] * len(self._mappings)

    def __getitem__(self, key):
        return self.columns[self._mappings[key]]

    def __setitem__(self, key, value):
        self.columns[self._mappings[key]] = value

    def __contains__(self, item):
        return item in self.mappings

    def __len__(self):
        return len(self.mappings)

    def __str__(self):
        return u'{' + u', '.join([u'{0}:{1}'.format(k, self.columns[v]) for (k, v) in self.mappings.items()]) + u'}'

    def convert_to_entity(self, entity, bulk_mappings):
        for mapping in bulk_mappings:
            try:
                mapping.convert_to_entity(self, entity)
            except Exception as ex:
                raise self._create_entity_read_exception(entity, mapping, ex)

    def _create_entity_read_exception(self, entity, mapping, ex):
        entity_type = str(type(entity))

        if isinstance(mapping, _SimpleBulkMapping):
            message = "Couldn't parse column {0} of {1} entity: {2}".format(
                mapping.header,
                entity_type,
                str(ex)
            )
        else:
            message = "Couldn't parse {0} entity: {1}".format(entity_type, str(ex))
        message += " See ColumnValues for detailed row information and InnerException for error details."
        message += u' row values: {0}'.format(self)

        return EntityReadException(message=message, row_values=str(self), inner_exception=ex)

    def try_get_value(self, header):
        if header not in self.mappings:
            return False, None
        return True, self[header]

    def to_dict(self):
        return dict([(k, self.columns[v]) for (k, v) in self.mappings.items()])

    @property
    def mappings(self):
        return self._mappings

    @property
    def columns(self):
        return self._columns
