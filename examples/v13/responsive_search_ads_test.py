import uuid
from auth_helper import *
from openapi_client.models.campaign import *

def main(authorization_data):
    try:
        # Create a campaign
        print("Creating campaign...")
        
        campaign = Campaign(
            name=f"Campaign_{uuid.uuid4()}",
            budget_type=BudgetLimitType.DAILYBUDGETSTANDARD,
            daily_budget=50.00,
            languages=['All'],
            time_zone='PacificTimeUSCanadaTijuana',
            campaign_type=CampaignType.SEARCH
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
        
        # Create an ad group
        print("\nCreating ad group...")
        
        ad_group = AdGroup(
            name=f"AdGroup_{uuid.uuid4()}",
            start_date=None,
            end_date=Date(day=31, month=12, year=datetime.now().year),
            cpc_bid=Bid(amount=0.10),
            language="English"
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
        
        # Create responsive search ads
        print("\nCreating responsive search ads...")
        
        ads = []
        
        # Responsive Search Ad requires multiple headlines and descriptions
        headlines = [
            AssetLink(asset=TextAsset(text="Find New Customers"), pinned_field="Headline1"),
            AssetLink(asset=TextAsset(text="Start Advertising on Contoso")),
            AssetLink(asset=TextAsset(text="Drive Sales"), pinned_field="Headline2"),
            AssetLink(asset=TextAsset(text="Increase Revenue")),
            AssetLink(asset=TextAsset(text="Contoso Solutions")),
            AssetLink(asset=TextAsset(text="Best Deals Here")),
            AssetLink(asset=TextAsset(text="Shop Now")),
            AssetLink(asset=TextAsset(text="Limited Time Offer")),
            AssetLink(asset=TextAsset(text="Exclusive Discounts")),
            AssetLink(asset=TextAsset(text="Top Quality Products")),
            AssetLink(asset=TextAsset(text="Fast Shipping")),
            AssetLink(asset=TextAsset(text="Customer Satisfaction")),
            AssetLink(asset=TextAsset(text="Trusted Brand")),
            AssetLink(asset=TextAsset(text="Great Prices")),
            AssetLink(asset=TextAsset(text="Buy Online Today"))
        ]
        
        descriptions = [
            AssetLink(asset=TextAsset(text="Find New Customers & Increase Sales! Start Advertising on Contoso Today.")),
            AssetLink(asset=TextAsset(text="Seamless Integration. Fast & Easy Setup. Get Started Today.")),
            AssetLink(asset=TextAsset(text="Join Thousands of Satisfied Customers. Shop Our Wide Selection.")),
            AssetLink(asset=TextAsset(text="Best Prices Guaranteed. Free Shipping on Orders Over $50."))
        ]
        
        responsive_search_ad = ResponsiveSearchAd(
            headlines=headlines,
            descriptions=descriptions,
            path1="seattle",
            path2="shoes",
            final_urls=["http://www.contoso.com/womenshoesale"],
            final_mobile_urls=["http://mobile.contoso.com/womenshoesale"]
        )
        
        ads.append(responsive_search_ad)
        
        add_ads_request = AddAdsRequest(
            ad_group_id=ad_group_ids[0],
            ads=ads
        )
        
        add_ads_response = campaign_service.add_ads(
            add_ads_request=add_ads_request
        )
        
        ad_ids = add_ads_response.AdIds
        print(f"Created {len(ad_ids)} responsive search ads")
        print(f"Ad IDs: {ad_ids}")
        
        if add_ads_response.PartialErrors:
            print(f"Partial Errors: {add_ads_response.PartialErrors}")
        
        # Get ads
        print("\nGetting responsive search ads...")
        
        get_ads_request = GetAdsByAdGroupIdRequest(
            ad_group_id=ad_group_ids[0],
            ad_types=[AdType.RESPONSIVESEARCH],
            return_additional_fields=None
        )
        
        get_ads_response = campaign_service.get_ads_by_ad_group_id(
            get_ads_by_ad_group_id_request=get_ads_request
        )
        
        retrieved_ads = get_ads_response.Ads
        print(f"Retrieved {len(retrieved_ads)} ads")
        
        for ad in retrieved_ads:
            if ad and hasattr(ad, 'Id'):
                print(f"  Ad ID: {ad.Id}")
                if hasattr(ad, 'Headlines'):
                    print(f"    Number of Headlines: {len(ad.Headlines)}")
                if hasattr(ad, 'Descriptions'):
                    print(f"    Number of Descriptions: {len(ad.Descriptions)}")
        
        # Update ad
        print("\nUpdating responsive search ad...")
        
        update_ads = []
        
        if len(retrieved_ads) > 0 and retrieved_ads[0]:
            # Update with new headlines and descriptions
            updated_headlines = [
                AssetLink(asset=TextAsset(text="Updated Find Customers")),
                AssetLink(asset=TextAsset(text="Updated Start Advertising")),
                AssetLink(asset=TextAsset(text="Updated Drive Sales")),
                AssetLink(asset=TextAsset(text="Updated Increase Revenue")),
                AssetLink(asset=TextAsset(text="Updated Solutions")),
                AssetLink(asset=TextAsset(text="Updated Best Deals")),
                AssetLink(asset=TextAsset(text="Updated Shop Now")),
                AssetLink(asset=TextAsset(text="Updated Time Offer")),
                AssetLink(asset=TextAsset(text="Updated Discounts"))
            ]
            
            updated_descriptions = [
                AssetLink(asset=TextAsset(text="Updated - Find New Customers & Increase Sales Today.")),
                AssetLink(asset=TextAsset(text="Updated - Seamless Integration & Fast Setup.")),
                AssetLink(asset=TextAsset(text="Updated - Join Satisfied Customers."))
            ]
            
            update_ad = ResponsiveSearchAd(
                id=ad_ids[0],
                headlines=updated_headlines,
                descriptions=updated_descriptions,
                final_urls=["http://www.contoso.com/womenshoesale"]
            )
            update_ads.append(update_ad)
        
        if update_ads:
            update_ads_request = UpdateAdsRequest(
                ad_group_id=ad_group_ids[0],
                ads=update_ads
            )
            
            update_ads_response = campaign_service.update_ads(
                update_ads_request=update_ads_request
            )
            
            if update_ads_response.PartialErrors:
                print(f"Partial Errors: {update_ads_response.PartialErrors}")
            else:
                print("Responsive search ad updated successfully")
        
        # Delete ads
        print("\nDeleting ads...")
        
        delete_ads_request = DeleteAdsRequest(
            ad_group_id=ad_group_ids[0],
            ad_ids=ad_ids
        )
        
        delete_ads_response = campaign_service.delete_ads(
            delete_ads_request=delete_ads_request
        )
        
        if delete_ads_response.PartialErrors:
            print(f"Partial Errors: {delete_ads_response.PartialErrors}")
        else:
            print(f"Deleted {len(ad_ids)} ads")
        
        # Delete ad group
        print("\nDeleting ad group...")
        
        delete_ad_groups_request = DeleteAdGroupsRequest(
            campaign_id=campaign_ids[0],
            ad_group_ids=ad_group_ids
        )
        
        campaign_service.delete_ad_groups(
            delete_ad_groups_request=delete_ad_groups_request
        )
        
        print(f"Deleted Ad Group ID {ad_group_ids[0]}")
        
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