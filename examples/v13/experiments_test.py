import uuid
from auth_helper import *
from openapi_client.models.campaign import *


def main(authorization_data):
    try:
        # Get eligible campaigns for experiments
        # Eligible campaigns must not have an experiment ID and must not use a shared budget
        print("Getting eligible campaigns for experiments...")
        
        get_campaigns_request = GetCampaignsByAccountIdRequest(
            account_id=authorization_data.account_id,
            campaign_type=CampaignType.SEARCH
        )
        
        get_campaigns_response = campaign_service.get_campaigns_by_account_id(
            get_campaigns_by_account_id_request=get_campaigns_request
        )
        
        campaigns = get_campaigns_response.Campaigns
        
        # Filter for eligible campaigns (no experiment ID and no budget ID)
        eligible_campaigns = [
            campaign for campaign in campaigns
            if not hasattr(campaign, 'ExperimentId') or campaign.ExperimentId is None
            and not hasattr(campaign, 'BudgetId') or campaign.BudgetId is None
        ]
        
        print(f"Found {len(eligible_campaigns)} eligible campaigns")
        
        if not eligible_campaigns:
            print("No eligible campaigns found. Please create a campaign without a shared budget first.")
            return
        
        # Use the first eligible campaign
        base_campaign = eligible_campaigns[0]
        print(f"Using base campaign: {base_campaign.Name} (ID: {base_campaign.Id})")
        
        # Add an experiment for the base campaign
        print("\nAdding experiment...")
        
        current_date = datetime.now()
        
        experiment = Experiment(
            base_campaign_id=base_campaign.Id,
            name=f"{base_campaign.Name}-Experiment{str(uuid.uuid4())[:8]}",
            traffic_split_percent=50,
            # Required. You must set the status to Active; however, the status will be set 
            # automatically by Microsoft Advertising to Creating, and the next time you retrieve 
            # the experiment its status will be either Active, Creating, CreationFailed, Paused, or Scheduled.
            experiment_status='Active',
            start_date=Date(
                day=current_date.day,
                month=current_date.month,
                year=current_date.year
            ),
            end_date=Date(
                day=31,
                month=12,
                year=current_date.year
            )
        )
        
        add_experiments_request = AddExperimentsRequest(
            experiments=[experiment]
        )
        
        add_experiments_response = campaign_service.add_experiments(
            add_experiments_request=add_experiments_request
        )
        
        experiment_ids = add_experiments_response.ExperimentIds
        print(f"Created Experiment IDs: {experiment_ids}")
        
        if add_experiments_response.PartialErrors:
            print(f"Partial Errors: {add_experiments_response.PartialErrors}")
        else:
            print("Experiment created successfully")
        
        # Get experiments by IDs
        print("\nGetting experiments by IDs...")
        
        get_experiments_request = GetExperimentsByIdsRequest(
            experiment_ids=experiment_ids
        )
        
        get_experiments_response = campaign_service.get_experiments_by_ids(
            get_experiments_by_ids_request=get_experiments_request
        )
        
        experiments = get_experiments_response.Experiments
        print(f"Retrieved {len(experiments)} experiments")
        
        for exp in experiments:
            print(f"  Experiment ID: {exp.Id}")
            print(f"  Name: {exp.Name}")
            print(f"  Status: {exp.ExperimentStatus}")
            print(f"  Base Campaign ID: {exp.BaseCampaignId}")
            if hasattr(exp, 'ExperimentCampaignId') and exp.ExperimentCampaignId:
                print(f"  Experiment Campaign ID: {exp.ExperimentCampaignId}")
            print(f"  Traffic Split: {exp.TrafficSplitPercent}%")
        
        if get_experiments_response.PartialErrors:
            print(f"Partial Errors: {get_experiments_response.PartialErrors}")
        
        # Clean up - delete the experiment
        print("\nDeleting experiment...")
        
        experiment = experiments[0]
        
        # If the experiment has graduated, delete the experiment campaign first
        if hasattr(experiment, 'ExperimentStatus') and experiment.ExperimentStatus == "Graduated":
            if hasattr(experiment, 'ExperimentCampaignId') and experiment.ExperimentCampaignId:
                print(f"Experiment has graduated. Deleting experiment campaign {experiment.ExperimentCampaignId}...")
                delete_campaign_request = DeleteCampaignsRequest(
                    account_id=authorization_data.account_id,
                    campaign_ids=[experiment.ExperimentCampaignId]
                )
                campaign_service.delete_campaigns(
                    delete_campaigns_request=delete_campaign_request
                )
        
        # Delete the experiment
        delete_experiments_request = DeleteExperimentsRequest(
            experiment_ids=[experiment.Id]
        )
        
        delete_experiments_response = campaign_service.delete_experiments(
            delete_experiments_request=delete_experiments_request
        )
        
        if delete_experiments_response.PartialErrors:
            print(f"Partial Errors: {delete_experiments_response.PartialErrors}")
        else:
            print(f"Deleted Experiment ID: {experiment.Id}")
        
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
    
    campaign_service = ServiceClient(
        service='CampaignManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )
    
    main(authorization_data)