#Import libraries
from biothings_explorer.trapi import TRAPI
import pandas as pd

#Pandas settings
pd.set_option('display.max_columns', 100)
pd.set_option('display.width', 500)



#Connect to Production server
tp = TRAPI()
tp.url = 'https://api.bte.ncats.io/v1/query'


#Query message
qg ={
    "message": {
        "query_graph": {
            "nodes": {
                "n0": {
                    "categories":["biolink:Pathway"],
                    "ids": "WIKIPATHWAYS:WP195"
                },
                "n1": {
                    "categories": ["biolink:Gene"]
                },
                "n2": {
                    "categories": ["biolink:ChemicalSubstance"]
                }

            },
            "edges": {
                "e01": {
                    "subject": "n0",
                    "object": "n1"
                },
                "e02": {
                    "subject": "n1",
                    "object": "n2"
                }
            }
        }
    }
}
tp.query_graph = qg

#Make the query
tp.query()

#Visualize the results for query edge e02 as DataFrame
df_e02 = tp.to_dataframe("e02")
print(df_e02)


#Sort by drugs which target most of the IL1 Signaling pathway participants
df_il1= df_e02.sort_values(by='object_num_source_nodes', ascending=False)[["object", "object_name", "object_num_source_nodes"]].drop_duplicates().head(20)
print (df_il1)