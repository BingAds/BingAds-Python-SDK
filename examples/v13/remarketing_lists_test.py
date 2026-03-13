import uuid
from auth_helper import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Check if UET tags already exist
        print("Checking for existing UET tags...")
        
        get_uet_tags_request = GetUetTagsByIdsRequest(
            tag_ids=None  # Get all UET tags
        )
        
        get_uet_tags_response = campaign_service.get_uet_tags_by_ids(
            get_uet_tags_by_ids_request=get_uet_tags_request
        )
        
        uet_tags = get_uet_tags_response.UetTags if get_uet_tags_response.UetTags else []
        
        print(f"Found {len(uet_tags)} existing UET tags")
        
        if get_uet_tags_response.PartialErrors:
            print(f"Partial Errors: {get_uet_tags_response.PartialErrors}")
        
        # Create a new UET tag if none exist
        if len(uet_tags) == 0:
            print("\nCreating new UET tag...")
            print("Before you can track conversions or target audiences using a remarketing list,")
            print("you need to create a UET tag, and then add the UET tag tracking code to every page of your website.")
            
            uet_tag = UetTag(
                name="New UET Tag" + str(uuid.uuid4())[:8],
                description="My First UET Tag" + str(uuid.uuid4())[:8]
            )
            
            add_uet_tags_request = AddUetTagsRequest(
                uet_tags=[uet_tag]
            )
            
            add_uet_tags_response = campaign_service.add_uet_tags(
                add_uet_tags_request=add_uet_tags_request
            )
            
            uet_tags = add_uet_tags_response.UetTags
            print(f"Created UET Tag ID: {uet_tags[0].Id}")
            
            if add_uet_tags_response.PartialErrors:
                print(f"Partial Errors: {add_uet_tags_response.PartialErrors}")
        else:
            print("Using existing UET tag")
        
        tag_id = uet_tags[0].Id
        print(f"\nUsing UET Tag ID: {tag_id}")
        
        # Create remarketing lists with different rule types
        print("\nCreating remarketing lists...")
        
        audiences = []
        
        # 1. Custom Events Rule
        custom_events_rule = CustomEventsRule(
            action="play",
            action_operator=StringOperator.EQUALS,
            category="video",
            category_operator=StringOperator.EQUALS,
            label="trailer",
            label_operator=StringOperator.EQUALS,
            value=5.0,
            value_operator=StringOperator.EQUALS
        )
        
        custom_events_list = RemarketingList(
            description="New list with CustomEventsRule",
            membership_duration=30,
            name="Remarketing List with CustomEventsRule " + str(uuid.uuid4())[:8],
            parent_id=authorization_data.account_id,
            scope=EntityScope.ACCOUNT,
            tag_id=tag_id,
            rule=custom_events_rule
        )
        audiences.append(custom_events_list)
        
        # 2. Page Visitors Rule
        page_visitors_rule = PageVisitorsRule(
            rule_item_groups=[
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.CONTAINS,
                            value="X"
                        ),
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.DOESNOTCONTAIN,
                            value="Z"
                        )
                    ]
                ),
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.DOESNOTBEGINWITH,
                            value="Y"
                        )
                    ]
                ),
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.EQUALS,
                            value="Z"
                        )
                    ]
                )
            ]
        )
        
        page_visitors_list = RemarketingList(
            description="New list with PageVisitorsRule",
            membership_duration=30,
            name="Remarketing List with PageVisitorsRule " + str(uuid.uuid4())[:8],
            parent_id=authorization_data.account_id,
            scope=EntityScope.ACCOUNT,
            tag_id=tag_id,
            rule=page_visitors_rule
        )
        audiences.append(page_visitors_list)
        
        # 3. Page Visitors Who Did Not Visit Another Page Rule
        page_visitors_who_did_not_visit_rule = PageVisitorsWhoDidNotVisitAnotherPageRule(
            include_rule_item_groups=[
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.CONTAINS,
                            value="X"
                        ),
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.DOESNOTCONTAIN,
                            value="Z"
                        )
                    ]
                ),
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.EQUALS,
                            value="Z"
                        )
                    ]
                )
            ],
            exclude_rule_item_groups=[
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.BEGINSWITH,
                            value="A"
                        ),
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.BEGINSWITH,
                            value="B"
                        )
                    ]
                ),
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.CONTAINS,
                            value="C"
                        )
                    ]
                )
            ]
        )
        
        page_visitors_who_did_not_visit_list = RemarketingList(
            description="New list with PageVisitorsWhoDidNotVisitAnotherPageRule",
            membership_duration=30,
            name="Remarketing List with PageVisitorsWhoDidNotVisitAnotherPageRule " + str(uuid.uuid4())[:8],
            parent_id=authorization_data.account_id,
            scope=EntityScope.ACCOUNT,
            tag_id=tag_id,
            rule=page_visitors_who_did_not_visit_rule
        )
        audiences.append(page_visitors_who_did_not_visit_list)
        
        # 4. Page Visitors Who Visited Another Page Rule
        page_visitors_who_visited_rule = PageVisitorsWhoVisitedAnotherPageRule(
            rule_item_groups=[
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.CONTAINS,
                            value="X"
                        ),
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.DOESNOTCONTAIN,
                            value="Z"
                        )
                    ]
                ),
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.EQUALS,
                            value="Z"
                        ),
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.DOESNOTBEGINWITH,
                            value="Y"
                        )
                    ]
                )
            ],
            another_rule_item_groups=[
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.BEGINSWITH,
                            value="A"
                        ),
                        StringRuleItem(
                            operand="ReferrerUrl",
                            operator=StringOperator.BEGINSWITH,
                            value="B"
                        )
                    ]
                ),
                RuleItemGroup(
                    items=[
                        StringRuleItem(
                            operand="Url",
                            operator=StringOperator.CONTAINS,
                            value="C"
                        )
                    ]
                )
            ]
        )
        
        page_visitors_who_visited_list = RemarketingList(
            description="New list with PageVisitorsWhoVisitedAnotherPageRule",
            membership_duration=30,
            name="Remarketing List with PageVisitorsWhoVisitedAnotherPageRule " + str(uuid.uuid4())[:8],
            parent_id=authorization_data.account_id,
            scope=EntityScope.ACCOUNT,
            tag_id=tag_id,
            rule=page_visitors_who_visited_rule
        )
        audiences.append(page_visitors_who_visited_list)
        
        # Add all remarketing lists
        add_audiences_request = AddAudiencesRequest(
            audiences=audiences
        )
        
        add_audiences_response = campaign_service.add_audiences(
            add_audiences_request=add_audiences_request
        )
        
        audience_ids = add_audiences_response.AudienceIds
        print(f"Created Audience IDs: {audience_ids}")
        
        if add_audiences_response.PartialErrors:
            print(f"Partial Errors: {add_audiences_response.PartialErrors}")
        else:
            print(f"Successfully created {len(audience_ids)} remarketing lists")
        
        # Create a campaign for remarketing
        print("\nCreating remarketing campaign...")
        
        campaign = Campaign(
            name="Remarketing Campaign " + str(uuid.uuid4())[:8],
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50.00,
            languages=['All'],
            time_zone='PacificTimeUSCanadaTijuana'
        )
        
        add_campaigns_request = AddCampaignsRequest(
            account_id=authorization_data.account_id,
            campaigns=[campaign]
        )
        
        add_campaigns_response = campaign_service.add_campaigns(
            add_campaigns_request=add_campaigns_request
        )
        
        campaign_ids = add_campaigns_response.CampaignIds
        print(f"Created Campaign ID: {campaign_ids[0]}")
        
        # Create an ad group with audience targeting
        print("\nCreating ad group with audience targeting...")
        
        current_year = datetime.now().year
        
        target_setting = TargetSetting(
            details=[
                TargetSettingDetail(
                    criterion_type_group=CriterionTypeGroup.AUDIENCE,
                    target_and_bid=True
                )
            ]
        )
        
        ad_group = AdGroup(
            name="Remarketing Ad Group" + str(uuid.uuid4())[:8],
            cpc_bid=Bid(amount=0.09),
            start_date=None,
            end_date=ModelDate(day=31, month=12, year=current_year),
            settings=[target_setting]
        )
        
        add_ad_groups_request = AddAdGroupsRequest(
            campaign_id=campaign_ids[0],
            ad_groups=[ad_group]
        )
        
        add_ad_groups_response = campaign_service.add_ad_groups(
            add_ad_groups_request=add_ad_groups_request
        )
        
        ad_group_ids = add_ad_groups_response.AdGroupIds
        print(f"Created Ad Group ID: {ad_group_ids[0]}")
        
        # Associate remarketing lists with ad group
        print("\nAssociating remarketing lists with ad group...")
        
        ad_group_criterions = []
        
        for audience_id in audience_ids:
            criterion = AudienceCriterion(
                audience_id=audience_id,
                audience_type=AudienceType.REMARKETINGLIST
            )
            
            ad_group_criterion = BiddableAdGroupCriterion(
                ad_group_id=ad_group_ids[0],
                criterion=criterion,
                criterion_bid=BidMultiplier(multiplier=20.0),
                status=AdGroupCriterionStatus.ACTIVE
            )
            
            ad_group_criterions.append(ad_group_criterion)
        
        add_ad_group_criterions_request = AddAdGroupCriterionsRequest(
            ad_group_criterions=ad_group_criterions,
            criterion_type=AdGroupCriterionType.AUDIENCE
        )
        
        add_ad_group_criterions_response = campaign_service.add_ad_group_criterions(
            add_ad_group_criterions_request=add_ad_group_criterions_request
        )
        
        criterion_ids = add_ad_group_criterions_response.AdGroupCriterionIds
        print(f"Created Ad Group Criterion IDs: {criterion_ids}")
        
        if add_ad_group_criterions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_ad_group_criterions_response.NestedPartialErrors}")
        else:
            print("Successfully associated remarketing lists with ad group")
        
        # Delete campaign
        print("\nDeleting campaign...")
        
        delete_campaigns_request = DeleteCampaignsRequest(
            account_id=authorization_data.account_id,
            campaign_ids=campaign_ids
        )
        
        campaign_service.delete_campaigns(
            delete_campaigns_request=delete_campaigns_request
        )
        
        print(f"Deleted Campaign ID {campaign_ids[0]}")
        
        print("\n" + "="*80)
        print("Test completed successfully!")
        print(f"Note: The remarketing lists and UET tag remain in your account and can be reused.")
        print("="*80)
        
    except Exception as ex:
        print(f"Error occurred: {str(ex)}")
        import traceback
        traceback.print_exc()

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