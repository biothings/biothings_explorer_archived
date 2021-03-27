import threading
import asyncio
import unittest
from biothings_explorer.user_query_dispatcher import SingleEdgeQueryDispatcher


def thread_function(index, result):
    loop = asyncio.new_event_loop()
    seqd = SingleEdgeQueryDispatcher(
        output_cls="Disease",
        input_id="MESH",
        output_id="MONDO",
        input_cls="ChemicalSubstance",
        pred="related_to",
        values="D014801",
        loop=loop,
    )
    seqd.query()
    result[index] = seqd.G


class TestMultiThreading(unittest.TestCase):
    def test_multithreading(self):
        threads = list()
        results = [None] * 3
        for index in range(3):
            x = threading.Thread(target=thread_function, args=(index, results))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()
        self.assertIn("MONDO:0005578", results[0])
        self.assertIn("MONDO:0005578", results[1])
        self.assertIn("MONDO:0005578", results[2])
