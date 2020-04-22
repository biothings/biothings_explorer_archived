# -*- coding: utf-8 -*-
"""Module to make asynchronous API calls.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

from urllib.parse import urljoin
import asyncio
from aiohttp import ClientSession, TCPConnector
from collections import Counter
import json

from .config import metadata
from .utils.common import add_s


class BioThingsCaller():
    """Call biothings APIs."""

    def __init__(self, batch_mode=False):
        """Set batch mode.
        
        :param: batch_mode (boolean): whether API support batch mode
        """
        self._batch_mode = batch_mode

    @property
    def batch_mode(self):
        return self._batch_mode

    @batch_mode.setter
    def batch_mode(self, value):
        self._batch_mode = value

    @staticmethod
    def construct_query_param(input_fields, output_fields, value, batch_mode, size, dotfield=False):
        """Construct query parameters with input, output and value."""
        get_params = 'q={input}:{value}&fields={output}&species=human&size=' + str(size)
        post_params = 'q={value}&scopes={input}&fields={output}&species=human&size=' + str(size)
        if ',' in input_fields and not batch_mode:
            _input = ' OR'.join([(_item + ':' + value) for _item in input_fields.split(',')])
            if dotfield:
                get_params += '&dotfield=true'
            return get_params.replace('{input}:{value}', _input).replace('{output}', output_fields)
        params = post_params if batch_mode else get_params
        if dotfield:
            params += '&dotfield=true'
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    @staticmethod
    def construct_path(url, param, value):
        """Construct url."""
        param = '{' + param + '}'
        url = url.replace(param, value)
        return url

    @staticmethod
    def print_request(method, url, params):
        if method == "GET":
            if params:
                params = '?' + params
            return url + params
        if method == "POST":
            return url + ' (POST "' + params + '")'
        return ''

    async def call_one_arbitrary_api(self, _input, session, verbose=False):
        base_url = _input['operation']['server'] + _input['operation']['path']
        method = _input['operation']['method']
        request_body = _input['operation'].get("requestBody")
        header = {'content-type': 'application/x-www-form-urlencoded'}
        if request_body:
            header = {'content-type': request_body.get("header")}
            request_body = eval(str(request_body["body"]).replace('{inputs[0]}', _input['value']))
        parameters = _input['operation'].get("parameters")
        if parameters:
            parameters = eval(str(parameters).replace('{inputs[0]}', _input['value']))
        if method == "get":
            try:
                async with session.get(base_url, params=parameters) as res:
                    if verbose:
                        print("{}: {}".format(base_url,parameters))
                    try:
                        res = await res.json()
                        return {
                            'internal_query_id': _input['internal_query_id'],
                            'result': res
                        }
                    except Exception as ex:
                        m = await res.text()
                        return {
                            'result': json.loads(m),
                            'internal_query_id': _input['internal_query_id']
                        }
            except Exception:
                if verbose:
                    print('{} failed'.format(_input['api']))
                return {
                    'internal_query_id': _input['internal_query_id'],
                    'result': {}
                }
        elif method == "post":
            try:
                async with session.post(base_url,
                                        params=parameters,
                                        data=request_body,
                                        headers=header) as res:
                    try:
                        print("{}: {}".format(base_url,parameters))
                        return {
                            'result': await res.json(),
                            'internal_query_id': _input['internal_query_id']
                        }
                    except Exception as ex1:
                        print(ex1)
                        print("Unable to fetch results from {}".format(_input['api']))
                        return {
                            'internal_query_id': _input['internal_query_id'],
                            'result': {}
                        }
            except Exception as ex:
                print(ex)
                if verbose:
                    print('{} failed'.format(_input['api']))
                return {
                    'result': {},
                    'internal_query_id': _input['internal_query_id']
                }


    async def call_one_api(self, _input, session, verbose=False):
        """Asynchronously make one API call.

        :param: _input (dict) : a python dict containing three keys, e.g. batch_mode, params, api
        :param: session (obj): a aiohttp session object
        """
        # check api type
        res = await self.call_one_arbitrary_api(_input, session, verbose=verbose)
        return res


    async def run(self, inputs, verbose=False):
        """Asynchronously make a list of API calls.

        :param: inputs (list): list of python dicts containing three keys
        """
        tasks = []
        # timeout = ClientTimeout(total=15)
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_one_api(i, session,
                                                               verbose=verbose))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            # print(responses)
            return responses

    def call_apis(self, inputs, verbose=False):
        self.log = []
        if verbose:
            cnt = Counter()
            if inputs:
                for _input in inputs:
                    cnt[_input['api']] += 1
            self.unique_apis = {_edge['api'] for _edge in inputs if _edge}
            if verbose:
                print("\nBTE found {} apis:\n".format(len(self.unique_apis)))
                for i, _api in enumerate(self.unique_apis):
                    print("API {}. {}({} API call{})".format(i + 1, _api, cnt[_api], add_s(cnt[_api])))
            self.log.append("\nBTE found {} apis:\n".format(len(self.unique_apis)))
            for i, _api in enumerate(self.unique_apis):
                self.log.append("API {}. {}({} API call{})".format(i + 1, _api, cnt[_api], add_s(cnt[_api])))
            print("\n\n==== Step #2: Query path execution ====")
            self.log.append("\n\n==== Step #2: Query path execution ====")
            print("NOTE: API requests are dispatched in parallel, so the list of APIs below is ordered by query time.\n")
            self.log.append("NOTE: API requests are dispatched in parallel, so the list of APIs below is ordered by query time.\n")
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(inputs, verbose=verbose))
        return (loop.run_until_complete(future), self.log)
