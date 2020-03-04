# -*- coding: utf-8 -*-

"""
biothings_explorer.mapping_parser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module contains code which parses the mapping file between
biothings schema and biothings API fields
"""
import requests
import asyncio
from aiohttp import ClientSession
from collections import Counter

from .config import metadata
from .utils import add_s


class BioThingsCaller():
    """call biothings APIs"""
    def __init__(self, batch_mode=False):
        self._batch_mode = batch_mode
        self.retry_count = 5

    @property
    def batch_mode(self):
        return self._batch_mode

    @batch_mode.setter
    def batch_mode(self, value):
        self._batch_mode = value

    def construct_query_param(self, input_fields, output_fields, value, batch_mode, size):
        """construct query parameters with input, output and value"""
        get_params = 'q={input}:{value}&fields={output}&species=human&size=' + str(size)
        post_params = 'q={value}&scopes={input}&fields={output}&species=human&size=' + str(size)
        if ',' in input_fields and not batch_mode:
            _input = ' OR'.join([(_item + ':' + value) for _item in input_fields.split(',')])
            return get_params.replace('{input}:{value}', _input).replace('{output}', output_fields)
        params = post_params if batch_mode else get_params
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    def construct_path(self, url, param, value):
        param = '{' + param + '}'
        url = url.replace(param, value)
        return url

    def requests_to_curl(self, method, url, params):
        if method == "GET":
            if params:
                params = '?' + params
            return "curl '" + url + params + "'"
        elif method == "POST":
            return "curl -d '" + str(params) + "' -H 'Content-Type: application/x-www-form-urlencoded' -X POST " + url

    def print_request(self, method, url, params):
        if method == "GET":
            if params:
                params = '?' + params
            return url + params
        elif method == "POST":
            return url + ' (POST "' + params + '")'


    async def call_one_api(self, _input, session, size, verbose=False):
        """asynchronous make one API call

        ...

        Attributes
        ----------
        _input: dict
            a python dict containing three keys
            batch_mode: boolean
            params: dict
            api: str
        session: obj
            a aiohttp session object
        """
        # check api type
        api_type = metadata[_input['api']]['api_type']
        # handle cases for API call using GET HTTP method
        if api_type == 'biothings':
            params = self.construct_query_param(_input['input'],
                                                _input['output'],
                                                _input['values'],
                                                _input['batch_mode'],
                                                size=size)
            if not _input['batch_mode']:
                uri_retry_count = 0
                while(uri_retry_count<self.retry_count):
                    try:
                        async with session.get(metadata[_input['api']]['url'],
                                            params=params) as res:
                            if verbose:
                                print("{}: {} - attempted {} time(s) before".format(_input['query_id'], self.print_request('GET', metadata[_input['api']]['url'], params), uri_retry_count))
                            try:
                                return await res.json()
                            except:
                                print("Unable to fetch results from {}".format(_input['api']))
                                return {}
                    except:                                        
                        uri_retry_count+=1
                        if verbose:
                            print('{} has failed {} time(s)'.format(_input['api'], uri_retry_count))
            # handle cases for API call using POST HTTP method
            else:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                uri_retry_count = 0
                while(uri_retry_count<self.retry_count):
                    try:
                            async with session.post(metadata[_input['api']]['url'],
                                                    data=params,
                                                    headers=headers) as res:
                                if verbose:
                                    print("{}: {} - attempted {} time(s) before".format(_input['query_id'], self.print_request("POST", metadata[_input['api']]['url'], params), uri_retry_count))
                                try:
                                    return await res.json()
                                except:
                                    print("Unable to fetch results from {}".format(_input['api']))
                                    return {}
                    except:
                        uri_retry_count+=1
                        if verbose:
                            print('{} has failed {} time(s)'.format(_input['api'], uri_retry_count))
        else:
            api_url = metadata[_input['api']]['url']
            api_param = metadata[_input['api']]['path']
            path = self.construct_path(api_url, api_param, _input['values'])
            uri_retry_count = 0
            while(uri_retry_count<self.retry_count):
                try:
                    async with session.get(path) as res:
                        if verbose:
                            print("trying: {}: {} - attempted {} time(s) before".format(_input['query_id'], path, uri_retry_count))
                        try:
                            return await res.json()
                        except:
                            print("Unable to fetch results from {}".format(_input['api']))
                            return {}
                    raise ValueError('Communication failure with API endpoint:{}'.format(_input['api']))
                except:
                    uri_retry_count+=1
                    if verbose:
                        print('{} has failed {} time(s)'.format(_input['api'], uri_retry_count))

    async def run(self, inputs, size, verbose=False):
        """asynchronous make one API call

        ...

        Attributes
        ----------
        inputs: list
            list of python dicts containing three keys
            batch_mode: boolean
            params: dict
            api: str
        """
        tasks = []
        # timeout = ClientTimeout(total=15)
        async with ClientSession() as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_one_api(i, session,
                                                               size=size,
                                                               verbose=verbose))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            # print(responses)
            return responses

    def call_apis(self, inputs, size=100, verbose=False):
        if verbose:
            cnt = Counter()
            if inputs:
                for _input in inputs:
                    cnt[_input['api']] += 1
            self.unique_apis = set([_edge['api'] for _edge in inputs if _edge])
            if verbose:
                print("\nBTE found {} apis:\n".format(len(self.unique_apis)))
                for i, _api in enumerate(self.unique_apis):
                    print("API {}. {}({} API call{})".format(i + 1, _api, cnt[_api], add_s(cnt[_api])))
            print("\n\n==== Step #2: Query path execution ====")
            print("NOTE: API requests are dispatched in parallel, so the list of APIs below is ordered by query time.\n")
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(inputs, size=size, verbose=verbose))
        return loop.run_until_complete(future)
