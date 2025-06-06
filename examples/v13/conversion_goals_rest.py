import uuid
from time import strftime, gmtime
import sys

from auth_helper_rest import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Before you can track conversions or target audiences using a remarketing list 
        # you need to create a UET tag, and then add the UET tag tracking code to every page of your website.
        
        # First check whether a tag has already been created
        get_uet_tags_by_ids_request = GetUetTagsByIdsRequest(
            tag_ids=None  # None to get all UET tags
        )
        
        get_uet_tags_response = campaign_service.get_uet_tags_by_ids(
            get_uet_tags_by_ids_request=get_uet_tags_by_ids_request
        )
        uet_tags = get_uet_tags_response.UetTags

        # Create a new UET tag if none exists
        if not uet_tags:
            uet_tag = UetTag(
                description="My First Uet Tag",
                name="New Uet Tag"
            )
            
            add_uet_tags_request = AddUetTagsRequest(
                uet_tags=[uet_tag]
            )
            
            add_uet_tags_response = campaign_service.add_uet_tags(
                add_uet_tags_request=add_uet_tags_request
            )
            uet_tags = add_uet_tags_response.UetTags

        if not uet_tags:
            print(f"You do not have any UET tags registered for CustomerId {authorization_data.customer_id}")
            sys.exit(0)
        
        # Use the first UET tag for conversion goals
        tag_id = uet_tags[0].Id

        # Create conversion goals
        conversion_goals = []

        # Duration Goal
        duration_goal = DurationGoal(
            conversion_window_in_minutes=30,
            count_type=ConversionGoalCountType.ALL,
            minimum_duration_in_seconds=60,
            name="My Duration Goal" + str(uuid.uuid4()),
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=5.00
            ),
            scope=EntityScope.ACCOUNT,
            status=ConversionGoalStatus.ACTIVE,
            tag_id=tag_id
        )
        conversion_goals.append(ConversionGoal(duration_goal))

        # Event Goal
        event_goal = EventGoal(
            goal_category=ConversionGoalCategory.PURCHASE,
            action_expression="play",
            action_operator=ExpressionOperator.CONTAINS,
            category_expression="video",
            category_operator=ExpressionOperator.CONTAINS,
            conversion_window_in_minutes=30,
            count_type=ConversionGoalCountType.ALL,
            label_expression="trailer",
            label_operator=ExpressionOperator.CONTAINS,
            name="My Event Goal" + str(uuid.uuid4()),
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=5.00
            ),
            scope=EntityScope.ACCOUNT,
            status=ConversionGoalStatus.ACTIVE,
            tag_id=tag_id,
            value=5.00,
            value_operator=ValueOperator.EQUALS
        )
        conversion_goals.append(ConversionGoal(event_goal))

        # Pages Viewed Per Visit Goal
        pages_viewed_goal = PagesViewedPerVisitGoal(
            conversion_window_in_minutes=30,
            count_type=ConversionGoalCountType.ALL,
            minimum_pages_viewed=5,
            name="My Pages Viewed Per Visit Goal" + str(uuid.uuid4()),
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=5.00
            ),
            scope=EntityScope.ACCOUNT,
            status=ConversionGoalStatus.ACTIVE,
            tag_id=tag_id
        )
        conversion_goals.append(ConversionGoal(pages_viewed_goal))

        # URL Goal
        url_goal = UrlGoal(
            goal_category=ConversionGoalCategory.PURCHASE,
            conversion_window_in_minutes=30,
            count_type=ConversionGoalCountType.ALL,
            name="My Url Goal" + str(uuid.uuid4()),
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=5.00
            ),
            scope=EntityScope.ACCOUNT,
            status=ConversionGoalStatus.ACTIVE,
            tag_id=tag_id,
            url_expression="contoso",
            url_operator=ExpressionOperator.CONTAINS
        )
        conversion_goals.append(ConversionGoal(url_goal))

        # App Install Goal
        app_install_goal = AppInstallGoal(
            app_platform="Windows",
            app_store_id="AppStoreIdGoesHere",
            conversion_window_in_minutes=30,
            count_type=ConversionGoalCountType.ALL,
            name="My App Install Goal" + str(uuid.uuid4()),
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=5.00
            ),
            scope=EntityScope.CUSTOMER,  # Account scope not supported for app install goals
            status=ConversionGoalStatus.ACTIVE,
            tag_id=None  # App Install goals do not use UET tag
        )
        conversion_goals.append(ConversionGoal(app_install_goal))

        # Add the conversion goals
        add_conversion_goals_request = AddConversionGoalsRequest(
            conversion_goals=conversion_goals
        )
        
        add_conversion_goals_response = campaign_service.add_conversion_goals(
            add_conversion_goals_request=add_conversion_goals_request
        )
        goal_ids = add_conversion_goals_response.ConversionGoalIds

        # Get the successful conversion goal IDs
        conversion_goal_ids = [goal_id for goal_id in goal_ids if goal_id is not None]
        
        # Get the created conversion goals
        conversion_goal_types = ConversionGoalType.APPINSTALL | ConversionGoalType.DURATION |  ConversionGoalType.EVENT | ConversionGoalType.PAGESVIEWEDPERVISIT | ConversionGoalType.URL
        
        get_goals_request = GetConversionGoalsByIdsRequest(
            conversion_goal_ids=conversion_goal_ids,
            conversion_goal_types=conversion_goal_types,
            return_additional_fields=ConversionGoalAdditionalField.VIEWTHROUGHCONVERSIONWINDOWINMINUTES
        )
        
        get_goals_response = campaign_service.get_conversion_goals_by_ids(
            get_conversion_goals_by_ids_request=get_goals_request
        )

        # Update conversion goals
        update_conversion_goals = []

        # Update Duration Goal (previously Event Goal)
        update_duration_goal = DurationGoal(
            conversion_window_in_minutes=60,
            count_type=ConversionGoalCountType.UNIQUE,
            id=conversion_goal_ids[1],  # Using Event Goal's ID to change type
            minimum_duration_in_seconds=120,
            name="My Updated Duration Goal",
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.FIXEDVALUE,
                value=10.00
            ),
            scope=EntityScope.ACCOUNT,
            status=ConversionGoalStatus.PAUSED,
            tag_id=tag_id
        )
        update_conversion_goals.append(ConversionGoal(update_duration_goal))

        # Update Event Goal
        update_event_goal = EventGoal(
            category_expression="video",
            category_operator=ExpressionOperator.EQUALS,
            id=conversion_goal_ids[0],
            name="My Updated Event Goal",
            revenue=ConversionGoalRevenue(
                type=ConversionGoalRevenueType.VARIABLEVALUE,
                value=5.00
            ),
            value=5.00,
            value_operator=ValueOperator.GREATERTHAN
        )
        update_conversion_goals.append(ConversionGoal(update_event_goal))

        # Update Pages Viewed Per Visit Goal
        update_pages_viewed_goal = PagesViewedPerVisitGoal(
            id=conversion_goal_ids[2],
            name="My Updated Pages Viewed Per Visit Goal"
        )
        update_conversion_goals.append(ConversionGoal(update_pages_viewed_goal))

        # Update URL Goal
        update_url_goal = UrlGoal(
            id=conversion_goal_ids[3],
            name="My Updated Url Goal",
            url_expression="Contoso",
            url_operator=ExpressionOperator.BEGINSWITH
        )
        update_conversion_goals.append(ConversionGoal(update_url_goal))

        # Update the conversion goals
        update_goals_request = UpdateConversionGoalsRequest(
            conversion_goals=update_conversion_goals
        )
        
        campaign_service.update_conversion_goals(
            update_conversion_goals_request=update_goals_request
        )

        # Get updated goals
        get_updated_goals_response = campaign_service.get_conversion_goals_by_ids(
            get_conversion_goals_by_ids_request=get_goals_request
        )

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