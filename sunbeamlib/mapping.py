import os

SN_STATS_TABLE_HEADER = [
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

    def __init__(self, file_path):
        self.file_path = file_path

    def _parse(self):
        parsed_list = []
        with open(self.file_path, 'r') as file:
            for line in file:
                elements = line.rstrip().split(':')
                number = elements[1].strip().split()[0]
                parsed_list.append(number)
        self._parsed_list = parsed_list

    def get_list(self):
        if getattr(self, '_parsed_list', None) is None:
            self._parse()
        return self._parsed_list


def generate_mapping_sn_stats(sn_stats_file_paths, output_file_path, sep=','):
    with open(output_file_path, "w") as output_file:
        print(sep.join(SN_STATS_TABLE_HEADER), file=output_file)
        for file_path in sn_stats_file_paths:
            sample_name = os.path.basename(file_path).split('.sn.stats')[0]
            print(sep.join([sample_name] + SnStatsParser(file_path).get_list()), file=output_file)
