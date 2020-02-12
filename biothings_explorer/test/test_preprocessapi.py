from pytest import fixture
import requests

@fixture
def ap():
    from biothings_explorer.preprocess_api import APIPreprocess
    return APIPreprocess

def test_preprocess_reasoner(ap):
    json_doc = requests.get('https://robokop.renci.org/api/simple/expand/gene/HGNC:30922/gene_family/').json()
    restructured_doc = ap(json_doc, 'reasoner').restructure()
    print(restructured_doc)
    assert 'part_of' in restructured_doc
    assert restructured_doc['part_of'][0]['target_id'] == "PANTHER.FAMILY:PTHR16057"
    assert restructured_doc['part_of'][0]['panther'] == "PTHR16057"