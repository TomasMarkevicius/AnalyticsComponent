from tornado.web import RequestHandler, HTTPError
from tornado.escape import json_decode
from jsonschema import validate, ValidationError
from analyticscomponent.logic import get_report, MalformedDataError


REPORT_SCHEMA = {
    "type": "object",
    "properties": {
        "date": {"type": "string"},
    },
    "required": ["date"],
}


class AnalyticsReportHandler(RequestHandler):
    async def post(self):
        if not self.request.body:
            raise HTTPError(status_code=400, log_message="Request body is missing")
        request = json_decode(self.request.body)
        try:
            validate(instance=request, schema=REPORT_SCHEMA)
        except ValidationError as e:
            raise HTTPError(status_code=400, log_message=str(e))
        try:
            report = get_report(request["date"])
        except MalformedDataError:
            err_msg = "Column contains invalid elements"
            raise HTTPError(status_code=400, log_message=err_msg)
        self.write(report)
        return report
