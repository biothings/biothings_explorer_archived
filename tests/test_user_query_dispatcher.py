import unittest
from biothings_explorer.user_query_dispatcher import FindConnection
from biothings_explorer.hint import Hint

ht = Hint()

class TestUserQueryDispatcher(unittest.TestCase):

    def test_result_section(self):
        """Find connection between TMPRSS2 and pentamidine through all intermediate nodes """
        tmprss2 = ht.query("TMPRSS2")['Gene'][0]
        pentamidine = ht.query("pentamidine")['ChemicalSubstance'][0]
        fc = FindConnection(input_obj=tmprss2, output_obj=pentamidine, intermediate_nodes=['BiologicalEntity'], registry=None)
        fc.connect(verbose=True)
        self.assertIn('PLXNA2', fc.fc.G)

