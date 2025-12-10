from auth_helper import *
from openapi_client.models.billing import *
import uuid

def main(authorization_data):
    try:
        # Add insertion order
        insertion_order = InsertionOrder(
            account_id=authorization_data.account_id,
            booking_country_code='US',
            name='testIO' + str(uuid.uuid4()),
            start_date=datetime.utcnow(),
            is_endless=True,
            comment='Test Insertion Order created by test',
            spend_cap_amount=1000.0
        )

        add_request = AddInsertionOrderRequest(insertion_order=insertion_order)
        add_response = billing_service.add_insertion_order(add_insertion_order_request=add_request)

        assert isinstance(add_response,
                          AddInsertionOrderResponse), "add_response is not an instance of AddInsertionOrderResponse"
        insertion_order_id = add_response.insertion_order_id
        assert insertion_order_id is not None, "Insertion Order ID is None"
        print(f"Insertion Order ID: {insertion_order_id}")

        # Search insertion order
        predicate = Predicate(
            field='AccountId',
            operator=PredicateOperator.EQUALS,
            value=authorization_data.account_id
        )
        paging = Paging(index=0, size=1)
        search_request = SearchInsertionOrdersRequest(predicates=[predicate], page_info=paging)
        search_response = billing_service.search_insertion_orders(search_insertion_orders_request=search_request)

        assert isinstance(search_response,
                          SearchInsertionOrdersResponse), "search_response is not an instance of SearchInsertionOrdersResponse"
        found_order = search_response.insertion_orders[0]
        assert found_order is not None, "found_order is None"
        print(f"found_order: {found_order}")


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

    billing_service = ServiceClient(
        service='CustomerBillingService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)