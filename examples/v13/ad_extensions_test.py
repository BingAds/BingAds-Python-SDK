import uuid
from auth_helper import *
from openapi_client.models.campaign import *

# Media file path - update with your own image
MEDIA_FILE_PATH = "c:\\dev\\media\\"
IMAGE_AD_EXTENSION_FILE_NAME = "imageadextension300x200.png"

def main(authorization_data):
    try:
        # Create a search campaign
        print("Creating campaign...")
        
        campaign = Campaign(
            name="Women's Shoes " + str(uuid.uuid4()),
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
        
        # Create ad extensions
        print("\nCreating ad extensions...")
        
        ad_extensions = []
        
        # Action Ad Extension
        action_extension = ActionAdExtension(
            action_type=ActionAdExtensionActionType.ACTNOW,
            final_urls=["http://www.contoso.com/womenshoesale"],
            language="English",
            status=AdExtensionStatus.ACTIVE
        )
        ad_extensions.append(action_extension)
        
        # Call Ad Extension with scheduling
        call_extension = CallAdExtension(
            country_code="US",
            phone_number="2065550100",
            is_call_only=False
        )
        
        # Schedule for Monday-Friday 9am-9pm
        call_day_time_ranges = []
        for day in [Day.MONDAY, Day.TUESDAY, Day.WEDNESDAY, Day.THURSDAY, Day.FRIDAY]:
            day_time = DayTime(
                day=day,
                start_hour=9,
                start_minute=Minute.ZERO,
                end_hour=21,
                end_minute=Minute.ZERO
            )
            call_day_time_ranges.append(day_time)
        
        from datetime import datetime
        current_year = datetime.now().year
        
        call_scheduling = Schedule(
            day_time_ranges=call_day_time_ranges,
            use_searcher_time_zone=False,
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year)
        )
        call_extension.Scheduling = call_scheduling
        ad_extensions.append(call_extension)
        
        # Callout Ad Extension
        callout_extension = CalloutAdExtension(
            text="Callout Text"
        )
        ad_extensions.append(callout_extension)
        
        # Location Ad Extension
        location_extension = LocationAdExtension(
            phone_number="206-555-0100",
            company_name="Alpine Ski House",
            address=Address(
                street_address="1234 Washington Place",
                street_address2="Suite 1210",
                city_name="Woodinville",
                province_name="WA",
                country_code="US",
                postal_code="98608"
            )
        )
        
        # Schedule for Saturday morning
        location_day_time = DayTime(
            day=Day.SATURDAY,
            start_hour=9,
            start_minute=Minute.ZERO,
            end_hour=12,
            end_minute=Minute.ZERO
        )
        
        location_scheduling = Schedule(
            day_time_ranges=[location_day_time],
            use_searcher_time_zone=False,
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year)
        )
        location_extension.Scheduling = location_scheduling
        ad_extensions.append(location_extension)
        
        # Price Ad Extension
        price_extension = PriceAdExtension(
            language="English",
            price_extension_type="Events",
            table_rows=[
                PriceTableRow(
                    currency_code="USD",
                    description="Come to the event",
                    final_urls=["http://www.contoso.com/womenshoesale"],
                    header="New Event",
                    price=9.99,
                    price_qualifier="From",
                    price_unit="PerDay"
                ),
                PriceTableRow(
                    currency_code="USD",
                    description="Come to the next event",
                    final_urls=["http://www.contoso.com/womenshoesale"],
                    header="Next Event",
                    price=9.99,
                    price_qualifier="From",
                    price_unit="PerDay"
                ),
                PriceTableRow(
                    currency_code="USD",
                    description="Come to the final event",
                    final_urls=["http://www.contoso.com/womenshoesale"],
                    header="Final Event",
                    price=9.99,
                    price_qualifier="From",
                    price_unit="PerDay"
                )
            ]
        )
        ad_extensions.append(price_extension)
        
        # Review Ad Extension
        review_extension = ReviewAdExtension(
            is_exact=True,
            source="Review Source Name",
            text="Review Text",
            url="http://review.contoso.com"
        )
        ad_extensions.append(review_extension)
        
        # Sitelink Ad Extension
        sitelink_extension = SitelinkAdExtension(
            description1="Simple & Transparent.",
            description2="No Upfront Cost.",
            display_text="Women's Shoe Sale",
            final_urls=["http://www.contoso.com/womenshoesale"]
        )
        ad_extensions.append(sitelink_extension)
        
        # Structured Snippet Ad Extension
        structured_snippet_extension = StructuredSnippetAdExtension(
            header="Brands",
            values=["Windows", "Xbox", "Skype"]
        )
        ad_extensions.append(structured_snippet_extension)
        
        # Add all extensions to the account's ad extension library
        add_extensions_request = AddAdExtensionsRequest(
            account_id=authorization_data.account_id,
            ad_extensions=ad_extensions
        )
        
        add_extensions_response = campaign_service.add_ad_extensions(
            add_ad_extensions_request=add_extensions_request
        )
        
        ad_extension_identities = add_extensions_response.AdExtensionIdentities
        print(f"Added {len(ad_extension_identities)} ad extensions")
        
        if add_extensions_response.NestedPartialErrors:
            print(f"Nested Partial Errors: {add_extensions_response.NestedPartialErrors}")
        
        # Build associations
        ad_extension_id_to_entity_id_associations = []
        ad_extension_ids = []
        
        for identity in ad_extension_identities:
            if identity and identity.Id:
                association = AdExtensionIdToEntityIdAssociation(
                    ad_extension_id=identity.Id,
                    entity_id=campaign_ids[0]
                )
                ad_extension_id_to_entity_id_associations.append(association)
                ad_extension_ids.append(identity.Id)
        
        # Associate the ad extensions with the campaign
        print("\nAssociating ad extensions with campaign...")
        
        set_associations_request = SetAdExtensionsAssociationsRequest(
            account_id=authorization_data.account_id,
            ad_extension_id_to_entity_id_associations=ad_extension_id_to_entity_id_associations,
            association_type=AssociationType.CAMPAIGN
        )
        
        set_associations_response = campaign_service.set_ad_extensions_associations(
            set_ad_extensions_associations_request=set_associations_request
        )
        
        if set_associations_response.PartialErrors:
            print(f"Partial Errors: {set_associations_response.PartialErrors}")
        else:
            print("Ad extensions successfully associated with campaign")
        
        # Get editorial rejection reasons
        print("\nGetting editorial reasons...")
        
        get_editorial_request = GetAdExtensionsEditorialReasonsRequest(
            account_id=authorization_data.account_id,
            ad_extension_id_to_entity_id_associations=ad_extension_id_to_entity_id_associations,
            association_type=AssociationType.CAMPAIGN
        )
        
        editorial_response = campaign_service.get_ad_extensions_editorial_reasons(
            get_ad_extensions_editorial_reasons_request=get_editorial_request
        )
        
        if editorial_response.EditorialReasons:
            print(f"Editorial Reasons: {editorial_response.EditorialReasons}")
        
        # Get location and call extensions
        print("\nGetting location and call extensions...")
        
        get_extensions_request = GetAdExtensionsByIdsRequest(
            account_id=authorization_data.account_id,
            ad_extension_ids=ad_extension_ids,
            ad_extension_type= AdExtensionsTypeFilter.LOCATIONADEXTENSION | AdExtensionsTypeFilter.CALLADEXTENSION
            ,
            return_additional_fields=None
        )
        
        get_extensions_response = campaign_service.get_ad_extensions_by_ids(
            get_ad_extensions_by_ids_request=get_extensions_request
        )
        
        extensions_to_update = []
        
        for extension in get_extensions_response.AdExtensions:
            if extension and extension.Id:
                # Remove scheduling
                extension.Scheduling = Schedule()
                extensions_to_update.append(extension)
        
        # Update extensions to remove scheduling
        if extensions_to_update:
            print("\nUpdating extensions to remove scheduling...")
            
            update_request = UpdateAdExtensionsRequest(
                account_id=authorization_data.account_id,
                ad_extensions=extensions_to_update
            )
            
            update_response = campaign_service.update_ad_extensions(
                update_ad_extensions_request=update_request
            )
            
            if update_response.NestedPartialErrors:
                print(f"Nested Partial Errors: {update_response.NestedPartialErrors}")
            else:
                print("Removed scheduling from extensions")
        
        # Clean up - delete associations
        print("\nDeleting ad extension associations...")
        
        delete_associations_request = DeleteAdExtensionsAssociationsRequest(
            account_id=authorization_data.account_id,
            ad_extension_id_to_entity_id_associations=ad_extension_id_to_entity_id_associations,
            association_type=AssociationType.CAMPAIGN
        )
        
        delete_associations_response = campaign_service.delete_ad_extensions_associations(
            delete_ad_extensions_associations_request=delete_associations_request
        )
        
        if delete_associations_response.PartialErrors:
            print(f"Partial Errors: {delete_associations_response.PartialErrors}")
        
        # Delete ad extensions
        print("Deleting ad extensions...")
        
        delete_extensions_request = DeleteAdExtensionsRequest(
            account_id=authorization_data.account_id,
            ad_extension_ids=ad_extension_ids
        )
        
        delete_extensions_response = campaign_service.delete_ad_extensions(
            delete_ad_extensions_request=delete_extensions_request
        )
        
        if delete_extensions_response.PartialErrors:
            print(f"Partial Errors: {delete_extensions_response.PartialErrors}")
        else:
            print("Deleted ad extensions")
        
        # Delete campaign
        print("Deleting campaign...")
        
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