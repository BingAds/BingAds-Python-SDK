from datetime import datetime
from auth_helper import *
from openapi_client.models.adinsight import *


def main():
    try:
        # Test 1: Get Keyword Ideas
        print("=" * 60)
        print("Test 1: Getting Keyword Ideas...")
        print("=" * 60)
        
        # Define attributes we want to retrieve for each keyword idea
        idea_attributes = [
            KeywordIdeaAttribute.ADGROUPID,
            KeywordIdeaAttribute.ADGROUPNAME,
            KeywordIdeaAttribute.KEYWORD,
            KeywordIdeaAttribute.SOURCE,
            KeywordIdeaAttribute.MONTHLYSEARCHCOUNTS,
            KeywordIdeaAttribute.SUGGESTEDBID,
            KeywordIdeaAttribute.COMPETITION,
            KeywordIdeaAttribute.RELEVANCE,
            KeywordIdeaAttribute.ADIMPRESSIONSHARE
        ]
        
        # Set up search parameters
        search_parameters = []
        
        # Date range parameter
        current_date = datetime.now()
        start_date = DayMonthAndYear(
            day=1,
            month=1,
            year=current_date.year - 1
        )
        end_date = DayMonthAndYear(
            day=1,
            month=current_date.month - 1 if current_date.month > 1 else 12,
            year=current_date.year - 1
        )
        
        date_range_param = DateRangeSearchParameter(
            start_date=start_date,
            end_date=end_date
        )
        search_parameters.append(date_range_param)
        
        # Query search parameter
        query_param = QuerySearchParameter(
            queries=["tennis", "tennis shoes", "running", "running shoes", "cross training", "running"]
        )
        search_parameters.append(query_param)
        
        # Language parameter
        language_criterion = LanguageCriterion(
            language="English"
        )
        language_param = LanguageSearchParameter(
            languages=[language_criterion]
        )
        search_parameters.append(language_param)
        
        # Location parameter (United States)
        location_criterion = LocationCriterion(
            location_id='190'
        )
        location_param = LocationSearchParameter(
            locations=[location_criterion]
        )
        search_parameters.append(location_param)
        
        # Network parameter
        network_criterion = NetworkCriterion(
            network=NetworkType.OWNEDANDOPERATEDANDSYNDICATEDSEARCH
        )
        network_param = NetworkSearchParameter(
            network=network_criterion
        )
        search_parameters.append(network_param)
        
        # Create the request
        get_keyword_ideas_request = GetKeywordIdeasRequest(
            expand_ideas=True,
            idea_attributes=idea_attributes,
            search_parameters=search_parameters
        )
        
        # Call the service
        keyword_ideas_response = ad_insight_service.get_keyword_ideas(
            get_keyword_ideas_request=get_keyword_ideas_request
        )
        
        keyword_ideas = keyword_ideas_response.KeywordIdeas
        
        if not keyword_ideas or len(keyword_ideas) == 0:
            print("No keyword ideas found.")
            return
        
        print(f"\nFound {len(keyword_ideas)} keyword ideas:")
        
        # Display first few keyword ideas
        for i, idea in enumerate(keyword_ideas[:10]):  # Show first 10
            print(f"\n  Keyword Idea {i+1}:")
            if hasattr(idea, 'Keyword'):
                print(f"    Keyword: {idea.Keyword}")
            if hasattr(idea, 'Source'):
                print(f"    Source: {idea.Source}")
            if hasattr(idea, 'AdGroupId'):
                print(f"    AdGroupId: {idea.AdGroupId}")
            if hasattr(idea, 'AdGroupName'):
                print(f"    AdGroupName: {idea.AdGroupName}")
            if hasattr(idea, 'SuggestedBid'):
                print(f"    SuggestedBid: {idea.SuggestedBid}")
            if hasattr(idea, 'Competition'):
                print(f"    Competition: {idea.Competition}")
            if hasattr(idea, 'Relevance'):
                print(f"    Relevance: {idea.Relevance}")
            if hasattr(idea, 'MonthlySearchCounts'):
                print(f"    MonthlySearchCounts: {idea.MonthlySearchCounts}")
        
        if len(keyword_ideas) > 10:
            print(f"\n  ... and {len(keyword_ideas) - 10} more keyword ideas")
        
        # Test 2: Get Keyword Traffic Estimates
        print("\n" + "=" * 60)
        print("Test 2: Getting Keyword Traffic Estimates...")
        print("=" * 60)
        
        # Build ad group estimators from keyword ideas
        idea_ad_group_ids = []
        for keyword_idea in keyword_ideas:
            if hasattr(keyword_idea, 'AdGroupId') and keyword_idea.AdGroupId:
                idea_ad_group_ids.append(keyword_idea.AdGroupId)
        
        # Get unique ad group IDs
        unique_ad_group_ids = list(set(idea_ad_group_ids))
        ad_group_estimator_count = len(unique_ad_group_ids)
        seed_offset = 0 if None in unique_ad_group_ids else 1
        
        print(f"\nBuilding {ad_group_estimator_count} ad group estimators...")
        
        # Initialize ad group estimators
        ad_group_estimators = []
        for index in range(ad_group_estimator_count):
            ad_group_estimator = AdGroupEstimator(
                keyword_estimators=[],
                max_cpc=5.00
            )
            ad_group_estimators.append(ad_group_estimator)
        
        # Populate keyword estimators for each ad group
        for keyword_idea in keyword_ideas:
            if not hasattr(keyword_idea, 'Keyword'):
                continue
                
            ad_group_id = keyword_idea.AdGroupId if hasattr(keyword_idea, 'AdGroupId') else None
            
            # Determine the index for this keyword's ad group
            if ad_group_id is not None:
                try:
                    index = unique_ad_group_ids.index(ad_group_id)
                except ValueError:
                    index = 0
            else:
                index = 0
            
            # Create keyword estimator
            suggested_bid = keyword_idea.SuggestedBid if hasattr(keyword_idea, 'SuggestedBid') and keyword_idea.SuggestedBid else None
            max_cpc = suggested_bid if suggested_bid and suggested_bid > 0.04 else None
            
            keyword = Keyword(
                text=keyword_idea.Keyword,
                match_type=MatchType.EXACT
            )
            
            keyword_estimator = KeywordEstimator(
                keyword=keyword,
                max_cpc=max_cpc
            )
            
            # Add to the appropriate ad group estimator
            ad_group_estimators[index].keyword_estimators.append(keyword_estimator)
        
        # Build campaign estimator
        negative_keyword = NegativeKeyword(
            text="foo",
            match_type=MatchType.EXACT
        )
        
        language_criterion = LanguageCriterion(
            language="English"
        )
        
        network_criterion = NetworkCriterion(
            network=NetworkType.OWNEDANDOPERATEDANDSYNDICATEDSEARCH
        )
        
        location_criterion = LocationCriterion(
            location_id='190'  # United States
        )
        
        campaign_estimator = CampaignEstimator(
            ad_group_estimators=ad_group_estimators,
            daily_budget=50.00,
            negative_keywords=[negative_keyword],
            criteria=[language_criterion, network_criterion, location_criterion]
        )
        
        # Create the request
        get_keyword_traffic_estimates_request = GetKeywordTrafficEstimatesRequest(
            campaign_estimators=[campaign_estimator]
        )
        
        # Call the service
        print("\nRequesting keyword traffic estimates...")
        traffic_estimates_response = ad_insight_service.get_keyword_traffic_estimates(
            get_keyword_traffic_estimates_request=get_keyword_traffic_estimates_request
        )
        
        campaign_estimates = traffic_estimates_response.CampaignEstimates
        
        if not campaign_estimates or len(campaign_estimates) == 0:
            print("No campaign estimates found.")
            return
        
        print(f"\nFound {len(campaign_estimates)} campaign estimate(s):")
        
        # Display campaign estimates
        for i, campaign_estimate in enumerate(campaign_estimates):
            print(f"\n  Campaign Estimate {i+1}:")
            
            if hasattr(campaign_estimate, 'AdGroupEstimates') and campaign_estimate.AdGroupEstimates:
                print(f"    Number of Ad Group Estimates: {len(campaign_estimate.AdGroupEstimates)}")
                
                # Show first few ad group estimates
                for j, ad_group_estimate in enumerate(campaign_estimate.AdGroupEstimates[:3]):
                    print(f"\n    Ad Group Estimate {j+1}:")
                    
                    if hasattr(ad_group_estimate, 'KeywordEstimates') and ad_group_estimate.KeywordEstimates:
                        print(f"      Number of Keyword Estimates: {len(ad_group_estimate.KeywordEstimates)}")
                        
                        # Show first few keyword estimates
                        for k, keyword_estimate in enumerate(ad_group_estimate.KeywordEstimates[:5]):
                            if hasattr(keyword_estimate, 'Keyword') and keyword_estimate.Keyword:
                                keyword_text = keyword_estimate.Keyword.Text if hasattr(keyword_estimate.Keyword, 'Text') else 'N/A'
                                print(f"        Keyword {k+1}: {keyword_text}")
                            
                            if hasattr(keyword_estimate, 'Minimum') and keyword_estimate.Minimum:
                                print(f"          Minimum Estimates:")
                                if hasattr(keyword_estimate.Minimum, 'AverageCpc'):
                                    print(f"            Average CPC: {keyword_estimate.Minimum.AverageCpc}")
                                if hasattr(keyword_estimate.Minimum, 'Clicks'):
                                    print(f"            Clicks: {keyword_estimate.Minimum.Clicks}")
                                if hasattr(keyword_estimate.Minimum, 'Impressions'):
                                    print(f"            Impressions: {keyword_estimate.Minimum.Impressions}")
                            
                            if hasattr(keyword_estimate, 'Maximum') and keyword_estimate.Maximum:
                                print(f"          Maximum Estimates:")
                                if hasattr(keyword_estimate.Maximum, 'AverageCpc'):
                                    print(f"            Average CPC: {keyword_estimate.Maximum.AverageCpc}")
                                if hasattr(keyword_estimate.Maximum, 'Clicks'):
                                    print(f"            Clicks: {keyword_estimate.Maximum.Clicks}")
                                if hasattr(keyword_estimate.Maximum, 'Impressions'):
                                    print(f"            Impressions: {keyword_estimate.Maximum.Impressions}")
                        
                        if len(ad_group_estimate.KeywordEstimates) > 5:
                            print(f"        ... and {len(ad_group_estimate.KeywordEstimates) - 5} more keyword estimates")
                
                if len(campaign_estimate.AdGroupEstimates) > 3:
                    print(f"\n    ... and {len(campaign_estimate.AdGroupEstimates) - 3} more ad group estimates")
        
        print("\n" + "=" * 60)
        print("Keyword planner test completed successfully!")
        print("=" * 60)
        
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
    
    ad_insight_service = ServiceClient(
        service='AdInsightService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )
    
    main()