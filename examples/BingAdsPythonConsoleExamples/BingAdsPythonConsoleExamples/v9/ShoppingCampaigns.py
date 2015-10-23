from bingads import *

import sys
import webbrowser
from time import gmtime, strftime
from suds import WebFault

# Optionally you can include logging to output traffic, for example the SOAP request and response.

#import logging
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('suds.client').setLevel(logging.DEBUG)


if __name__ == '__main__':
    print("Python loads the web service proxies at runtime, so you will observe " \
          "a performance delay between program launch and main execution...\n")

    ENVIRONMENT='production'
    DEVELOPER_TOKEN='YourDeveloperTokenGoesHere'
    CLIENT_ID='YourClientIdGoesHere'    

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
        version=9,
    )

    customer_service=ServiceClient(
        'CustomerManagementService', 
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
        version=9,
    )
        

def authenticate_with_username():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with PasswordAuthentication.
    '''
    global authorization_data
    authentication=PasswordAuthentication(
        user_name='UserNameGoesHere',
        password='PasswordGoesHere'
    )

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication

def authenticate_with_oauth():
    ''' 
    Sets the authentication property of the global AuthorizationData instance with OAuthDesktopMobileAuthCodeGrant.
    '''
    global authorization_data
    authentication=OAuthDesktopMobileAuthCodeGrant(
        client_id=CLIENT_ID
    )

    # Assign this authentication instance to the global authorization_data. 
    authorization_data.authentication=authentication   

    # Register the callback function to automatically save the refresh token anytime it is refreshed.
    # Uncomment this line if you want to store your refresh token. Be sure to save your refresh token securely.
    authorization_data.authentication.token_refreshed_callback=save_refresh_token
    
    refresh_token=get_refresh_token()
    
    # If we have a refresh token let's refresh it
    if refresh_token is not None:
        authentication.request_oauth_tokens_by_refresh_token(refresh_token)
    else:
        webbrowser.open(authentication.get_authorization_endpoint(), new=1)
        # For Python 3.x use 'input' instead of 'raw_input'
        if(sys.version_info.major >= 3):
            response_uri=input(
                "You need to provide consent for the application to access your Bing Ads accounts. " \
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )
        else:
            response_uri=raw_input(
                "You need to provide consent for the application to access your Bing Ads accounts. " \
                "After you have granted consent in the web browser for the application to access your Bing Ads accounts, " \
                "please enter the response URI that includes the authorization 'code' parameter: \n"
            )

        # Request access and refresh tokens using the URI that you provided manually during program execution.
        authentication.request_oauth_tokens_by_response_uri(response_uri=response_uri) 

def get_refresh_token():
    ''' 
    Returns a refresh token if stored locally.
    '''
    file=None
    try:
        file=open("refresh.txt")
        line=file.readline()
        file.close()
        return line if line else None
    except IOError:
        if file:
            file.close()
        return None

def save_refresh_token(oauth_tokens):
    ''' 
    Stores a refresh token locally. Be sure to save your refresh token securely.
    '''
    with open("refresh.txt","w+") as file:
        file.write(oauth_tokens.refresh_token)
        file.close()
    return None

def search_accounts_by_user_id(user_id):
    ''' 
    Search for account details by UserId.
    
    :param user_id: The Bing Ads user identifier.
    :type user_id: long
    :return: List of accounts that the user can manage.
    :rtype: ArrayOfAccount
    '''
    global customer_service
   
    paging={
        'Index': 0,
        'Size': 10
    }

    predicates={
        'Predicate': [
            {
                'Field': 'UserId',
                'Operator': 'Equals',
                'Value': user_id,
            },
        ]
    }

    search_accounts_request={
        'PageInfo': paging,
        'Predicates': predicates
    }
        
    return customer_service.SearchAccounts(
        PageInfo=paging,
        Predicates=predicates
    )

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
    # There was an error while trying to deserialize parameter https://bingads.microsoft.com/CampaignManagement/v9:Entities.
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

def output_campaign_ids(campaign_ids):
    for id in campaign_ids:
        output_status_message("Campaign successfully added and assigned CampaignId {0}\n".format(id))

def output_ad_group_ids(ad_group_ids):
    for id in ad_group_ids:
        output_status_message("AdGroup successfully added and assigned AdGroupId {0}\n".format(id))

def output_ad_results(ads, ad_ids, ad_errors):
    
    # Since len(ads['Ad']) and len(ad_errors['long']) usually differ, we will need to adjust the ad_errors index 
    # as successful indices are counted. 
    success_count=0 

    # There is an issue in the SUDS library, where if Index 0 of ArrayOfNullableOflong is empty it is not returned. 
    # In this case we will need to adjust the index used to access ad_ids.
    suds_index_0_gap=len(ads['Ad']) - len(ad_ids['long'])

    error_index=0

    for ad_index in range(len(ads['Ad'])):
        attribute_value=None
        if ads['Ad'][ad_index].Type == 'Product':
            attribute_value="PromotionalText: {0}".format(ads['Ad'][ad_index].PromotionalText)
        else:
            attribute_value="Invalid Ad Type for Shopping Campaigns"
        
        if ad_errors is not None \
            and ad_errors['BatchError'] is not None \
            and ad_index < len(ad_errors['BatchError']) + success_count \
            and ad_index == ad_errors['BatchError'][error_index].Index:
            # One ad may have multiple errors, for example editorial errors in multiple publisher countries
            while(error_index < len(ad_errors['BatchError']) and ad_errors['BatchError'][error_index].Index == ad_index):
                output_status_message("Ad[{0}] ({1}) not added due to the following error:".format(ad_index, attribute_value))
                output_status_message("Index: {0}".format(ad_errors['BatchError'][error_index].Index))
                output_status_message("Code: {0}".format(ad_errors['BatchError'][error_index].Code))
                output_status_message("ErrorCode: {0}".format(ad_errors['BatchError'][error_index].ErrorCode))
                output_status_message("Message: {0}".format(ad_errors['BatchError'][error_index].Message))
                if ad_errors['BatchError'][error_index].Type == 'EditorialError':
                    output_status_message("DisapprovedText: {0}".format(ad_errors['BatchError'][error_index].DisapprovedText)) 
                    output_status_message("Location: {0}".format(ad_errors['BatchError'][error_index].Location)) 
                    output_status_message("PublisherCountry: {0}".format(ad_errors['BatchError'][error_index].PublisherCountry)) 
                    output_status_message("ReasonCode: {0}".format(ad_errors['BatchError'][error_index].ReasonCode)) 
                error_index=error_index + 1
        elif ad_ids['long'][ad_index - suds_index_0_gap] is not None:
            output_status_message("Ad[{0}] ({1}) successfully added and assigned AdId {2}".format( 
                        ad_index,
                        attribute_value,
                        ad_ids['long'][ad_index - suds_index_0_gap]))
            success_count=success_count + 1
        output_status_message('')

def output_product_partitions(ad_group_criterions):
    """
    Outputs the list of AdGroupCriterion, formatted as a tree. 
    Each AdGroupCriterion must be either a BiddableAdGroupCriterion or NegativeAdGroupCriterion. 
    To ensure the complete tree is represented, you should first call GetAdGroupCriterionsByAdGroupId 
    where CriterionTypeFilter is ProductPartition, and pass the returned list of AdGroupCriterion to this method. 

    :param ad_group_criterions: The list of ad group criterions to output formatted as a tree.
    :type ad_group_criterions: ArrayOfAdGroupCriterion

    """

    # Set up the tree for output

    child_branches={}
    tree_root=None

    for ad_group_criterion in ad_group_criterions['AdGroupCriterion']:
        partition=ad_group_criterion.Criterion
        child_branches[ad_group_criterion.Id]=campaign_service.factory.create('ArrayOfAdGroupCriterion')

        # The product partition with ParentCriterionId set to null is the root node.
        if partition.ParentCriterionId is not None:
            child_branches[partition.ParentCriterionId].AdGroupCriterion.append(ad_group_criterion)
        else:
            tree_root=ad_group_criterion

    # Outputs the tree root node and any children recursively
    output_product_partition_tree(tree_root, child_branches, 0)

def output_product_partition_tree(node, child_branches, tree_level):
    """
    Outputs the details of the specified product partition node, 
    and passes any children to itself recursively.

    :param node: The node to output, whether a Subdivision or Unit.
    :type node: AdGroupCriterion
    :param child_branches: The child branches or nodes if any exist.
    :type child_branches: dict{long, ArrayOfAdGroupCriterion}
    :param tree_level: The number of descendents from the tree root node. 
     Used by this operation to format the tree structure output.
    :type tree_level: int

    """

    pad=''
    for i in range(0, tree_level):
        pad=pad + '\t'
    output_status_message("{0}{1}".format(
        pad,
        node.Criterion.PartitionType)
    )

    output_status_message("{0}ParentCriterionId: {1}".format(
        pad,
        node.Criterion.ParentCriterionId)
    )

    output_status_message("{0}Id: {1}".format(
        pad,
        node.Id)
    )

    if node.Criterion.PartitionType == 'Unit':
        if node.Type == 'BiddableAdGroupCriterion':
            output_status_message("{0}Bid Amount: {1}".format(
                pad,
                node.CriterionBid.Bid.Amount)
            )
        elif node.Type == 'NegativeAdGroupCriterion':
            output_status_message("{0}Not Bidding on this Condition".format(
                pad)
            )
           

    null_attribute="(All other)" if node.Criterion.ParentCriterionId != None else "(Tree Root)"
    output_status_message("{0}Attribute: {1}".format(
        pad,
        null_attribute if node.Criterion.Condition.Attribute is None else node.Criterion.Condition.Attribute)
    )

    output_status_message("{0}Operand: {1}\n".format(
        pad,
        node.Criterion.Condition.Operand)
    )

    for child_node in child_branches[node.Id]['AdGroupCriterion']:
        output_product_partition_tree(child_node, child_branches, tree_level + 1)

def get_root_node(ad_group_criterions):
    """
    Returns the root node of a tree. This operation assumes that a complete 
    product partition tree is provided for one ad group. The node that has
    null ParentCriterionId is the root node.

    :param ad_group_criterions: The ad group criterions that contain the product partition tree.
    :type ad_group_criterions: ArrayOfAdGroupCriterion
    :return: The ad group criterion that was added to the list of PartitionActions.
    :rtype: AdGroupCriterion

    """

    root_node=None
    for ad_group_criterion in ad_group_criterions['AdGroupCriterion']:
        if ad_group_criterion.Criterion.ParentCriterionId is None:
            root_node=ad_group_criterion
            break

    return root_node


class PartitionActionHelper:
    """ 
    Helper class used to maintain a list of product partition actions for an ad group.
    The list of partition actions can be passed to the Bing Ads ApplyProductPartitionActions service operation.
    """

    def __init__(self,
                 ad_group_id):
        """ 
        Initialize an instance of this class.

        :param ad_group_id: Each criterion is associated with the same ad group.
        :type ad_group_id: long
        
        """

        self._ad_group_id=ad_group_id
        self._reference_id=-1
        self._partition_actions=campaign_service.factory.create('ArrayOfAdGroupCriterionAction')

    @property
    def partition_actions(self):
        """ 
        The list of partition actions that can be passed to the Bing Ads ApplyProductPartitionActions service operation.

        :rtype: ArrayOfAdGroupCriterionAction
        """

        return self._partition_actions

    def add_subdivision(self, parent, condition):
        """ 
        Sets the Add action for a new BiddableAdGroupCriterion corresponding to the specified ProductCondition, 
        and adds it to the helper's list of AdGroupCriterionAction.

        :param parent: The parent of the product partition subdivision that you want to add.
        :type parent: AdGroupCriterion
        :param condition: The condition or product filter for the new product partition.
        :type condition: ProductCondition
        :return: The ad group criterion that was added to the list of PartitionActions.
        :rtype: AdGroupCriterion
        """

        biddable_ad_group_criterion=campaign_service.factory.create('BiddableAdGroupCriterion')
        product_partition=campaign_service.factory.create('ProductPartition')
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.Id if parent != None else None
        product_partition.Condition=condition
        product_partition.PartitionType='Subdivision'
        biddable_ad_group_criterion.Criterion=product_partition
        biddable_ad_group_criterion.CriterionBid=None
        biddable_ad_group_criterion.AdGroupId=self._ad_group_id
        biddable_ad_group_criterion.Status=None
        if hasattr(biddable_ad_group_criterion, 'EditorialStatus'):
            biddable_ad_group_criterion.EditorialStatus=None
        biddable_ad_group_criterion.Id=self._reference_id
        self._reference_id=self._reference_id
        self._reference_id-=1

        partition_action=campaign_service.factory.create('AdGroupCriterionAction')
        partition_action.Action='Add'
        partition_action.AdGroupCriterion=biddable_ad_group_criterion
        self._partition_actions.AdGroupCriterionAction.append(partition_action)

        return biddable_ad_group_criterion

    def add_unit(self, parent, condition, bid_amount, is_negative=False):
        """ 
        Sets the Add action for a new AdGroupCriterion corresponding to the specified ProductCondition, 
        and adds it to the helper's list of AdGroupCriterionAction.

        :param parent: The parent of the product partition unit that you want to add.
        :type parent: AdGroupCriterion
        :param condition: The condition or product filter for the new product partition.
        :type condition: ProductCondition
        :param bid_amount: The bid amount for the new product partition.
        :type bid_amount: double
        :param is_negative: (Optional) Indicates whether or not to add a NegativeAdGroupCriterion. 
         The default value is False, in which case a BiddableAdGroupCriterion will be added.
        :type is_negative: bool
        :return: The ad group criterion that was added to the list of PartitionActions.
        :rtype: AdGroupCriterion
        """

        ad_group_criterion=None
        if is_negative:
            ad_group_criterion=campaign_service.factory.create('NegativeAdGroupCriterion')
        else:
            ad_group_criterion=campaign_service.factory.create('BiddableAdGroupCriterion')
            fixed_bid=campaign_service.factory.create('FixedBid')
            bid=campaign_service.factory.create('Bid')
            bid.Amount=bid_amount
            fixed_bid.Bid=bid
            ad_group_criterion.CriterionBid=fixed_bid
            
        ad_group_criterion.AdGroupId=self._ad_group_id
        if hasattr(ad_group_criterion, 'EditorialStatus'):
            ad_group_criterion.EditorialStatus=None
        ad_group_criterion.Status=None

        product_partition=campaign_service.factory.create('ProductPartition')
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.Id if parent != None else None
        product_partition.Condition=condition
        product_partition.PartitionType='Unit'
        ad_group_criterion.Criterion=product_partition=product_partition

        partition_action=campaign_service.factory.create('AdGroupCriterionAction')
        partition_action.Action='Add'
        partition_action.AdGroupCriterion=ad_group_criterion
        self._partition_actions.AdGroupCriterionAction.append(partition_action)

        return ad_group_criterion

    def delete_partition(self, ad_group_criterion):
        """ 
        Sets the Delete action for the specified AdGroupCriterion, 
        and adds it to the helper's list of AdGroupCriterionAction.

        :param ad_group_criterion: The ad group criterion whose product partition you want to delete.
        :type ad_group_criterion: AdGroupCriterion
        """

        ad_group_criterion.AdGroupId=self._ad_group_id
        ad_group_criterion.Status=None
        if hasattr(ad_group_criterion, 'EditorialStatus'):
            ad_group_criterion.EditorialStatus=None

        partition_action=campaign_service.factory.create('AdGroupCriterionAction')
        partition_action.Action='Delete'
        partition_action.AdGroupCriterion=ad_group_criterion
        self._partition_actions.AdGroupCriterionAction.append(partition_action)

    def update_partition(self, biddable_ad_group_criterion):
        """ 
        Sets the Update action for the specified BiddableAdGroupCriterion, 
        and adds it to the helper's list of AdGroupCriterionAction. 
        You can only update the CriterionBid, DestinationUrl, Param1, Param2, and Param3 elements 
        of the BiddableAdGroupCriterion. 
        When working with product partitions, youu cannot update the Criterion (ProductPartition). 
        To update a ProductPartition, you must delete the existing node (delete_partition) and 
        add a new one (add_unit or add_subdivision) during the same call to ApplyProductPartitionActions.

        :param ad_group_criterion: The biddable ad group criterion to update.
        :type ad_group_criterion: BiddableAdGroupCriterion
        """

        biddable_ad_group_criterion.AdGroupId=self._ad_group_id
        biddable_ad_group_criterion.Status=None
        if hasattr(biddable_ad_group_criterion, 'EditorialStatus'):
            biddable_ad_group_criterion.EditorialStatus=None

        partition_action=campaign_service.factory.create('AdGroupCriterionAction')
        partition_action.Action='Update'
        partition_action.AdGroupCriterion=biddable_ad_group_criterion
        self._partition_actions.AdGroupCriterionAction.append(partition_action)

# Main execution
if __name__ == '__main__':

    try:
        # You should authenticate for Bing Ads production services with a Microsoft Account, 
        # instead of providing the Bing Ads username and password set. 
        # Authentication with a Microsoft Account is currently not supported in Sandbox.
        authenticate_with_oauth()

        # Uncomment to run with Bing Ads legacy UserName and Password credentials.
        # For example you would use this method to authenticate in sandbox.
        #authenticate_with_username()
        
        # Set to an empty user identifier to get the current authenticated Bing Ads user,
        # and then search for all accounts the user may access.
        user=customer_service.GetUser(None).User
        accounts=search_accounts_by_user_id(user.Id)

        # For this example we'll use the first account.
        authorization_data.account_id=accounts['Account'][0].Id
        authorization_data.customer_id=accounts['Account'][0].ParentCustomerId
        
        # Get a list of all Bing Merchant Center stores associated with your CustomerId

        stores=campaign_service.GetBMCStoresByCustomerId()
        if stores is None:
            output_status_message(
                "You do not have any BMC stores registered for CustomerId {0}.\n".format(authorization_data.customer_id)
            )
            sys.exit(0)

        #Add a new Bing Shopping campaign that will be associated with a ProductScope criterion.
        # - Set the CampaignType element of the Campaign to Shopping.
        # - Create a ShoppingSetting instance and set its Priority (0, 1, or 2), SalesCountryCode, and StoreId elements. 
        #   Add this shopping setting to the Settings list of the Campaign.

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
        campaign=campaign_service.factory.create('Campaign')
        settings=campaign_service.factory.create('ArrayOfSetting')
        setting=campaign_service.factory.create('ShoppingSetting')
        setting.Priority=0
        setting.SalesCountryCode ='US'
        setting.StoreId=stores['BMCStore'][0].Id
        settings.Setting.append(setting)
        campaign.Settings=settings
        campaign.CampaignType=['Shopping']
        campaign.Name='Bing Shopping Campaign ' + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        campaign.Description='Bing Shopping Campaign Example.'
        campaign.BudgetType='MonthlyBudgetSpendUntilDepleted'
        campaign.MonthlyBudget=1000
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.DaylightSaving='true' 
        campaign.Status='Paused'
        campaigns.Campaign.append(campaign)

        campaign_ids=campaign_service.AddCampaigns(
            AccountId=authorization_data.account_id,
            Campaigns=campaigns
        )['long']

        output_campaign_ids(campaign_ids)

        
        #Optionally, you can create a ProductScope criterion that will be associated with your Bing Shopping campaign. 
        #Use the product scope criterion to include a subset of your product catalog, for example a specific brand, 
        #category, or product type. A campaign can only be associated with one ProductScope, which contains a list 
        #of up to 7 ProductCondition. You'll also be able to specify more specific product conditions for each ad group.
        

        campaign_criterions=campaign_service.factory.create('ArrayOfCampaignCriterion')
        campaign_criterion=campaign_service.factory.create('CampaignCriterion')
        product_scope=campaign_service.factory.create('ProductScope')
        conditions=campaign_service.factory.create('ArrayOfProductCondition')
        condition_new=campaign_service.factory.create('ProductCondition')
        condition_new.Operand='Condition'
        condition_new.Attribute='New'
        conditions.ProductCondition.append(condition_new)
        condition_custom_label_0=campaign_service.factory.create('ProductCondition')
        condition_custom_label_0.Operand='CustomLabel0'
        condition_custom_label_0.Attribute='MerchantDefinedCustomLabel'
        conditions.ProductCondition.append(condition_custom_label_0)
        product_scope.Conditions=conditions
        campaign_criterion.CampaignId=campaign_ids[0]
        campaign_criterion.BidAdjustment=None # Reserved for future use
        campaign_criterion.Criterion=product_scope
        campaign_criterions.CampaignCriterion.append(campaign_criterion)

        add_campaign_criterions_response=campaign_service.AddCampaignCriterions(
            CampaignCriterions=campaign_criterions,
            CriterionType='ProductScope'
        )
        
        # Specify one or more ad groups.

        ad_groups=campaign_service.factory.create('ArrayOfAdGroup')
        ad_group=campaign_service.factory.create('AdGroup')
        ad_group.Name="Product Categories"
        ad_group.AdDistribution=['Search']
        ad_group.BiddingModel='Keyword'
        ad_group.PricingModel='Cpc'
        ad_group.Network=None
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=2015
        ad_group.EndDate=end_date
        ad_group.Language='English'
        ad_groups.AdGroup.append(ad_group)

        ad_group_ids=campaign_service.AddAdGroups(
            CampaignId=campaign_ids[0],
            AdGroups=ad_groups
        )['long']
        output_ad_group_ids(ad_group_ids)

        # Bid on all products

        helper=PartitionActionHelper(ad_group_ids[0])
        
        root_condition=campaign_service.factory.create('ProductCondition')
        root_condition.Operand='All'
        root_condition.Attribute=None

        root=helper.add_unit(
            None,
            root_condition,
            0.35,
            False
        )

        output_status_message("Applying only the root as a Unit with a bid . . . \n")
        apply_product_partition_actions_response=campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )

        ad_group_criterions=campaign_service.GetAdGroupCriterionsByAdGroupId(
            AccountId=authorization_data.account_id,
            AdGroupId=ad_group_ids[0],
            CriterionTypeFilter='ProductPartition'
        )

        output_status_message("The ad group's product partition only has a tree root node: \n")
        output_product_partitions(ad_group_criterions)

        # Let's update the bid of the root Unit we just added.

        updated_root=campaign_service.factory.create('BiddableAdGroupCriterion')
        fixed_bid=campaign_service.factory.create('FixedBid')
        bid=campaign_service.factory.create('Bid')
        bid.Amount=0.45
        fixed_bid.Bid=bid
        updated_root.Id=apply_product_partition_actions_response.AdGroupCriterionIds['long'][0]
        updated_root.CriterionBid=fixed_bid
                
        helper=PartitionActionHelper(ad_group_ids[0])
        helper.update_partition(updated_root)

        output_status_message("Updating the bid for the tree root node . . . \n")
        campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )

        ad_group_criterions=campaign_service.GetAdGroupCriterionsByAdGroupId(
            AccountId=authorization_data.account_id,
            AdGroupId=ad_group_ids[0],
            CriterionTypeFilter='ProductPartition'
        )

        output_status_message("Updated the bid for the tree root node: \n")
        output_product_partitions(ad_group_criterions)

        
        #Now we will overwrite any existing tree root, and build a product partition group tree structure in multiple steps. 
        #You could build the entire tree in a single call since there are less than 5,000 nodes; however, 
        #we will build it in steps to demonstrate how to use the results from ApplyProductPartitionActions to update the tree. 
        
        #For a list of validation rules, see the Bing Shopping Campaigns technical guide:
        #https://msdn.microsoft.com/en-US/library/bing-ads-campaign-management-bing-shopping-campaigns.aspx
        

        helper=PartitionActionHelper(ad_group_ids[0])

        #Check whether a root node exists already.

        ad_group_criterions=campaign_service.GetAdGroupCriterionsByAdGroupId(
            AccountId=authorization_data.account_id,
            AdGroupId=ad_group_ids[0],
            CriterionTypeFilter='ProductPartition'
        )

        existing_root=get_root_node(ad_group_criterions)
        if existing_root is not None:
            helper.delete_partition(existing_root)

        root_condition=campaign_service.factory.create('ProductCondition')
        root_condition.Operand='All'
        root_condition.Attribute=None
        root=helper.add_subdivision(
            None, 
            root_condition
        )

        
        #The direct children of any node must have the same Operand. 
        #For this example we will use CategoryL1 nodes as children of the root. 
        #For a list of valid CategoryL1 through CategoryL5 values, see the Bing Category Taxonomy:
        #http://advertise.bingads.microsoft.com/en-us/WWDocs/user/search/en-us/Bing_Category_Taxonomy.txt
        
        animals_condition=campaign_service.factory.create('ProductCondition')
        animals_condition.Operand='CategoryL1'
        animals_condition.Attribute='Animals & Pet Supplies'
        animals_subdivision=helper.add_subdivision(
            root,
            animals_condition
        )

        
        #If you use a CategoryL2 node, it must be a descendant (child or later) of a CategoryL1 node. 
        #In other words you cannot have a CategoryL2 node as parent of a CategoryL1 node. 
        #For this example we will a CategoryL2 node as child of the CategoryL1 Animals & Pet Supplies node. 
        
        pet_supplies_condition=campaign_service.factory.create('ProductCondition')
        pet_supplies_condition.Operand='CategoryL2'
        pet_supplies_condition.Attribute='Pet Supplies'
        pet_supplies_subdivision=helper.add_subdivision(
            animals_subdivision,
            pet_supplies_condition
        )

        brand_a_condition=campaign_service.factory.create('ProductCondition')
        brand_a_condition.Operand='Brand'
        brand_a_condition.Attribute='Brand A'
        brand_a=helper.add_unit(
            pet_supplies_subdivision,
            brand_a_condition,
            0.35,
            False
        )

        
        #If you won't bid on Brand B, set the helper method's bidAmount to '0' and isNegative to True. 
        #The helper method will create a NegativeAdGroupCriterion and apply the condition.
        
        brand_b_condition=campaign_service.factory.create('ProductCondition')
        brand_b_condition.Operand='Brand'
        brand_b_condition.Attribute='Brand B'
        brand_b=helper.add_unit(
            pet_supplies_subdivision,
            brand_b_condition,
            0,
            True
        )

        other_brands_condition=campaign_service.factory.create('ProductCondition')
        other_brands_condition.Operand='Brand'
        other_brands_condition.Attribute=None
        other_brands=helper.add_unit(
            pet_supplies_subdivision,
            other_brands_condition,
            0.35,
            False
        )

        other_pet_supplies_condition=campaign_service.factory.create('ProductCondition')
        other_pet_supplies_condition.Operand='CategoryL2'
        other_pet_supplies_condition.Attribute=None
        other_pet_supplies=helper.add_unit(
            animals_subdivision,
            other_pet_supplies_condition,
            0.35,
            False
        )

        electronics_condition=campaign_service.factory.create('ProductCondition')
        electronics_condition.Operand='CategoryL1'
        electronics_condition.Attribute='Electronics'
        electronics=helper.add_unit(
            root,
            electronics_condition,
            0.35,
            False
        )

        other_categoryL1_condition=campaign_service.factory.create('ProductCondition')
        other_categoryL1_condition.Operand='CategoryL1'
        other_categoryL1_condition.Attribute=None
        other_categoryL1=helper.add_unit(
            root,
            other_categoryL1_condition,
            0.35,
            False
        )

        output_status_message("Applying product partitions to the ad group . . . \n")
        apply_product_partition_actions_response=campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )

        # To retrieve product partitions after they have been applied, call GetAdGroupCriterionsByAdGroupId. 
        # The product partition with ParentCriterionId set to null is the root node.

        ad_group_criterions=campaign_service.GetAdGroupCriterionsByAdGroupId(
            AccountId=authorization_data.account_id,
            AdGroupId=ad_group_ids[0],
            CriterionTypeFilter='ProductPartition'
        )

        
        #The product partition group tree now has 9 nodes. 
                 
        #All other (Root Node)
        #|
        #+-- Animals & Pet Supplies (CategoryL1)
        #|    |
        #|    +-- Pet Supplies (CategoryL2)
        #|    |    |
        #|    |    +-- Brand A
        #|    |    |    
        #|    |    +-- Brand B
        #|    |    |    
        #|    |    +-- All other (Brand)
        #|    |         
        #|    +-- All other (CategoryL2)
        #|        
        #+-- Electronics (CategoryL1)
        #|   
        #+-- All other (CategoryL1)

        output_status_message("The product partition group tree now has 9 nodes: \n")
        output_product_partitions(ad_group_criterions)
        
        
        #Let's replace the Electronics (CategoryL1) node created above with an Electronics (CategoryL1) node that 
        #has children i.e. Brand C (Brand), Brand D (Brand), and All other (Brand) as follows: 
                 
        #Electronics (CategoryL1)
        #|
        #+-- Brand C (Brand)
        #|
        #+-- Brand D (Brand)
        #|
        #+-- All other (Brand)

        helper=PartitionActionHelper(ad_group_ids[0])

        
        #To replace a node we must know its Id and its ParentCriterionId. In this case the parent of the node 
        #we are replacing is All other (Root Node), and was created at Index 1 of the previous ApplyProductPartitionActions call. 
        #The node that we are replacing is Electronics (CategoryL1), and was created at Index 8. 
        
        root_id=apply_product_partition_actions_response.AdGroupCriterionIds['long'][1]
        electronics.Id=apply_product_partition_actions_response.AdGroupCriterionIds['long'][8]
        helper.delete_partition(electronics)

        parent=campaign_service.factory.create('BiddableAdGroupCriterion')
        parent.Id=root_id

        electronics_subdivision_condition=campaign_service.factory.create('ProductCondition')
        electronics_subdivision_condition.Operand='CategoryL1'
        electronics_subdivision_condition.Attribute='Electronics'
        electronics_subdivision=helper.add_subdivision(
            parent,
            electronics_subdivision_condition
        )

        brand_c_condition=campaign_service.factory.create('ProductCondition')
        brand_c_condition.Operand='Brand'
        brand_c_condition.Attribute='Brand C'
        brand_c=helper.add_unit(
            electronics_subdivision,
            brand_c_condition,
            0.35,
            False
        )

        brand_d_condition=campaign_service.factory.create('ProductCondition')
        brand_d_condition.Operand='Brand'
        brand_d_condition.Attribute='Brand D'
        brand_d=helper.add_unit(
            electronics_subdivision,
            brand_d_condition,
            0.35,
            False
        )

        other_electronics_brands_condition=campaign_service.factory.create('ProductCondition')
        other_electronics_brands_condition.Operand='Brand'
        other_electronics_brands_condition.Attribute=None
        other_electronics_brands=helper.add_unit(
            electronics_subdivision,
            other_electronics_brands_condition,
            0.35,
            False
        )

        output_status_message(
            "Updating the product partition group to refine Electronics (CategoryL1) with 3 child nodes . . . \n"
        )
        apply_product_partition_actions_response=campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )
                
        ad_group_criterions=campaign_service.GetAdGroupCriterionsByAdGroupId(
            AccountId=authorization_data.account_id,
            AdGroupId=ad_group_ids[0],
            CriterionTypeFilter='ProductPartition'
        )

        
        #The product partition group tree now has 12 nodes, including the children of Electronics (CategoryL1):
                 
        #All other (Root Node)
        #|
        #+-- Animals & Pet Supplies (CategoryL1)
        #|    |
        #|    +-- Pet Supplies (CategoryL2)
        #|    |    |
        #|    |    +-- Brand A
        #|    |    |    
        #|    |    +-- Brand B
        #|    |    |    
        #|    |    +-- All other (Brand)
        #|    |         
        #|    +-- All other (CategoryL2)
        #|        
        #+-- Electronics (CategoryL1)
        #|    |
        #|    +-- Brand C (Brand)
        #|    |
        #|    +-- Brand D (Brand)
        #|    |
        #|    +-- All other (Brand)
        #|   
        #+-- All other (CategoryL1)        

        output_status_message(
            "The product partition group tree now has 12 nodes, including the children of Electronics (CategoryL1): \n"
        )
        output_product_partitions(ad_group_criterions)

        
        #Create a product ad. You must add at least one ProductAd to the corresponding ad group. 
        #A ProductAd is not used directly for delivered ad copy. Instead, the delivery engine generates 
        #product ads from the product details that it finds in your Bing Merchant Center store's product catalog. 
        #The primary purpose of the ProductAd object is to provide promotional text that the delivery engine 
        #adds to the product ads that it generates. For example, if the promotional text is set to 
        #'Free shipping on $99 purchases', the delivery engine will set the product ad's description to 
        #'Free shipping on $99 purchases.'
        
        ads=campaign_service.factory.create('ArrayOfAd')
        product_ad=campaign_service.factory.create('ProductAd')
        product_ad.PromotionalText='Free shipping on $99 purchases.'
        product_ad.Type='Product'
        product_ad.Status=None
        product_ad.EditorialStatus=None
        ads.Ad.append(product_ad)

        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids[0],
            Ads=ads
        )
        ad_ids={
                'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
            }
        ad_errors={
                'BatchError': add_ads_response.PartialErrors['BatchError'] if add_ads_response.PartialErrors else None
            }    

        output_ad_results(ads, ad_ids, ad_errors)

        #Delete the campaign, ad group, criterion, and ad that were previously added. 
        #You should remove this region if you want to view the added entities in the 
        #Bing Ads web application or another tool.

        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id,
            CampaignIds={
                    'long': campaign_ids
                }
        )

        for campaign_id in campaign_ids:
            output_status_message("Deleted CampaignId {0}\n".format(campaign_id))

        output_status_message("Program execution completed")

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)
