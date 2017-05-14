# Common

def output_partial_errors(partial_errors):
    if not partial_errors:
        return None
    output_status_message("BatchError (PartialErrors) item:\n")
    for error in partial_errors['BatchError']:
        output_status_message("\tIndex: {0}".format(error.Index))
        output_status_message("\tCode: {0}".format(error.Code))
        output_status_message("\tErrorCode: {0}".format(error.ErrorCode))
        output_status_message("\tMessage: {0}\n".format(error.Message))

        # In the case of an EditorialError, more details are available
        if error.Type == "EditorialError" and error.ErrorCode == "CampaignServiceEditorialValidationError":
            output_status_message("\tDisapprovedText: {0}".format(error.DisapprovedText))
            output_status_message("\tLocation: {0}".format(error.Location))
            output_status_message("\tPublisherCountry: {0}".format(error.PublisherCountry))
            output_status_message("\tReasonCode: {0}\n".format(error.ReasonCode))

def output_nested_partial_errors(nested_partial_errors):
    if not nested_partial_errors:
        return None
    output_status_message("BatchErrorCollection (NestedPartialErrors) item:\n")
    for collection in nested_partial_errors['BatchErrorCollection']:
        # The top level list index.
        if collection is not None:
            if hasattr(collection, 'Code'):
                output_status_message("\tIndex: {0}".format(collection.Index))
                output_status_message("\tCode: {0}".format(collection.Code))
                output_status_message("\tErrorCode: {0}".format(collection.ErrorCode))
                output_status_message("\tMessage: {0}\n".format(collection.Message))
            
            # The nested list of batch errors
            for error in collection.BatchErrors['BatchError']:
                output_status_message("\tIndex: {0}".format(error.Index))
                output_status_message("\tCode: {0}".format(error.Code))
                output_status_message("\tErrorCode: {0}".format(error.ErrorCode))
                output_status_message("\tMessage: {0}\n".format(error.Message))

                # In the case of an EditorialError, more details are available
                if error.Type == "EditorialError" and error.ErrorCode == "CampaignServiceEditorialValidationError":
                    output_status_message("\tDisapprovedText: {0}".format(error.DisapprovedText))
                    output_status_message("\tLocation: {0}".format(error.Location))
                    output_status_message("\tPublisherCountry: {0}".format(error.PublisherCountry))
                    output_status_message("\tReasonCode: {0}\n".format(error.ReasonCode))

def output_operation_errors(operation_errors, partial_errors):
    if hasattr(operation_errors, 'OperationError'):
        for error in operation_errors['OperationError']:
            output_status_message("OperationError");
            output_status_message("Code: {0}\nMessage: {1}\n".format(error.Code, error.Message))

    if hasattr(partial_errors, 'ArrayOfOperationError'):
        for errors in partial_errors['ArrayOfOperationError']:
            if errors is not None:
                for error in errors['OperationError']:
                    if error is not None:
                        output_status_message("OperationError");
                        output_status_message("Code: {0}\nMessage: {1}\n".format(error.Code, error.Message))

def output_status_message(message):
    print(message)

def output_bing_ads_webfault_error(error):
    if hasattr(error, 'ErrorCode'):
        output_status_message("ErrorCode: {0}".format(error.ErrorCode))
    if hasattr(error, 'Code'):
        output_status_message("Code: {0}".format(error.Code))
    if hasattr(error, 'Message'):
        output_status_message("Message: {0}".format(error.Message))
    output_status_message('')

def output_webfault_errors(ex):
    if hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFault') \
        and hasattr(ex.fault.detail.ApiFault, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFault.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFault.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'AdApiFaultDetail') \
        and hasattr(ex.fault.detail.AdApiFaultDetail, 'Errors') \
        and hasattr(ex.fault.detail.AdApiFaultDetail.Errors, 'AdApiError'):
        api_errors=ex.fault.detail.AdApiFaultDetail.Errors.AdApiError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.ApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ApiFaultDetail') \
        and hasattr(ex.fault.detail.ApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.ApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.ApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'BatchErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.BatchErrors, 'BatchError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.BatchErrors.BatchError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'EditorialErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.EditorialErrors, 'EditorialError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.EditorialErrors.EditorialError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'EditorialApiFaultDetail') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail, 'OperationErrors') \
        and hasattr(ex.fault.detail.EditorialApiFaultDetail.OperationErrors, 'OperationError'):
        api_errors=ex.fault.detail.EditorialApiFaultDetail.OperationErrors.OperationError
        if type(api_errors) == list:
            for api_error in api_errors:
                output_bing_ads_webfault_error(api_error)
        else:
            output_bing_ads_webfault_error(api_errors)
    # Handle serialization errors e.g. The formatter threw an exception while trying to deserialize the message: 
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v11:Entities.
    elif hasattr(ex.fault, 'detail') \
        and hasattr(ex.fault.detail, 'ExceptionDetail'):
        api_errors=ex.fault.detail.ExceptionDetail
        if type(api_errors) == list:
            for api_error in api_errors:
                output_status_message(api_error.Message)
        else:
            output_status_message(api_errors.Message)
    else:
        raise Exception('Unknown WebFault')
        

# Ad Insight

def output_budget_opportunities(budget_opportunities, campaign_id):
    if budget_opportunities is not None and len(budget_opportunities) > 0:
        for budget_opportunity in budget_opportunities['BudgetOpportunity']:
            output_status_message("BudgetPoints: ")
            for budget_point in budget_opportunity.BudgetPoints['BudgetPoint']:
                output_budget_point(budget_point)
            output_status_message("BudgetType: {0}".format(budget_opportunity.BudgetType))
            output_status_message("CampaignId: {0}".format(budget_opportunity.CampaignId))
            output_status_message("CurrentBudget: {0}".format(budget_opportunity.CurrentBudget))
            output_status_message("IncreaseInClicks: {0}".format(budget_opportunity.IncreaseInClicks))
            output_status_message("IncreaseInImpressions: {0}".format(budget_opportunity.IncreaseInImpressions))
            output_status_message("OpportunityKey: {0}".format(budget_opportunity.OpportunityKey))
            output_status_message("PercentageIncreaseInClicks: {0}".format(budget_opportunity.PercentageIncreaseInClicks))
            output_status_message("PercentageIncreaseInImpressions: {0}".format(budget_opportunity.PercentageIncreaseInImpressions))
            output_status_message("RecommendedBudget: {0}".format(budget_opportunity.RecommendedBudget))
    else:
        output_status_message("There are no budget opportunities for CampaignId: {0}".format(campaign_id))

