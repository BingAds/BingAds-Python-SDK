from openapi_client.api_client import ApiClient
from openapi_client.models.campaign.add_audiences_request import AddAudiencesRequest
from openapi_client.models.campaign.add_campaigns_response import AddCampaignsResponse
from openapi_client.models.campaign.audience import Audience
from openapi_client.models.campaign.ai_prompt_audience import AIPromptAudience
from openapi_client.models.campaign.bidding_scheme import BiddingScheme
from openapi_client.models.campaign.campaign import Campaign
from openapi_client.models.campaign.target_cpm_bidding_scheme import TargetCpmBiddingScheme


def test_nullable_campaign_ids_accept_null_items():
    response = AddCampaignsResponse(CampaignIds=["123", None])
    assert response.to_dict()["CampaignIds"] == ["123", None]


def test_ai_prompt_audience_dispatch_and_request_serialization():
    audience = Audience.from_dict({"Type": "AIPrompt", "Prompt": "example"})
    assert isinstance(audience, AIPromptAudience)
    request = AddAudiencesRequest(Audiences=[audience])
    serialized = ApiClient().sanitize_for_serialization(request)
    assert serialized["Audiences"][0]["Type"] == "AIPrompt"
    assert serialized["Audiences"][0]["Prompt"] == "example"


def test_target_cpm_bidding_scheme_dispatch():
    scheme = BiddingScheme.from_dict({"Type": "TargetCpm"})
    assert isinstance(scheme, TargetCpmBiddingScheme)
    campaign = Campaign(BiddingScheme=scheme)
    assert campaign.bidding_scheme is scheme
    serialized = ApiClient().sanitize_for_serialization(campaign)
    assert serialized["BiddingScheme"]["Type"] == "TargetCpm"
