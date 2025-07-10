import base64
import timeit

from auth_helper import *
from campaignmanagement_example_helper import *
def main(authorization_data):

    try:

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        campaign.Name="Perf test campaign " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaigns.Campaign.append(campaign)

        output_status_message("-----\nAddCampaigns:")
        add_campaigns_response=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )
        campaign_ids={
            'long': add_campaigns_response.CampaignIds['long'] if add_campaigns_response.CampaignIds['long'] else None
        }
        output_status_message("CampaignIds:")
        output_array_of_long(campaign_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_campaigns_response.PartialErrors)

        ad_groups = campaign_service.factory.create('ArrayOfAdGroup')
        for i in range(100):
            ad_group = set_elements_to_none(campaign_service.factory.create('AdGroup'))
            ad_group.Name = "Perf test ad group" + str(i)
            ad_group.Language = "English"
            ad_groups.AdGroup.append(ad_group)

        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups
        )
        execution_time = timeit.timeit(get_method(campaign_ids), number=20)
        print(f"execution time: {execution_time} seconds.")

        output_status_message("-----\nDeleteCampaigns:")
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted Campaign Id {0}".format(campaign_ids['long'][0]))

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def get_method(campaign_ids):
    def _get():
        get_response = campaign_service.GetAdGroupsByCampaignId(
            CampaignId=campaign_ids['long'][0]
        )
        print("get ad groups")
    return _get

# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")

    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    customer_service=ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    authenticate(authorization_data)

    main(authorization_data)
