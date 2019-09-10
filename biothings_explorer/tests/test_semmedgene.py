import unittest
from biothings_explorer.registry import Registry
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher


class TestSingleHopQuery(unittest.TestCase):
    def setUp(self):
        self.reg = Registry()
    """
    def test_semmedgene_interactswith(self):
        # test <gene, interactswith, chemical>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0243575',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0016213' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0255423',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0887892' in seqd.G)
        # test <chemical, interactswith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0016213',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0243575' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0887892',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0255423' in seqd.G)
        # test <gene, interactswith, biologicalprocess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0070630',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1373124' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0074147',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1373045' in seqd.G)
        # test <biologicalprocess, interactswith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1373124',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0070630' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1373045',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0074147' in seqd.G)
        # test <gene, interactswith, cell>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Cell',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1705372',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0443611' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Cell',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1421286',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1521882' in seqd.G)
        # test <cell, interactswith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Cell',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0443611',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1705372' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Cell',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1521882',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1421286' in seqd.G)
        # test <gene, interactswith, cellularcomponent>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0678928',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1520175' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1423960',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1521553' in seqd.G)
        # test <cellularcomponent, interactswith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1520175',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0678928' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1521553',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1423960' in seqd.G)
        # test <gene, interactswith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0384930',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1424626' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0030016',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0030016' in seqd.G)
        # test <gene, interactswith, gene> reverse
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1424626',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0384930' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0030016',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0030016' in seqd.G)

    def test_semmedgene_increaseactivity(self):
        # test <gene, increasesActivityOf, biologicalprocess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0001457',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1373051' in seqd.G)
        # test <biologicalprocess, increasesActivityOf, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1373051',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0001457' in seqd.G)
        # test <gene, increasesActivityOf, AnatomicalEntity>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='AnatomicalEntity',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1335208',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1442335' in seqd.G)
        # test <AnatomicalEntity, increasesActivityOf, Gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1442335',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1335208' in seqd.G)
        # test <gene, increasesActivityOf, Cell>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Cell',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0120465',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1517354' in seqd.G)
        # test <Cell, increasesActivityOf, Gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Cell',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1517354',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0120465' in seqd.G)
        # test <gene, increasesActivityOf, CellularComponent>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1334043',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1335464' in seqd.G)
        self.assertTrue('C1520175' in seqd.G)
        self.assertTrue('C1520539' in seqd.G)
        # test <CellularComponent, increasesActivityOf, Gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1335464',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1334043' in seqd.G)
        # test <gene, increasesActivityOf, PhenotypicFeature>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1332102',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0034917' in seqd.G)
        # test <PhenotypicFeature, increasesActivityOf, Gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0034917',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1332102' in seqd.G)
        # test <gene, increasesActivityOf, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0763423',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0296468' in seqd.G)
        # test <Gene, increasesActivityOf, Gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0296468',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0763423' in seqd.G)
    """

    def test_semmedgene_decreaseactivity(self):
        # test <gene, decreasesActivityOf, biologicalprocess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C1366489',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0015214' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0254917',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0597295' in seqd.G)
        # test <biologicalprocess, decreasesActivityOf, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred=None,
                                         values='C0015214',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1366489' in seqd.G)
        # test <gene, decreasesActivityOf, cell>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Cell',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C0025636',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0014792' in seqd.G)
        # test <cell, decreasesActivityOf, gene>
        """ too many results
        seqd = SingleEdgeQueryDispatcher(input_cls='Cell',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C0014792',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0025636' in seqd.G)
        """
        # test <gene, decreasesActivityOf, cellularcomponent>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C1539530',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1525451' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C0024707',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1167518' in seqd.G)
        # test <cellularcomponent, decreasesActivityOf, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C1525451',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1539530' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C1167518',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0024707' in seqd.G)
        # test <gene, decreasesActivityOf, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C0257495',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1413043' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C1413043',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0257495' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C1705316',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0314621' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C0314621',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1705316' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C0652780',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0022956' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C0022956',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0652780' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C1366480',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0079686' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C0079686',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1366480' in seqd.G)
        # test <gene, decreasesActivityOf, phenotype>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C0769262',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0034917' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:umls',
                                         pred='bts:decreasesActivityOf',
                                         values='C1704879',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0019699' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C0034917',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0769262' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:activityDecreasedBy',
                                         values='C0019699',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1704879' in seqd.G)

    def test_semmedgene_associatedwith(self):
        # test <gene, associatedwith, AnatomicalEntity>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='AnatomicalEntity',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1332102',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0233929' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0233929',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1332102' in seqd.G)
        # test <gene, associatedwith, AnatomicalEntity>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='AnatomicalEntity',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C3642141',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0860209' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0860209',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C3642141' in seqd.G)
        # test <gene, associatedwith, AnatomicalEntity>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='AnatomicalEntity',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1539778',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0229671' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='AnatomicalEntity',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0229671',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1539778' in seqd.G)
        # test <gene, associatedwith, BiologicalProcess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0245686',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1159455' in seqd.G)
        """ Too many response
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1159455',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0245686' in seqd.G)
        """
        # test <gene, associatedwith, BiologicalProcess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0596223',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0524869' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0524869',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0596223' in seqd.G)
        # test <gene, associatedwith, BiologicalProcess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0740201',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0027540' in seqd.G)
        """
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0027540',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0740201' in seqd.G)
        """
        # test <gene, associatedwith, BiologicalProcess>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='BiologicalProcess',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0283793',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0301642' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='BiologicalProcess',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0301642',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0283793' in seqd.G)
        # test <gene, associatedwith, CellularComponent>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0646821',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1167317' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1167317',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0646821' in seqd.G)
        # test <gene, associatedwith, CellularComponent>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='CellularComponent',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0247934',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1156020' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='CellularComponent',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1156020',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0247934' in seqd.G)
        # test <gene, associatedwith, ChemicalSubstance>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1418576',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0023828' in seqd.G)
        # test <gene, associatedwith, ChemicalSubstance>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0919426',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0035608' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0035608',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0919426' in seqd.G)
        # test <gene, associatedwith, ChemicalSubstance>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0033164',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0016360' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0016360',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0033164' in seqd.G)
        # test <gene, associatedwith, ChemicalSubstance>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='ChemicalSubstance',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0017375',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0020281' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='ChemicalSubstance',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0020281',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0017375' in seqd.G)
        # test <gene, associatedwith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0812246',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0314621' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0314621',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0812246' in seqd.G)
        # test <gene, associatedwith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0079941',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0079686' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0079686',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0079941' in seqd.G)
        # test <gene, associatedwith, gene>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1426490',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0473780' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0473780',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1426490' in seqd.G)
        # test <gene, associatedwith, phenotypicfeature>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C1332118',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0019699' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0019699',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C1332118' in seqd.G)
        # test <gene, associatedwith, phenotypicfeature>
        seqd = SingleEdgeQueryDispatcher(input_cls='Gene',
                                         input_id='bts:umls',
                                         output_cls='PhenotypicFeature',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0524889',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0856536' in seqd.G)
        seqd = SingleEdgeQueryDispatcher(input_cls='PhenotypicFeature',
                                         input_id='bts:umls',
                                         output_cls='Gene',
                                         output_id='bts:umls',
                                         pred='bts:associatedWith',
                                         values='C0856536',
                                         registry=self.reg)
        seqd.query()
        self.assertTrue('C0524889' in seqd.G)


if __name__ == '__main__':
    unittest.main()
