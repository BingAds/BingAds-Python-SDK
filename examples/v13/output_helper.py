from campaignmanagement_example_helper import *
import json

# Common

def output_bing_ads_webfault_error(error):
    if hasattr(error, 'ErrorCode'):
        output_status_message("ErrorCode: {0}".format(error.ErrorCode))
    if hasattr(error, 'Code'):
        output_status_message("Code: {0}".format(error.Code))
    if hasattr(error, 'Details'):
        output_status_message("Details: {0}".format(error.Details))
    if hasattr(error, 'FieldPath'):
        output_status_message("FieldPath: {0}".format(error.FieldPath))
    if hasattr(error, 'Message'):
        output_status_message("Message: {0}".format(error.Message))
    output_status_message('')

def output_webfault_errors(ex):
    if not hasattr(ex.fault, "detail"):
        raise Exception("Unknown WebFault")

    error_attribute_sets = (
        ["ApiFault", "OperationErrors", "OperationError"],
        ["AdApiFaultDetail", "Errors", "AdApiError"],
        ["ApiFaultDetail", "BatchErrors", "BatchError"],
        ["ApiFaultDetail", "OperationErrors", "OperationError"],
        ["EditorialApiFaultDetail", "BatchErrors", "BatchError"],
        ["EditorialApiFaultDetail", "EditorialErrors", "EditorialError"],
        ["EditorialApiFaultDetail", "OperationErrors", "OperationError"],
    )

    for error_attribute_set in error_attribute_sets:
        if output_error_detail(ex.fault.detail, error_attribute_set):
            return

    # Handle serialization errors, for example: The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v13:Entities.
    if hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors=ex.fault.detail.ExceptionDetail
        if isinstance(api_errors, list):
            for api_error in api_errors:
                output_status_message(api_error.Message)
        else:
            output_status_message(api_errors.Message)
        return
    
    raise Exception("Unknown WebFault")

def output_error_detail(error_detail, error_attribute_set):
    api_errors = error_detail
    for field in error_attribute_set:
        api_errors = getattr(api_errors, field, None)
    if api_errors is None:
        return False
    if isinstance(api_errors, list):
        for api_error in api_errors:
            output_bing_ads_webfault_error(api_error)
    else:
        output_bing_ads_webfault_error(api_errors)
    return True

# Bulk

def output_percent_complete(progress):
    output_status_message("Percent Complete: {0}".format(progress.percent_complete))
   
def output_bulk_errors(errors):
    for error in errors:
        if error.error is not None:
            output_status_message("Number: {0}".format(error.error))
        output_status_message("Error: {0}".format(error.number))
        if error.editorial_reason_code is not None:
            output_status_message("EditorialTerm: {0}".format(error.editorial_term))
            output_status_message("EditorialReasonCode: {0}".format(error.editorial_reason_code))
            output_status_message("EditorialLocation: {0}".format(error.editorial_location))
            output_status_message("PublisherCountries: {0}".format(error.publisher_countries))
        output_status_message('')

def output_bulk_quality_score_data(quality_score_data):
    if quality_score_data is not None:
        output_status_message("KeywordRelevance: {0}".format(quality_score_data.keyword_relevance))
        output_status_message("LandingPageRelevance: {0}".format(quality_score_data.landing_page_relevance))
        output_status_message("LandingPageUserExperience: {0}".format(quality_score_data._landing_page_user_experience))
        output_status_message("QualityScore: {0}".format(quality_score_data.quality_score))

def output_bulk_bid_suggestions(bid_suggestions):
    if bid_suggestions is not None:
        output_status_message("BestPosition: {0}".format(bid_suggestions.best_position))
        output_status_message("MainLine: {0}".format(bid_suggestions.main_line))
        output_status_message("FirstPage: {0}".format(bid_suggestions.first_page))

