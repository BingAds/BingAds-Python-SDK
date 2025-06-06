import base64
import uuid

from auth_helper_rest import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        detail = TargetSettingDetail(
            criterion_type_group="Audience",
            target_and_bid=False
        )
        target_setting = TargetSetting(details=[detail])
        bidding_scheme = ManualCpcBiddingScheme()
        param1 = CustomParameter(
            key='season',
            value='christmas'
        )
        param2 = CustomParameter(
            key='promocode',
            value='NYC123'
        )
        campaign = Campaign(
            id=None,
            Name='testCampaign' + str(uuid.uuid4()),
            status='Active',
            daily_budget=20.0,
            budget_type=BudgetLimitType.DAILYBUDGETACCELERATED,
            time_zone=None,
            settings=[
                Setting(target_setting)
            ],
            campaign_type=CampaignType.SEARCH,
            audience_ads_bid_adjustment=10,
            tracking_url_template='',
            final_url_suffix='',
            url_custom_parameters=CustomParameters(
                parameters=[param1, param2
                            ], ),
            bidding_scheme=BiddingScheme(bidding_scheme),
            languages=[
                'All'
            ], )
        campaign.DailyBudget = 10.0
        add_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=[campaign],
        )

        create_response = campaign_service.add_campaigns(
            add_campaigns_request=add_request
        )
        assert(len(create_response.campaign_ids) > 0)
        campaign_id = create_response.campaign_ids[0]

        if hasattr(create_response, 'partial_errors') and create_response.partial_errors:
            print(f"Partial errors in create response: {create_response.partial_errors}")

        # 2. Get the created Campaign
        get_request = GetCampaignsByIdsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=[campaign_id],
            campaign_type=CampaignType.SEARCH | CampaignType.AUDIENCE
        )

        get_response = campaign_service.get_campaigns_by_ids(
            get_campaigns_by_ids_request=get_request
        )

        if hasattr(get_response, 'partial_errors') and get_response.partial_errors:
            print(f"Partial errors in get response: {get_response.partial_errors}")

        assert(len(get_response.campaigns) == 1)
        retrieved_campaign = get_response.campaigns[0]
        assert(campaign.name == retrieved_campaign.name)

        # 3. Update the Campaign
        update_campaign = Campaign(name='MyTestCampaign',
                                   daily_budget=10.0,
                                   id=campaign_id)
        update_request = UpdateCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=[update_campaign]
        )

        update_response = campaign_service.update_campaigns(
            update_campaigns_request=update_request
        )

        if hasattr(update_response, 'partial_errors') and update_response.partial_errors:
            print(f"Partial errors in get response: {update_response.partial_errors}")

        # 4. Get the updated Campaign
        get_response = campaign_service.get_campaigns_by_ids(
            get_campaigns_by_ids_request=get_request
        )

        assert('MyTestCampaign' == get_response.campaigns[0].name)
        assert(10.0 == get_response.campaigns[0].daily_budget)

        # 5. Delete the Campaign
        delete_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=[campaign_id]
        )

        delete_response = campaign_service.delete_campaigns(
            delete_campaigns_request=delete_request
        )
        if hasattr(delete_response, 'partial_errors') and delete_response.partial_errors:
            print(f"Partial errors in delete response: {delete_response.partial_errors}")

        get_response = campaign_service.get_campaigns_by_ids(
            get_campaigns_by_ids_request=get_request
        )
        assert (1 == len(get_response.partial_errors))

    except Exception as ex:
        print(f"Error occurred: {str(ex)}")


if __name__ == '__main__':
    print("Loading the web service client...")

    authorization_data = AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    authenticate(authorization_data)

    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)
