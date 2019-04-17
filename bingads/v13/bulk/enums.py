from enum import Enum

class ResultFileType(Enum):
    """ Defines the possible types of result files.  """

    full_download = 1
    """ The result file represents the full sync of entities that were specified in the download request. """

    partial_download = 2
    """ The result file represents the partial sync of entities that were specified in the download request. """

    upload = 3
    """ The result file represents the entities specified in the upload request, or the corresponding errors, or both entities and errors. """
