from auth_helper import *
from bulk_service_manager_helper import *
from output_helper import *

# You must provide credentials in auth_helper.py.


def main(authorization_data):

    errors=[]

    try:
        # The Bing Merchant Center Store Id cannot be retrieved via the Bulk service, 
        # so we'll use the Campaign Management service i.e., the GetBMCStoresByCustomerId service operation below.

        # Get a list of all Bing Merchant Center stores associated with your CustomerId.

        output_status_message("-----\nGetBMCStoresByCustomerId:")
        stores=campaign_service.GetBMCStoresByCustomerId()['BMCStore']
        if stores is None:
            output_status_message(
                "You do not have any BMC stores registered for CustomerId {0}.".format(authorization_data.customer_id)
            )
            sys.exit(0)

        upload_entities=[]

        # Create a Shopping campaign with product conditions.
           
        bulk_campaign=BulkCampaign()
        bulk_campaign.client_id='YourClientIdGoesHere'
        campaign=set_elements_to_none(campaign_service.factory.create('Campaign'))
        campaign.BudgetType='DailyBudgetStandard'
        campaign.CampaignType=['Shopping']
        campaign.DailyBudget=50
        languages=campaign_service.factory.create('ns3:ArrayOfstring')
        languages.string.append('All')
        campaign.Languages=languages
        campaign.Name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())
        settings=campaign_service.factory.create('ArrayOfSetting')
        setting=set_elements_to_none(campaign_service.factory.create('ShoppingSetting'))
        setting.Priority=0
        setting.SalesCountryCode ='US'
        setting.StoreId=stores[0].Id
        settings.Setting.append(setting)
        campaign.Settings=settings
        campaign.TimeZone='PacificTimeUSCanadaTijuana'
        campaign.Id=CAMPAIGN_ID_KEY
        bulk_campaign.campaign=campaign
        upload_entities.append(bulk_campaign)

        # Optionally, you can create a ProductScope criterion that will be associated with your Bing Shopping campaign. 
        # You'll also be able to add more specific product conditions for each ad group.

        bulk_campaign_product_scope=BulkCampaignProductScope()
        bulk_campaign_product_scope.status='Active'
        campaign_criterion=set_elements_to_none(campaign_service.factory.create('CampaignCriterion'))
        product_scope=set_elements_to_none(campaign_service.factory.create('ProductScope'))
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
        campaign_criterion.CampaignId=CAMPAIGN_ID_KEY
        campaign_criterion.Criterion=product_scope
        bulk_campaign_product_scope.biddable_campaign_criterion=campaign_criterion
        upload_entities.append(bulk_campaign_product_scope)

        # Create the ad group that will have the product partitions.

        bulk_ad_group=BulkAdGroup()
        bulk_ad_group.campaign_id=CAMPAIGN_ID_KEY
        ad_group=set_elements_to_none(campaign_service.factory.create('AdGroup'))
        ad_group.Id=AD_GROUP_ID_KEY
        ad_group.Name="Product Categories"
        ad_group.Status='Paused'
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        end_date.Year=strftime("%Y", gmtime())
        ad_group.EndDate=end_date
        cpc_bid=campaign_service.factory.create('Bid')
        cpc_bid.Amount=0.09
        ad_group.CpcBid=cpc_bid
        bulk_ad_group.ad_group=ad_group
        upload_entities.append(bulk_ad_group)

        #Create a product ad. You must add at least one product ad to the ad group. 
        #The product ad identifier can be used for reporting analytics.
        #Use Merchant Promotions if you want tags to appear at the bottom of your product ad 
        #as "special offer" links, helping to increase customer engagement. For details
        #on Merchant Promotions see https://help.bingads.microsoft.com/#apex/3/en/56805/0.
        
        bulk_product_ad=BulkProductAd()
        bulk_product_ad.ad_group_id=AD_GROUP_ID_KEY
        ads=campaign_service.factory.create('ArrayOfAd')
        product_ad=set_elements_to_none(campaign_service.factory.create('ProductAd'))
        product_ad.Type='Product'
        bulk_product_ad.ad=product_ad
        upload_entities.append(bulk_product_ad)
        
        output_status_message("-----\nAdding the campaign, product scope, ad group, and ad...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")
        
        # Write the upload output
        
        campaign_results=[]
        campaign_product_scope_results=[]
        ad_group_results=[]
        product_ad_results=[]

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                output_bulk_campaigns([entity])
            if isinstance(entity, BulkCampaignProductScope):
                campaign_product_scope_results.append(entity)
                output_bulk_campaign_product_scopes([entity])
            if isinstance(entity, BulkAdGroup):
                ad_group_results.append(entity)
                output_bulk_ad_groups([entity])
            if isinstance(entity, BulkProductAd):
                product_ad_results.append(entity)
                output_bulk_product_ads([entity])

        ad_group_id=ad_group_results.pop(0).ad_group.Id

        # Bid all products

        helper=ProductPartitionHelper(ad_group_id)
        
        root_condition=set_elements_to_none(campaign_service.factory.create('ProductCondition'))
        root_condition.Operand='All'
        root_condition.Attribute=None

        root=helper.add_unit(
            None,
            root_condition,
            0.35,
            False,
            "root"
        )

        output_status_message("-----\nApplying only the root as a Unit with a bid...")
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)

        output_status_message("The ad group's product partition only has a tree root node:")
        output_bulk_product_partitions(product_partitions)

        # Let's update the bid of the root Unit we just added.

        updated_root=get_node_by_client_id(apply_bulk_product_partition_actions_results, "root")
        fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
        fixed_bid.Amount=0.45
        updated_root.ad_group_criterion.CriterionBid=fixed_bid
        
        helper=ProductPartitionHelper(ad_group_id)
        helper.update_partition(updated_root)

        output_status_message("-----\nUpdating the bid for the tree root node...")
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)

        output_status_message("Updated the bid for the tree root node:")
        output_bulk_product_partitions(product_partitions)
        
        # Initialize and overwrite any existing tree root, and build a product partition group tree structure in multiple steps. 
        # You could build the entire tree in a single call since there are less than 20,000 nodes; however, 
        # we will build it in steps to demonstrate how to use the results from bulk upload to update the tree. 
        
        helper=ProductPartitionHelper(ad_group_id)

        # Check whether a root node exists already.

        existing_root=get_node_by_client_id(apply_bulk_product_partition_actions_results, "root")
        if existing_root is not None:
            existing_root.client_id="deletedroot"
            helper.delete_partition(existing_root)

        root_condition=campaign_service.factory.create('ProductCondition')
        root_condition.Operand='All'
        root_condition.Attribute=None
        root=helper.add_subdivision(
            None, 
            root_condition,
            "root"
        )
        
        #The direct children of any node must have the same Operand. 
        #For this example we will use CategoryL1 nodes as children of the root. 
        #For a list of valid CategoryL1 through CategoryL5 values, see the Bing Category Taxonomy:
        #http://go.microsoft.com/fwlink?LinkId=507666
        
        animals_condition=campaign_service.factory.create('ProductCondition')
        animals_condition.Operand='CategoryL1'
        animals_condition.Attribute='Animals & Pet Supplies'
        animals_subdivision=helper.add_subdivision(
            root,
            animals_condition,
            "animals_subdivision"
        )
        
        #If you use a CategoryL2 node, it must be a descendant (child or later) of a CategoryL1 node. 
        #In other words you cannot have a CategoryL2 node as parent of a CategoryL1 node. 
        #For this example we will a CategoryL2 node as child of the CategoryL1 Animals & Pet Supplies node. 
        
        pet_supplies_condition=campaign_service.factory.create('ProductCondition')
        pet_supplies_condition.Operand='CategoryL2'
        pet_supplies_condition.Attribute='Pet Supplies'
        pet_supplies_subdivision=helper.add_subdivision(
            animals_subdivision,
            pet_supplies_condition,
            "pet_supplies_subdivision"
        )

        brand_a_condition=campaign_service.factory.create('ProductCondition')
        brand_a_condition.Operand='Brand'
        brand_a_condition.Attribute='Brand A'
        brand_a=helper.add_unit(
            pet_supplies_subdivision,
            brand_a_condition,
            0.35,
            False,
            "brand_a"
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
            True,
            "brand_b"
        )

        other_brands_condition=campaign_service.factory.create('ProductCondition')
        other_brands_condition.Operand='Brand'
        other_brands_condition.Attribute=None
        other_brands=helper.add_unit(
            pet_supplies_subdivision,
            other_brands_condition,
            0.35,
            False,
            "other_brands"
        )

        other_pet_supplies_condition=campaign_service.factory.create('ProductCondition')
        other_pet_supplies_condition.Operand='CategoryL2'
        other_pet_supplies_condition.Attribute=None
        other_pet_supplies=helper.add_unit(
            animals_subdivision,
            other_pet_supplies_condition,
            0.35,
            False,
            "other_pet_supplies"
        )

        electronics_condition=campaign_service.factory.create('ProductCondition')
        electronics_condition.Operand='CategoryL1'
        electronics_condition.Attribute='Electronics'
        electronics=helper.add_unit(
            root,
            electronics_condition,
            0.35,
            False,
            "electronics"
        )

        other_categoryL1_condition=campaign_service.factory.create('ProductCondition')
        other_categoryL1_condition.Operand='CategoryL1'
        other_categoryL1_condition.Attribute=None
        other_categoryL1=helper.add_unit(
            root,
            other_categoryL1_condition,
            0.35,
            False,
            "other_categoryL1"
        )

        output_status_message("-----\nApplying product partitions to the ad group...")
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)
        
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

        output_status_message("The product partition group tree now has 9 nodes:")
        output_bulk_product_partitions(product_partitions)
                
        #Let's replace the Electronics (CategoryL1) node created above with an Electronics (CategoryL1) node that 
        #has children i.e. Brand C (Brand), Brand D (Brand), and All other (Brand) as follows: 
                 
        #Electronics (CategoryL1)
        #|
        #+-- Brand C (Brand)
        #|
        #+-- Brand D (Brand)
        #|
        #+-- All other (Brand)

        helper=ProductPartitionHelper(ad_group_id)
        
        #To replace a node we must know its Id and its ParentCriterionId. In this case the parent of the node 
        #we are replacing is All other (Root Node), and was created at Index 1 of the previous ApplyProductPartitionActions call. 
        #The node that we are replacing is Electronics (CategoryL1), and was created at Index 8. 
        
        root_id=get_node_by_client_id(apply_bulk_product_partition_actions_results, "root").ad_group_criterion.Id
        electronics.ad_group_criterion.Id=get_node_by_client_id(apply_bulk_product_partition_actions_results, "electronics").ad_group_criterion.Id
        helper.delete_partition(electronics)

        parent=BulkAdGroupProductPartition()
        parent.ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        parent.ad_group_criterion.Id=root_id

        electronics_subdivision_condition=campaign_service.factory.create('ProductCondition')
        electronics_subdivision_condition.Operand='CategoryL1'
        electronics_subdivision_condition.Attribute='Electronics'
        electronics_subdivision=helper.add_subdivision(
            parent,
            electronics_subdivision_condition,
            "electronics_subdivision"
        )

        brand_c_condition=campaign_service.factory.create('ProductCondition')
        brand_c_condition.Operand='Brand'
        brand_c_condition.Attribute='Brand C'
        brand_c=helper.add_unit(
            electronics_subdivision,
            brand_c_condition,
            0.35,
            False,
            "brand_c"
        )

        brand_d_condition=campaign_service.factory.create('ProductCondition')
        brand_d_condition.Operand='Brand'
        brand_d_condition.Attribute='Brand D'
        brand_d=helper.add_unit(
            electronics_subdivision,
            brand_d_condition,
            0.35,
            False,
            "brand_d"
        )

        other_electronics_brands_condition=campaign_service.factory.create('ProductCondition')
        other_electronics_brands_condition.Operand='Brand'
        other_electronics_brands_condition.Attribute=None
        other_electronics_brands=helper.add_unit(
            electronics_subdivision,
            other_electronics_brands_condition,
            0.35,
            False,
            "other_electronics_brands"
        )

        output_status_message(
            "-----\nUpdating the product partition group to refine Electronics (CategoryL1) with 3 child nodes..."
        )
        apply_bulk_product_partition_actions_results=apply_bulk_product_partition_actions(helper.partition_actions)

        product_partitions=get_bulk_ad_group_product_partition_tree(ad_group_id)
        
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
            "The product partition group tree now has 12 nodes, including the children of Electronics (CategoryL1):"
        )
        output_bulk_product_partitions(product_partitions)

        # Delete the campaign and everything it contains e.g., ad groups and ads.
                
        upload_entities=[]

        for campaign_result in campaign_results:
            campaign_result.campaign.Status='Deleted'
            upload_entities.append(campaign_result)
            
        output_status_message("-----\nDeleting the campaign and everything it contains e.g., ad groups and ads...")
        download_entities=write_entities_and_upload_file(
            bulk_service_manager=bulk_service_manager, 
            upload_entities=upload_entities)

        output_status_message("Upload results:")

        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                output_bulk_campaigns([entity])

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)

