import json


class LiquidPlannerException(Exception):
    def __init__(self, response, msg=None):
        self.response = response

        if msg is None:
            msg = self.extract_message_from_response(response)

        super(LiquidPlannerException, self).__init__(msg)

    def extract_message_from_response(self, response):
        if response.headers['content-type'].startswith('application/json'):
            data = json.loads(response.text)
            msg = "{}: {}".format(data["error"], data["message"])
            
            return msg

        else:
            # Not a JSON response, use a generic message
            return "Unknown error"


class LiquidPlannerBadRequest(LiquidPlannerException):
    # HTTP 400: Bad Request
    pass

class LiquidPlannerUnauthorized(LiquidPlannerException):
    # HTTP 401: Unauthorized
    pass

class LiquidPlannerUnprocessableEntity(LiquidPlannerException):
    # HTTP 422: Unprocessable Entity
    pass

class LiquidPlannerNotFound(LiquidPlannerException):
    # HTTP 404: Not Found
    pass

class LiquidPlannerInternalError(LiquidPlannerException):
    # HTTP 500: Internal Server Error
    pass

class LiquidPlannerNotImplemented(LiquidPlannerException):
    # HTTP 501: Not Implemented
    pass

class LiquidPlannerUnavailable(LiquidPlannerException):
    # HTTP 503: Service Unavailable
    pass

