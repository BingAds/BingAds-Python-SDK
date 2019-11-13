from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data):

    try:
        # Get a list of all Bing Merchant Center stores associated with your CustomerId.

        output_status_message("-----\nGetBMCStoresByCustomerId:")
        stores=campaign_service.GetBMCStoresByCustomerId()['BMCStore']
        if stores is None:
            output_status_message(
                "You do not have any BMC stores registered for CustomerId {0}.".format(authorization_data.customer_id)
            )
            sys.exit(0)

        # Create a Shopping campaign with product conditions.

        campaigns=campaign_service.factory.create('ArrayOfCampaign')
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
                
        # Optionally, you can create a ProductScope criterion that will be associated with your Microsoft Shopping campaign. 
        # You'll also be able to add more specific product conditions for each ad group.

        campaign_criterions=campaign_service.factory.create('ArrayOfCampaignCriterion')
        campaign_criterion=set_elements_to_none(campaign_service.factory.create('BiddableCampaignCriterion'))
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
        campaign_criterion.CampaignId=campaign_ids['long'][0]
        campaign_criterion.CriterionBid=None # Not applicable for product scope
        campaign_criterion.Criterion=product_scope
        campaign_criterions.CampaignCriterion.append(campaign_criterion)

        output_status_message("-----\nAddCampaignCriterions:")
        add_campaign_criterions_response = campaign_service.AddCampaignCriterions(
            CampaignCriterions=campaign_criterions,
            CriterionType='ProductScope'
        )
        campaign_criterion_ids={
            'long': add_campaign_criterions_response.CampaignCriterionIds['long'] 
            if add_campaign_criterions_response.CampaignCriterionIds['long'] else None
        }
        output_status_message("CampaignCriterionIds:")
        output_array_of_long(campaign_criterion_ids)
        output_status_message("NestedPartialErrors:")
        output_array_of_batcherrorcollection(add_campaign_criterions_response.NestedPartialErrors) 
        
        # Create the ad group that will have the product partitions.

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

        # Bid all products

        helper=PartitionActionHelper(ad_group_ids['long'][0])
        
        root_condition=campaign_service.factory.create('ProductCondition')
        root_condition.Operand='All'
        root_condition.Attribute=None

        root=helper.add_unit(
            None,
            root_condition,
            0.35,
            False
        )

        output_status_message("-----\nApplyProductPartitionActions:")
        output_status_message("Applying only the root as a Unit with a bid...")
        apply_product_partition_actions_response=campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )

        output_status_message("-----\nGetAdGroupCriterionsByIds:")
        ad_group_criterions=campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=None,
            CriterionType='ProductPartition'
        )

        output_status_message("The ad group's product partition only has a tree root node: \n")
        output_product_partitions(ad_group_criterions)

        # Let's update the bid of the root Unit we just added.

        updated_root=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        fixed_bid=set_elements_to_none(campaign_service.factory.create('FixedBid'))
        fixed_bid.Amount=0.45
        updated_root.Id=apply_product_partition_actions_response.AdGroupCriterionIds['long'][0]
        updated_root.CriterionBid=fixed_bid
                
        helper=PartitionActionHelper(ad_group_ids['long'][0])
        helper.update_partition(updated_root)

        output_status_message("-----\nApplyProductPartitionActions:")
        output_status_message("Updating the bid for the tree root node...")
        campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )

        output_status_message("-----\nGetAdGroupCriterionsByIds:")
        ad_group_criterions=campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=None,
            CriterionType='ProductPartition'
        )

        output_status_message("Updated the bid for the tree root node: \n")
        output_product_partitions(ad_group_criterions)
        
        # Initialize and overwrite any existing tree root, and build a product partition group tree structure in multiple steps. 
        # You could build the entire tree in a single call since there are less than 20,000 nodes; however, 
        # we will build it in steps to demonstrate how to use the results from bulk upload to update the tree. 
        
        helper=PartitionActionHelper(ad_group_ids['long'][0])

        #Check whether a root node exists already.

        output_status_message("-----\nGetAdGroupCriterionsByIds:")
        ad_group_criterions=campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=None,
            CriterionType='ProductPartition'
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
        #https://go.microsoft.com/fwlink?LinkId=507666
        
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

        output_status_message("-----\nApplyProductPartitionActions:")
        output_status_message("Applying product partitions to the ad group...")
        apply_product_partition_actions_response=campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )

        # To retrieve product partitions after they have been applied, call GetAdGroupCriterionsByIds. 
        # The product partition with ParentCriterionId set to null is the root node.

        output_status_message("-----\nGetAdGroupCriterionsByIds:")
        ad_group_criterions=campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=None,
            CriterionType='ProductPartition'
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

        helper=PartitionActionHelper(ad_group_ids['long'][0])
        
        #To replace a node we must know its Id and its ParentCriterionId. In this case the parent of the node 
        #we are replacing is All other (Root Node), and was created at Index 1 of the previous ApplyProductPartitionActions call. 
        #The node that we are replacing is Electronics (CategoryL1), and was created at Index 8. 
        
        root_id=apply_product_partition_actions_response.AdGroupCriterionIds['long'][1]
        electronics.Id=apply_product_partition_actions_response.AdGroupCriterionIds['long'][8]
        helper.delete_partition(electronics)

        parent=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
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

        output_status_message("-----\nApplyProductPartitionActions:")
        output_status_message(
            "Updating the product partition group to refine Electronics (CategoryL1) with 3 child nodes..."
        )
        apply_product_partition_actions_response=campaign_service.ApplyProductPartitionActions(
            CriterionActions=helper.partition_actions
        )
                
        output_status_message("-----\nGetAdGroupCriterionsByIds:")
        ad_group_criterions=campaign_service.GetAdGroupCriterionsByIds(
            AdGroupId=ad_group_ids['long'][0],
            AdGroupCriterionIds=None,
            CriterionType='ProductPartition'
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
        
        #Create a product ad. You must add at least one product ad to the ad group. 
        #The product ad identifier can be used for reporting analytics.
        #Use Merchant Promotions if you want tags to appear at the bottom of your product ad 
        #as "special offer" links, helping to increase customer engagement. For details
        #on Merchant Promotions see https://help.bingads.microsoft.com/#apex/3/en/56805/0.
        
        ads=campaign_service.factory.create('ArrayOfAd')
        product_ad=set_elements_to_none(campaign_service.factory.create('ProductAd'))
        product_ad.Type='Product'
        product_ad.Status=None
        product_ad.EditorialStatus=None
        ads.Ad.append(product_ad)

        output_status_message("-----\nAddAds:")
        add_ads_response=campaign_service.AddAds(
            AdGroupId=ad_group_ids['long'][0],
            Ads=ads
        )
        ad_ids={
            'long': add_ads_response.AdIds['long'] if add_ads_response.AdIds['long'] else None
        }
        output_status_message("AdIds:")
        output_array_of_long(ad_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_ads_response.PartialErrors)
        
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

def output_product_partitions(ad_group_criterions):
    """
    Outputs the list of AdGroupCriterion, formatted as a tree. 
    Each AdGroupCriterion must be either a BiddableAdGroupCriterion or NegativeAdGroupCriterion. 
    To ensure the complete tree is represented, you should first call GetAdGroupCriterionsByIds 
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
                node.CriterionBid.Amount)
            )
        elif node.Type == 'NegativeAdGroupCriterion':
            output_status_message("{0}Not Bidding on this Condition".format(
                pad)
            )
           

    null_attribute="(All other)" if node.Criterion.ParentCriterionId is not None else "(Tree Root)"
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

        biddable_ad_group_criterion=set_elements_to_none(campaign_service.factory.create('BiddableAdGroupCriterion'))
        product_partition=set_elements_to_none(campaign_service.factory.create('ProductPartition'))
        # If the root node is a unit, it would not have a parent
        product_partition.ParentCriterionId=parent.Id if parent is not None else None
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

        partition_action=set_elements_to_none(campaign_service.factory.create('AdGroupCriterionAction'))
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
        product_partition.ParentCriterionId=parent.Id if parent is not None else None
        product_partition.Condition=condition
        product_partition.PartitionType='Unit'
        ad_group_criterion.Criterion=product_partition=product_partition

        partition_action=set_elements_to_none(campaign_service.factory.create('AdGroupCriterionAction'))
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

        partition_action=set_elements_to_none(campaign_service.factory.create('AdGroupCriterionAction'))
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

        partition_action=set_elements_to_none(campaign_service.factory.create('AdGroupCriterionAction'))
        partition_action.Action='Update'
        partition_action.AdGroupCriterion=biddable_ad_group_criterion
        self._partition_actions.AdGroupCriterionAction.append(partition_action)

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
