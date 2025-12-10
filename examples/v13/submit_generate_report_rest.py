from auth_helper import *
from openapi_client.models.reporting import *
import time


def main(authorization_data):
    try:
        # Submit generate report
        report_request = AccountPerformanceReportRequest(
            format=ReportFormat.TSV,
            report_name='My Account Performance Report',
            return_only_complete_data=False,
            aggregation=ReportAggregation.WEEKLY,
            scope=AccountReportScope(account_ids=[authorization_data.account_id]),
            time=ReportTime(predefined_time=ReportTimePeriod.YESTERDAY),
            columns=[AccountPerformanceReportColumn.TIMEPERIOD, AccountPerformanceReportColumn.ACCOUNTID,
                     AccountPerformanceReportColumn.ACCOUNTNAME, AccountPerformanceReportColumn.CLICKS,
                     AccountPerformanceReportColumn.IMPRESSIONS, AccountPerformanceReportColumn.CTR,
                     AccountPerformanceReportColumn.AVERAGECPC, AccountPerformanceReportColumn.SPEND,
                     AccountPerformanceReportColumn.DEVICEOS]
        )

        submit_request = SubmitGenerateReportRequest(report_request=report_request)
        submit_response = reporting_service.submit_generate_report(
            submit_generate_report_request=submit_request
        )

        report_request_id = submit_response.report_request_id
        assert (len(report_request_id) > 0)

        # Poll generate report
        wait_time = 10
        for i in range(30):
            time.sleep(wait_time)
            poll_request = PollGenerateReportRequest(report_request_id=report_request_id)
            poll_response = reporting_service.poll_generate_report(poll_generate_report_request=poll_request)
            if not isinstance(poll_response, PollGenerateReportResponse):
                print(f"PollGenerateReportResponse: {poll_response}")
                raise AssertionError("PollGenerateReportResponse should be an instance of PollGenerateReportResponse")

            status = poll_response.report_request_status.status
            result_file_url = poll_response.report_request_status.report_download_url
            print(f"RequestStatus: {status}")
            print(f"ReportDownloadUrl: {result_file_url}")

            if status in (ReportRequestStatusType.SUCCESS, ReportRequestStatusType.ERROR):
                request_status = status
                break

        if request_status is None:
            raise AssertionError("RequestStatus should not be null")

        if request_status == ReportRequestStatusType.SUCCESS:
            print("The report is successfully completed.")
        elif request_status == ReportRequestStatusType.ERROR:
            raise Exception("The report request failed.")
        else:
            raise Exception("The report request is taking longer than expected.")

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

    reporting_service = ServiceClient(
        service='ReportingService',
        version=13,
        authorization_data=authorization_data,
        environment=ENVIRONMENT,
    )

    main(authorization_data)