"""
Repro: BulkFileReader raises EntityReadException on audience-type rows
due to missing 'SupportedCampaignTypes' attribute on REST Pydantic models.

Bug summary:
  BulkAudience._MAPPINGS accesses c.audience.SupportedCampaignTypes (PascalCase).
  The REST SDK creates audience objects as Pydantic models (openapi_client) whose
  Python attribute is supported_campaign_types (snake_case). Accessing the PascalCase
  name raises AttributeError, which is wrapped as EntityReadException and stops
  iteration — causing all rows after the first audience row to be silently lost.

Affected entity types (all share BulkAudience._MAPPINGS):
  Remarketing List, Custom Audience, In Market Audience, Product Audience,
  Combined List, Customer List, Similar Remarketing List,
  Impression Based Remarketing List

Run this script directly (no API credentials needed):
  python bulk_audience_supported_campaign_types_bug_repro.py
"""

import os
import sys
import tempfile

# Allow running from the examples/v13 directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from bingads.v13.bulk import BulkFileReader
from bingads.v13.bulk.exceptions import EntityReadException


# ---------------------------------------------------------------------------
# Minimal bulk CSV content that triggers the bug.
#
# Column subset chosen to include all headers touched by BulkAudience._MAPPINGS
# and BulkRemarketingList._MAPPINGS. The BulkFileReader treats missing columns
# as None, so extra headers not listed here are harmless.
#
# Row layout:
#   Row 1 – Remarketing List  (triggers EntityReadException when read)
#   Row 2 – Custom Audience   (lost because iteration stops after row 1 fails)
# ---------------------------------------------------------------------------
BULK_CSV_CONTENT = (
    "Type,Status,Id,Parent Id,Audience,Description,"
    "Membership Duration,Scope,Tag Id,"
    "Audience Search Size,Audience Network Size,"
    "Supported Campaign Types,Remarketing Rule\n"
    "Remarketing List,Active,11111,22222,"
    "Test Remarketing List,A remarketing list,"
    "30,Account,33333,"
    "1000,500,"
    "Search;Shopping,\n"
    "Custom Audience,Active,44444,22222,"
    "Test Custom Audience,A custom audience,"
    "30,Account,,"
    "200,100,"
    "Search;Display,\n"
)


def write_csv_to_temp_file(content):
    fd, path = tempfile.mkstemp(suffix='.csv', prefix='bulk_audience_repro_')
    os.close(fd)
    with open(path, 'w', encoding='utf-8-sig') as f:
        f.write(content)
    return path


def reproduce_bug():
    """
    Demonstrates that BulkFileReader raises EntityReadException when it encounters
    an audience-type row, and that all rows after the failing row are never read.

    Root cause:
      BulkAudience._MAPPINGS SupportedCampaignTypes mapping evaluates
          c.audience.SupportedCampaignTypes   (PascalCase getattr)
      before calling csv_to_field_SupportedCampaignTypes(). In the REST SDK the
      audience object is a Pydantic BaseModel whose field is stored as
      supported_campaign_types (snake_case). getattr raises AttributeError, which
      row_values.convert_to_entity() wraps into EntityReadException.
    """
    csv_path = write_csv_to_temp_file(BULK_CSV_CONTENT)

    print("=" * 70)
    print("Repro: BulkFileReader EntityReadException on audience rows")
    print("=" * 70)
    print(f"\nTemp bulk CSV: {csv_path}")
    print("\nCSV content:")
    print(BULK_CSV_CONTENT)

    entities_read = []
    exception_caught = None

    try:
        with BulkFileReader(file_path=csv_path) as reader:
            for entity in reader.read_entities():
                entities_read.append(entity)
                print(f"  Read entity: {type(entity).__name__}")
    except EntityReadException as ex:
        exception_caught = ex
        print(f"\n[BUG TRIGGERED] EntityReadException raised during iteration:")
        print(f"  Message   : {ex}")
        print(f"  Inner exc : {ex.inner_exception}")
        print(f"\n  Entities read before failure : {len(entities_read)}")
        print(f"  Entities lost (never read)   : 2 total - {len(entities_read)} read = "
              f"{2 - len(entities_read)} lost")
    except Exception as ex:
        print(f"\n[UNEXPECTED ERROR] {type(ex).__name__}: {ex}")
        raise
    finally:
        os.unlink(csv_path)

    print("\n" + "-" * 70)
    if exception_caught is not None:
        inner = exception_caught.inner_exception
        is_attribute_error = isinstance(inner, AttributeError)
        missing_attr = 'SupportedCampaignTypes' in str(inner)

        print("Bug confirmed:" if (is_attribute_error and missing_attr) else "Unexpected error:")
        print(f"  AttributeError on SupportedCampaignTypes : {is_attribute_error and missing_attr}")
        print(f"  Rows lost after first audience row       : {2 - len(entities_read) > 0}")
    else:
        print("No EntityReadException raised — bug may be fixed or not reproduced.")
        print(f"Entities read: {len(entities_read)}")
    print("=" * 70)

    return exception_caught


def demonstrate_attribute_error_directly():
    """
    Shows the AttributeError directly without going through the full bulk pipeline.

    In the REST SDK, _CAMPAIGN_OBJECT_FACTORY_V13.create('RemarketingList') returns
    a Pydantic BaseModel. Accessing the PascalCase alias 'SupportedCampaignTypes'
    on the model raises AttributeError because the Python field name is
    'supported_campaign_types'.
    """
    from bingads.service_client import _CAMPAIGN_OBJECT_FACTORY_V13

    print("\n" + "=" * 70)
    print("Direct attribute access demonstration")
    print("=" * 70)

    remarketing_list = _CAMPAIGN_OBJECT_FACTORY_V13.create('RemarketingList')
    print(f"\nCreated object type: {type(remarketing_list).__name__}")

    # snake_case access (correct for Pydantic models) — succeeds
    try:
        val = remarketing_list.supported_campaign_types
        print(f"  remarketing_list.supported_campaign_types  -> {val!r}  [OK]")
    except AttributeError as ex:
        print(f"  remarketing_list.supported_campaign_types  -> AttributeError: {ex}  [UNEXPECTED]")

    # PascalCase access (used by BulkAudience._MAPPINGS) — raises AttributeError
    try:
        val = remarketing_list.SupportedCampaignTypes
        print(f"  remarketing_list.SupportedCampaignTypes    -> {val!r}  [Bug NOT reproduced]")
    except AttributeError as ex:
        print(f"  remarketing_list.SupportedCampaignTypes    -> AttributeError: {ex}  [BUG]")

    print("=" * 70)


if __name__ == '__main__':
    demonstrate_attribute_error_directly()
    reproduce_bug()
