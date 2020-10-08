import asyncio
import json
import traceback
from json import JSONDecodeError
from math import floor
from collections import Counter, defaultdict
from aiohttp import ClientSession, TCPConnector, ClientTimeout

from ..resolve_ids import asyncQuery
from .query_builder import QueryBuilder
from .api_response_transform import Transformer
from ..config_new import MAX_CONCURRENT_QUERIES_ON_SINGLE_API
from .filter import filter_response


class APIQueryDispatcher:
    def __init__(self, edges, verbose=False):
        """Construct inputs for APIQueryDispatcher
        
        params
        ======
        edges: an array of BTE edges with input added
        """
        self.edges = edges
        self.countAPIs()
        self.verbose = verbose
        if verbose:
            self.api_id = {}
            cnt = 1
            print(
                "BTE found {} APIs based on SmartAPI Meta-KG.\n".format(
                    len(self.api_cnt.keys())
                )
            )
            for k, v in self.api_cnt.items():
                print("API {}. {} ({} API calls)".format(cnt, k, v))
                self.api_id[k] = {"id": cnt, "current": 1}
                cnt += 1
            print("\n")

    def countAPIs(self):
        self.api_cnt = Counter()
        if self.edges:
            for edge in self.edges:
                self.api_cnt[edge["association"]["api_name"]] += 1

    @staticmethod
    def print_request(method, url, params, request_body, json_body=None):
        if params:
            url += "?"
            params = [(str(m) + "=" + str(n)) for m, n in params.items()]
            url += "&".join(params)
        if method == "get":
            return url
        if method == "post":
            if request_body:
                url += " (POST -d "
                url += str(request_body)
                url += ")"
            if json_body:
                url += " (POST -d "
                url += str(json_body)
                url += ")"
            return url
        return ""

    async def callSingleAPI(self, edge, session):
        qb = QueryBuilder(edge)
        if qb.config.get("json"):
            try:
                async with session.post(
                    qb.config.get("url"),
                    json=qb.config.get("json"),
                    timeout=ClientTimeout(8),
                ) as res:
                    if self.verbose:
                        print(
                            "API {}: {}".format(
                                str(self.api_id[edge["association"]["api_name"]]["id"])
                                + "."
                                + str(
                                    self.api_id[edge["association"]["api_name"]][
                                        "current"
                                    ]
                                ),
                                self.print_request(
                                    "post",
                                    qb.config.get("url"),
                                    qb.config.get("params"),
                                    qb.config.get("data"),
                                    qb.config.get("json"),
                                ),
                            )
                        )
                    if res.status >= 400:
                        if self.verbose:
                            print(
                                "API call to {} with input {} failed with status code {}".format(
                                    edge["association"]["api_name"],
                                    edge["input"],
                                    res.status,
                                )
                            )
                        return
                    try:
                        res = await res.json()
                    except JSONDecodeError:
                        res = await res.text()
                        res = json.loads(res)
                    tf = Transformer({"response": res, "edge": edge})
                    result = tf.transform()
                    if self.verbose:
                        print(
                            "API {} {}: {} hits".format(
                                str(self.api_id[edge["association"]["api_name"]]["id"])
                                + "."
                                + str(
                                    self.api_id[edge["association"]["api_name"]][
                                        "current"
                                    ]
                                ),
                                edge["association"]["api_name"],
                                len(result),
                            )
                        )
                    if "filter" in edge:
                        result = filter_response(result, edge["filter"])
                        if self.verbose:
                            print(
                                "API {} {}: {} hits after applying filters".format(
                                    str(
                                        self.api_id[edge["association"]["api_name"]][
                                            "id"
                                        ]
                                    )
                                    + "."
                                    + str(
                                        self.api_id[edge["association"]["api_name"]][
                                            "current"
                                        ]
                                    ),
                                    edge["association"]["api_name"],
                                    len(result),
                                )
                            )
                    if self.verbose:
                        self.api_id[edge["association"]["api_name"]]["current"] += 1
                    return result
            except asyncio.TimeoutError:
                if self.verbose:
                    print(
                        "API call to {} with input {} failed with timeout error. Current timeout limit is 5 seconds".format(
                            edge["association"]["api_name"], edge["input"]
                        )
                    )
                return
            except Exception as e:
                if self.verbose:
                    traceback.print_exc()
                    print(
                        "API call to {} with input {} failed with unknown response".format(
                            edge["association"]["api_name"], edge["input"]
                        )
                    )
                return
        elif qb.config.get("method") == "get":
            try:
                async with session.get(
                    qb.config.get("url"),
                    params=qb.config.get("params"),
                    timeout=ClientTimeout(8),
                ) as res:
                    if self.verbose:
                        print(
                            "API {}: {}".format(
                                str(self.api_id[edge["association"]["api_name"]]["id"])
                                + "."
                                + str(
                                    self.api_id[edge["association"]["api_name"]][
                                        "current"
                                    ]
                                ),
                                self.print_request(
                                    "get",
                                    qb.config.get("url"),
                                    qb.config.get("params"),
                                    qb.config.get("data"),
                                ),
                            )
                        )
                    if res.status >= 400:
                        if self.verbose:
                            print(
                                "API call to {} with input {} failed with status code {}".format(
                                    edge["association"]["api_name"],
                                    edge["input"],
                                    res.status,
                                )
                            )
                        return
                    try:
                        res = await res.json()
                    except JSONDecodeError:
                        res = await res.text()
                        res = json.loads(res)
                    tf = Transformer({"response": res, "edge": edge})
                    result = tf.transform()
                    if self.verbose:
                        print(
                            "API {} {}: {} hits".format(
                                str(self.api_id[edge["association"]["api_name"]]["id"])
                                + "."
                                + str(
                                    self.api_id[edge["association"]["api_name"]][
                                        "current"
                                    ]
                                ),
                                edge["association"]["api_name"],
                                len(result),
                            )
                        )
                    if "filter" in edge:
                        result = filter_response(result, edge["filter"])
                        if self.verbose:
                            print(
                                "API {} {}: {} hits after applying filters".format(
                                    str(
                                        self.api_id[edge["association"]["api_name"]][
                                            "id"
                                        ]
                                    )
                                    + "."
                                    + str(
                                        self.api_id[edge["association"]["api_name"]][
                                            "current"
                                        ]
                                    ),
                                    edge["association"]["api_name"],
                                    len(result),
                                )
                            )
                    if self.verbose:
                        self.api_id[edge["association"]["api_name"]]["current"] += 1
                    return result
            except asyncio.TimeoutError:
                if self.verbose:
                    print(
                        "API call to {} with input {} failed with timeout error. Current timeout limit is 5 seconds".format(
                            edge["association"]["api_name"], edge["input"]
                        )
                    )
                return
            except Exception as e:
                if self.verbose:
                    traceback.print_exc()
                    print(
                        "API call to {} with input {} failed with unknown response".format(
                            edge["association"]["api_name"], edge["input"]
                        )
                    )
                return
        elif qb.config.get("method") == "post":
            try:
                async with session.post(
                    qb.config.get("url"),
                    params=qb.config.get("params"),
                    data=qb.config.get("data"),
                    headers=qb.POST_HEADER,
                    timeout=ClientTimeout(20),
                ) as res:
                    if self.verbose:
                        print(
                            "API {}: {}".format(
                                str(self.api_id[edge["association"]["api_name"]]["id"])
                                + "."
                                + str(
                                    self.api_id[edge["association"]["api_name"]][
                                        "current"
                                    ]
                                ),
                                self.print_request(
                                    "post",
                                    qb.config.get("url"),
                                    qb.config.get("params"),
                                    qb.config.get("data"),
                                ),
                            )
                        )
                    if res.status >= 400:
                        if self.verbose:
                            print(
                                "API call to {} with input {} failed with status code {}".format(
                                    edge["association"]["api_name"],
                                    edge["input"],
                                    res.status,
                                )
                            )
                            print("config", qb.config)
                        return
                    res = await res.json()
                    tf = Transformer({"response": res, "edge": edge})
                    result = tf.transform()
                    if self.verbose:
                        print(
                            "API {} {}: {} hits".format(
                                str(self.api_id[edge["association"]["api_name"]]["id"])
                                + "."
                                + str(
                                    self.api_id[edge["association"]["api_name"]][
                                        "current"
                                    ]
                                ),
                                edge["association"]["api_name"],
                                len(result),
                            )
                        )
                    if "filter" in edge:
                        result = filter_response(result, edge["filter"])
                        if self.verbose:
                            print(
                                "API {} {}: {} hits after applying filters".format(
                                    str(
                                        self.api_id[edge["association"]["api_name"]][
                                            "id"
                                        ]
                                    )
                                    + "."
                                    + str(
                                        self.api_id[edge["association"]["api_name"]][
                                            "current"
                                        ]
                                    ),
                                    edge["association"]["api_name"],
                                    len(result),
                                )
                            )
                    if self.verbose:
                        self.api_id[edge["association"]["api_name"]]["current"] += 1
                    return result
            except asyncio.TimeoutError:
                if self.verbose:
                    print(
                        "API call to {} with input {} failed with timeout error. Current timeout limit is 20 seconds".format(
                            edge["association"]["api_name"], edge["input"]
                        )
                    )
                return
            except Exception as e:
                if self.verbose:
                    traceback.print_exc()
                    print(
                        "API call to {} with input {} failed with unknown response".format(
                            edge["association"]["api_name"], edge["input"]
                        )
                    )
                return

    async def annotate(self, res, session):
        output_ids = defaultdict(set)
        for item in res:
            output_ids[item["$association"]["output_type"]].add(item["$output"])
        resolved_ids = await asyncQuery(output_ids, session)
        for item in res:
            if item["$output"] in resolved_ids:
                item["$output_id_mapping"] = {
                    "resolved_ids": resolved_ids[item["$output"]],
                    "original": item["$output"],
                }
                item["label"] = resolved_ids[item["$output"]]["id"]["label"]
                item["id"] = item["$output"] = resolved_ids[item["$output"]]["id"][
                    "identifier"
                ]
            else:
                item["label"] = item["id"] = item["$output"]
        return res

    def scheduleQueryTasks(self, session):
        tasks = defaultdict(list)
        cnt = Counter()
        for edge in self.edges:
            if edge["query_operation"]["server"].startswith(
                "https://biothings.ncats.io"
            ):
                api = "pending API"
            else:
                api = edge["association"]["api_name"]
            cnt[api] += 1
            if api == "MyVariant.info API":
                tasks[cnt[api]].append(self.callSingleAPI(edge, session))
            if api == "pending API":
                task_id = floor(cnt[api] / 2)
                tasks[task_id].append(self.callSingleAPI(edge, session))
            else:
                task_id = floor(cnt[api] / MAX_CONCURRENT_QUERIES_ON_SINGLE_API)
                tasks[task_id].append(self.callSingleAPI(edge, session))
        return tasks

    async def asyncQuery(self):
        """Asynchronously make a list of API calls."""
        if self.verbose:
            print("==== Step #2: Query path execution ====\n")
            print(
                "NOTE: API requests are dispatched in parallel, so the list of APIs below is ordered by query time.\n"
            )
        responses = []
        timeout = ClientTimeout(total=5)
        async with ClientSession(
            timeout=timeout, connector=TCPConnector(ssl=False)
        ) as session:
            tasks = self.scheduleQueryTasks(session)
            for task in tasks.values():
                res = await asyncio.gather(*task)
                for _res in res:
                    if _res:
                        responses += _res
            if responses:
                if self.verbose:
                    print("\nBTE starts to perform id-to-object translation.\n")
                responses = await self.annotate(responses, session)
            return responses

    def syncQuery(self, loop=None):
        if not loop:
            loop = asyncio.get_event_loop()
        # return loop.create_task(self.asyncQuery())
        return loop.run_until_complete(self.asyncQuery())
