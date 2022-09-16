from analyticscomponent.app import make_app
from unittest import main
from tornado.testing import AsyncHTTPTestCase
from json import dumps, loads
from mock import patch


REPORT_MOCK_DICT = {
    "customers": 9,
    "total_discount_amount": 130429980.26309249,
    "items": 2895,
    "order_total_avg": 15895179.735734595,
    "discount_rate_avg": 1.6839138282952828,
    "commissions": {
        "promotions": {
            "1": 0,
            "3": 0,
            "2": 0,
            "5": 0,
            "4": 0
        },
        "total": 0,
        "order_average": 0
    }
}


@patch("analyticscomponent.handlers.api_handlers.get_report")
class TestReport(AsyncHTTPTestCase):
    def setUp(self):
        super(TestReport, self).setUp()

    def get_app(self):
        return make_app()

    def test_get_report_success(self, report_mock):
        report_mock.return_value = REPORT_MOCK_DICT
        body = {
            "date": "2019-08-02",
        }

        response = self.fetch(
            '/report',
            method='POST',
            body=dumps(body)
        )
        self.assertEqual(loads(response.body), REPORT_MOCK_DICT)

    def test_get_report_request_validation(self, report_mock):
        report_mock.return_value = REPORT_MOCK_DICT
        body = {
            "date": 5,
        }

        response = self.fetch(
            '/report',
            method='POST',
            body=dumps(body)
        )
        self.assertEqual(response.code, 400)


if __name__ == "__main__":
    main()