def output_bulk_feeds(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkFeed:")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))
        output_status_message("CustomAttributes: {0}".format(json.dumps(entity.custom_attributes, sort_keys=True, indent=4, separators=(',', ': '))))
        output_status_message("Id: {0}".format(entity.id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Name: {0}".format(entity.name))
        output_status_message("Status: {0}".format(entity.status))
        output_status_message("SubType: {0}".format(entity.sub_type))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_feed_items(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkFeedItem:")
        output_status_message("AdGroupName: {0}".format(entity.ad_group))
        output_status_message("AudienceId: {0}".format(entity.audience_id))
        output_status_message("CampaignName: {0}".format(entity.campaign))
        output_status_message("ClientId: {0}".format(entity.client_id))
        output_status_message("CustomAttributes: {0}".format(json.dumps(entity.custom_attributes, sort_keys=True, indent=4, separators=(',', ': '))))
        if hasattr(entity, 'daytime_ranges') and entity.daytime_ranges is not None:
            output_status_message("DayTimeRanges:")
            for daytime_range in entity.daytime_ranges:
                output_daytime(daytime_range)
        output_status_message("DevicePreference: {0}".format(entity.device_preference))
        output_status_message("EndDate: {0}".format(entity.end_date))
        output_status_message("FeedId: {0}".format(entity.feed_id))
        output_status_message("Id: {0}".format(entity.id))
        output_status_message("IntentOption: {0}".format(entity.intent_option))
        output_status_message("Keyword: {0}".format(entity.keyword))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("LocationId: {0}".format(entity.location_id))
        output_status_message("MatchType: {0}".format(entity.match_type))
        output_status_message("StartDate: {0}".format(entity.start_date))
        output_status_message("Status: {0}".format(entity.status))

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_dynamic_search_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkDynamicSearchAd:")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management DynamicSearchAd Object
        output_ad(entity.dynamic_search_ad)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_expanded_text_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkExpandedTextAd:")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management ExpandedTextAd Object
        output_ad(entity.expanded_text_ad)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_product_partitions(bulk_ad_group_product_partitions):
    """
    Outputs the list of BulkAdGroupProductPartition which each contain an AdGroupCriterion, formatted as a tree. 
    Each AdGroupCriterion must be either a BiddableAdGroupCriterion or NegativeAdGroupCriterion. 

    :param bulk_ad_group_product_partitions: The list of BulkAdGroupProductPartition to output formatted as a tree.
    :type bulk_ad_group_product_partitions: BulkAdGroupProductPartition[]

    """

    # Set up the tree for output

    child_branches={}
    tree_root=None

    for bulk_ad_group_product_partition in bulk_ad_group_product_partitions:
        ad_group_criterion=bulk_ad_group_product_partition.ad_group_criterion
        partition=ad_group_criterion.Criterion
        child_branches[ad_group_criterion.Id]=[]

        # The product partition with ParentCriterionId set to null is the root node.
        if partition.ParentCriterionId is not None:
            child_branches[partition.ParentCriterionId].append(bulk_ad_group_product_partition)
        else:
            tree_root=bulk_ad_group_product_partition

    # Outputs the tree root node and any children recursively
    output_bulk_product_partition_tree(tree_root, child_branches, 0)

def output_bulk_product_partition_tree(node, child_branches, tree_level):
    """
    Outputs the details of the specified product partition node, 
    and passes any children to itself recursively.

    :param node: The node to output, whether a Subdivision or Unit.
    :type node: BulkAdGroupProductPartition
    :param child_branches: The child branches or nodes if any exist.
    :type child_branches: dict{long, BulkAdGroupProductPartition[]}
    :param tree_level: The number of descendents from the tree root node. 
     Used by this operation to format the tree structure output.
    :type tree_level: int

    """

    if node is None:
        return

    ad_group_criterion=node.ad_group_criterion

    pad=''
    for i in range(0, tree_level):
        pad=pad + '\t'
    output_status_message("{0}{1}".format(
        pad,
        ad_group_criterion.Criterion.PartitionType)
    )

    output_status_message("{0}ParentCriterionId: {1}".format(
        pad,
        ad_group_criterion.Criterion.ParentCriterionId)
    )

    output_status_message("{0}Id: {1}".format(
        pad,
        ad_group_criterion.Id)
    )

    if ad_group_criterion.Criterion.PartitionType == 'Unit':
        if ad_group_criterion.Type == 'BiddableAdGroupCriterion':
            output_status_message("{0}Bid Amount: {1}".format(
                pad,
                ad_group_criterion.CriterionBid.Amount)
            )
        elif ad_group_criterion.Type == 'NegativeAdGroupCriterion':
            output_status_message("{0}Not Bidding on this Condition".format(
                pad)
            )
           

    null_attribute="(All other)" if ad_group_criterion.Criterion.ParentCriterionId is not None else "(Tree Root)"
    output_status_message("{0}Attribute: {1}".format(
        pad,
        null_attribute if ad_group_criterion.Criterion.Condition.Attribute is None else ad_group_criterion.Criterion.Condition.Attribute)
    )

    output_status_message("{0}Operand: {1}\n".format(
        pad,
        ad_group_criterion.Criterion.Condition.Operand)
    )

    for child_node in child_branches[ad_group_criterion.Id]:
        output_bulk_product_partition_tree(child_node, child_branches, tree_level + 1)


def output_bulk_product_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkProductAd:")
        output_status_message("AdGroupId: {0}".format(entity.ad_group_id))
        output_status_message("AdGroupName: {0}".format(entity.ad_group_name))
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management ProductAd Object
        output_ad(entity.ad)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')


def output_bulk_keywords(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkKeyword:")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_quality_score_data(entity.quality_score_data)
        output_bulk_bid_suggestions(entity.bid_suggestions)

        # Output the Campaign Management Keyword Object
        output_keyword(entity.keyword)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_action_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkActionAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management ActionAdExtension Object
        output_adextension(entity.action_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_action_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignActionAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_app_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAppAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management AppAdExtension Object
        output_adextension(entity.app_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_app_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignAppAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
                
def output_bulk_call_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCallAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management CallAdExtension Object
        output_adextension(entity.call_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_call_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignCallAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_callout_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCalloutAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management CalloutAdExtension Object
        output_adextension(entity.callout_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_callout_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignCalloutAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_location_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkLocationAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management LocationAdExtension Object
        output_adextension(entity.location_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_location_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignLocationAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_price_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkPriceAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management PriceAdExtension Object
        output_adextension(entity.price_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_price_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignPriceAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_review_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkReviewAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management ReviewAdExtension Object
        output_adextension(entity.review_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_review_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignReviewAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_sitelink_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkSitelinkAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management SitelinkAdExtension Object
        output_adextension(entity.sitelink_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_sitelink_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignSitelinkAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
       
def output_bulk_structured_snippet_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkStructuredSnippetAdExtension:")
        output_status_message("Account Id: {0}".format(entity.account_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management StructuredSnippetAdExtension Object
        output_adextension(entity.structured_snippet_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_structured_snippet_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignStructuredSnippetAdExtension:")
        if entity.ad_extension_id_to_entity_id_association is not None:
            output_status_message("AdExtensionId: {0}".format(entity.ad_extension_id_to_entity_id_association.AdExtensionId))
            output_status_message("EntityId: {0}".format(entity.ad_extension_id_to_entity_id_association.EntityId))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("Client Id: {0}".format(entity.client_id))
        output_status_message("Editorial Status: {0}".format(entity.editorial_status))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Status: {0}".format(entity.status))
        
        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_remarketing_lists(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkRemarketingList:")
        output_status_message("Status: {0}".format(entity.status))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management RemarketingList Object
        output_audience(entity.remarketing_list)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_ad_group_remarketing_list_associations(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupRemarketingListAssociation:")
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management BiddableAdGroupCriterion Object
        output_biddableadgroupcriterion(entity.biddable_ad_group_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_ad_group_dynamic_search_ad_targets(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupDynamicSearchAdTarget:")
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management BiddableAdGroupCriterion Object
        output_biddableadgroupcriterion(entity.biddable_ad_group_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_ad_group_negative_dynamic_search_ad_targets(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupNegativeDynamicSearchAdTarget:")
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management NegativeAdGroupCriterion Object
        output_negativeadgroupcriterion(entity.negative_ad_group_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_budgets(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkBudget:")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
            
        output_status_message("Status: {0}".format(entity.status))

        # Output the Campaign Management Budget Object
        output_budget(entity.budget)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaigns(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaign:")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management Campaign Object
        output_campaign(entity.campaign)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_ad_groups(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroup:")
        output_status_message("Campaign Id: {0}".format(entity.campaign_id))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management AdGroup Object
        output_adgroup(entity.ad_group)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_ad_group_product_partitions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupProductPartition:")
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("AdGroupName: {0}".format(entity.ad_group_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # BulkAdGroupProductPartition can have either BiddableAdGroupCriterion or NegativeAdGroupCriterion
        if entity.ad_group_criterion is None:
            output_status_message("Criterion is null or invalid.")
        elif entity.ad_group_criterion.Type == 'BiddableAdGroupCriterion':
            # Output the Campaign Management BiddableAdGroupCriterion
            output_biddableadgroupcriterion(entity.ad_group_criterion)
        elif entity.ad_group_criterion.Type == 'NegativeAdGroupCriterion':
            # Output the Campaign Management NegativeAdGroupCriterion
            output_negativeadgroupcriterion(entity.ad_group_criterion)
        else:
            output_status_message("Unknown ad group criterion type.")

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_product_scopes(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignProductScope:")
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management BiddableCampaignCriterion
        output_biddablecampaigncriterion(entity.biddable_campaign_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_offlineconversions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkOfflineConversion:")
        output_status_message("ClientId: {0}".format(entity.client_id))

        # Output the Campaign Management OfflineConversion Object
        output_offlineconversion(entity.offline_conversion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
