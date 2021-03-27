# How to Access the BTE TRAPI service through BTE Python Client

## Import and Initialize

```python
from biothings_explorer.trapi import TRAPI
tp = TRAPI()
```

## Set TRAPI service url

By default, this libary will use the BTE dev server as the access point for TRAPI service.

If you would like to use the production server, you can change it using:

```python
tp.url = 'https://api.bte.ncats.io/v1/query
```

You can also point to a local instance of BTE TRAPI service running at your local computer:

```python
tp.url = 'http://localhost:3000/v1/query
```

## Query the TRAPI service

For details regarding how to construct TRAPI query, pls refer to [Documentation for TRAPI](https://github.com/NCATSTranslator/ReasonerAPI/blob/master/TranslatorReasonerAPI.yaml).

If you have a TRAPI query in mind, you can query BTE as below:

```python
qg = {
	"message": {
		"query_graph": {
			"nodes": {
				"n0": {
					"id": "NCBIGENE:1017",
					"category":"biolink:Gene"
				},
                "n2": {
                    "category": "biolink:Protein"
                }
			},
			"edges": {
				"e01": {
					"subject": "n0",
                    "object": "n2"
                }
			}
		}
	}
}
tp.query_graph = qg
tp.query()
```

## Access the results

You can view the results for individual edges as below:

```python
# below would get all query results for e01 edge as a Pandas DataFrame
df = tp.to_dataframe("e01")

```

## Example Jupyter Notebook

Please find example notebook [here](https://github.com/biothings/biothings_explorer/blob/master/jupyter%20notebooks/How_to_use_bte_trapi_through_py_client.ipynb)