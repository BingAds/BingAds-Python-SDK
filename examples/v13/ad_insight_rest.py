from auth_helper_rest import *
from openapi_client.models.adinsight import *


def main(authorization_data):
    try:
        # Add a budget that can be shared by campaigns in the same account.
        retrieve_recommendations_request = RetrieveRecommendationsRequest(
            max_count=5,
            recommendation_types=["KEYWORD"]
        )

        retrieve_recommendations_response = ad_insight_service.retrieve_recommendations(
            retrieve_recommendations_request=retrieve_recommendations_request
        )
        assert(retrieve_recommendations_response != None)

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

    ad_insight_service = ServiceClient(
        service='AdInsightService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)