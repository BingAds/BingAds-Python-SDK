from auth_helper import *
from bingads.v13.bulk import *
from openapi_client.models.campaign import *
from datetime import datetime

def main(authorization_data):
    try:
        # Create campaign and various ad extensions using bulk API
        print("Adding campaign and ad extensions...")
        
        upload_entities = []
        
        # Create a BulkCampaign
        bulk_campaign = BulkCampaign()
        bulk_campaign.account_id = authorization_data.account_id
        campaign = Campaign(
            budget_type='DailyBudgetStandard',
            daily_budget=50,
            languages=['All'],
            name="Women's Shoes " + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()),
            time_zone='PacificTimeUSCanadaTijuana'
        )
        bulk_campaign.campaign = campaign
        upload_entities.append(bulk_campaign)
        
        final_urls = ["https://www.contoso.com/womenshoesale"]
        current_year = datetime.now().year
        
        # 1. Action Ad Extension
        bulk_action_ad_extension = BulkActionAdExtension()
        bulk_action_ad_extension.account_id = authorization_data.account_id
        action_ad_extension = ActionAdExtension(
            action_type='ActNow',
            final_urls=final_urls,
            language="English",
            status='Active'
        )
        bulk_action_ad_extension.action_ad_extension = action_ad_extension
        upload_entities.append(bulk_action_ad_extension)
        
        # Association for Action Ad Extension
        bulk_campaign_action_ad_extension = BulkCampaignActionAdExtension()
        action_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-21',  # Negative ID references extension in same file
            entity_id='-11'  # Negative ID references campaign in same file
        )
        bulk_campaign_action_ad_extension.ad_extension_id_to_entity_id_association = action_association
        upload_entities.append(bulk_campaign_action_ad_extension)
        
        # 2. App Ad Extension (may fail without valid AppStoreId)
        bulk_app_ad_extension = BulkAppAdExtension()
        bulk_app_ad_extension.account_id = authorization_data.account_id
        app_ad_extension = AppAdExtension(
            app_platform="Windows",
            app_store_id="AppStoreIdGoesHere",
            display_text="Contoso",
            destination_url="DestinationUrlGoesHere",
            status=None
        )
        bulk_app_ad_extension.app_ad_extension = app_ad_extension
        upload_entities.append(bulk_app_ad_extension)
        
        bulk_campaign_app_ad_extension = BulkCampaignAppAdExtension()
        app_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-22',
            entity_id='-11'
        )
        bulk_campaign_app_ad_extension.ad_extension_id_to_entity_id_association = app_association
        upload_entities.append(bulk_campaign_app_ad_extension)
        
        # 3. Call Ad Extension with scheduling
        bulk_call_ad_extension = BulkCallAdExtension()
        bulk_call_ad_extension.account_id = authorization_data.account_id
        call_ad_extension = CallAdExtension(
            country_code="US",
            phone_number="2065550100",
            is_call_only=False,
            status=None
        )
        
        # Schedule for Monday-Friday 9am-9pm
        call_day_time_ranges = []
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            day_time = DayTime(
                day=day,
                start_hour=9,
                start_minute='Zero',
                end_hour=21,
                end_minute='Zero'
            )
            call_day_time_ranges.append(day_time)
        
        call_scheduling = Schedule(
            day_time_ranges=call_day_time_ranges,
            use_searcher_time_zone=False,
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year)
        )
        call_ad_extension.Scheduling = call_scheduling
        bulk_call_ad_extension.call_ad_extension = call_ad_extension
        upload_entities.append(bulk_call_ad_extension)
        
        bulk_campaign_call_ad_extension = BulkCampaignCallAdExtension()
        call_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-23',
            entity_id='-11'
        )
        bulk_campaign_call_ad_extension.ad_extension_id_to_entity_id_association = call_association
        upload_entities.append(bulk_campaign_call_ad_extension)
        
        # 4. Callout Ad Extension
        bulk_callout_ad_extension = BulkCalloutAdExtension()
        bulk_callout_ad_extension.account_id = authorization_data.account_id
        callout_ad_extension = CalloutAdExtension(
            text="Callout Text",
            status=None
        )
        bulk_callout_ad_extension.callout_ad_extension = callout_ad_extension
        upload_entities.append(bulk_callout_ad_extension)
        
        bulk_campaign_callout_ad_extension = BulkCampaignCalloutAdExtension()
        callout_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-24',
            entity_id='-11'
        )
        bulk_campaign_callout_ad_extension.ad_extension_id_to_entity_id_association = callout_association
        upload_entities.append(bulk_campaign_callout_ad_extension)
        
        # 5. Location Ad Extension with scheduling
        bulk_location_ad_extension = BulkLocationAdExtension()
        bulk_location_ad_extension.account_id = authorization_data.account_id
        location_ad_extension = LocationAdExtension(
            phone_number="206-555-0100",
            company_name="Contoso Shoes",
            address=Address(
                street_address="1234 Washington Place",
                street_address2="Suite 1210",
                city_name="Woodinville",
                province_name="WA",
                country_code="US",
                postal_code="98608"
            ),
            status=None
        )
        
        # Schedule for Saturday morning
        location_scheduling = Schedule(
            day_time_ranges=[
                DayTime(
                    day='Saturday',
                    start_hour=9,
                    start_minute='Zero',
                    end_hour=12,
                    end_minute='Zero'
                )
            ],
            use_searcher_time_zone=False,
            start_date=None,
            end_date=Date(day=31, month=12, year=current_year)
        )
        location_ad_extension.Scheduling = location_scheduling
        bulk_location_ad_extension.location_ad_extension = location_ad_extension
        upload_entities.append(bulk_location_ad_extension)
        
        bulk_campaign_location_ad_extension = BulkCampaignLocationAdExtension()
        location_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-25',
            entity_id='-11'
        )
        bulk_campaign_location_ad_extension.ad_extension_id_to_entity_id_association = location_association
        upload_entities.append(bulk_campaign_location_ad_extension)
        
        # 6. Price Ad Extension
        bulk_price_ad_extension = BulkPriceAdExtension()
        bulk_price_ad_extension.account_id = authorization_data.account_id
        price_ad_extension = PriceAdExtension(
            language="English",
            price_extension_type="Events",
            table_rows=[
                PriceTableRow(
                    currency_code="USD",
                    description="Come to the event",
                    final_urls=final_urls,
                    header="New Event",
                    price=9.99,
                    price_qualifier="From",
                    price_unit="PerDay"
                ),
                PriceTableRow(
                    currency_code="USD",
                    description="Come to the next event",
                    final_urls=final_urls,
                    header="Next Event",
                    price=9.99,
                    price_qualifier="From",
                    price_unit="PerDay"
                ),
                PriceTableRow(
                    currency_code="USD",
                    description="Come to the final event",
                    final_urls=final_urls,
                    header="Final Event",
                    price=9.99,
                    price_qualifier="From",
                    price_unit="PerDay"
                )
            ]
        )
        bulk_price_ad_extension.price_ad_extension = price_ad_extension
        upload_entities.append(bulk_price_ad_extension)
        
        bulk_campaign_price_ad_extension = BulkCampaignPriceAdExtension()
        price_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-26',
            entity_id='-11'
        )
        bulk_campaign_price_ad_extension.ad_extension_id_to_entity_id_association = price_association
        upload_entities.append(bulk_campaign_price_ad_extension)
        
        # 7. Review Ad Extension
        bulk_review_ad_extension = BulkReviewAdExtension()
        bulk_review_ad_extension.account_id = authorization_data.account_id
        review_ad_extension = ReviewAdExtension(
            is_exact=True,
            source="Review Source Name",
            text="Review Text",
            url="https://review.contoso.com",
            status=None
        )
        bulk_review_ad_extension.review_ad_extension = review_ad_extension
        upload_entities.append(bulk_review_ad_extension)
        
        bulk_campaign_review_ad_extension = BulkCampaignReviewAdExtension()
        review_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-27',
            entity_id='-11'
        )
        bulk_campaign_review_ad_extension.ad_extension_id_to_entity_id_association = review_association
        upload_entities.append(bulk_campaign_review_ad_extension)
        
        # 8. Sitelink Ad Extension
        bulk_sitelink_ad_extension = BulkSitelinkAdExtension()
        bulk_sitelink_ad_extension.account_id = authorization_data.account_id
        sitelink_ad_extension = SitelinkAdExtension(
            description1="Simple & Transparent.",
            description2="No Upfront Cost.",
            display_text="Women's Shoe Sale",
            final_urls=final_urls
        )
        bulk_sitelink_ad_extension.sitelink_ad_extension = sitelink_ad_extension
        upload_entities.append(bulk_sitelink_ad_extension)
        
        bulk_campaign_sitelink_ad_extension = BulkCampaignSitelinkAdExtension()
        sitelink_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-28',
            entity_id='-11'
        )
        bulk_campaign_sitelink_ad_extension.ad_extension_id_to_entity_id_association = sitelink_association
        upload_entities.append(bulk_campaign_sitelink_ad_extension)
        
        # 9. Structured Snippet Ad Extension
        bulk_structured_snippet_ad_extension = BulkStructuredSnippetAdExtension()
        bulk_structured_snippet_ad_extension.account_id = authorization_data.account_id
        structured_snippet_ad_extension = StructuredSnippetAdExtension(
            header="Brands",
            values=["Windows", "Xbox", "Skype"]
        )
        bulk_structured_snippet_ad_extension.structured_snippet_ad_extension = structured_snippet_ad_extension
        upload_entities.append(bulk_structured_snippet_ad_extension)
        
        bulk_campaign_structured_snippet_ad_extension = BulkCampaignStructuredSnippetAdExtension()
        structured_snippet_association = AdExtensionIdToEntityIdAssociation(
            ad_extension_id='-29',
            entity_id='-11'
        )
        bulk_campaign_structured_snippet_ad_extension.ad_extension_id_to_entity_id_association = structured_snippet_association
        upload_entities.append(bulk_campaign_structured_snippet_ad_extension)
        
        # Upload all entities
        print(f"Uploading {len(upload_entities)} entities...")
        
        download_entities = list(bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        ))
        
        print("\nUpload results:")
        
        campaign_results = []
        action_ad_extension_results = []
        app_ad_extension_results = []
        call_ad_extension_results = []
        callout_ad_extension_results = []
        location_ad_extension_results = []
        price_ad_extension_results = []
        review_ad_extension_results = []
        sitelink_ad_extension_results = []
        structured_snippet_ad_extension_results = []
        
        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                campaign_results.append(entity)
                if entity.campaign and entity.campaign.Id:
                    print(f"Campaign ID: {entity.campaign.Id}, Name: {entity.campaign.Name}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkActionAdExtension):
                action_ad_extension_results.append(entity)
                if entity.action_ad_extension and entity.action_ad_extension.Id:
                    print(f"Action Ad Extension ID: {entity.action_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkCampaignActionAdExtension):
                if entity.has_errors:
                    print(f"Campaign Action Ad Extension Association Errors: {entity.errors}")
            elif isinstance(entity, BulkAppAdExtension):
                app_ad_extension_results.append(entity)
                if entity.has_errors:
                    print(f"App Ad Extension Errors (expected): {entity.errors}")
            elif isinstance(entity, BulkCallAdExtension):
                call_ad_extension_results.append(entity)
                if entity.call_ad_extension and entity.call_ad_extension.Id:
                    print(f"Call Ad Extension ID: {entity.call_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkCalloutAdExtension):
                callout_ad_extension_results.append(entity)
                if entity.callout_ad_extension and entity.callout_ad_extension.Id:
                    print(f"Callout Ad Extension ID: {entity.callout_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkLocationAdExtension):
                location_ad_extension_results.append(entity)
                if entity.location_ad_extension and entity.location_ad_extension.Id:
                    print(f"Location Ad Extension ID: {entity.location_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkPriceAdExtension):
                price_ad_extension_results.append(entity)
                if entity.price_ad_extension and entity.price_ad_extension.Id:
                    print(f"Price Ad Extension ID: {entity.price_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkReviewAdExtension):
                review_ad_extension_results.append(entity)
                if entity.review_ad_extension and entity.review_ad_extension.Id:
                    print(f"Review Ad Extension ID: {entity.review_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkSitelinkAdExtension):
                sitelink_ad_extension_results.append(entity)
                if entity.sitelink_ad_extension and entity.sitelink_ad_extension.Id:
                    print(f"Sitelink Ad Extension ID: {entity.sitelink_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
            elif isinstance(entity, BulkStructuredSnippetAdExtension):
                structured_snippet_ad_extension_results.append(entity)
                if entity.structured_snippet_ad_extension and entity.structured_snippet_ad_extension.Id:
                    print(f"Structured Snippet Ad Extension ID: {entity.structured_snippet_ad_extension.Id}")
                if entity.has_errors:
                    print(f"  Errors: {entity.errors}")
        
        # Delete campaign and ad extensions
        print("\nDeleting campaign and ad extensions...")
        
        upload_entities = []
        
        for campaign_result in campaign_results:
            if campaign_result.campaign:
                campaign_result.campaign.Status = 'Deleted'
            upload_entities.append(campaign_result)
        
        for action_ad_extension_result in action_ad_extension_results:
            if action_ad_extension_result.action_ad_extension:
                action_ad_extension_result.action_ad_extension.Status = 'Deleted'
            upload_entities.append(action_ad_extension_result)
        
        # Note: App ad extensions likely failed, so skip deleting them
        
        for call_ad_extension_result in call_ad_extension_results:
            if call_ad_extension_result.call_ad_extension:
                call_ad_extension_result.call_ad_extension.Status = 'Deleted'
            upload_entities.append(call_ad_extension_result)
        
        for callout_ad_extension_result in callout_ad_extension_results:
            if callout_ad_extension_result.callout_ad_extension:
                callout_ad_extension_result.callout_ad_extension.Status = 'Deleted'
            upload_entities.append(callout_ad_extension_result)
        
        for location_ad_extension_result in location_ad_extension_results:
            if location_ad_extension_result.location_ad_extension:
                location_ad_extension_result.location_ad_extension.Status = 'Deleted'
            upload_entities.append(location_ad_extension_result)
        
        for price_ad_extension_result in price_ad_extension_results:
            if price_ad_extension_result.price_ad_extension:
                price_ad_extension_result.price_ad_extension.Status = 'Deleted'
            upload_entities.append(price_ad_extension_result)
        
        for review_ad_extension_result in review_ad_extension_results:
            if review_ad_extension_result.review_ad_extension:
                review_ad_extension_result.review_ad_extension.Status = 'Deleted'
            upload_entities.append(review_ad_extension_result)
        
        for sitelink_ad_extension_result in sitelink_ad_extension_results:
            if sitelink_ad_extension_result.sitelink_ad_extension:
                sitelink_ad_extension_result.sitelink_ad_extension.Status = 'Deleted'
            upload_entities.append(sitelink_ad_extension_result)
        
        for structured_snippet_ad_extension_result in structured_snippet_ad_extension_results:
            if structured_snippet_ad_extension_result.structured_snippet_ad_extension:
                structured_snippet_ad_extension_result.structured_snippet_ad_extension.Status = 'Deleted'
            upload_entities.append(structured_snippet_ad_extension_result)
        
        download_entities = list(bulk_service_manager.upload_entities(
            EntityUploadParameters(
                entities=upload_entities,
                response_mode='ErrorsAndResults'
            )
        ))
        
        print("Delete results:")
        for entity in download_entities:
            if isinstance(entity, BulkCampaign):
                print(f"Deleted Campaign ID: {entity.campaign.Id if entity.campaign else 'N/A'}")
            elif hasattr(entity, 'has_errors') and entity.has_errors:
                print(f"Delete Error: {entity.errors}")
        
        print("\nProgram execution completed")
        
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
    
    bulk_service_manager = BulkServiceManager(
        authorization_data=authorization_data,
        poll_interval_in_milliseconds=5000,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)