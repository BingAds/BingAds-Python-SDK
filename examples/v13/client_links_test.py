from auth_helper import *
from openapi_client.models.customer import *
import uuid

def main(authorization_data):
    try:
        # Add client links
        client_link = ClientLink(
            client_entity_id=authorization_data.account_id,
            managing_customer_id=authorization_data.customer_id,
            is_bill_to_client=True,
            name="Test client link" + str(uuid.uuid4()),
            start_date=None,
            suppress_notification=False
        )

        add_request = AddClientLinksRequest(client_links=[client_link])
        add_response = customer_service.add_client_links(add_client_links_request=add_request)
        assert isinstance(add_response,
                          AddClientLinksResponse), "add_response is not an instance of AddInsertionOrderResponse"

        # Search client links
        paging = Paging(index=0, size=100)
        predicate = Predicate(
            field='ClientAccountId',
            operator=PredicateOperator.IN,
            value=authorization_data.account_id
        )
        order_by = OrderBy(field=OrderByField.NUMBER, order=SortOrder.ASCENDING)

        request = SearchClientLinksRequest(
            predicates=[predicate],
            ordering=[order_by],
            page_info=paging
        )
        response = customer_service.search_client_links(search_client_links_request=request)
        client_links = response.client_links
        assert (len(client_links) > 0)
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

    customer_service = ServiceClient(
        service='CustomerManagementService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)