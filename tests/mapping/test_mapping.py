import os
from unittest import TestCase

from sunbeamlib.mapping import SnStatsParser


class TestSnStatsParser(TestCase):

    def test_parse(self):
        file_path = os.path.join(os.path.dirname(__file__), "test_file.sn.stats")
        expected_list = [
            '2365742',
            '0',
            '2365742',
            '1',
            '1182871',
            '1182871',
            '2328257',
            '2301812',
            '37485',
            '1690132',
            '2365742',
            '0',
            '286150',
            '0',
            '146733',
            '352602173',
            '176455583',
            '176146590',
            '347259282',
            '323220572',
            '0',
            '0',
            '3641584',
            '1.126656e-02',
            '149',
            '149',
            '149',
            '150',
            '150',
            '150',
            '36.2',
            '323.2',
            '67.9',
            '842331',
            '2966',
            '26',
            '305583',
            '71.4',
        ]
        tested_list = SnStatsParser(file_path).get_list()
        self.assertListEqual(tested_list, expected_list)