def output_budget_point(budget_point):
    if budget_point is not None:
        output_status_message("BudgetAmount: {0}".format(budget_point.BudgetAmount))
        output_status_message("BudgetPointType: {0}".format(budget_point.BudgetPointType))
        output_status_message("EstimatedWeeklyClicks: {0}".format(budget_point.EstimatedWeeklyClicks))
        output_status_message("EstimatedWeeklyCost: {0}".format(budget_point.EstimatedWeeklyCost))
        output_status_message("EstimatedWeeklyImpressions: {0}".format(budget_point.EstimatedWeeklyImpressions))


# Bulk

def output_percent_complete(progress):
    output_status_message("Percent Complete: {0}\n".format(progress.percent_complete))
   
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

def output_bulk_performance_data(performance_data):
    if performance_data is not None:
        output_status_message("AverageCostPerClick: {0}".format(performance_data.average_cost_per_click))
        output_status_message("AverageCostPerThousandImpressions: {0}".format(performance_data.average_cost_per_thousand_impressions))
        output_status_message("AveragePosition: {0}".format(performance_data.average_position))
        output_status_message("Clicks: {0}".format(performance_data.clicks))
        output_status_message("ClickThroughRate: {0}".format(performance_data.click_through_rate))
        output_status_message("Conversions: {0}".format(performance_data.conversions))
        output_status_message("CostPerConversion: {0}".format(performance_data.cost_per_conversion))
        output_status_message("Impressions: {0}".format(performance_data.impressions))
        output_status_message("Spend: {0}".format(performance_data.spend))

