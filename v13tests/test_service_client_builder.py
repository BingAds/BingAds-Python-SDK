import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

from bingads.service_client import ServiceClient, _CAMPAIGN_OBJECT_FACTORY_V13
from suds import null


class TestServiceClientBuilder(unittest.TestCase):
    def setUp(self):
        self.transport = patch("suds.transport.http.HttpTransport.send",
                               side_effect=AssertionError("Offline test must not send requests"))
        self.transport.start()
        self.addCleanup(self.transport.stop)
        self.campaign = ServiceClient("campaignmanagement", 13, nosend=True)

    def test_optional_enum_defaults_and_explicit_values_in_both_factories(self):
        for environment in ("production", "sandbox"):
            client = ServiceClient("campaignmanagement", 13, environment=environment, nosend=True)
            for factory in (client.factory, _CAMPAIGN_OBJECT_FACTORY_V13):
                image = factory.create("Image")
                self.assertIsNone(image.AdvertiserAILabel)
                media = client.factory.create("ArrayOfMedia")
                media.Media = [image]
                for value in (None, "AIContent", "", null()):
                    with self.subTest(environment=environment, value=value):
                        image.AdvertiserAILabel = value
                        xml = ET.fromstring(client.AddMedia(AccountId=1, Media=media).envelope)
                        label = xml.find(".//{*}AdvertiserAILabel")
                        if value is None:
                            self.assertIsNone(label)
                        elif value == "AIContent":
                            self.assertEqual("AIContent", label.text)
                        elif value == "":
                            self.assertIsNone(label.text)
                            self.assertEqual({}, label.attrib)
                        else:
                            self.assertEqual("true", label.get(
                                "{http://www.w3.org/2001/XMLSchema-instance}nil"))

    def test_nested_optional_enum_is_omitted_without_removing_complex_object(self):
        adgroup = self.campaign.factory.create("AdGroup")
        self.assertIsNotNone(adgroup.AdRotation)
        self.assertIsNone(adgroup.AdRotation.Type)
        groups = self.campaign.factory.create("ArrayOfAdGroup")
        groups.AdGroup = [adgroup]
        xml = ET.fromstring(self.campaign.AddAdGroups(CampaignId=1, AdGroups=groups).envelope)
        rotation = xml.find(".//{*}AdRotation")
        self.assertIsNotNone(rotation)
        self.assertIsNone(rotation.find("{*}Type"))
        adgroup.AdRotation.Type = "RotateAdsEvenly"
        xml = ET.fromstring(self.campaign.AddAdGroups(CampaignId=1, AdGroups=groups).envelope)
        self.assertEqual("RotateAdsEvenly", xml.find(".//{*}AdRotation/{*}Type").text)

    def test_flags_and_array_wrappers_keep_existing_defaults_and_values(self):
        campaign = self.campaign.factory.create("Campaign")
        self.assertIsNone(campaign.CampaignType)
        self.assertIsNotNone(campaign.Languages)
        self.assertEqual([], campaign.Languages.string)
        campaigns = self.campaign.factory.create("ArrayOfCampaign")
        self.assertEqual([], campaigns.Campaign)
        campaigns.Campaign = [campaign]
        for value in (None, "Search Shopping"):
            campaign.CampaignType = value
            xml = ET.fromstring(self.campaign.AddCampaigns(AccountId=1, Campaigns=campaigns).envelope)
            element = xml.find(".//{*}CampaignType")
            if value is None:
                self.assertIsNone(element)
            else:
                self.assertEqual(value, element.text)

    def test_repeated_enum_stays_a_list_and_serializes_explicit_items(self):
        types = self.campaign.factory.create("ArrayOfAdType")
        self.assertEqual([], types.AdType)
        for values in ([], ["Text", "Image"], [""]):
            types.AdType = values
            xml = ET.fromstring(self.campaign.GetAdsByAdGroupId(AdGroupId=1, AdTypes=types).envelope)
            self.assertEqual([value or None for value in values],
                             [element.text for element in xml.findall(".//{*}AdType")])

    def test_reporting_optional_enum_is_omitted_and_required_enum_is_unchanged(self):
        client = ServiceClient("reporting", 13, nosend=True)
        request = client.factory.create("AccountPerformanceReportRequest")
        self.assertIsNone(request.Format)
        self.assertIsNotNone(request.Aggregation)
        xml = ET.fromstring(client.SubmitGenerateReport(ReportRequest=request).envelope)
        self.assertIsNone(xml.find(".//{*}Format"))
        self.assertIsNotNone(xml.find(".//{*}Aggregation"))
        request.Format = "Csv"
        request.Aggregation = "Daily"
        xml = ET.fromstring(client.SubmitGenerateReport(ReportRequest=request).envelope)
        self.assertEqual("Csv", xml.find(".//{*}Format").text)
        self.assertEqual("Daily", xml.find(".//{*}Aggregation").text)