def apply_bulk_product_partition_actions(upload_entities):
    download_entities=write_entities_and_upload_file(
        bulk_service_manager=bulk_service_manager, 
        upload_entities=upload_entities)

    output_status_message("Upload results:")
    
    bulk_ad_group_product_partitions=[]

    for entity in download_entities:
        if isinstance(entity, BulkAdGroupProductPartition):
            bulk_ad_group_product_partitions.append(entity)
            output_bulk_ad_group_product_partitions([entity])

    return bulk_ad_group_product_partitions

def get_bulk_ad_group_product_partition_tree(ad_group_id):
    download_parameters=DownloadParameters(
        download_entities=[
            'AdGroupProductPartitions'
        ],
        result_file_directory=FILE_DIRECTORY,
        result_file_name=DOWNLOAD_FILE_NAME,
        overwrite_result_file=True,
        last_sync_time_in_utc=None
    )
    download_entities=download_file(
        bulk_service_manager=bulk_service_manager, 
        download_parameters=download_parameters)
    
    bulk_ad_group_product_partitions=[]
    
    for entity in download_entities:
        if isinstance(entity, BulkAdGroupProductPartition) and entity.ad_group_criterion is not None and entity.ad_group_criterion.AdGroupId == ad_group_id:
            bulk_ad_group_product_partitions.append(entity)

    return bulk_ad_group_product_partitions

