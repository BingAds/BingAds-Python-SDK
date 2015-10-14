from . import DownloadFileType
from bingads.v10.internal.bulk.object_writer import _BulkObjectWriter


class BulkFileWriter:
    """ Provides methods to write bulk entities to a file.

    For more information about the Bulk File Schema, see http://go.microsoft.com/fwlink/?LinkID=620269.

    :param file_path: The file path of the bulk file to write.
    :type file_path: str
    :param file_format: The bulk file format.
    :type file_format: DownloadFileType
    """

    def __init__(self, file_path, file_format=DownloadFileType.csv):
        self._file_path = file_path
        self._file_format = file_format
        self._bulk_object_writer = _BulkObjectWriter(file_path=self.file_path, file_format=self.file_format)
        self._bulk_object_writer.__enter__()
        self._bulk_object_writer.write_file_metadata()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._bulk_object_writer.__exit__(exc_type, exc_value, traceback)

    def close(self):
        self.__exit__(None, None, None)

    def write_entity(self, entity, exclude_readonly_data=False):
        """ Writes the specified :class:`.BulkEntity` to the file.

        Bulk entities that are derived from :class:`._SingleRecordBulkEntity` will be written to a single row in the file.
        Bulk entities that are derived from :class:`._MultiRecordBulkEntity` will be written to multiple rows in the file.

        :param entity: The bulk entity to write to the file.
        :type entity: BulkEntity
        :param exclude_readonly_data: excludeReadonlyData indicates whether readonly data (such as errors, performance data etc.)
                                    should be excluded when writing to file
        :type exclude_readonly_data: bool
        :rtype: None
        """

        entity.write_to_stream(self._bulk_object_writer, exclude_readonly_data=exclude_readonly_data)

    @property
    def file_path(self):
        """ The file path of the bulk file to write.

        :rtype: str
        """

        return self._file_path

    @property
    def file_format(self):
        """ The bulk file format.

        :rtype: DownloadFileType
        """

        return self._file_format
