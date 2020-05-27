import os
from typing import Dict, List, Set

SN_STATS_TABLE_HEADER: List[str] = [
    'Sample',
    'raw total sequences',
    'filtered sequences',
    'sequences',
    'is sorted',
    '1st fragments',
    'last fragments',
    'reads mapped',
    'reads mapped and paired',
    'reads unmapped',
    'reads properly paired',
    'reads paired',
    'reads duplicated',
    'reads MQ0',
    'reads QC failed',
    'non-primary alignments',
    'total length',
    'total first fragment length',
    'total last fragment length',
    'bases mapped',
    'bases mapped (cigar)',
    'bases trimmed',
    'bases duplicated',
    'mismatches',
    'error rate',
    'average length',
    'average first fragment length',
    'average last fragment length',
    'maximum length',
    'maximum first fragment length',
    'maximum last fragment length',
    'average quality',
    'insert size average',
    'insert size standard deviation',
    'inward oriented pairs',
    'outward oriented pairs',
    'pairs with other orientation',
    'pairs on different chromosomes',
    'percentage of properly paired reads (%)',
]


class SnStatsParser:

    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def _parse(self):
        parsed_list: List[str] = []
        with open(self.file_path, 'r') as file:
            for line in file:
                elements: List[str] = line.rstrip().split(':')
                number: str = elements[1].strip().split()[0]
                parsed_list.append(number)
        self._parsed_list: List[str] = parsed_list

    def get_list(self):
        if getattr(self, '_parsed_list', None) is None:
            self._parse()
        return self._parsed_list


class GeneCountParser:
    """
    Parse counts from count_unique_ref rule
    """

    def __init__(self, file_path: str):
        self.file_path: str = file_path

    def _parse(self):
        parsed_dict: Dict[str, str] = {}
        with open(self.file_path, 'r') as file:
            for line in file:
                elements: List[str] = line.strip().split()
                parsed_dict[elements[1]] = elements[0]
        self._parsed_dict: Dict(str) = parsed_dict

    def get_dict(self):
        if getattr(self, '_parsed_dict', None) is None:
            self._parse()
        return self._parsed_dict


def generate_mapping_sn_stats(
      sn_stats_file_paths: List[str], output_file_path: str, sep: str = ','
):
    with open(output_file_path, "w") as output_file:
        print(sep.join(SN_STATS_TABLE_HEADER), file=output_file)
        for file_path in sn_stats_file_paths:
            sample_name: str = os.path.basename(file_path).split('.sn.stats')[0]
            print(sep.join([sample_name] + SnStatsParser(file_path).get_list()), file=output_file)


class CountMatrixBuilder:

    def __init__(self, gene_count_file_path: list):
        self.file_paths: List[str] = gene_count_file_path
        # We need to build a dict for each sample
        self.all_gene_counts: Dict(Dict(str)) = {}
        # We also keep track of all gene names found for each samples
        self.gene_names: Set[str] = set()
        # When writing header, we need to freeze the order of the samples
        self.samples_names: List[str] = []

    def parse_files(self):
        for file_path in self.file_paths:
            sample_name: str = os.path.basename(file_path).split('_ref_counts.txt')[0]
            sample_gene_counts = GeneCountParser(file_path).get_dict()
            self.all_gene_counts[sample_name] = sample_gene_counts
            self.gene_names = self.gene_names.union(set(sample_gene_counts.keys()))

    def _build_header(self, sep: str):
        self.samples_names = list(self.all_gene_counts.keys())
        col_names: List[str] = ['Genes'] + self.samples_names
        return sep.join(col_names)

    def _build_gene_line(self, gene: str, sep: str):
        gene_counts: List[str] = [gene]
        for sample in self.samples_names:
            gene_counts.append(self.all_gene_counts[sample].get(gene, '0'))
        return sep.join(gene_counts)

    def output_matrix(self, output_file_path: str, sep: str):
        with open(output_file_path, "w") as output_file:
            print(self._build_header(sep), file=output_file)
            for gene in self.gene_names:
                print(self._build_gene_line(gene, sep), file=output_file)


def build_gene_count_matrix(
      gene_count_file_paths: List[str], output_file_path: str, sep: str = ','
):
    count_builder = CountMatrixBuilder(gene_count_file_paths)
    count_builder.parse_files()
    count_builder.output_matrix(output_file_path, sep)
