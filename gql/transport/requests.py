from __future__ import absolute_import

import requests
from graphql.execution import ExecutionResult
from graphql.language.printer import print_ast

from .http import HTTPTransport


class RequestsHTTPTransport(HTTPTransport):

    def execute(self, document, variable_values=None):
        query_str = print_ast(document)
        request = requests.post(
            self.url,
            data={
                'query': query_str,
                'variables': variable_values
            },
            headers=self.client_headers
        )
        result = request.json()
        assert 'errors' in result or 'data' in result, 'Received non-compatible response "{}"'.format(result)
        return ExecutionResult(
            errors=result.get('errors'),
            data=result.get('data')
        )
