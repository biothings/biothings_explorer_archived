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


class BioThingsCaller():
    """call biothings APIs"""
    def __init__(self, batch_mode=False):
        self.url_pattern = {'mygene.info': "http://mygene.info/v3/query",
                            'myvariant.info': 'http://myvariant.info/v1/query',
                            "mychem.info": "http://mychem.info/v1/query",
                            "mydisease.info": "http://mydisease.info/v1/query",
                            "semmed": "http://pending.biothings.io/semmed/query",
                            "semmedanatomy": "https://pending.biothings.io/semmed_anatomy/query",
                            "semmedbp": "https://pending.biothings.io/semmedbp/query",
                            "semmedchemical": "https://pending.biothings.io/semmedchemical/query",
                            "semmedgene": "https://pending.biothings.io/semmedgene/query",
                            "semmedphenotype": "https://pending.biothings.io/semmedphenotype/query"}
        self._batch_mode = batch_mode

    @property
    def batch_mode(self):
        return self._batch_mode

    @batch_mode.setter
    def batch_mode(self, value):
        self._batch_mode = value

    def construct_query_param(self, input_fields, output_fields, value, batch_mode):
        """construct query parameters with input, output and value"""
        get_params = 'q={input}:{value}&fields={output}'
        post_params = 'q={value}&scopes={input}&fields={output}'
        if ',' in input_fields and not batch_mode:
            _input = ' OR'.join([(_item + ':' + value) for _item in input_fields.split(',')])
            return get_params.replace('{input}:{value}', _input).replace('{output}', output_fields)
        params = post_params if batch_mode else get_params
        return params.replace('{input}', input_fields).replace('{output}',output_fields).replace('{value}', value)

    def call_api(self, api, _input, _output, value):
        """make api calls"""
        params = self.construct_query_param(_input, _output, value, self._batch_mode)
        if not self._batch_mode:
            return requests.get(self.url_pattern[api], params=params).json()
        else:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            return requests.post(self.url_pattern[api],
                                 data=params,
                                 headers=headers).json()

    async def call_one_api(self, _input, session):
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
        # handle cases for API call using GET HTTP method
        params = self.construct_query_param(_input['input'],
                                            _input['output'],
                                            _input['values'],
                                            _input['batch_mode'])
        if not _input['batch_mode']:
            async with session.get(self.url_pattern[_input['api']],
                                   params=params) as res:
                return await res.json()
        # handle cases for API call using POST HTTP method
        else:
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            async with session.post(self.url_pattern[_input['api']],
                                    data=params,
                                    headers=headers) as res:
                return await res.json()

    async def run(self, inputs):
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
        async with ClientSession() as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_one_api(i, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            return responses

    def call_apis(self, inputs):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(inputs))
        return loop.run_until_complete(future)
