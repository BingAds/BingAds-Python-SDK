from auth_helper import *
from campaignmanagement_example_helper import *

# You must provide credentials in auth_helper.py.

def main(authorization_data): 

    try:
        # Choose a base campaign for the experiment.

        output_status_message("-----\nGetCampaignsByAccountId:")
        campaigns=campaign_service.GetCampaignsByAccountId(
            AccountId=authorization_data.account_id, 
            CampaignType=['Search'])
        output_status_message("Campaigns:")
        output_array_of_campaign(campaigns)

        # The base campaign cannot be an experiment of another base campaign
        # i.e., the campaign's ExperimentId must be nil. 
        # Likewise the base campaign cannot use a shared budget
        # i.e., the campaign's BudgetId must be nil. 
 
        base_campaign=None
        for campaign in campaigns['Campaign']:
            if ((hasattr(campaign, 'ExperimentId') and campaign.ExperimentId is None) or not hasattr(campaign, 'ExperimentId')) \
            and campaign.BudgetId is None:
                base_campaign=campaign
                break

        if base_campaign is None:
            output_status_message("You do not have any campaigns that are eligible for experiments.")
            sys.exit(0)
        
        # Create the experiment

        experiments=campaign_service.factory.create('ArrayOfExperiment')
        experiment=set_elements_to_none(campaign_service.factory.create('Experiment'))
        experiment.BaseCampaignId=base_campaign.Id
        end_date=campaign_service.factory.create('Date')
        end_date.Day=31
        end_date.Month=12
        current_time=gmtime()
        end_date.Year=current_time.tm_year + 1
        experiment.EndDate=end_date
        experiment.ExperimentCampaignId=None
        experiment.ExperimentStatus="Active"
        experiment.ExperimentType=None
        experiment.Id=None
        experiment.Name=base_campaign.Name + "-Experiment"
        start_date=campaign_service.factory.create('Date')
        start_date.Day=current_time.tm_mday
        start_date.Month=current_time.tm_mon
        start_date.Year=current_time.tm_year
        experiment.StartDate=start_date
        experiment.TrafficSplitPercent=50
        experiments.Experiment.append(experiment)

        output_status_message("-----\nAddExperiments:")
        add_experiments_response=campaign_service.AddExperiments(
            Experiments=experiments
        )
        experiment_ids={
            'long': add_experiments_response.ExperimentIds['long'] if add_experiments_response.ExperimentIds['long'] else None
        }
        output_status_message("ExperimentIds:")
        output_array_of_long(experiment_ids)
        output_status_message("PartialErrors:")
        output_array_of_batcherror(add_experiments_response.PartialErrors)

        output_status_message("-----\nGetExperimentsByIds:")
        get_experiments_by_ids_response=campaign_service.GetExperimentsByIds(
            ExperimentIds=experiment_ids,
            PageInfo=None
        )
        output_status_message("Experiments:")
        output_array_of_experiment(get_experiments_by_ids_response.Experiments)

        experiment=get_experiments_by_ids_response.Experiments['Experiment'][0]
        campaign_ids={
            'long': [experiment.ExperimentCampaignId]
        }

        # If the experiment is in a Graduated state, then the former experiment campaign 
        # is now an independent campaign that must be deleted separately. 
        # Otherwise if you delete the base campaign (not shown here), 
        # the experiment campaign and experiment itself are also deleted.

        output_status_message("-----\nDeleteCampaigns:")
        campaign_service.DeleteCampaigns(
            AccountId=authorization_data.account_id, 
            CampaignIds=campaign_ids
        )
        output_status_message("Deleted Experiment Campaign Id {0} with Status '{1}'".format(
            experiment.ExperimentCampaignId,
            experiment.ExperimentStatus))

        output_status_message("-----\nDeleteExperiments:")
        campaign_service.DeleteExperiments(
            ExperimentIds=experiment_ids)
        for id in experiment_ids['long']:
            output_status_message("Deleted Experiment Id {0}".format(id))

    except WebFault as ex:
        output_webfault_errors(ex)
    except Exception as ex:
        output_status_message(ex)


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
