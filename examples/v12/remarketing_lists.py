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
        uet_tags=campaign_service.GetUetTagsByIds(
            TagIds=None
        ).UetTags

        # If you do not already have a UET tag that can be used, or if you need another UET tag, 
        # call the AddUetTags service operation to create a new UET tag. If the call is successful, 
        # the tracking script that you should add to your website is included in a corresponding 
        # UetTag within the response message. 

        if (uet_tags is None or len(uet_tags) < 1):
            uet_tags=campaign_service.factory.create('ArrayOfUetTag')
            uet_tag=set_elements_to_none(campaign_service.factory.create('UetTag'))
            uet_tag.Description = "My First Uet Tag"
            uet_tag.Name = "New Uet Tag"
            output_status_message("-----\nAddUetTags:")
            uet_tags=campaign_service.AddUetTags(
                UetTags=uet_tags
            ).UetTags

        if (uet_tags is None or len(uet_tags) < 1):
            output_status_message(
                "You do not have any UET tags registered for CustomerId {0}.".format(authorization_data.customer_id)
            )
            sys.exit(0)

        output_status_message("List of all UET Tags:")
        output_array_of_uettag(uet_tags)

        # After you retreive the tracking script from the AddUetTags or GetUetTagsByIds operation, 
        # the next step is to add the UET tag tracking code to your website. 

        # We will use the same UET tag for the remainder of this example.
        tag_id = uet_tags['UetTag'][0].Id

        # Add remarketing lists that depend on the UET Tag Id retreived above.
        add_audiences=campaign_service.factory.create('ArrayOfAudience')
        custom_events_list=set_elements_to_none(campaign_service.factory.create('RemarketingList'))
        custom_events_list.Description="New list with CustomEventsRule"
        custom_events_list.MembershipDuration=30
        custom_events_list.Name="Remarketing List with CustomEventsRule " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        custom_events_list.ParentId=authorization_data.account_id
        # The rule definition is translated to the following logical expression: 
        # (Category Equals video) and (Action Equals play) and (Label Equals trailer) 
        # and (Value Equals 5)
        custom_events_rule=set_elements_to_none(campaign_service.factory.create('CustomEventsRule'))
        # The type of user interaction you want to track.
        custom_events_rule.Action="play"
        custom_events_rule.ActionOperator='Equals'
        # The category of event you want to track. 
        custom_events_rule.Category="video"
        custom_events_rule.CategoryOperator='Equals'
        # The name of the element that caused the action.
        custom_events_rule.Label="trailer"
        custom_events_rule.LabelOperator='Equals'
        # A numerical value associated with that event. 
        # Could be length of the video played etc.
        custom_events_rule.Value=5.00
        custom_events_rule.ValueOperator='Equals'
        custom_events_list.Rule=custom_events_rule
        custom_events_list.Scope='Account'
        custom_events_list.TagId=tag_id            
        add_audiences.Audience.append(custom_events_list)
                    
        page_visitors_list=set_elements_to_none(campaign_service.factory.create('RemarketingList'))  
        page_visitors_list.Description="New list with PageVisitorsRule"
        page_visitors_list.MembershipDuration=30
        page_visitors_list.Name="Remarketing List with PageVisitorsRule " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        page_visitors_list.ParentId=authorization_data.account_id
        # The rule definition is translated to the following logical expression: 
        # ((Url Contains X) and (ReferrerUrl DoesNotContain Z)) or ((Url DoesNotBeginWith Y)) 
        # or ((ReferrerUrl Equals Z))
        page_visitors_rule=set_elements_to_none(campaign_service.factory.create('PageVisitorsRule'))
        page_visitors_rule_item_groups=campaign_service.factory.create('ArrayOfRuleItemGroup')
        page_visitors_rule_item_group_a=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_rule_items_a=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_rule_item_a=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_rule_item_a.Operand="Url"
        page_visitors_rule_item_a.Operator='Contains'
        page_visitors_rule_item_a.Value="X"
        page_visitors_rule_items_a.RuleItem.append(page_visitors_rule_item_a)   
        page_visitors_rule_item_aa=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_rule_item_aa.Operand="ReferrerUrl"
        page_visitors_rule_item_aa.Operator='DoesNotContain'
        page_visitors_rule_item_aa.Value="Z"
        page_visitors_rule_items_a.RuleItem.append(page_visitors_rule_item_aa)    
        page_visitors_rule_item_group_a.Items=page_visitors_rule_items_a
        page_visitors_rule_item_groups.RuleItemGroup.append(page_visitors_rule_item_group_a)
        page_visitors_rule_item_group_b=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_rule_items_b=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_rule_item_b=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_rule_item_b.Operand="Url"
        page_visitors_rule_item_b.Operator='DoesNotBeginWith'
        page_visitors_rule_item_b.Value="Y"
        page_visitors_rule_items_b.RuleItem.append(page_visitors_rule_item_b)            
        page_visitors_rule_item_group_b.Items=page_visitors_rule_items_b
        page_visitors_rule_item_groups.RuleItemGroup.append(page_visitors_rule_item_group_b)
        page_visitors_rule_item_group_c=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_rule_items_c=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_rule_item_c=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_rule_item_c.Operand="ReferrerUrl"
        page_visitors_rule_item_c.Operator='Equals'
        page_visitors_rule_item_c.Value="Z"
        page_visitors_rule_items_c.RuleItem.append(page_visitors_rule_item_c)            
        page_visitors_rule_item_group_c.Items=page_visitors_rule_items_c
        page_visitors_rule_item_groups.RuleItemGroup.append(page_visitors_rule_item_group_c)
        page_visitors_rule.RuleItemGroups=page_visitors_rule_item_groups
        page_visitors_list.Rule=page_visitors_rule
        page_visitors_list.Scope='Account'
        page_visitors_list.TagId=tag_id 
        add_audiences.Audience.append(page_visitors_list)
        
        page_visitors_who_did_not_visit_another_page_list=set_elements_to_none(campaign_service.factory.create('RemarketingList'))        
        page_visitors_who_did_not_visit_another_page_list.Description="New list with PageVisitorsWhoDidNotVisitAnotherPageRule"
        page_visitors_who_did_not_visit_another_page_list.MembershipDuration=30
        page_visitors_who_did_not_visit_another_page_list.Name="Remarketing List with PageVisitorsWhoDidNotVisitAnotherPageRule " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        page_visitors_who_did_not_visit_another_page_list.ParentId=authorization_data.account_id
        # The rule definition is translated to the following logical expression: 
        # (((Url Contains X) and (ReferrerUrl DoesNotContain Z)) or ((Url DoesNotBeginWith Y)) 
        # or ((ReferrerUrl Equals Z))) 
        # and not (((Url BeginsWith A) and (ReferrerUrl BeginsWith B)) or ((Url Contains C)))
        page_visitors_who_did_not_visit_another_page_rule=set_elements_to_none(campaign_service.factory.create('PageVisitorsWhoDidNotVisitAnotherPageRule'))            
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_groups=campaign_service.factory.create('ArrayOfRuleItemGroup')
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_group_a=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_did_not_visit_another_page_exclude_rule_items_a=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_a=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_a.Operand="Url"
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_a.Operator='BeginsWith'
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_a.Value="A"
        page_visitors_who_did_not_visit_another_page_exclude_rule_items_a.RuleItem.append(page_visitors_who_did_not_visit_another_page_exclude_rule_item_a)   
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_aa=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_aa.Operand="ReferrerUrl"
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_aa.Operator='BeginsWith'
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_aa.Value="B"
        page_visitors_who_did_not_visit_another_page_exclude_rule_items_a.RuleItem.append(page_visitors_who_did_not_visit_another_page_exclude_rule_item_aa)    
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_group_a.Items=page_visitors_who_did_not_visit_another_page_exclude_rule_items_a
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_groups.RuleItemGroup.append(page_visitors_who_did_not_visit_another_page_exclude_rule_item_group_a)
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_group_b=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_did_not_visit_another_page_exclude_rule_items_b=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_b=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_b.Operand="Url"
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_b.Operator='Contains'
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_b.Value="C"
        page_visitors_who_did_not_visit_another_page_exclude_rule_items_b.RuleItem.append(page_visitors_who_did_not_visit_another_page_exclude_rule_item_b)            
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_group_b.Items=page_visitors_who_did_not_visit_another_page_exclude_rule_items_b
        page_visitors_who_did_not_visit_another_page_exclude_rule_item_groups.RuleItemGroup.append(page_visitors_who_did_not_visit_another_page_exclude_rule_item_group_b)
        page_visitors_who_did_not_visit_another_page_rule.ExcludeRuleItemGroups=page_visitors_who_did_not_visit_another_page_exclude_rule_item_groups            
        page_visitors_who_did_not_visit_another_page_include_rule_item_groups=campaign_service.factory.create('ArrayOfRuleItemGroup')
        page_visitors_who_did_not_visit_another_page_include_rule_item_group_a=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_did_not_visit_another_page_include_rule_items_a=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_did_not_visit_another_page_include_rule_item_a=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_include_rule_item_a.Operand="Url"
        page_visitors_who_did_not_visit_another_page_include_rule_item_a.Operator='Contains'
        page_visitors_who_did_not_visit_another_page_include_rule_item_a.Value="X"
        page_visitors_who_did_not_visit_another_page_include_rule_items_a.RuleItem.append(page_visitors_who_did_not_visit_another_page_include_rule_item_a)   
        page_visitors_who_did_not_visit_another_page_include_rule_item_aa=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_include_rule_item_aa.Operand="ReferrerUrl"
        page_visitors_who_did_not_visit_another_page_include_rule_item_aa.Operator='DoesNotContain'
        page_visitors_who_did_not_visit_another_page_include_rule_item_aa.Value="Z"
        page_visitors_who_did_not_visit_another_page_include_rule_items_a.RuleItem.append(page_visitors_who_did_not_visit_another_page_include_rule_item_aa)    
        page_visitors_who_did_not_visit_another_page_include_rule_item_group_a.Items=page_visitors_who_did_not_visit_another_page_include_rule_items_a
        page_visitors_who_did_not_visit_another_page_include_rule_item_groups.RuleItemGroup.append(page_visitors_who_did_not_visit_another_page_include_rule_item_group_a)
        page_visitors_who_did_not_visit_another_page_include_rule_item_group_b=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_did_not_visit_another_page_include_rule_items_b=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_did_not_visit_another_page_include_rule_item_b=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_include_rule_item_b.Operand="Url"
        page_visitors_who_did_not_visit_another_page_include_rule_item_b.Operator='DoesNotBeginWith'
        page_visitors_who_did_not_visit_another_page_include_rule_item_b.Value="Y"
        page_visitors_who_did_not_visit_another_page_include_rule_items_b.RuleItem.append(page_visitors_who_did_not_visit_another_page_include_rule_item_b)            
        page_visitors_who_did_not_visit_another_page_include_rule_item_group_b.Items=page_visitors_who_did_not_visit_another_page_include_rule_items_b
        page_visitors_who_did_not_visit_another_page_include_rule_item_groups.RuleItemGroup.append(page_visitors_who_did_not_visit_another_page_include_rule_item_group_b)
        page_visitors_who_did_not_visit_another_page_include_rule_item_group_c=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_did_not_visit_another_page_include_rule_items_c=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_did_not_visit_another_page_include_rule_item_c=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_did_not_visit_another_page_include_rule_item_c.Operand="ReferrerUrl"
        page_visitors_who_did_not_visit_another_page_include_rule_item_c.Operator='Equals'
        page_visitors_who_did_not_visit_another_page_include_rule_item_c.Value="Z"
        page_visitors_who_did_not_visit_another_page_include_rule_items_c.RuleItem.append(page_visitors_who_did_not_visit_another_page_include_rule_item_c)            
        page_visitors_who_did_not_visit_another_page_include_rule_item_group_c.Items=page_visitors_who_did_not_visit_another_page_include_rule_items_c
        page_visitors_who_did_not_visit_another_page_include_rule_item_groups.RuleItemGroup.append(page_visitors_who_did_not_visit_another_page_include_rule_item_group_c)
        page_visitors_who_did_not_visit_another_page_rule.IncludeRuleItemGroups=page_visitors_who_did_not_visit_another_page_include_rule_item_groups
        page_visitors_who_did_not_visit_another_page_list.Rule=page_visitors_who_did_not_visit_another_page_rule
        page_visitors_who_did_not_visit_another_page_list.Scope='Account'
        page_visitors_who_did_not_visit_another_page_list.TagId=tag_id   
        add_audiences.Audience.append(page_visitors_who_did_not_visit_another_page_list)

        page_visitors_who_visited_another_page_list=set_elements_to_none(campaign_service.factory.create('RemarketingList'))  
        page_visitors_who_visited_another_page_list.Description="New list with PageVisitorsWhoVisitedAnotherPageRule"
        page_visitors_who_visited_another_page_list.MembershipDuration=30
        page_visitors_who_visited_another_page_list.Name="Remarketing List with PageVisitorsWhoVisitedAnotherPageRule " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        page_visitors_who_visited_another_page_list.ParentId=authorization_data.account_id
        # The rule definition is translated to the following logical expression: 
        # (((Url Contains X) and (ReferrerUrl NotEquals Z)) or ((Url DoesNotBeginWith Y)) or 
        # ((ReferrerUrl Equals Z))) 
        # and (((Url BeginsWith A) and (ReferrerUrl BeginsWith B)) or ((Url Contains C)))
        page_visitors_who_visited_another_page_rule=set_elements_to_none(campaign_service.factory.create('PageVisitorsWhoVisitedAnotherPageRule'))         
        page_visitors_who_visited_another_page_another_rule_item_groups=campaign_service.factory.create('ArrayOfRuleItemGroup')
        page_visitors_who_visited_another_page_another_rule_item_group_a=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_visited_another_page_another_rule_items_a=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_visited_another_page_another_rule_item_a=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_another_rule_item_a.Operand="Url"
        page_visitors_who_visited_another_page_another_rule_item_a.Operator='BeginsWith'
        page_visitors_who_visited_another_page_another_rule_item_a.Value="A"
        page_visitors_who_visited_another_page_another_rule_items_a.RuleItem.append(page_visitors_who_visited_another_page_another_rule_item_a)   
        page_visitors_who_visited_another_page_another_rule_item_aa=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_another_rule_item_aa.Operand="ReferrerUrl"
        page_visitors_who_visited_another_page_another_rule_item_aa.Operator='BeginsWith'
        page_visitors_who_visited_another_page_another_rule_item_aa.Value="B"
        page_visitors_who_visited_another_page_another_rule_items_a.RuleItem.append(page_visitors_who_visited_another_page_another_rule_item_aa)    
        page_visitors_who_visited_another_page_another_rule_item_group_a.Items=page_visitors_who_visited_another_page_another_rule_items_a
        page_visitors_who_visited_another_page_another_rule_item_groups.RuleItemGroup.append(page_visitors_who_visited_another_page_another_rule_item_group_a)
        page_visitors_who_visited_another_page_another_rule_item_group_b=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_visited_another_page_another_rule_items_b=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_visited_another_page_another_rule_item_b=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_another_rule_item_b.Operand="Url"
        page_visitors_who_visited_another_page_another_rule_item_b.Operator='Contains'
        page_visitors_who_visited_another_page_another_rule_item_b.Value="C"
        page_visitors_who_visited_another_page_another_rule_items_b.RuleItem.append(page_visitors_who_visited_another_page_another_rule_item_b)            
        page_visitors_who_visited_another_page_another_rule_item_group_b.Items=page_visitors_who_visited_another_page_another_rule_items_b
        page_visitors_who_visited_another_page_another_rule_item_groups.RuleItemGroup.append(page_visitors_who_visited_another_page_another_rule_item_group_b)
        page_visitors_who_visited_another_page_rule.AnotherRuleItemGroups=page_visitors_who_visited_another_page_another_rule_item_groups            
        page_visitors_who_visited_another_page_rule_item_groups=campaign_service.factory.create('ArrayOfRuleItemGroup')
        page_visitors_who_visited_another_page_rule_item_group_a=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_visited_another_page_rule_items_a=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_visited_another_page_rule_item_a=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_rule_item_a.Operand="Url"
        page_visitors_who_visited_another_page_rule_item_a.Operator='Contains'
        page_visitors_who_visited_another_page_rule_item_a.Value="X"
        page_visitors_who_visited_another_page_rule_items_a.RuleItem.append(page_visitors_who_visited_another_page_rule_item_a)   
        page_visitors_who_visited_another_page_rule_item_aa=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_rule_item_aa.Operand="ReferrerUrl"
        page_visitors_who_visited_another_page_rule_item_aa.Operator='DoesNotContain'
        page_visitors_who_visited_another_page_rule_item_aa.Value="Z"
        page_visitors_who_visited_another_page_rule_items_a.RuleItem.append(page_visitors_who_visited_another_page_rule_item_aa)    
        page_visitors_who_visited_another_page_rule_item_group_a.Items=page_visitors_who_visited_another_page_rule_items_a
        page_visitors_who_visited_another_page_rule_item_groups.RuleItemGroup.append(page_visitors_who_visited_another_page_rule_item_group_a)
        page_visitors_who_visited_another_page_rule_item_group_b=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_visited_another_page_rule_items_b=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_visited_another_page_rule_item_b=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_rule_item_b.Operand="Url"
        page_visitors_who_visited_another_page_rule_item_b.Operator='DoesNotBeginWith'
        page_visitors_who_visited_another_page_rule_item_b.Value="Y"
        page_visitors_who_visited_another_page_rule_items_b.RuleItem.append(page_visitors_who_visited_another_page_rule_item_b)            
        page_visitors_who_visited_another_page_rule_item_group_b.Items=page_visitors_who_visited_another_page_rule_items_b
        page_visitors_who_visited_another_page_rule_item_groups.RuleItemGroup.append(page_visitors_who_visited_another_page_rule_item_group_b)
        page_visitors_who_visited_another_page_rule_item_group_c=set_elements_to_none(campaign_service.factory.create('RuleItemGroup'))
        page_visitors_who_visited_another_page_rule_items_c=campaign_service.factory.create('ArrayOfRuleItem')
        page_visitors_who_visited_another_page_rule_item_c=set_elements_to_none(campaign_service.factory.create('StringRuleItem'))
        page_visitors_who_visited_another_page_rule_item_c.Operand="ReferrerUrl"
        page_visitors_who_visited_another_page_rule_item_c.Operator='Equals'
        page_visitors_who_visited_another_page_rule_item_c.Value="Z"
        page_visitors_who_visited_another_page_rule_items_c.RuleItem.append(page_visitors_who_visited_another_page_rule_item_c)            
        page_visitors_who_visited_another_page_rule_item_group_c.Items=page_visitors_who_visited_another_page_rule_items_c
        page_visitors_who_visited_another_page_rule_item_groups.RuleItemGroup.append(page_visitors_who_visited_another_page_rule_item_group_c)
        page_visitors_who_visited_another_page_rule.RuleItemGroups=page_visitors_who_visited_another_page_rule_item_groups
        page_visitors_who_visited_another_page_list.Rule=page_visitors_who_visited_another_page_rule
        page_visitors_who_visited_another_page_list.Scope='Account'
        page_visitors_who_visited_another_page_list.TagId=tag_id   
        add_audiences.Audience.append(page_visitors_who_visited_another_page_list)  

        # RemarketingList extends the Audience base class. 
        # We manage remarketing lists with Audience operations.

        output_status_message("-----\nAddAudiences:")
        add_audiences_response=campaign_service.AddAudiences(
            Audiences=add_audiences
        )
        audience_ids={
            'long': add_audiences_response.AudienceIds['long'] if add_audiences_response.AudienceIds['long'] else None
        }
        output_status_message("AudienceIds:")
        output_array_of_long(audience_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_audiences_response.PartialErrors) 

        # Add an ad group in a campaign. The ad group will later be associated with remarketing lists. 

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.DailyBudget=50
        campaign.Description="Red shoes line."
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
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

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Name="Women's Red Shoe Sale"
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        current_time=gmtime()
        end_date.Year=current_time.tm_year + 1
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        # Applicable for all remarketing lists that are associated with this ad group. TargetAndBid indicates 
        # that you want to show ads only to people included in the remarketing list, with the option to change
        # the bid amount. Ads in this ad group will only show to people included in the remarketing list.
        ad_group_settings=campaign_service.factory.create('ArrayOfSetting')
        ad_group_target_setting=campaign_service.factory.create('TargetSetting')
        ad_group_audience_target_setting_detail=campaign_service.factory.create('TargetSettingDetail')
        ad_group_audience_target_setting_detail.CriterionTypeGroup='Audience'
        ad_group_audience_target_setting_detail.TargetAndBid=True
        ad_group_target_setting.Details.TargetSettingDetail.append(ad_group_audience_target_setting_detail)
        ad_group_settings.Setting.append(ad_group_target_setting)
        ad_group.Settings=ad_group_settings
        ad_groups.AdGroup.append(ad_group)

        output_status_message("-----\nAddAdGroups:")
        add_ad_groups_response=campaign_service.AddAdGroups(
            CampaignId=campaign_ids['long'][0],
            AdGroups=ad_groups,
            ReturnInheritedBidStrategyTypes=False
        )
        ad_group_ids={
            'long': add_ad_groups_response.AdGroupIds['long'] if add_ad_groups_response.AdGroupIds['long'] else None
        }
        output_status_message("AdGroupIds:")
        output_array_of_long(ad_group_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ad_groups_response.PartialErrors)

        # Associate all of the remarketing lists created above with the new ad group.

        ad_group_remarketing_list_associations=campaign_service.factory.create('ArrayOfAdGroupCriterion')

        for audience_id in audience_ids['long']:
            if audience_id is not None:
                biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
                biddable_ad_group_criterion.AdGroupId=ad_group_ids['long'][0]
                biddable_ad_group_criterion.Status='Active'
                audience_criterion=set_elements_to_none(campaign_service.factory.create('AudienceCriterion'))
                audience_criterion.AudienceId=audience_id
                audience_criterion.AudienceType='RemarketingList'
                biddable_ad_group_criterion.Criterion=audience_criterion
                bid_multiplier=set_elements_to_none(campaign_service.factory.create('BidMultiplier'))
                bid_multiplier.Multiplier=20.00
                biddable_ad_group_criterion.CriterionBid=bid_multiplier
                ad_group_remarketing_list_associations.AdGroupCriterion.append(biddable_ad_group_criterion)
         
        output_status_message("-----\nAddAdGroupCriterions:")
        add_ad_group_criterions_response = campaign_service.AddAdGroupCriterions(
            AdGroupCriterions=ad_group_remarketing_list_associations,
            CriterionType='Audience'
        )
        ad_group_criterion_ids={
            'long': add_ad_group_criterions_response.AdGroupCriterionIds['long'] if add_ad_group_criterions_response.AdGroupCriterionIds['long'] else None
        }
        output_status_message("AdGroupCriterionIds:")
        output_array_of_long(ad_group_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherror(add_ad_group_criterions_response.NestedPartialErrors)

        # Delete the campaign and everything it contains e.g., ad groups and ads.

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
        version=12,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