def output_bulk_campaigns(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaign: \n")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management Campaign Object
        output_campaign(entity.campaign)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_expanded_text_ads(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkExpandedTextAd: \n")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)

        # Output the Campaign Management ExpandedTextAd Object
        output_expanded_text_ad(entity.expanded_text_ad)

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
        output_status_message("BulkProductAd: \n")
        output_status_message("AdGroupId: {0}".format(entity.ad_group_id))
        output_status_message("AdGroupName: {0}".format(entity.ad_group_name))
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)

        # Output the Campaign Management ProductAd Object
        output_product_ad(entity.ad)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')


def output_bulk_keywords(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkKeyword: \n")
        output_status_message("AdGroup Id: {0}".format(entity.ad_group_id))
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)
        output_bulk_bid_suggestions(entity.bid_suggestions)

        # Output the Campaign Management Keyword Object
        output_keyword(entity.keyword)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_app_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAppAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management AppAdExtension Object
        output_app_ad_extension(entity.app_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_app_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignAppAdExtension: \n")
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
        output_status_message("BulkCallAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management CallAdExtension Object
        output_call_ad_extension(entity.call_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_call_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignCallAdExtension: \n")
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
        output_status_message("BulkCalloutAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management CalloutAdExtension Object
        output_callout_ad_extension(entity.callout_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_callout_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignCalloutAdExtension: \n")
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
        output_status_message("BulkLocationAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management LocationAdExtension Object
        output_location_ad_extension(entity.location_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_location_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignLocationAdExtension: \n")
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
        output_status_message("BulkReviewAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management ReviewAdExtension Object
        output_review_ad_extension(entity.review_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_review_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignReviewAdExtension: \n")
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
                
def output_bulk_site_link_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkSiteLinkAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management SiteLinksAdExtension Object
        output_site_links_ad_extension(entity.site_links_ad_extension)

        if entity.site_links is not None and len(entity.site_links) > 0:
            output_bulk_site_links(entity.site_links)

        output_status_message('')

def output_bulk_site_links(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkSiteLink: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        output_status_message("Ad Extension Id: {0}".format(entity.ad_extension_id))
        output_status_message("Client Id: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))
        output_status_message("Order: {0}".format(entity.order))
        output_status_message("Status: {0}".format(entity.status))
        output_status_message("Version: {0}".format(entity.version))
        
        # Output the Campaign Management SiteLink Object
        output_site_links([entity.site_link])

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_site_link_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignSiteLinkAdExtension: \n")
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

def output_bulk_sitelink2_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkSitelink2AdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management Sitelink2AdExtension Object
        output_sitelink2_ad_extension(entity.sitelink2_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_sitelink2_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignSitelink2AdExtension: \n")
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
        output_status_message("BulkStructuredSnippetAdExtension: \n")
        output_status_message("Account Id: {0}".format(entity.account_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management StructuredSnippetAdExtension Object
        output_structured_snippet_ad_extension(entity.structured_snippet_ad_extension)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_campaign_structured_snippet_ad_extensions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignStructuredSnippetAdExtension: \n")
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
        output_status_message("BulkRemarketingList: \n")
        output_status_message("Status: {0}".format(entity.status))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management RemarketingList Object
        output_remarketing_list(entity.remarketing_list)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_ad_group_remarketing_list_associations(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupRemarketingListAssociation: \n")
        output_status_message("AdGroup Name: {0}".format(entity.ad_group_name))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management BiddableAdGroupCriterion Object
        output_biddable_ad_group_criterion(entity.biddable_ad_group_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')


def output_bulk_budgets(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkBudget: \n")
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
        output_status_message("BulkCampaign: \n")
        output_status_message("AccountId: {0}".format(entity.account_id))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management Campaign Object
        output_campaign(entity.campaign)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_ad_groups(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroup: \n")
        output_status_message("Campaign Id: {0}".format(entity.campaign_id))
        output_status_message("Campaign Name: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        output_status_message("IsExpired: {0}".format(entity.is_expired))
        
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        output_bulk_performance_data(entity.performance_data)
        output_bulk_quality_score_data(entity.quality_score_data)

        # Output the Campaign Management AdGroup Object
        output_ad_group(entity.ad_group)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')

def output_bulk_ad_group_product_partitions(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkAdGroupProductPartition: \n")
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("AdGroupName: {0}".format(entity.ad_group_name))
        output_status_message("ClientId: {0}".format(entity.client_id))
        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # BulkAdGroupProductPartition can have either BiddableAdGroupCriterion or NegativeAdGroupCriterion
        if entity.ad_group_criterion is None:
            output_status_message("Criterion is null or invalid.\n")
        elif entity.ad_group_criterion.Type == 'BiddableAdGroupCriterion':
            # Output the Campaign Management BiddableAdGroupCriterion
            output_biddable_ad_group_criterion(entity.ad_group_criterion)
        elif entity.ad_group_criterion.Type == 'NegativeAdGroupCriterion':
            # Output the Campaign Management NegativeAdGroupCriterion
            output_negative_ad_group_criterion(entity.ad_group_criterion)
        else:
            output_status_message("Unknown ad group criterion type.\n")

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')
        
def output_bulk_campaign_product_scopes(bulk_entities):
    for entity in bulk_entities:
        output_status_message("BulkCampaignProductScope: \n")
        output_status_message("CampaignName: {0}".format(entity.campaign_name))
        output_status_message("ClientId: {0}".format(entity.client_id))

        if entity.last_modified_time is not None:
            output_status_message("LastModifiedTime: {0}".format(entity.last_modified_time))

        # Output the Campaign Management BiddableCampaignCriterion
        output_biddable_campaign_criterion(entity.biddable_campaign_criterion)

        if entity.has_errors:
            output_bulk_errors(entity.errors)

        output_status_message('')


# Campaign Management

def output_keyword(keyword):
    if keyword is not None:
        output_status_message("Bid.Amount: {0}".format(
            keyword.Amount if keyword.Bid is not None else None)
        )
        output_bidding_scheme(keyword.BiddingScheme)
        output_status_message("DestinationUrl: {0}".format(keyword.DestinationUrl))
        output_status_message("EditorialStatus: {0}".format(keyword.EditorialStatus))
        output_status_message("FinalMobileUrls: ")
        if keyword.FinalMobileUrls is not None:
            for final_mobile_url in keyword.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if keyword.FinalUrls is not None:
            for final_url in keyword.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("ForwardCompatibilityMap: ")
        if keyword.ForwardCompatibilityMap is not None and len(keyword.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in text_ad.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(keyword.Id))
        output_status_message("MatchType: {0}".format(keyword.MatchType))
        output_status_message("Param1: {0}".format(keyword.Param1))
        output_status_message("Param2: {0}".format(keyword.Param2))
        output_status_message("Param3: {0}".format(keyword.Param3))
        output_status_message("Status: {0}".format(keyword.Status))
        output_status_message("Text: {0}".format(keyword.Text))
        output_status_message("TrackingUrlTemplate: {0}".format(keyword.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if keyword.UrlCustomParameters is not None and keyword.UrlCustomParameters.Parameters is not None:
            for custom_parameter in keyword.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_negative_keyword_ids(id_collections):
    if not hasattr(id_collections, 'IdCollection'):
        return None
    for index in range(0, len(id_collections['IdCollection'])):
        output_status_message("NegativeKeyword Ids at entity index {0}:\n".format(index))
        for id in id_collections['IdCollection'][index].Ids['long']:
            output_status_message("\tId: {0}\n".format(id))

def output_entity_negative_keywords(entity_negative_keywords):
    if not hasattr(entity_negative_keywords, 'EntityNegativeKeyword'):
        return None
    output_status_message("EntityNegativeKeyword item:\n")
    for entity_negative_keyword in entity_negative_keywords['EntityNegativeKeyword']:
        output_status_message("\tEntityId: {0}".format(entity_negative_keyword.EntityId))
        output_status_message("\tEntityType: {0}\n".format(entity_negative_keyword.EntityType))
        output_negative_keywords(entity_negative_keyword.NegativeKeywords)
      

def output_negative_keywords(negative_keywords):
    if not hasattr(negative_keywords, 'NegativeKeyword'):
        return None
    output_status_message("NegativeKeyword item:\n")
    for negative_keyword in negative_keywords['NegativeKeyword']:
        output_status_message("\tText: {0}".format(negative_keyword.Text))
        output_status_message("\tId: {0}".format(negative_keyword.Id))
        output_status_message("\tMatchType: {0}\n".format(negative_keyword.MatchType))

def output_negative_keyword_results(
            shared_list_id,
            shared_list_items,
            shared_list_item_ids,
            partial_errors
        ):
    if not hasattr(shared_list_items, 'SharedListItem'):
        return None
    for index in range(0, len(shared_list_items['SharedListItem'])-1):
        # Determine if the SharedListItem is a NegativeKeyword.
        if shared_list_items['SharedListItem'][index].Type == 'NegativeKeyword':
            # Determine if the corresponding index has a valid identifier
            if shared_list_item_ids['long'][index] > 0:
                output_status_message(
                    "NegativeKeyword[{0}] ({1}) successfully added to NegativeKeywordList ({2}) and assigned Negative Keyword Id {3}.".format(
                        index,
                        shared_list_items['SharedListItem'][index].Text,
                        shared_list_id,
                        shared_list_item_ids['long'][index]
                    )
                )
            else:
                output_status_message("SharedListItem is not a NegativeKeyword.")
    output_partial_errors(partial_errors)

def output_shared_entity_associations(associations):
    if not hasattr(associations, 'SharedEntityAssociation'):
        return None
    output_status_message("SharedEntityAssociation item:\n")
    for shared_entity_association in associations['SharedEntityAssociation']:
        output_status_message("\tEntityId: {0}".format(shared_entity_association.EntityId))
        output_status_message("\tEntityType: {0}".format(shared_entity_association.EntityType))
        output_status_message("\tSharedEntityId: {0}".format(shared_entity_association.SharedEntityId))
        output_status_message("\tSharedEntityType: {0}\n".format(shared_entity_association.SharedEntityType))
    

def output_bidding_scheme(bidding_scheme):
    if bidding_scheme is None or type(bidding_scheme).__name__ == 'BiddingScheme':
        return
    elif type(bidding_scheme).__name__ == 'EnhancedCpcBiddingScheme':
        output_status_message("BiddingScheme: EnhancedCpc")
    elif type(bidding_scheme).__name__ == 'InheritFromParentBiddingScheme':
        output_status_message("BiddingScheme: InheritFromParent")
    elif type(bidding_scheme).__name__ == 'MaxConversionsBiddingScheme':
        output_status_message("BiddingScheme: MaxConversions")
    elif type(bidding_scheme).__name__ == 'ManualCpcBiddingScheme':
        output_status_message("BiddingScheme: ManualCpc")
    elif type(bidding_scheme).__name__ == 'TargetCpaBiddingScheme':
        output_status_message("BiddingScheme: TargetCpa")
    elif type(bidding_scheme).__name__ == 'MaxClicksBiddingScheme':
        output_status_message("BiddingScheme: MaxClicks")

def output_ids(ids):
    for id in ids['long']:
        output_status_message("Id {0}".format(id))
    output_status_message('')

def output_campaign(campaign):
    if campaign is not None:
        output_status_message("BudgetType: {0}".format(campaign.BudgetType))
        output_status_message("CampaignType: {0}".format(campaign.CampaignType))
        output_status_message("DailyBudget: {0}".format(campaign.DailyBudget))
        output_status_message("Description: {0}".format(campaign.Description))
        output_status_message("ForwardCompatibilityMap: ")
        if campaign.ForwardCompatibilityMap is not None and len(campaign.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in campaign.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(campaign.Id))
        output_status_message("Name: {0}".format(campaign.Name))
        output_status_message("NativeBidAdjustment: {0}".format(campaign.NativeBidAdjustment))
        if campaign.Settings is not None:
            output_status_message("Settings: ")
            for setting in campaign.Settings['Setting']:
                if setting.Type == 'ShoppingSetting':
                    output_status_message("\tShoppingSetting: ")
                    output_status_message("\t\tPriority: {0}".format(setting.Priority))
                    output_status_message("\t\tSalesCountryCode: {0}".format(setting.SalesCountryCode))
                    output_status_message("\t\tStoreId: {0}".format(setting.StoreId))
        output_status_message("Status: {0}".format(campaign.Status))
        output_status_message("TimeZone: {0}".format(campaign.TimeZone))
        output_status_message("TrackingUrlTemplate: {0}".format(campaign.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if campaign.UrlCustomParameters is not None and campaign.UrlCustomParameters.Parameters is not None:
            for custom_parameter in campaign.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))
        output_status_message('')

def output_budget(budget):
    if budget is not None:
        output_status_message("Amount: {0}".format(budget.Amount))
        output_status_message("AssociationCount: {0}".format(budget.AssociationCount))
        output_status_message("BudgetType: {0}".format(budget.BudgetType))
        output_status_message("Id: {0}".format(budget.Id))
        output_status_message("Name: {0}\n".format(budget.Name))

def output_ad_group(ad_group):
    if ad_group is not None:
        output_status_message("AdDistribution: {0}".format(ad_group.AdDistribution))
        output_status_message("AdRotation: {0}".format(
            ad_group.AdRotation.Type if ad_group.AdRotation is not None else None)
        )
        output_bidding_scheme(ad_group.BiddingScheme)
        output_status_message("ForwardCompatibilityMap: ")
        if ad_group.ForwardCompatibilityMap is not None and len(ad_group.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in ad_group.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(ad_group.Id))
        output_status_message("Language: {0}".format(ad_group.Language))
        output_status_message("Name: {0}".format(ad_group.Name))
        output_status_message("NativeBidAdjustment: {0}".format(ad_group.NativeBidAdjustment))
        output_status_message("Network: {0}".format(ad_group.Network))
        output_status_message("RemarketingTargetingSetting: {0}".format(ad_group.RemarketingTargetingSetting))
        output_status_message("SearchBid: {0}".format(
            ad_group.SearchBid.Amount if ad_group.SearchBid is not None else None)
        )
        output_status_message("Status: {0}".format(ad_group.Status))
        output_status_message("TrackingUrlTemplate: {0}".format(ad_group.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if ad_group.UrlCustomParameters is not None and ad_group.UrlCustomParameters.Parameters is not None:
            for custom_parameter in ad_group.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))


def output_ad(ad):
    if ad is not None:
        output_status_message("DevicePreference: {0}".format(ad.DevicePreference))
        output_status_message("EditorialStatus: {0}".format(ad.EditorialStatus))
        output_status_message("FinalMobileUrls: ")
        if ad.FinalMobileUrls is not None:
            for final_mobile_url in ad.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if ad.FinalUrls is not None:
            for final_url in ad.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("ForwardCompatibilityMap: ")
        if ad.ForwardCompatibilityMap is not None and len(ad.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in ad.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(ad.Id))
        output_status_message("Status: {0}".format(ad.Status))
        output_status_message("TrackingUrlTemplate: {0}".format(ad.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if ad.UrlCustomParameters is not None and ad.UrlCustomParameters.Parameters is not None:
            for custom_parameter in ad.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_expanded_text_ad(ad):
    if ad is not None:
        # Output inherited properties of the Ad base class.
        output_ad(ad)
            
        # Output properties that are specific to the ExpandedTextAd
        output_status_message("DisplayUrl: {0}".format(ad.DisplayUrl))
        output_status_message("Path1: {0}".format(ad.Path1))
        output_status_message("Path2: {0}".format(ad.Path2))
        output_status_message("Text: {0}".format(ad.Text))
        output_status_message("TitlePart1: {0}".format(ad.TitlePart1))
        output_status_message("TitlePart2: {0}".format(ad.TitlePart2))
     

def output_product_ad(ad):
    if ad is not None:
        # Output inherited properties of the Ad base class.
        output_ad(ad)
            
        # Output properties that are specific to the ExpandedTextAd
        output_status_message("PromotionalText: {0}".format(ad.PromotionalText))
        
def output_ad_extensions(ad_extensions, ad_extension_editorial_reason_collection):
    if not ad_extensions:
        return None
    index=0
    for extension in ad_extensions['AdExtension']:
        if extension is None or extension.Id is None:
            output_status_message('Extension is empty or invalid.')
        else:
            if extension.Type == 'AppAdExtension':
                output_app_ad_extension(extension)
            elif extension.Type == 'CallAdExtension':
                output_call_ad_extension(extension)
            elif extension.Type == 'CalloutAdExtension':
                output_callout_ad_extension(extension)
            elif extension.Type == 'ImageAdExtension':
                output_image_ad_extension(extension)
            elif extension.Type == 'LocationAdExtension':
                output_location_ad_extension(extension)
            elif extension.Type == 'ReviewAdExtension':
                output_review_ad_extension(extension)
            elif extension.Type == 'SiteLinksAdExtension':
                output_site_links_ad_extension(extension)
            elif extension.Type == 'Sitelink2AdExtension':
                output_sitelink2_ad_extension(extension)
            elif extension.Type == 'StructuredSnippetAdExtension':
                output_structured_snippet_ad_extension(extension)
            else:
                output_status_message("Unknown extension type")

        if hasattr(ad_extension_editorial_reason_collection, 'Reasons'):

            # Print any editorial rejection reasons for the corresponding extension. This example 
            # assumes the same list index for adExtensions and adExtensionEditorialReasonCollection
            # as defined above.

            for ad_extension_editorial_reason \
            in ad_extension_editorial_reason_collection.Reasons['AdExtensionEditorialReason']:
            
                if ad_extension_editorial_reason is not None \
                and ad_extension_editorial_reason.PublisherCountries is not None:

                    output_status_message("Editorial Rejection Location: {0}".format(ad_extension_editorial_reason.Location))
                    output_status_message("Editorial Rejection PublisherCountries: ")
                    for publisher_country in ad_extension_editorial_reason.PublisherCountries['string']:
                        output_status_message("  " + publisher_country)
                    
                    output_status_message("Editorial Rejection ReasonCode: {0}".format(ad_extension_editorial_reason.ReasonCode))
                    output_status_message("Editorial Rejection Term: {0}".format(ad_extension_editorial_reason.Term))
                              
        index=index+1

    output_status_message('')

def output_ad_extension(extension):
    if extension is not None:
        output_status_message("Id: {0}".format(extension.Id))
        output_status_message("Type: {0}".format(extension.Type))
        output_status_message("ForwardCompatibilityMap: ")
        if extension.ForwardCompatibilityMap is not None:
            for pair in extension.ForwardCompatibilityMap['KeyValuePairOfstringstring']:
                output_status_message("Key: {0}".format(pair.Key))
                output_status_message("Value: {0}".format(pair.Value))
        output_status_message("Scheduling: ")
        # Scheduling is not emitted by default, so we must first test whether it exists.
        if hasattr(extension, 'Scheduling') and extension.Scheduling is not None:
            output_schedule(extension.Scheduling)
        output_status_message("Status: {0}".format(extension.Status))
        output_status_message("Version: {0}".format(extension.Version))

def output_schedule(schedule):
    if schedule is not None:
        if schedule.DayTimeRanges is not None:
            for day_time in schedule.DayTimeRanges['DayTime']:
                output_status_message("Day: {0}".format(day_time.Day))
                output_status_message("EndHour: {0}".format(day_time.EndHour))
                output_status_message("EndMinute: {0}".format(day_time.EndMinute))
                output_status_message("StartHour: {0}".format(day_time.StartHour))
                output_status_message("StartMinute: {0}".format(day_time.StartMinute))
        if schedule.EndDate is not None:
            output_status_message(("EndDate: {0}/{1}/{2}".format( 
            schedule.EndDate.Month,
            schedule.EndDate.Day,
            schedule.EndDate.Year)))
        if schedule.StartDate is not None:
            output_status_message(("StartDate: {0}/{1}/{2}".format(
            schedule.StartDate.Month,
            schedule.StartDate.Day,
            schedule.StartDate.Year)))
        use_searcher_time_zone = \
            True if (schedule.UseSearcherTimeZone is not None and schedule.UseSearcherTimeZone == True) else False
        output_status_message("UseSearcherTimeZone: {0}".format(use_searcher_time_zone))

def output_app_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the AppAdExtension
        output_status_message("AppPlatform: {0}".format(extension.AppPlatform))
        output_status_message("AppStoreId: {0}".format(extension.AppStoreId))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("DisplayText: {0}".format(extension.DisplayText))

def output_call_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the CallAdExtension
        output_status_message("CountryCode: {0}".format(extension.CountryCode))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("IsCallOnly: {0}".format(extension.IsCallOnly))
        output_status_message("IsCallTrackingEnabled: {0}".format(extension.IsCallTrackingEnabled))
        output_status_message("PhoneNumber: {0}".format(extension.PhoneNumber))
        output_status_message("RequireTollFreeTrackingNumber: {0}".format(extension.RequireTollFreeTrackingNumber))

def output_callout_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the CalloutAdExtension
        output_status_message("Callout Text: {0}".format(extension.Text))

def output_image_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the ImageAdExtension
        output_status_message("AlternativeText: {0}".format(extension.AlternativeText))
        output_status_message("Description: {0}".format(extension.Description))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("FinalMobileUrls: ")
        if extension.FinalMobileUrls is not None:
            for final_mobile_url in extension.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if extension.FinalUrls is not None:
            for final_url in extension.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("ImageMediaIds: ")
        if extension.ImageMediaIds is not None:
            for id in extension.ImageMediaIds['string']:
                output_status_message("\t{0}".format(id))
        output_status_message("TrackingUrlTemplate: {0}".format(extension.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if extension.UrlCustomParameters is not None and extension.UrlCustomParameters.Parameters is not None:
            for custom_parameter in extension.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_location_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the LocationAdExtension
        if extension.Address is not None:
            output_status_message("CityName: {0}".format(extension.Address.CityName))
            output_status_message("CountryCode: {0}".format(extension.Address.CountryCode))
            output_status_message("PostalCode: {0}".format(extension.Address.PostalCode))
            output_status_message("ProvinceCode: {0}".format(extension.Address.ProvinceCode))
            output_status_message("ProvinceName: {0}".format(extension.Address.ProvinceName))
            output_status_message("StreetAddress: {0}".format(extension.Address.StreetAddress))
            output_status_message("StreetAddress2: {0}".format(extension.Address.StreetAddress2))
        output_status_message("CompanyName: {0}".format(extension.CompanyName))
        output_status_message("GeoCodeStatus: {0}".format(extension.GeoCodeStatus))
        if extension.GeoPoint is not None:
            output_status_message("GeoPoint: ")
            output_status_message("LatitudeInMicroDegrees: {0}".format(extension.GeoPoint.LatitudeInMicroDegrees))
            output_status_message("LongitudeInMicroDegrees: {0}".format(extension.GeoPoint.LongitudeInMicroDegrees))
        output_status_message("IconMediaId: {0}".format(extension.IconMediaId))
        output_status_message("ImageMediaId: {0}".format(extension.ImageMediaId))
        output_status_message("PhoneNumber: {0}".format(extension.PhoneNumber))

def output_review_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the ReviewAdExtension
        output_status_message("IsExact: {0}".format(extension.IsExact))
        output_status_message("Source: {0}".format(extension.Source))
        output_status_message("Text: {0}".format(extension.Text))
        output_status_message("Url: {0}".format(extension.Url))

def output_structured_snippet_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the StructuredSnippetAdExtension
        output_status_message("Header: {0}".format(extension.Header))
        for value in extension.Values['string']:
            output_status_message("\t{0}".format(value))
        
def output_site_links_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the SiteLinksAdExtension
        output_site_links(extension.SiteLinks['SiteLink'])

def output_site_links(site_links):
    if site_links is not None:
        for site_link in site_links:
            output_status_message("Description1: {0}".format(site_link.Description1))
            output_status_message("Description2: {0}".format(site_link.Description2))
            output_status_message("DevicePreference: {0}".format(site_link.DevicePreference))
            output_status_message("DisplayText: {0}".format(site_link.DisplayText))
            output_status_message("DestinationUrl: {0}".format(site_link.DestinationUrl))
            output_status_message("FinalMobileUrls: ")
            if site_link.FinalMobileUrls is not None:
                for final_mobile_url in site_link.FinalMobileUrls['string']:
                    output_status_message("\t{0}".format(final_mobile_url))
            output_status_message("FinalUrls: ")
            if site_link.FinalUrls is not None:
                for final_url in site_link.FinalUrls['string']:
                    output_status_message("\t{0}".format(final_url))
            output_status_message("TrackingUrlTemplate: {0}".format(site_link.TrackingUrlTemplate))
            output_status_message("UrlCustomParameters: ")
            if site_link.UrlCustomParameters is not None and site_link.UrlCustomParameters.Parameters is not None:
                for custom_parameter in site_link.UrlCustomParameters.Parameters['CustomParameter']:
                    output_status_message("\tKey: {0}".format(custom_parameter.Key))
                    output_status_message("\tValue: {0}".format(custom_parameter.Value))
            
def output_sitelink2_ad_extension(extension):
    if extension is not None:
        # Output inherited properties of the AdExtension base class.
        output_ad_extension(extension)

        # Output properties that are specific to the Sitelink2AdExtension
        output_status_message("Description1: {0}".format(extension.Description1))
        output_status_message("Description2: {0}".format(extension.Description2))
        output_status_message("DevicePreference: {0}".format(extension.DevicePreference))
        output_status_message("DisplayText: {0}".format(extension.DisplayText))
        output_status_message("DestinationUrl: {0}".format(extension.DestinationUrl))
        output_status_message("FinalMobileUrls: ")
        if extension.FinalMobileUrls is not None:
            for final_mobile_url in extension.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if extension.FinalUrls is not None:
            for final_url in extension.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("TrackingUrlTemplate: {0}".format(extension.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if extension.UrlCustomParameters is not None and extension.UrlCustomParameters.Parameters is not None:
            for custom_parameter in extension.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))

def output_account_migration_statuses_info(account_migration_statuses_info):
    if account_migration_statuses_info is not None:
        output_status_message("AccountId: {0}".format(account_migration_statuses_info.AccountId))
        for migration_status_info in account_migration_statuses_info['MigrationStatusInfo']:
            output_migration_status_info(migration_status_info)
            
def output_migration_status_info(migration_status_info):
    if migration_status_info is not None and migration_status_info[1] is not None:
        output_status_message("MigrationType: {0}".format(migration_status_info[1][0].MigrationType))
        output_status_message("StartTimeInUtc: {0}".format(migration_status_info[1][0].StartTimeInUtc))
        output_status_message("Status: {0}".format(migration_status_info[1][0].Status))

def output_audience(audience):
    if audience is not None:
        output_status_message("Description: {0}".format(audience.Description))
        output_status_message("ForwardCompatibilityMap: ")
        if audience.ForwardCompatibilityMap is not None and len(audience.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
            for pair in audience.ForwardCompatibilityMap:
                output_status_message("Key: {0}".format(pair.key))
                output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(audience.Id))
        output_status_message("MembershipDuration: {0}".format(audience.MembershipDuration))
        output_status_message("Name: {0}".format(audience.Name))
        output_status_message("ParentId: {0}".format(audience.ParentId))
        output_status_message("Scope: {0}".format(audience.Scope))

def output_remarketing_list(remarketing_list):
    if remarketing_list is not None:
        # Output inherited properties of the Audience base class.
        output_audience(remarketing_list)

        # Output properties that are specific to the RemarketingList        
        output_status_message("TagId: {0}".format(remarketing_list.TagId))
        output_remarketing_rule(remarketing_list.Rule)

def output_remarketing_rule(remarketing_rule):
    if remarketing_rule is not None:    
        if remarketing_rule.Type == 'CustomEvents':
            output_status_message("Action: {0}".format(remarketing_rule.Action))
            output_status_message("ActionOperator: {0}".format(remarketing_rule.ActionOperator))
            output_status_message("Operator: {0}".format(remarketing_rule.Category))
            output_status_message("CategoryOperator: {0}".format(remarketing_rule.CategoryOperator))
            output_status_message("Operator: {0}".format(remarketing_rule.Label))
            output_status_message("LabelOperator: {0}".format(remarketing_rule.LabelOperator))
            output_status_message("Operator: {0}".format(remarketing_rule.Value))
            output_status_message("ValueOperator: {0}".format(remarketing_rule.ValueOperator))
        elif remarketing_rule.Type == 'PageVisitors':
            if remarketing_rule.RuleItemGroups is not None:
                output_status_message("RuleItemGroups: ")
                output_rule_item_groups(remarketing_rule.RuleItemGroups)
        elif remarketing_rule.Type == 'PageVisitorsWhoDidNotVisitAnotherPage':
            if remarketing_rule.ExcludeRuleItemGroups is not None:
                output_status_message("ExcludeRuleItemGroups: ")
                output_rule_item_groups(remarketing_rule.ExcludeRuleItemGroups)
            if remarketing_rule.IncludeRuleItemGroups is not None:
                output_status_message("IncludeRuleItemGroups: ")
                output_rule_item_groups(remarketing_rule.IncludeRuleItemGroups)
        elif remarketing_rule.Type == 'PageVisitorsWhoVisitedAnotherPage':
            if remarketing_rule.AnotherRuleItemGroups is not None:
                output_status_message("AnotherRuleItemGroups: ")
                output_rule_item_groups(remarketing_rule.AnotherRuleItemGroups)
            if remarketing_rule.RuleItemGroups is not None:
                output_status_message("RuleItemGroups: ")
                output_rule_item_groups(remarketing_rule.RuleItemGroups)
        else:
            output_status_message("Unknown remarketing rule type.\n")

def output_rule_item_groups(rule_item_groups):
    if rule_item_groups is not None:
        for rule_item_group in rule_item_groups['RuleItemGroup']:
            if rule_item_group.Items is not None:
                for rule_item in rule_item_group.Items['RuleItem']:
                    if rule_item is not None and rule_item.Type == 'String':
                        output_status_message("\tOperand: {0}".format(rule_item.Operand))
                        output_status_message("\tOperator: {0}".format(rule_item.Operator))
                        output_status_message("\tValue: {0}".format(rule_item.Value))
                    else:
                        output_status_message("Unknown remarketing rule item type.\n")

def output_uet_tag(uet_tag):
    if uet_tag is not None:
        output_status_message("Description: {0}".format(uet_tag.Description))
        output_status_message("Id: {0}".format(uet_tag.Id))
        output_status_message("Name: {0}".format(uet_tag.Name))
        output_status_message("TrackingNoScript: {0}".format(uet_tag.TrackingNoScript))
        output_status_message("TrackingScript: {0}".format(uet_tag.TrackingScript))
        output_status_message("TrackingStatus: {0}\n".format(uet_tag.TrackingStatus))
    
def output_conversion_goal(conversion_goal):
    if conversion_goal is not None:
        output_status_message("ConversionWindowInMinutes: {0}".format(conversion_goal.ConversionWindowInMinutes))
        output_status_message("CountType: {0}".format(conversion_goal.CountType))
        output_status_message("Id: {0}".format(conversion_goal.Id))
        output_status_message("Name: {0}".format(conversion_goal.Name))
        output_conversion_goal_revenue(conversion_goal.Revenue)
        output_status_message("Scope: {0}".format(conversion_goal.Scope))
        output_status_message("Status: {0}".format(conversion_goal.Status))
        output_status_message("TagId: {0}".format(conversion_goal.TagId))
        output_status_message("TrackingStatus: {0}".format(conversion_goal.TrackingStatus))
        output_status_message("Type: {0}".format(conversion_goal.Type))

        if conversion_goal.Type == 'AppInstall':
            output_status_message("AppPlatform: {0}".format(conversion_goal.AppPlatform))
            output_status_message("AppStoreId: {0}\n".format(conversion_goal.AppStoreId))
        elif conversion_goal.Type == 'Duration':
            output_status_message("MinimumDurationInSeconds: {0}\n".format(conversion_goal.MinimumDurationInSeconds))
        elif conversion_goal.Type == 'Event':
            output_status_message("ActionExpression: {0}".format(conversion_goal.ActionExpression))
            output_status_message("ActionOperator: {0}".format(conversion_goal.ActionOperator))
            output_status_message("CategoryExpression: {0}".format(conversion_goal.CategoryExpression))
            output_status_message("CategoryOperator: {0}".format(conversion_goal.CategoryOperator))
            output_status_message("LabelExpression: {0}".format(conversion_goal.LabelExpression))
            output_status_message("LabelOperator: {0}".format(conversion_goal.LabelOperator))
            output_status_message("Value: {0}".format(conversion_goal.Value))
            output_status_message("ValueOperator: {0}\n".format(conversion_goal.ValueOperator))
        elif conversion_goal.Type == 'PagesViewedPerVisit':
            output_status_message("MinimumPagesViewed: {0}\n".format(conversion_goal.MinimumPagesViewed))
        elif conversion_goal.Type == 'Url':
            output_status_message("UrlExpression: {0}".format(conversion_goal.UrlExpression))
            output_status_message("UrlOperator: {0}\n".format(conversion_goal.UrlOperator))

def output_conversion_goal_revenue(conversion_goal_revenue):
    if conversion_goal_revenue is not None:
        output_status_message("CurrencyCode: {0}".format(conversion_goal_revenue.CurrencyCode))
        output_status_message("Type: {0}".format(conversion_goal_revenue.Type))
        output_status_message("Value: {0}".format(conversion_goal_revenue.Value))
                                             
def output_biddable_ad_group_criterion(ad_group_criterion):
    if ad_group_criterion is not None:
        # Output inherited properties of the AdGroupCriterion base class.
        output_ad_group_criterion(ad_group_criterion)

        # Output properties that are specific to the BiddableAdGroupCriterion
        output_criterion_bid(ad_group_criterion.CriterionBid)

        output_status_message("DestinationUrl: {0}".format(ad_group_criterion.DestinationUrl))
        if ad_group_criterion.EditorialStatus is not None:
            output_status_message("EditorialStatus: {0}".format(ad_group_criterion.EditorialStatus['value']))
        output_status_message("FinalMobileUrls: ")
        if ad_group_criterion.FinalMobileUrls is not None:
            for final_mobile_url in ad_group_criterion.FinalMobileUrls['string']:
                output_status_message("\t{0}".format(final_mobile_url))
        output_status_message("FinalUrls: ")
        if ad_group_criterion.FinalUrls is not None:
            for final_url in ad_group_criterion.FinalUrls['string']:
                output_status_message("\t{0}".format(final_url))
        output_status_message("TrackingUrlTemplate: {0}".format(ad_group_criterion.TrackingUrlTemplate))
        output_status_message("UrlCustomParameters: ")
        if ad_group_criterion.UrlCustomParameters is not None and ad_group_criterion.UrlCustomParameters.Parameters is not None:
            for custom_parameter in ad_group_criterion.UrlCustomParameters.Parameters['CustomParameter']:
                output_status_message("\tKey: {0}".format(custom_parameter.Key))
                output_status_message("\tValue: {0}".format(custom_parameter.Value))
              
def output_negative_ad_group_criterion(ad_group_criterion):
    if ad_group_criterion is not None:
        # Output inherited properties of the AdGroupCriterion base class.
        output_ad_group_criterion(ad_group_criterion)
         
        # There aren't any properties that are specific to the NegativeAdGroupCriterion  

def output_ad_group_criterions(ad_group_criterions):
    for ad_group_criterion in ad_group_criterions['AdGroupCriterion']:
        if ad_group_criterion is None:
            output_status_message("Criterion is null or invalid.\n")
        elif ad_group_criterion.Type == 'BiddableAdGroupCriterion':
            output_biddable_ad_group_criterion(ad_group_criterion)
        elif ad_group_criterion.Type == 'NegativeAdGroupCriterion':
            output_negative_ad_group_criterion(ad_group_criterion)
        else:
            output_status_message("Unknown ad group criterion type.\n")
        
def output_ad_group_criterion(ad_group_criterion):
    if ad_group_criterion is not None:
        output_status_message("AdGroupId: {0}".format(ad_group_criterion.AdGroupId))
        output_criterion(ad_group_criterion.Criterion)   
        output_status_message("Id: {0}".format(ad_group_criterion.Id))
        output_status_message("Status: {0}".format(ad_group_criterion.Status))
        output_status_message("AdGroupCriterion Type: {0}".format(ad_group_criterion.Type))        
        
def output_biddable_campaign_criterion(campaign_criterion):
    if campaign_criterion is not None:
        # Output inherited properties of the CampaignCriterion base class.
        output_campaign_criterion(campaign_criterion)

        # Output properties that are specific to the BiddableCampaignCriterion
        output_criterion_bid(campaign_criterion.CriterionBid)
                      
def output_negative_campaign_criterion(campaign_criterion):
    if campaign_criterion is not None:
        # Output inherited properties of the CampaignCriterion base class.
        output_campaign_criterion(campaign_criterion)
         
        # There aren't any properties that are specific to the NegativeCampaignCriterion  

def output_campaign_criterions(campaign_criterions):
    for campaign_criterion in campaign_criterions['CampaignCriterion']:
        if campaign_criterion is None:
            output_status_message("Criterion is null or invalid.\n")
        elif campaign_criterion.Type == 'BiddableCampaignCriterion':
            output_biddable_campaign_criterion(campaign_criterion)
        elif campaign_criterion.Type == 'NegativeCampaignCriterion':
            output_negative_campaign_criterion(campaign_criterion)
        else:
            output_status_message("Unknown ad group criterion type.\n")
        
def output_campaign_criterion(campaign_criterion):
    if campaign_criterion is not None:
        output_status_message("CampaignId: {0}".format(campaign_criterion.CampaignId))
        output_criterion(campaign_criterion.Criterion) 
        if campaign_criterion.ForwardCompatibilityMap is not None and len(campaign_criterion.ForwardCompatibilityMap.KeyValuePairOfstringstring) > 0:
           for pair in campaign_criterion.ForwardCompatibilityMap:
               output_status_message("Key: {0}".format(pair.key))
               output_status_message("Value: {0}".format(pair.value))
        output_status_message("Id: {0}".format(campaign_criterion.Id))
        output_status_message("Status: {0}".format(campaign_criterion.Status))
        output_status_message("CampaignCriterion Type: {0}".format(campaign_criterion.Type))        
        
def output_criterion(criterion):
    if criterion is not None:
        output_status_message("Criterion Type: {0}".format(criterion.Type))
        if criterion.Type == 'ProductPartition':
            output_product_partition(criterion)
        elif criterion.Type == 'ProductScope':
            output_product_scope(criterion)
        elif criterion.Type == 'Webpage':
            output_webpage(criterion)
        elif criterion.Type == 'AudienceCriterion':
            output_audience_criterion(criterion)
        else:
            output_status_message("Unknown criterion type.\n")

def output_product_partition(criterion):
    if criterion is not None:
        output_status_message("ParentCriterionId: {0}".format(criterion.ParentCriterionId))
        output_status_message("PartitionType: {0}".format(criterion.PartitionType))
        if criterion.Condition is not None:
            output_status_message("Operand: {0}".format(criterion.Condition.Operand))
            output_status_message("Attribute: {0}".format(criterion.Condition.Attribute))
        
def output_product_scope(criterion):
    if criterion is not None:
        output_status_message("Product Conditions:")
        if criterion.Conditions is not None and len(criterion.Conditions) > 0:
            for condition in criterion.Conditions['ProductCondition']:
                output_status_message("Operand: {0}".format(condition.Operand))
                output_status_message("Attribute: {0}".format(condition.Attribute))

def output_webpage(criterion):
    if criterion is not None \
        and criterion.Parameter is not None \
        and criterion.Parameter.Conditions is not None \
        and len(criterion.Parameter.Conditions) > 0:

        output_status_message("Webpage CriterionName: {0}".format(criterion.Parameter.CriterionName))
        output_status_message("Webpage Conditions:")
        for condition in criterion.Conditions['WebpageCondition']:
            output_status_message("Operand: {0}".format(condition.Operand))
            output_status_message("Argument: {0}".format(condition.Argument))
            
def output_audience_criterion(criterion):
    if criterion is not None:
        output_status_message("AudienceId: {0}".format(criterion.AudienceId))
        output_status_message("AudienceType: {0}".format(criterion.AudienceType))
        
def output_criterion_bid(criterion_bid):
    if criterion_bid is not None:
        output_status_message("CriterionBid Type: {0}".format(criterion_bid.Type))
        if criterion_bid.Type == 'FixedBid':
            output_fixed_bid(criterion_bid)
        elif criterion_bid.Type == 'BidMultiplier':
            output_bid_multiplier(criterion_bid)

def output_fixed_bid(criterion_bid):
    if criterion_bid is not None:
        output_status_message("Fixed Bid Amount: {0}".format(criterion_bid.Amount))

def output_bid_multiplier(criterion_bid):
    if criterion_bid is not None:
        output_status_message("Bid Multiplier: {0}".format(criterion_bid.Multiplier))

def output_fixed_bid(fixed_bid):
    if fixed_bid is not None:
        output_status_message("Amount: {0}".format(fixed_bid.Amount))

def output_product_partition(product_partition):
    if product_partition is not None:
        output_status_message("ParentCriterionId: {0}".format(product_partition.ParentCriterionId))
        output_status_message("PartitionType: {0}".format(product_partition.PartitionType))
        if product_partition.Condition is not None:
            output_status_message("Condition: ")
            output_status_message("Operand: {0}".format(product_partition.Condition.Operand))
            output_status_message("Attribute: {0}".format(product_partition.Condition.Attribute))
      
# Customer Management


def output_client_links(client_links):
    if hasattr(client_links, 'ClientLink'):
        for client_link in client_links['ClientLink']:
            output_status_message("Status: {0}".format(client_link.Status))
            output_status_message("ClientAccountId: {0}".format(client_link.ClientAccountId))
            output_status_message("ClientAccountNumber: {0}".format(client_link.ClientAccountNumber))
            output_status_message("ManagingAgencyCustomerId: {0}".format(client_link.ManagingCustomerId))
            output_status_message("ManagingCustomerNumber: {0}".format(client_link.ManagingCustomerNumber))
            output_status_message("IsBillToClient: True" if client_link.IsBillToClient else "IsBillToClient: False")
            output_status_message("InviterEmail: {0}".format(client_link.InviterEmail))
            output_status_message("InviterName: {0}".format(client_link.InviterName))
            output_status_message("InviterPhone: {0}".format(client_link.InviterPhone))
            output_status_message("LastModifiedByUserId: {0}".format(client_link.LastModifiedByUserId))
            output_status_message("LastModifiedDateTime: {0}".format(client_link.LastModifiedDateTime))
            output_status_message("Name: {0}".format(client_link.Name))
            output_status_message("Note: {0}".format(client_link.Note))
            output_status_message('')

def output_user_invitations(user_invitations):
    if user_invitations is None:
        return

    for user_invitation in user_invitations:
        output_status_message("FirstName: {0}".format(user_invitation.FirstName))
        output_status_message("LastName: {0}".format(user_invitation.LastName))
        output_status_message("Email: {0}".format(user_invitation.Email))
        output_status_message("Role: {0}".format(user_invitation.Role))
        output_status_message("Invitation Id: {0}\n".format(user_invitation.Id))

def output_user(user):
    output_status_message("User Id {0}".format(user.Id))
    output_status_message("UserName {0}".format(user.UserName))
    output_status_message("First Name {0}".format(user.Name.FirstName))
    output_status_message("Last Name {0}\n".format(user.Name.LastName))

def output_user_roles(roles):
    for role in roles:
        if role == 16:
            output_status_message("16 - The user has the Advertiser Campaign Manager role.")
        elif role == 33:
            output_status_message("33 - The user has the Aggregator role.")
        elif role == 41:
            output_status_message("41 - The user has the Super Admin role.")
        elif role == 100:
            output_status_message("100 - The user has the Viewer role.")
        elif role == 203:
            output_status_message("203 - The user has the Standard role.")
        else:
            output_status_message("{0} - The user has a deprecated, internal, or unknown user role.".format(role))
    output_status_message('')

def output_account(account):
    if account is None:
        return None
    
    output_status_message("Account Id {0}".format(account.Id))
    output_status_message("Account Number {0}".format(account.Number))
    output_status_message("Account Name {0}".format(account.Name))
    output_status_message("Account Parent Customer Id: {0}\n".format(account.ParentCustomerId))
