from pytest import fixture

@fixture
def ht():
    from biothings_explorer.hint import Hint
    return Hint()

def test_ht_gene(ht):
    assert ht.query("CXCR4")['Gene'][0]['symbol'] == 'CXCR4'