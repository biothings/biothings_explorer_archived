# -*- coding: utf-8 -*-
"""Module to make asynchronous API calls.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

import asyncio
from aiohttp import ClientSession, TCPConnector
from collections import Counter
import json
from .utils.common import add_s


class BioThingsCaller():
    """Call biothings APIs."""

    @staticmethod
    def print_request(method, url, params, request_body):
        if params:
            url += '?'
            params = [(str(m) + '=' + str(n)) for m,n in params.items()]
            url += '&'.join(params)
        if method == "get":
            return url
        if method == "post":
            if request_body:
                url += ' (POST -d '
                request_body = [(str(m) + '=' + str(n)) for m,n in request_body.items()]
                url += '&'.join(request_body)
                url += ')'
            return url
        return ''

    async def call_one_arbitrary_api(self, _input, session, verbose=False):
        base_url = _input['operation']['server'].strip('/') + _input['operation']['path']
        method = _input['operation']['method']
        request_body = _input['operation'].get("requestBody")
        header = {'content-type': 'application/x-www-form-urlencoded'}
        if request_body:
            if request_body.get("header"):
                header = {'content-type': request_body.get("header")}
            request_body = eval(str(request_body["body"]).replace('{inputs[0]}', _input['value']))
        parameters = _input['operation'].get("parameters")
        if parameters:
            if _input['operation'].get('path_params'):
                for path_param in _input['operation']['path_params']:
                    path_value_template = parameters.get(path_param)
                    base_url = base_url.replace('{' + path_param + '}', path_value_template).replace('{inputs[0]}', _input['value'])
                    parameters.pop(path_param)
            parameters = eval(str(parameters).replace('{inputs[0]}', _input['value']))
        query_url = self.print_request(method, base_url, parameters, request_body)
        if method == "get":
            try:
                async with session.get(base_url, params=parameters) as res:
                    if verbose:
                        print("{}: {}".format(_input['internal_query_id'], query_url))
                    try:
                        if res.status in [400, 404]:
                            print('{} {} failed'.format(_input['internal_query_id'], _input['api']))
                            return {
                            'internal_query_id': _input['internal_query_id'],
                            'result': {}
                            }
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
                    print('{} {} failed'.format(_input['internal_query_id'], _input['api']))
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
                        if res.status in [400, 404]:
                            print('{} {} failed'.format(_input['internal_query_id'], _input['api']))
                            return {
                            'internal_query_id': _input['internal_query_id'],
                            'result': {}
                            }
                        if verbose:
                            print("{}: {}".format(_input['internal_query_id'], query_url))
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
                    print('{}: {} failed'.format(_input['internal_query_id'], _input['api']))
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
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
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
