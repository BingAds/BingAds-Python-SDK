__author__ = 'Bing Ads SDK Team'
__email__ = 'bing_ads_sdk@microsoft.com'

from .exceptions import *
from .enums import *
from .bulk_operation_progress_info import *
from .bulk_operation_status import *
from .download_parameters import *
from .upload_parameters import *
from .bulk_operation import *
from .file_reader import *
from .file_writer import *
from .bulk_service_manager import *
from .entities import *

# Enable REST-style Pydantic model support for bulk entities
# This allows users to use modern REST models like:
#   campaign = Campaign(campaign_type=CampaignType.SEARCH, ...)
# Instead of SOAP-style factory-created objects
from bingads.v13.internal.rest_adapter import ensure_rest_support
ensure_rest_support()