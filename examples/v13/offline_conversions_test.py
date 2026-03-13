import uuid
from datetime import timezone
from auth_helper import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Create an offline conversion goal
        print("Creating offline conversion goal...")
        
        goal_name = f"TEST_OFFLINE_CONVERSION_GOAL{str(uuid.uuid4())[:8]}"
        print(f"Goal Name: {goal_name}")
        print("Note: A conversion goal cannot be deleted, so please choose an appropriate name.")
        
        offline_conversion_goal = OfflineConversionGoal(
            # Determines how long after a click that you want to count offline conversions.
            # 43200 minutes = 30 days
            conversion_window_in_minutes=43200,
            # If the count type is 'Unique' then only the first offline conversion will be counted.
            # By setting the count type to 'All', then all offline conversions for the same
            # MicrosoftClickId with different conversion times will be added cumulatively.
            count_type=ConversionGoalCountType.ALL,
            name=goal_name,
            # The default conversion currency code and value. Each offline conversion can override it.
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=5.00
            ),
            scope=EntityScope.ACCOUNT,
            status=ConversionGoalStatus.ACTIVE,
            goal_category=ConversionGoalCategory.PURCHASE
        )
        
        add_conversion_goals_request = AddConversionGoalsRequest(
            conversion_goals=[offline_conversion_goal]
        )
        
        add_conversion_goals_response = campaign_service.add_conversion_goals(
            add_conversion_goals_request=add_conversion_goals_request
        )
        
        conversion_goal_ids = add_conversion_goals_response.ConversionGoalIds
        print(f"Created Conversion Goal IDs: {conversion_goal_ids}")
        
        if add_conversion_goals_response.PartialErrors:
            print(f"Partial Errors: {add_conversion_goals_response.PartialErrors}")
        else:
            print("Offline conversion goal created successfully")
        
        # Get the offline conversion goal
        print("\nGetting offline conversion goal...")
        
        get_conversion_goals_request = GetConversionGoalsByIdsRequest(
            conversion_goal_ids=conversion_goal_ids,
            conversion_goal_types=ConversionGoalType.OFFLINECONVERSION
        )
        
        get_conversion_goals_response = campaign_service.get_conversion_goals_by_ids(
            get_conversion_goals_by_ids_request=get_conversion_goals_request
        )
        
        conversion_goals = get_conversion_goals_response.ConversionGoals
        print(f"Retrieved {len(conversion_goals)} conversion goals")
        
        for goal in conversion_goals:
            if goal:
                print(f"  Goal ID: {goal.Id}")
                print(f"  Goal Name: {goal.Name}")
                print(f"  Goal Status: {goal.Status}")
                print(f"  Conversion Window: {goal.ConversionWindowInMinutes} minutes")
        
        if get_conversion_goals_response.PartialErrors:
            print(f"Partial Errors: {get_conversion_goals_response.PartialErrors}")
        
        # Get account properties
        # Every time you create a new OfflineConversionGoal via either the Bing Ads web application 
        # or Campaign Management API, the MSCLKIDAutoTaggingEnabled value of the corresponding 
        # AccountProperty is set to 'true' automatically. We can confirm the setting now.
        print("\nGetting account properties...")
        
        get_account_properties_request = GetAccountPropertiesRequest(
            account_property_names=[AccountPropertyName.MSCLKIDAUTOTAGGINGENABLED]
        )
        
        get_account_properties_response = campaign_service.get_account_properties(
            get_account_properties_request=get_account_properties_request
        )
        
        account_properties = get_account_properties_response.AccountProperties
        print(f"Account Properties:")
        
        for prop in account_properties:
            if prop:
                print(f"  Name: {prop.Name}")
                print(f"  Value: {prop.Value}")
        
        if get_account_properties_response.PartialErrors:
            print(f"Partial Errors: {get_account_properties_response.PartialErrors}")
        
        # Apply offline conversions
        print("\nApplying offline conversions...")
        print("Note: This example demonstrates the API call, but it will likely fail because")
        print("you must wait at least 2 hours after creating the goal before applying conversions.")
        
        # Get current UTC time
        current_utc_time = datetime.now(timezone.utc)
        
        offline_conversion = OfflineConversion(
            # If you do not specify an offline conversion currency code,
            # then the 'CurrencyCode' element of the goal's 'ConversionGoalRevenue' is used.
            conversion_currency_code="USD",
            # The conversion name must match the 'Name' of the 'OfflineConversionGoal'.
            # If it does not match you won't observe any error, although the offline
            # conversion will not be counted.
            conversion_name=goal_name,
            # The date and time must be in UTC, should align to the date and time of the
            # recorded click (MicrosoftClickId), and cannot be in the future.
            conversion_time=current_utc_time,
            # If you do not specify an offline conversion value,
            # then the 'Value' element of the goal's 'ConversionGoalRevenue' is used.
            conversion_value=10.0,
            # Use a real Microsoft Click ID from your account
            microsoft_click_id="f894f652ea334e739002f7167ab8f8e3"
        )
        
        apply_offline_conversions_request = ApplyOfflineConversionsRequest(
            offline_conversions=[offline_conversion]
        )
        
        apply_offline_conversions_response = campaign_service.apply_offline_conversions(
            apply_offline_conversions_request=apply_offline_conversions_request
        )
        
        if apply_offline_conversions_response.PartialErrors:
            print(f"Partial Errors (expected): {apply_offline_conversions_response.PartialErrors}")
            print("This is expected because we just created the goal and need to wait 2 hours.")
        else:
            print("Offline conversions applied successfully")
        
        print("\n" + "="*80)
        print("Test completed successfully!")
        print(f"Note: The conversion goal '{goal_name}' (ID: {conversion_goal_ids[0]}) ")
        print("has been created and CANNOT be deleted. It will remain in your account.")
        print("="*80)
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("Loading the web service client...")
    print("\n" + "="*80)
    print("WARNING: This test creates an offline conversion goal that CANNOT be deleted!")
    print("Please ensure you want to proceed before running this test.")
    print("="*80 + "\n")
    
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