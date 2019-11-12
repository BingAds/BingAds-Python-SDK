from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Before you can track conversions or target audiences using a remarketing list 
        # you need to create a UET tag, and then add the UET tag tracking code to every page of your website.
        # For more information, please see Universal Event Tracking at https://go.microsoft.com/fwlink/?linkid=829965.

        # First you should call the GetUetTagsByIds operation to check whether a tag has already been created. 
        # You can leave the TagIds element null or empty to request all UET tags available for the customer.

        output_status_message("-----\nGetUetTagsByIds:")
        get_uet_tags_by_ids_response=campaign_service.GetUetTagsByIds(
            TagIds=None)
        uet_tags=get_uet_tags_by_ids_response.UetTags
        output_status_message("UetTags:")
        output_array_of_uettag(uet_tags)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(get_uet_tags_by_ids_response.PartialErrors)

        # If you do not already have a UET tag that can be used, or if you need another UET tag, 
        # call the AddUetTags service operation to create a new UET tag. If the call is successful, 
        # the tracking script that you should add to your website is included in a corresponding 
        # UetTag within the response message. 

        if uet_tags is None or len(uet_tags) < 1:
            uet_tags=campaign_service.factory.create('ArrayOfUetTag')
            uet_tag=set_elements_to_none(campaign_service.factory.create('UetTag'))
            uet_tag.Description="My First Uet Tag"
            uet_tag.Name="New Uet Tag"
            uet_tags.UetTag.append(uet_tag)
            
            add_uet_tags_response=campaign_service.AddUetTags(
                UetTags=uet_tags)
            uet_tags=add_uet_tags_response.UetTags
            output_status_message("UetTags:")
            output_array_of_uettag(uet_tags)
            output_status_message("PartialErrors:")
            output_array_of_batcherror(add_uet_tags_response.PartialErrors)

        if uet_tags is None or len(uet_tags) < 1:
            output_status_message(
                "You do not have any UET tags registered for CustomerId {0}.".format(authorization_data.customer_id)
            )
            sys.exit(0)
        
        # After you retreive the tracking script from the AddUetTags or GetUetTagsByIds operation, 
        # the next step is to add the UET tag tracking code to your website. 
        # We will use the same UET tag for the remainder of this example.

        tag_id = uet_tags['UetTag'][0].Id

        # Add conversion goals that depend on the UET Tag Id retreived above.
        # Please note that you cannot delete conversion goals. If you want to stop 
        # tracking conversions for the goal, you can set the goal status to Paused.

        conversion_goals=campaign_service.factory.create('ArrayOfConversionGoal')

        duration_goal=set_elements_to_none(campaign_service.factory.create('DurationGoal'))
        duration_goal.ConversionWindowInMinutes = 30
        duration_goal.CountType = 'All'
        duration_goal.MinimumDurationInSeconds = 60
        duration_goal.Name = "My Duration Goal"
        duration_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        duration_goal_revenue.Type='FixedValue'
        duration_goal_revenue.Value=5.00
        duration_goal_revenue.CurrencyCode=None
        duration_goal.Revenue = duration_goal_revenue
        duration_goal.Scope = 'Account'
        duration_goal.Status = 'Active'
        duration_goal.TagId = tag_id
        conversion_goals.ConversionGoal.append(duration_goal)

        event_goal=set_elements_to_none(campaign_service.factory.create('EventGoal'))
        # The type of user interaction you want to track.
        event_goal.ActionExpression = "play"
        event_goal.ActionOperator = 'Contains'
        # The category of event you want to track. 
        event_goal.CategoryExpression = "video"
        event_goal.CategoryOperator = 'Contains'
        event_goal.ConversionWindowInMinutes = 30
        event_goal.CountType = 'All'
        # The name of the element that caused the action.
        event_goal.LabelExpression = "trailer"
        event_goal.LabelOperator = 'Contains'
        event_goal.Name = "My Event Goal"
        event_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        event_goal_revenue.Type='FixedValue'
        event_goal_revenue.Value=5.00
        event_goal_revenue.CurrencyCode=None
        event_goal.Revenue = event_goal_revenue
        event_goal.Scope = 'Account'
        event_goal.Status = 'Active'
        event_goal.TagId = tag_id
        # A numerical value associated with that event. 
        # Could be length of the video played etc.
        event_goal.Value = 5.00
        event_goal.ValueOperator = 'Equals'
        conversion_goals.ConversionGoal.append(event_goal)

        pages_viewed_per_visit_goal=set_elements_to_none(campaign_service.factory.create('PagesViewedPerVisitGoal'))
        pages_viewed_per_visit_goal.ConversionWindowInMinutes = 30
        pages_viewed_per_visit_goal.CountType = 'All'
        pages_viewed_per_visit_goal.MinimumPagesViewed = 5
        pages_viewed_per_visit_goal.Name = "My Pages Viewed Per Visit Goal"
        pages_viewed_per_visit_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        pages_viewed_per_visit_goal_revenue.Type='FixedValue'
        pages_viewed_per_visit_goal_revenue.Value=5.00
        pages_viewed_per_visit_goal_revenue.CurrencyCode=None
        pages_viewed_per_visit_goal.Revenue = pages_viewed_per_visit_goal_revenue
        pages_viewed_per_visit_goal.Scope = 'Account'
        pages_viewed_per_visit_goal.Status = 'Active'
        pages_viewed_per_visit_goal.TagId = tag_id
        conversion_goals.ConversionGoal.append(pages_viewed_per_visit_goal)
            
        url_goal=set_elements_to_none(campaign_service.factory.create('UrlGoal'))
        url_goal.ConversionWindowInMinutes = 30
        url_goal.CountType = 'All'
        url_goal.Name = "My Url Goal"
        url_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        url_goal_revenue.Type='FixedValue'
        url_goal_revenue.Value=5.00
        url_goal_revenue.CurrencyCode=None
        url_goal.Revenue = url_goal_revenue
        url_goal.Scope = 'Account'
        url_goal.Status = 'Active'
        url_goal.TagId = tag_id
        url_goal.UrlExpression = "contoso"
        url_goal.UrlOperator = 'Contains'
        conversion_goals.ConversionGoal.append(url_goal)

        app_install_goal=set_elements_to_none(campaign_service.factory.create('AppInstallGoal'))
        # You must provide a valid app platform and app store identifier, 
        # otherwise this goal will not be added successfully. 
        app_install_goal.AppPlatform = "Windows"
        app_install_goal.AppStoreId = "AppStoreIdGoesHere"
        app_install_goal.ConversionWindowInMinutes = 30
        app_install_goal.CountType = 'All'
        app_install_goal.Name = "My App Install Goal"
        app_install_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        app_install_goal_revenue.Type='FixedValue'
        app_install_goal_revenue.Value=5.00
        app_install_goal_revenue.CurrencyCode=None
        app_install_goal.Revenue = app_install_goal_revenue
        # Account scope is not supported for app install goals. You can
        # set scope to Customer or don't set it for the same result.
        app_install_goal.Scope = 'Customer'
        app_install_goal.Status = 'Active'
        # The TagId is inherited from the ConversionGoal base class,
        # however, App Install goals do not use a UET tag.
        app_install_goal.TagId = None
        conversion_goals.ConversionGoal.append(app_install_goal)

        output_status_message("-----\nAddConversionGoals:")
        add_conversion_goals_response=campaign_service.AddConversionGoals(
            ConversionGoals=conversion_goals)
        goal_ids={
            'long': add_conversion_goals_response.ConversionGoalIds['long'] if add_conversion_goals_response.ConversionGoalIds['long'] else None
        }
        output_status_message("ConversionGoalIds:")
        output_array_of_long(goal_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_conversion_goals_response.PartialErrors)
        
        # Find the conversion goals that were added successfully. 
        
        conversion_goal_ids = []
        for goal_id in goal_ids['long']:
            if goal_id is not None:
                conversion_goal_ids.append(goal_id)
        
        conversion_goal_types='AppInstall ' \
                              'Duration ' \
                              'Event ' \
                              'PagesViewedPerVisit ' \
                              'Url'
        
        return_additional_fields = 'ViewThroughConversionWindowInMinutes'

        output_status_message("-----\nGetConversionGoalsByIds:")
        get_conversion_goals_response = campaign_service.GetConversionGoalsByIds(
            ConversionGoalIds={'long': conversion_goal_ids}, 
            ConversionGoalTypes=conversion_goal_types,
            ReturnAdditionalFields=return_additional_fields
        )
        output_status_message("ConversionGoals:")
        output_array_of_conversiongoal(get_conversion_goals_response.ConversionGoals)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(get_conversion_goals_response.PartialErrors)
        
        update_conversion_goals=campaign_service.factory.create('ArrayOfConversionGoal')

        update_duration_goal=set_elements_to_none(campaign_service.factory.create('DurationGoal'))
        update_duration_goal.ConversionWindowInMinutes = 60
        update_duration_goal.CountType = 'Unique'
        # You can change the conversion goal type e.g. in this example an event goal
        # had been created above at index 1. Now we are using the returned identifier
        # at index 1 to update the type from EventGoal to DurationGoal.
        update_duration_goal.Id=conversion_goal_ids[1]
        update_duration_goal.MinimumDurationInSeconds = 120
        update_duration_goal.Name = "My Updated Duration Goal"
        update_duration_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        update_duration_goal_revenue.Type='FixedValue'
        update_duration_goal_revenue.Value=10.00
        update_duration_goal_revenue.CurrencyCode=None
        update_duration_goal.Revenue = update_duration_goal_revenue
        # The Scope cannot be updated, even if you update the goal type.
        # You can either send the same value or leave Scope empty.
        update_duration_goal.Scope = 'Account'
        update_duration_goal.Status = 'Paused'
        # You can update the tag as needed. In this example we will explicitly use the same UET tag.
        # To keep the UET tag unchanged, you can also leave this element nil or empty.
        update_duration_goal.TagId = tag_id
        update_conversion_goals.ConversionGoal.append(update_duration_goal)

        update_event_goal=set_elements_to_none(campaign_service.factory.create('EventGoal'))
        # For both add and update conversion goal operations, you must include one or more  
        # of the following events:
        # ActionExpression, CategoryExpression, LabelExpression, or Value. 
        
        # For example if you do not include ActionExpression during update,
        # any existing ActionOperator and ActionExpression settings will be deleted.
        update_event_goal.ActionExpression = None
        update_event_goal.ActionOperator = None
        update_event_goal.CategoryExpression = "video"
        update_event_goal.CategoryOperator = 'Equals'
        update_event_goal.Id = conversion_goal_ids[0]
        # You cannot update the operator unless you also include the expression.
        # The following attempt to update LabelOperator will result in an error.
        update_event_goal.LabelExpression = None
        update_event_goal.LabelOperator = 'Equals'
        update_event_goal.Name = "My Updated Event Goal"
        update_event_goal_revenue=set_elements_to_none(campaign_service.factory.create('ConversionGoalRevenue'))
        update_event_goal_revenue.Type='VariableValue'
        update_event_goal_revenue.Value=5.00
        update_event_goal_revenue.CurrencyCode=None
        update_event_goal.Revenue = update_event_goal_revenue
        # You must specify the previous settings unless you want
        # them replaced during the update conversion goal operation.
        update_event_goal.Value=5.00
        update_event_goal.ValueOperator = 'GreaterThan'
        update_conversion_goals.ConversionGoal.append(update_event_goal)

        update_pages_viewed_per_visit_goal=set_elements_to_none(campaign_service.factory.create('PagesViewedPerVisitGoal'))
        update_pages_viewed_per_visit_goal.Id = conversion_goal_ids[2]
        update_pages_viewed_per_visit_goal.Name = "My Updated Pages Viewed Per Visit Goal"
        update_conversion_goals.ConversionGoal.append(update_pages_viewed_per_visit_goal)
            
        update_url_goal=set_elements_to_none(campaign_service.factory.create('UrlGoal'))
        update_url_goal.Id = conversion_goal_ids[3]
        update_url_goal.Name = "My Updated Url Goal"
        # If not specified during update, the previous Url settings are retained.
        # If the expression is set, then the operator must also be set, and vice versa.
        update_url_goal.UrlExpression = 'Contoso'
        update_url_goal.UrlOperator = 'BeginsWith'
        update_conversion_goals.ConversionGoal.append(update_url_goal)

        output_status_message("-----\nUpdateConversionGoals:")
        update_conversion_goals_response = campaign_service.UpdateConversionGoals(
            ConversionGoals=update_conversion_goals)
        if hasattr(update_conversion_goals_response, 'BatchError'):
            output_status_message("PartialErrors:")
            output_array_of_batcherror(update_conversion_goals_response)
                
        output_status_message("-----\nGetConversionGoalsByIds:")
        get_conversion_goals_response = campaign_service.GetConversionGoalsByIds(
            ConversionGoalIds={'long': conversion_goal_ids}, 
            ConversionGoalTypes=conversion_goal_types,
            ReturnAdditionalFields=return_additional_fields)
        output_status_message("ConversionGoals:")
        output_array_of_conversiongoal(get_conversion_goals_response.ConversionGoals)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(get_conversion_goals_response.PartialErrors)

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

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
        
    authenticate(authorization_data)
        
    main(authorization_data)
