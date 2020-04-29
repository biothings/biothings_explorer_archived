# -*- coding: utf-8 -*-
"""Module to make asynchronous API calls.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

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

    async def call_one_biothings_api(self, _input, session, size, dotfield=False, verbose=False):
        params = self.construct_query_param(_input['input'],
                                            _input['output'],
                                            _input['values'],
                                            _input['batch_mode'],
                                            size=size,
                                            dotfield=dotfield)
        if not _input['batch_mode']:
            try:
                async with session.get(metadata[_input['api']]['url'],
                                       params=params) as res:
                    if verbose:
                        print("{}: {}".format(_input['query_id'], self.print_request('GET', metadata[_input['api']]['url'], params)))
                    try:
                        return await res.json()
                    except Exception:
                        print("Unable to fetch results from {}".format(_input['api']))
                        return {}
            except Exception:
                if verbose:
                    print('{} failed'.format(_input['api']))
                return {}
        else:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            try:
                async with session.post(metadata[_input['api']]['url'],
                                        data=params,
                                        headers=headers) as res:
                    if verbose:
                        print("{}: {}".format(_input['query_id'], self.print_request("POST", metadata[_input['api']]['url'], params)))
                    try:
                        return await res.json()
                    except:
                        print("Unable to fetch results from {}".format(_input['api']))
                        return {}
            except Exception:
                if verbose:
                    print('{} failed'.format(_input['api']))
                return {}

    async def call_one_non_biothings_api(self, _input, session, verbose=False):
        api_url = metadata[_input['api']]['url']
        api_param = metadata[_input['api']]['path']
        path = self.construct_path(api_url, api_param, _input['values'])
        try:
            async with session.get(path) as res:
                if verbose:
                    print("{}: {}".format(_input['query_id'], path))
                try:
                    return await res.json()
                except Exception as ex:
                    print(ex)
                    m = await res.text()
                    return json.loads(m)
        except Exception:
            if verbose:
                print('{} failed'.format(_input['api']))
            return {}

    async def call_one_api(self, _input, session, size, dotfield=False, verbose=False):
        """Asynchronously make one API call.

        :param: _input (dict) : a python dict containing three keys, e.g. batch_mode, params, api
        :param: session (obj): a aiohttp session object
        """
        # check api type
        api_type = metadata[_input['api']]['api_type']
        if api_type == 'biothings':
            res = await self.call_one_biothings_api(_input, session, size, dotfield=dotfield, verbose=verbose)
        else:
            res = await self.call_one_non_biothings_api(_input, session, verbose=verbose)
        return res


    async def run(self, inputs, size, dotfield=False, verbose=False):
        """Asynchronously make a list of API calls.

        :param: inputs (list): list of python dicts containing three keys
        """
        tasks = []
        # timeout = ClientTimeout(total=15)
        async with ClientSession(connector=TCPConnector(verify_ssl=False)) as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_one_api(i, session,
                                                               size=size,
                                                               dotfield=dotfield,
                                                               verbose=verbose))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            # print(responses)
            return responses

    def call_apis(self, inputs, size=100, dotfield=False, verbose=False):
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
        future = asyncio.ensure_future(self.run(inputs, size=size, dotfield=dotfield, verbose=verbose))
        return (loop.run_until_complete(future), self.log)
