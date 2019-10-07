# -*- coding: utf-8 -*-

"""
biothings_explorer.hint
~~~~~~~~~~~~~~~~~~~~~~~

Display bioentities in biothings explorer based on user specified input
"""
import asyncio
from aiohttp import ClientSession
from .config import metadata

BIOTHINGS = [k for k, v in metadata.items() if v.get("api_type") == 'biothings']


class Hint():
    def __init__(self, size=5):
        """Guess appropriate bio-entity based on user input

        params
        ------
        size: the max number of documents returned for each bioentity type
        """
        self.clients = []
        self.types = []
        self.post_apis = []
        self.get_apis = []
        self.id_ranks = []
        self.size = size

    def get_primary_id(self, client, json_doc, _type):
        """Get the primary id of a biological entity"""
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
        """make asynchronous API calls

        params
        ------
        _input: str, user specified input
        session: aiohttp session object
        """
        if _input['api'] in self.post_apis:
            async with session.post(_input['url'], data=_input['data']) as res:
                try:
                    return await res.json()
                except:
                    print("Unable to fetch results from {}".format(_input['api']))
                    return {}
        else:
            async with session.get(_input['url'], params=_input['data']) as res:
                try:
                    return await res.json()
                except:
                    print("Unable to fetch results from {}".format(_input['api']))
                    return {}

    async def run(self, _input):
        """run API call tasks

        params
        ------
        _input: str, user typed text
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
                    _item['data']['q'] = "_id:" + _input + " OR name:" + _input + v["add"]
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
            for (k, v, j) in zip(self.clients, responses, self.types):
                # response could be from GET or POST, need to restructure
                if 'hits' in v:
                    v = v['hits']
                for _v in v:
                    if 'notfound' in _v:
                        continue
                    else:
                        _res = {}
                        display = ''
                        for field_name in metadata[k]['fields']:
                            if field_name in _v:
                                if metadata[k]['fields'][field_name] not in _res:
                                    _res[metadata[k]['fields'][field_name]] = _v[field_name]
                                    display += metadata[k]['fields'][field_name] + '(' + str(_v[field_name]) + ')' + ' '
                        _res['display'] = display
                        _res['type'] = j
                        primary = self.get_primary_id(k, _res, j)
                        _res.update({'primary': primary})
                        final_res[j].append(_res)
            return final_res

    def query(self, _input):
        """Query APIs based on user input

        params
        ------
        _input: str, user specified input
        """
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self.run(_input))
        return loop.run_until_complete(future)
