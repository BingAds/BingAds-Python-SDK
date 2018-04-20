from datetime import datetime, timedelta

from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        offline_conversion_goal_name = "My Offline Conversion Goal " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        conversion_goals=campaign_service.factory.create('ArrayOfConversionGoal')

        offline_conversion_goal=set_elements_to_none(campaign_service.factory.create('OfflineConversionGoal'))
        # Determines how long after a click that you want to count offline conversions. 
        offline_conversion_goal.ConversionWindowInMinutes = 43200
        # If the count type is 'Unique' then only the first offline conversion will be counted.
        # By setting the count type to 'All', then all offline conversions for the same
        # MicrosoftClickId with different conversion times will be added cumulatively. 
        offline_conversion_goal.CountType = 'All'
        offline_conversion_goal.Name = offline_conversion_goal_name
        # The default conversion currency code and value. Each offline conversion can override it.
        offline_conversion_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        offline_conversion_goal_revenue.CurrencyCode=None
        offline_conversion_goal_revenue.Type='FixedValue'
        offline_conversion_goal_revenue.Value=5.00
        offline_conversion_goal.Revenue = offline_conversion_goal_revenue
        offline_conversion_goal.Scope = 'Account'
        offline_conversion_goal.Status = 'Active'
        # The TagId is inherited from the ConversionGoal base class,
        # however, Offline Conversion goals do not use a UET tag.
        offline_conversion_goal.TagId = None
        conversion_goals.ConversionGoal.append(offline_conversion_goal)

        add_conversion_goals_response=campaign_service.AddConversionGoals(ConversionGoals=conversion_goals)
        
        # Find the conversion goals that were added successfully. 

        conversion_goal_ids = []
        for goal_id in add_conversion_goals_response.ConversionGoalIds['long']:
            if goal_id is not None:
                conversion_goal_ids.append(goal_id)

        output_status_message("List of errors returned from AddConversionGoals (if any):\n")
        output_array_of_batcherror(add_conversion_goals_response.PartialErrors)
        
        conversion_goal_types='OfflineConversion'
        
        get_conversion_goals_by_ids_response = campaign_service.GetConversionGoalsByIds(
            ConversionGoalIds={'long': conversion_goal_ids}, 
            ConversionGoalTypes=conversion_goal_types
        )

        output_status_message("List of conversion goals:\n")
        output_array_of_conversiongoal(get_conversion_goals_by_ids_response.ConversionGoals)
        
        # Every time you create a new OfflineConversionGoal via either the Bing Ads web application or Campaign Management API, 
        # the MSCLKIDAutoTaggingEnabled value of the corresponding AccountProperty is set to 'true' automatically.
        # We can confirm the setting now.

        account_property_names=campaign_service.factory.create('ArrayOfAccountPropertyName')
        account_property_names.AccountPropertyName.append([
            'MSCLKIDAutoTaggingEnabled'
        ])

        output_status_message("Get account properties...\n")
        get_account_properties_response = campaign_service.GetAccountProperties(AccountPropertyNames=account_property_names)
        output_array_of_accountproperty(get_account_properties_response.AccountProperties)

        offline_conversions=campaign_service.factory.create('ArrayOfOfflineConversion')

        offline_conversion=set_elements_to_none(campaign_service.factory.create('OfflineConversion'))
        # If you do not specify an offline conversion currency code, 
        # then the 'CurrencyCode' element of the goal's 'ConversionGoalRevenue' is used.
        offline_conversion.ConversionCurrencyCode = "USD"
        # The conversion name must match the 'Name' of the 'OfflineConversionGoal'.
        # If it does not match you won't observe any error, although the offline
        # conversion will not be counted.
        offline_conversion.ConversionName = offline_conversion_goal_name
        # The date and time must be in UTC, should align to the date and time of the 
        # recorded click (MicrosoftClickId), and cannot be in the future.
        offline_conversion.ConversionTime = datetime.utcnow()
        # If you do not specify an offline conversion value, 
        # then the 'Value' element of the goal's 'ConversionGoalRevenue' is used.
        offline_conversion.ConversionValue = 10
        offline_conversion.MicrosoftClickId = "f894f652ea334e739002f7167ab8f8e3"
        offline_conversions.OfflineConversion.append(offline_conversion)

        # After the OfflineConversionGoal is set up, wait two hours before sending Bing Ads the offline conversions. 
        # This example would not succeed in production because we created the goal very recently i.e., 
        # please see above call to AddConversionGoals. 

        output_status_message("Apply the offline conversion...\n")
        apply_offline_conversions_response = campaign_service.ApplyOfflineConversions(OfflineConversions=offline_conversions)
        output_array_of_offlineconversion(offline_conversions)

        output_status_message("List of errors returned from ApplyOfflineConversions (if any):\n")
        output_array_of_batcherror(apply_offline_conversions_response)

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

# Main execution
if __name__ == '__main__':

    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=11,
    )

    print(campaign_service.soap_client)

    # You should authenticate for Bing Ads production services with a Microsoft Account, 
    # instead of providing the Bing Ads username and password set. 
            
    authenticate(authorization_data)
        
    main(authorization_data)
