from .enums import DownloadFileType, ResultFileType
from .entities.bulk_entity import BulkEntity
from bingads.v11.internal.bulk.stream_reader import _BulkStreamReader
from bingads.v11.internal.bulk.entities.multi_record_bulk_entity import _MultiRecordBulkEntity


class BulkFileReader:
    """ Provides a method to read bulk entities from a bulk file and make them accessible as an enumerable list.

    For more information about the Bulk File Schema, see https://go.microsoft.com/fwlink/?linkid=846127.
    """

    def __init__(self,
                 file_path,
                 file_format=DownloadFileType.csv,
                 result_file_type=ResultFileType.full_download,
                 encoding='utf-8-sig'):
        """ Initializes a new instance of this class with the specified file details.

        :param file_path: The path of the bulk file to read.
        :type file_path: str
        :param file_format: The bulk file format.
        :type file_format: DownloadFileType
        :param result_file_type: The result file type.
        :type result_file_type: ResultFileType
        :param encoding: The encoding of bulk file.
        :type encoding: str
        """

        self._file_path = file_path
        self._file_format = file_format
        self._result_file_type = result_file_type
        self._encoding = encoding

        self._is_for_full_download = result_file_type is ResultFileType.full_download
        self._entities_iterator = None
        self._bulk_stream_reader = _BulkStreamReader(file_path=self.file_path, file_format=self.file_format, encoding=self._encoding)
        self._bulk_stream_reader.__enter__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._entities_iterator = None
        self._bulk_stream_reader.__exit__(exc_type, exc_value, traceback)

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def close(self):
        self.__exit__(None, None, None)

    def next(self):
        return self.read_next_entity()

    def read_next_entity(self):
        """ Reads next entity from the bulk file.

        :return: next entity
        :rtype: BulkEntity
        """

        if self._entities_iterator is None:
            self._entities_iterator = self.read_entities()

        return next(self._entities_iterator)

    def read_entities(self):
        """ Gets an enumerable list of bulk entities that were read from the file.

        :return: an generator over the entities
        :rtype: collections.Iterator[BulkEntity]
        """

        next_batch = self._read_next_batch()

        while next_batch is not None:
            for entity in next_batch:
                yield entity
            next_batch = self._read_next_batch()

    def _read_next_batch(self):
        """ Reads next batch of entities from the file.

        Batch means a set of related entities.
        It can be one :class:`._SingleRecordBulkEntity`, one :class:`._MultiRecordBulkEntity` containing its child
        entities or a set of related child entities (for example several :class:`.BulkSiteLink`s logically belonging
        to the same SiteLink Ad Extension.

        :return: Next batch of entities
        :rtype: _SingleRecordBulkEntity or _MultiRecordBulkEntity
        """

        next_object = self._bulk_stream_reader.read()

        if next_object is None:
            return None
        if next_object.can_enclose_in_multiline_entity:
            multi_record_entity = next_object.enclose_in_multiline_entity()
            multi_record_entity.read_related_data_from_stream(self._bulk_stream_reader)
            if self._is_for_full_download:
                return [multi_record_entity]
            return self._extract_child_entities_if_needed(multi_record_entity)
        if isinstance(next_object, BulkEntity):
            return [next_object]
        raise NotImplementedError()

    def _extract_child_entities_if_needed(self, entity):
        # If the entity is a MultiLine entity and it has all child objects (delete all row was present), just return it
        if not isinstance(entity, _MultiRecordBulkEntity) or entity.all_children_are_present:
            yield entity
        else:
            # If not all child objects are present (there was no delete all row and we only have part of the MultiLine entity), return child object individually
            for child_generator in (
                    self._extract_child_entities_if_needed(child_entity)
                    for child_entity in entity.child_entities):
                for child in child_generator:
                    yield child

    @property
    def file_path(self):
        """ The path of the bulk file to read.

        :rtype: str
        """

        return self._file_path

    @property
    def file_format(self):
        """ The bulk file format.

        :rtype: DownloadFileType
        """

        return self._file_format

    @property
    def result_file_type(self):
        """ The result file type.

        :rtype: ResultFileType
        """

        return self._result_file_type

    @property
    def encoding(self):
        """ The encoding of bulk file.

        :rtype: str
        """

        return self._encoding
