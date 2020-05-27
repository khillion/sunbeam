import os
from unittest import TestCase

from sunbeamlib.mapping import CountMatrixBuilder, GeneCountParser, SnStatsParser


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


class TestGeneCountParser(TestCase):

    def test_parse(self):
        file_path = os.path.join(os.path.dirname(__file__), "sample1_test_count_unique_ref.txt")
        expected_dict = {
            'gene1': '42',
            'gene2': '15',
            'gene4': '8'
        }
        tested_dict = GeneCountParser(file_path).get_dict()
        self.assertDictEqual(tested_dict, expected_dict)


class TestCountMatrixBuilder(TestCase):

    def test_parse_files(self):
        file_paths = [
            os.path.join(os.path.dirname(__file__), "sample1_test_count_unique_ref.txt"),
            os.path.join(os.path.dirname(__file__), "sample2_test_count_unique_ref.txt")
        ]
        expected_gene_counts = {
            'sample1': {
                'gene1': '42',
                'gene2': '15',
                'gene4': '8'
            },
            'sample2': {
                'gene1': '4',
                'gene2': '5',
                'gene3': '6'
            },
        }
        expected_gene_names = set(
            ['gene1', 'gene2', 'gene3', 'gene4']
        )
        builder = CountMatrixBuilder(file_paths)
        builder.parse_files()
        self.assertSetEqual(builder.gene_names, expected_gene_names)
        self.assertDictEqual(builder.all_gene_counts, expected_gene_counts)
