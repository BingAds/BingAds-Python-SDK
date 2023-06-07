from abc import ABCMeta, abstractmethod


class _BulkMapping(metaclass=ABCMeta):
    @abstractmethod
    def convert_to_csv(self, entity, row_values):
        raise NotImplementedError()

    @abstractmethod
    def convert_to_entity(self, row_values, entity):
        raise NotImplementedError()


class _SingleFieldBulkMapping(_BulkMapping, metaclass=ABCMeta):
    def __init__(self, csv_to_field, filed_to_csv):
        self._csv_to_field = csv_to_field
        self._field_to_csv = filed_to_csv

    @property
    def csv_to_field(self):
        """

        :rtype: str -> T
        """

        return self._csv_to_field

    @property
    def field_to_csv(self):
        """

        :rtype: T -> str
        :return:
        """
        return self._field_to_csv

    def convert_to_csv(self, entity, row_values):
        if self.field_to_csv is None:
            return None
        row_values[self.parse_header(entity)] = self.field_to_csv(entity)

    def convert_to_entity(self, row_values, entity):
        # Bulk file can have fewer column than SDK knows, so to have the ability to read old file, if cannot find column
        # just return None for that column, if it is mandatory, then will throw exception later, if not, then pass.

        self.csv_to_field(entity, row_values.try_get_value(self.parse_header(entity))[1])

    @abstractmethod
    def parse_header(self, entity):
        raise NotImplementedError()


class _SimpleBulkMapping(_SingleFieldBulkMapping):
    def __init__(self, header, csv_to_field, field_to_csv=None):
        super(_SimpleBulkMapping, self).__init__(csv_to_field, field_to_csv)
        self._header = header

    @property
    def header(self):
        """

        :rtype: str

        """
        return self._header

    def parse_header(self, entity):
        return self.header


class _DynamicColumnNameMapping(_SingleFieldBulkMapping):
    def __init__(self, header_func, csv_to_field, field_to_csv=None):
        super(_DynamicColumnNameMapping, self).__init__(csv_to_field, field_to_csv)
        self._header_func = header_func

    @property
    def header_func(self):
        """

        :rtype: T -> str
        """
        return self._header_func

    def parse_header(self, entity):
        return self.header_func(entity)


class _ComplexBulkMapping(_BulkMapping):
    def __init__(self, entity_to_csv, csv_to_entity):
        self._entity_to_csv = entity_to_csv
        self._csv_to_entity = csv_to_entity

    @property
    def csv_to_entity(self):
        """

        :rtype: _RowValues -> T
        """

        return self._csv_to_entity

    @property
    def entity_to_csv(self):
        """

        :rtype: T -> _RowValues
        """

        return self._entity_to_csv

    def convert_to_csv(self, entity, row_values):
        self.entity_to_csv(entity, row_values)

    def convert_to_entity(self, row_values, entity):
        self.csv_to_entity(row_values, entity)
