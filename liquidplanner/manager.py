from __future__ import unicode_literals


import requests

from .exceptions import *

class Manager(object):

    def __init__(self, config, name, url, options):
        self.config = config
        self.name = name
        self.url = url
        self.options = options

        # Special plural handling for entities ending in 'y' 
        if self.name[-3:] == 'ies':
            self.singular = self.name[:-3] + 'y'
        elif self.name[-1] == 's':
            self.singular = self.name[:-1]
        else:
            self.singular = self.name

        self.base_url = "https://app.liquidplanner.com/api"
        self.timeout = 10 # seconds

    def _make_request(self, method, url, data=None, params=None, headers=None):
        from liquidplanner import __version__ as VERSION
        if headers is None:
            headers = {}

        # Use the JSON API
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        # Set a user-agent so LiquidPlanner knows the traffic is 
        # coming from pyliquidplanner
        headers['User-Agent'] = 'pyliquidplanner/{} {}'.format(
                VERSION, requests.utils.default_user_agent())

        # Make sure we get the expected API version
        headers['X-API-Version'] = '3.0.0'

        serialized_data = None
        if data:
            # JSON encode the body
            serialized_data = json.dumps(data)

        full_uri = self.base_url + url

        response = getattr(requests, method)(
            full_uri, data=serialized_data, headers=headers, params=params,
            auth=self.config.credentials.auth, timeout=self.timeout)

        if response.status_code in [200, 201]:
            return self._parse_api_response(response)

        elif response.status_code == 400:
            raise LiquidPlannerBadRequest(response)

        elif response.status_code == 401:
            raise LiquidPlannerUnauthorized(response)

        elif response.status_code == 422:
            raise LiquidPlannerUnprocessableEntity(response)

        elif response.status_code == 404:
            raise LiquidPlannerNotFound(response)

        elif response.status_code == 500:
            raise LiquidPlannerInternalError(response)

        elif response.status_code == 501:
            raise LiquidPlannerNotImplemented(response)

        elif response.status_code == 503:
            raise LiquidPlannerUnavailable(response)

        else:
            raise LiquidPlannerException(response, 
                msg="Unknown HTTP response code: {0}".format(response.status_code))

    def _parse_api_response(self, response):
        # We expect only JSON encoded replies. We simply deserialize and return.
        return response.json()

    def _format_url(self, url, tokens=None):
        if tokens is None:
            tokens = {}

        if not 'workspace_id' in tokens:
            tokens['workspace_id'] = self.config.workspace_id

        return url.format(**tokens)

    def all(self, include=None, filters=None, filter_conjunction=None,
            order=None, limit=None, depth=None, leaves=None):
        """Fetch all records
        
        :param include: list of related entities to include
        :param filters: list of filters to apply
        :param filter_conjunction: can be 'OR' to change default from 'AND'
        :param order: sort order, one of 'earliest_start' or 'updated_at'
        :param limit: max number of records to return
        :param depth: limit tree depth (only makes sense for treeitems)
        :param leaves: include leaf nodes (only makes sense for treeitems)"""
        params = {}

        if include is not None:
            params["include"] = ",".join(include)

        if filters is not None:
            params["filter[]"] = filters

        if filter_conjunction is not None:
            params["filter_conjunction"] = filter_conjunction

        if order is not None:
            params["order"] = order

        if limit is None:
            params["limit"] = limit

        if depth is not None:
            params["depth"] = depth

        if leaves:
            params["leaves"] = "true"

        url = self._format_url(self.url)

        return self._make_request('get', url, params=params)

    def _help_json(self):
        return self._make_request('get', 'help.json')

    def get(self, id, include=None, depth=None, leaves=None, item_context=None, filter_context=None):
        """Get the record with the given id
        
        :param include: optional list of related entities to include"""
        params = {}

        if include is not None:
            params["include"] = ",".join(include)

        if depth is not None:
            params["depth"] = depth

        if leaves is not None:
            params["leaves"] = str(item_context).lower()

        if item_context is not None:
            params["item_context"] = str(item_context).lower()

        if filter_context is not None:
            params["filter_context"] = str(filter_context).lower()
        
        
        url = self._format_url(self.url + "/{id}", {"id": id})

        return self._make_request('get', url, params=params)

    def update(self, obj, id=None):
        """Save an existing record.
        
        `id` can be omitted if set in the object.

        Ensure that only modifiable fields are present."""
        if id is None:
            id = obj.pop("id")

        url = self._format_url(self.url + "/{id}", {"id": id})

        return self._make_request('put', url, data={self.singular: obj})

    def create(self, obj):
        """Insert a new record"""
        url = self._format_url(self.url)

        return self._make_request('post', url, data={self.singular: obj})