def get_node_by_client_id(product_partitions, client_id=None):
    """
    Returns the root node of a tree. This operation assumes that a complete 
    product partition tree is provided for one ad group. The node that has
    null ParentCriterionId is the root node.

    :param product_partitions: The list of BulkAdGroupProductPartition that make up the product partition tree.
    :type product_partitions: BulkAdGroupProductPartition[]
    :return: The BulkAdGroupProductPartition corresponding to the specified Client Id.
    :rtype: BulkAdGroupProductPartition

    """

    client_node=None
    for product_partition in product_partitions:
        if product_partition.client_id == client_id:
            client_node=product_partition
            break

    return client_node


class ProductPartitionHelper:
    """ 
    Helper class used to maintain a list of product partition actions for an ad group.
    The list of partition actions can be uploaded to the Bulk service.
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
        self._partition_actions=[]

    @property
    def partition_actions(self):
        """ 
        The list of BulkAdGroupProductPartition that can be uploaded to the Bulk service

        :rtype: BulkAdGroupProductPartition[]
        """

        return self._partition_actions

    def add_subdivision(self, parent, condition, client_id=None):
        """ 
        Sets the Add action for a new BiddableAdGroupCriterion corresponding to the specified ProductCondition, 
        and adds it to the helper's list of BulkAdGroupProductPartition.

        :param parent: The parent of the product partition subdivision that you want to add.
        :type parent: BulkAdGroupProductPartition
        :param condition: The condition or product filter for the new product partition.
        :type condition: ProductCondition
        :param client_id: The Client Id in the bulk upload file corresponding to the product partition.
        :type client_id: string
        :return: The BulkAdGroupProductPartition that was added to the list of partition_actions.
        :rtype: BulkAdGroupProductPartition
        """

        biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        product_partition=set_elements_to_none(campaign_service.factory.create('ProductPartition'))
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.ad_group_criterion.Id if parent is not None and parent.ad_group_criterion is not None else None
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

        partition_action=BulkAdGroupProductPartition()
        partition_action.client_id=client_id
        partition_action.ad_group_criterion=biddable_ad_group_criterion
        self._partition_actions.append(partition_action)

        return partition_action

    def add_unit(self, parent, condition, bid_amount, is_negative=False, client_id=None):
        """ 
        Sets the Add action for a new AdGroupCriterion corresponding to the specified ProductCondition, 
        and adds it to the helper's list of BulkAdGroupProductPartition.

        :param parent: The parent of the product partition unit that you want to add.
        :type parent: BulkAdGroupProductPartition
        :param condition: The condition or product filter for the new product partition.
        :type condition: ProductCondition
        :param bid_amount: The bid amount for the new product partition.
        :type bid_amount: double
        :param is_negative: (Optional) Indicates whether or not to add a NegativeAdGroupCriterion. 
         The default value is False, in which case a BiddableAdGroupCriterion will be added.
        :type is_negative: bool
        :param client_id: The Client Id in the bulk upload file corresponding to the product partition.
        :type client_id: string
        :return: The BulkAdGroupProductPartition that was added to the list of partition_actions.
        :rtype: BulkAdGroupProductPartition
        """

        ad_group_criterion=None
        if is_negative:
            ad_group_criterion=set_elements_to_none(campaign_service.factory.create('NegativeAdGroupCriterion'))
        else:
            ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
            fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
            fixed_bid.Amount=bid_amount
            ad_group_criterion.CriterionBid=fixed_bid
            
        ad_group_criterion.AdGroupId=self._ad_group_id
        if hasattr(ad_group_criterion, 'EditorialStatus'):
            ad_group_criterion.EditorialStatus=None
        ad_group_criterion.Status=None

        product_partition=set_elements_to_none(campaign_service.factory.create('ProductPartition'))
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.ad_group_criterion.Id if parent is not None and parent.ad_group_criterion is not None else None
        product_partition.Condition=condition
        product_partition.PartitionType='Unit'
        ad_group_criterion.Criterion=product_partition

        partition_action=BulkAdGroupProductPartition()
        partition_action.client_id=client_id
        partition_action.ad_group_criterion=ad_group_criterion
        self._partition_actions.append(partition_action)

        return partition_action

    def delete_partition(self, bulk_ad_group_product_partition):
        """ 
        Sets the Delete action for the specified AdGroupCriterion, 
        and adds it to the helper's list of BulkAdGroupProductPartition.

        :param bulk_ad_group_product_partition: The BulkAdGroupProductPartition whose product partition you want to delete.
        :type bulk_ad_group_product_partition: BulkAdGroupProductPartition
        """

        if bulk_ad_group_product_partition is not None and bulk_ad_group_product_partition.ad_group_criterion is not None:
            bulk_ad_group_product_partition.ad_group_criterion.AdGroupId=self._ad_group_id
            bulk_ad_group_product_partition.ad_group_criterion.Status='Deleted'
            if hasattr(bulk_ad_group_product_partition.ad_group_criterion, 'EditorialStatus'):
                bulk_ad_group_product_partition.ad_group_criterion.EditorialStatus=None
            self._partition_actions.append(bulk_ad_group_product_partition)

    def update_partition(self, bulk_ad_group_product_partition):
        """ 
        Sets the Update action for the specified BiddableAdGroupCriterion, 
        and adds it to the helper's list of BulkAdGroupProductPartition. 
        You can only update the CriterionBid and DestinationUrl elements 
        of the BiddableAdGroupCriterion. 
        When working with product partitions, youu cannot update the Criterion (ProductPartition). 
        To update a ProductPartition, you must delete the existing node (delete_partition) and 
        add a new one (add_unit or add_subdivision) during the same upload.

        :param bulk_ad_group_product_partition: The BulkAdGroupProductPartition to update.
        :type bulk_ad_group_product_partition: BulkAdGroupProductPartition
        """

        if bulk_ad_group_product_partition is not None and bulk_ad_group_product_partition.ad_group_criterion is not None:
            bulk_ad_group_product_partition.ad_group_criterion.AdGroupId=self._ad_group_id
            bulk_ad_group_product_partition.ad_group_criterion.Status=None
            if hasattr(bulk_ad_group_product_partition.ad_group_criterion, 'EditorialStatus'):
                bulk_ad_group_product_partition.ad_group_criterion.EditorialStatus=None
            self._partition_actions.append(bulk_ad_group_product_partition)


# Main execution
if __name__ == '__main__':

    print("Loading the web service client proxies...")
    
    authorization_data=AuthorizationData(
        account_id=None,
        customer_id=None,
        developer_token=DEVELOPER_TOKEN,
        authentication=None,
    )

    bulk_service_manager=BulkServiceManager(
        authorization_data=authorization_data, 
        poll_interval_in_milliseconds=5000, 
        environment=ENVIRONMENT,
    )

    campaign_service=ServiceClient(
        service='CampaignManagementService', 
        version=13,
        authorization_data=authorization_data, 
        environment=ENVIRONMENT,
    )
        
    authenticate(authorization_data)
        
    main(authorization_data)
