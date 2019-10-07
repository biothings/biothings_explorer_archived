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

from .config import metadata


class BioThingsCaller():
    """call biothings APIs"""
    def __init__(self, batch_mode=False):
        self._batch_mode = batch_mode

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

    def call_api(self, api, _input, _output, value, api_type):
        """make api calls"""
        params = self.construct_query_param(_input, _output, value, self._batch_mode)
        if not self._batch_mode:
            return requests.get(metadata[api]['url'], params=params).json()
        else:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            return requests.post(metadata[api]['url'],
                                 data=params,
                                 headers=headers).json()

    async def call_one_api(self, _input, session, size):
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
                async with session.get(metadata[_input['api']]['url'],
                                       params=params) as res:
                    try:
                        return await res.json()
                    except:
                        print("Unable to fetch results from {}".format(_input['api']))
                        return {}
            # handle cases for API call using POST HTTP method
            else:
                headers = {'content-type': 'application/x-www-form-urlencoded'}
                async with session.post(metadata[_input['api']]['url'],
                                        data=params,
                                        headers=headers) as res:
                    try:
                        return await res.json()
                    except:
                        print("Unable to fetch results from {}".format(_input['api']))
                        return {}
        else:
            api_url = metadata[_input['api']]['url']
            api_param = metadata[_input['api']]['path']
            path = self.construct_path(api_url, api_param, _input['values'])
            async with session.get(path) as res:
                try:
                    return await res.json()
                except:
                    return {}

    async def run(self, inputs, size):
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
                                                               size=size))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            # print(responses)
            return responses

    def call_apis(self, inputs, size=100):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(inputs, size=size))
        return loop.run_until_complete(future)
