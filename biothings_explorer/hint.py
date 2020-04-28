# -*- coding: utf-8 -*-
"""Display bioentities in biothings explorer based on user specified input.

.. moduleauthor:: Jiwen Xin <kevinxin@scripps.edu>


"""

import asyncio
from aiohttp import ClientSession
from .config import metadata
BIOTHINGS = [k for k, v in metadata.items() if v.get("api_type") == 'biothings']


class Hint():
    """Query any biomedical ID or name into BioThings objects, which contain mappings to many common identifiers. \
        Generally, the top result returned by the Hint module will be the correct item, but you should confirm that using the identifiers shown."""

    def __init__(self, size=5):
        """Guess appropriate bio-entities based on user input.

        :param: size: The max number of documents returned for each bioentity type.
        """
        self.clients = []
        self.types = []
        self.post_apis = []
        self.get_apis = []
        self.id_ranks = []
        self.size = size

    @staticmethod
    def get_primary_id(client, json_doc, _type):
        """Get the primary id of a biological entity
        
        :param: client: the name of the API
        :param: json_doc: the API output
        :param: _type: the main entity type of the output, e.g. Gene, SequenceVariant
        """
        # parse the id rank info from metadata
        ranks = metadata[client]['id_ranks']
        res = {}
        # loop through the id rank list, e.g. ['chembl', 'drugbank', ...]
        # the id rank list is ranked based on priorirty
        for _id in ranks:
            # if an id of higher priority is found, set it as the primary id
            if _id in json_doc:
                res['identifier'] = _id
                res['cls'] = _type
                res['value'] = json_doc[_id]
                break
        return res

    async def call_api(self, _input, session):
        """Make asynchronous API calls.

        :param: _input: str, user specified input
        :param: session: aiohttp session object
        """
        if _input['api'] in self.post_apis:
            async with session.post(_input['url'], data=_input['data']) as res:
                try:
                    return await res.json()
                except Exception:
                    print("Unable to fetch results from {}".format(_input['api']))
                    return {}
        else:
            async with session.get(_input['url'], params=_input['data']) as res:
                try:
                    return await res.json()
                except Exception:
                    print("Unable to fetch results from {}".format(_input['api']))
                    return {}

    def construct_single_hint_obj(self, api, res, doc_type):
        """Construct a single Hint Object

        :param: api: the name of API
        :param: res: the JSON response from API
        :param: doc_type: the main entity type of the API output
        """
        result = {}
        display = ''
        for field_name in metadata[api]['fields']:
            if field_name in res:
                if metadata[api]['fields'][field_name] not in result:
                    result[metadata[api]['fields'][field_name]] = res[field_name]
                    display += metadata[api]['fields'][field_name] + '(' + str(res[field_name]) + ')' + ' '
        result['display'] = display
        result['type'] = doc_type
        primary = self.get_primary_id(api, result, doc_type)
        result.update({'primary': primary})
        return result

    async def run(self, _input):
        """Run API call tasks.

        :param: _input (str): user typed text
        """
        inputs = []
        for k, v in metadata.items():
            # check if an API can be used for hint
            if v.get('hint'):
                self.clients.append(k)
                self.types.append(v['doc_type'])
                if v['method'] == 'get':
                    self.get_apis.append(k)
                elif v['method'] == 'post':
                    self.post_apis.append(k)
                _item = {'url': v['url'],
                         'api': k,
                         'data': {'q': ["'" + _input + "'"],
                                  'scopes': ','.join(v['scopes']),
                                  'fields': ','.join(v['fields']),
                                  'size': self.size,
                                  'dotfield': 1
                                 }
                         }
                if 'add' in v:
                    _item['data']['q'] = '(_id:"' + _input + '" OR name:"' + _input + '")' + v["add"]
                inputs.append(_item)
        tasks = []
        async with ClientSession( ) as session:
            for i in inputs:
                task = asyncio.ensure_future(self.call_api(i, session))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)
            final_res = {}
            for j in self.types:
                final_res[j] = []
            for (api, res, _type) in zip(self.clients, responses, self.types):
                # response could be from GET or POST, need to restructure
                if 'hits' in res:
                    res = res['hits']
                for _v in res:
                    if 'notfound' in _v:
                        continue
                    _res = self.construct_single_hint_obj(api, _v, _type)
                    final_res[_type].append(_res)
            return final_res

    def query(self, _input):
        """Query APIs based on user input.

        :param: _input (str): user specified input, could be any biomeidcal id or name

        Returns
        -------
            hint Object: A dict containing all possible ids corresponding to the input

        Examples
        --------

        >>> from biothings_explorer.hint import Hint
        >>> ht = Hint()
        >>> ht.query('CXCR4')
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(_input))
        return loop.run_until_complete(future)
