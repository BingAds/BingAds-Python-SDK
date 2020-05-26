from bingads.v13.bulk.entities import QualityScoreData
from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

from bingads.v13.internal.bulk.string_table import _StringTable
from bingads.v13.internal.bulk.entities.single_record_bulk_entity import _SingleRecordBulkEntity
from bingads.v13.internal.bulk.mappings import _SimpleBulkMapping, _ComplexBulkMapping
from bingads.v13.internal.extensions import *


class BulkExperiment(_SingleRecordBulkEntity):
    """ Represents an experiment.

    This class exposes the property :attr:`experiment` that can be read and written as fields of the Experiment record
    in a bulk file.

    For more information, see Experiment at https://go.microsoft.com/fwlink/?linkid=846127.

    *See also:*

    * :class:`.BulkServiceManager`
    * :class:`.BulkOperation`
    * :class:`.BulkFileReader`
    * :class:`.BulkFileWriter`
    """

    def __init__(self, experiment=None):
        super(BulkExperiment, self).__init__()
        self._experiment = experiment

    @property
    def experiment(self):
        """ The experiment.
        """
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment

    _MAPPINGS = [
        _SimpleBulkMapping(
            header=_StringTable.Id,
            field_to_csv=lambda c: bulk_str(c.experiment.Id),
            csv_to_field=lambda c, v: setattr(c.experiment, 'Id', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Status,
            field_to_csv=lambda c: c.experiment.ExperimentStatus,
            csv_to_field=lambda c, v: setattr(c.experiment, 'ExperimentStatus', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.Name,
            field_to_csv=lambda c: c.experiment.Name,
            csv_to_field=lambda c, v: setattr(c.experiment, 'Name', v)
        ),
        _SimpleBulkMapping(
            header=_StringTable.StartDate,
            field_to_csv=lambda c: bulk_date_str(c.experiment.StartDate),
            csv_to_field=lambda c, v: setattr(c.experiment, 'StartDate', parse_date(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.EndDate,
            field_to_csv=lambda c: field_to_csv_SchedulingDate(c.experiment.EndDate, c.experiment.Id),
            csv_to_field=lambda c, v: setattr(c.experiment, 'EndDate', parse_date(v))
        ),
        _SimpleBulkMapping(
            header=_StringTable.TrafficSplitPercent,
            field_to_csv=lambda c: bulk_str(c.experiment.TrafficSplitPercent),
            csv_to_field=lambda c, v: setattr(c.experiment, 'TrafficSplitPercent', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.BaseCampaignId,
            field_to_csv=lambda c: bulk_str(c.experiment.BaseCampaignId),
            csv_to_field=lambda c, v: setattr(c.experiment, 'BaseCampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ExperimentCampaignId,
            field_to_csv=lambda c: bulk_str(c.experiment.ExperimentCampaignId),
            csv_to_field=lambda c, v: setattr(c.experiment, 'ExperimentCampaignId', int(v) if v else None)
        ),
        _SimpleBulkMapping(
            header=_StringTable.ExperimentType,
            field_to_csv=lambda c: c.experiment.ExperimentType,
            csv_to_field=lambda c, v: setattr(c.experiment, 'ExperimentType', v)
        ),
    ]

    def process_mappings_from_row_values(self, row_values):
        self.experiment = _CAMPAIGN_OBJECT_FACTORY_V13.create('Experiment')
        row_values.convert_to_entity(self, BulkExperiment._MAPPINGS)

    def process_mappings_to_row_values(self, row_values, exclude_readonly_data):
        self._validate_property_not_null(self._experiment, 'Experiment')
        self.convert_to_values(row_values, BulkExperiment._MAPPINGS)

    def read_additional_data(self, stream_reader):
        super(BulkExperiment, self).read_additional_data(stream_reader)