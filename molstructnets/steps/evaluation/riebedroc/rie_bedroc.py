import h5py
import numpy

from steps.evaluation.shared import rie_bedroc
from util import data_validation, file_structure, constants, csv_file


class RieBedroc:

    @staticmethod
    def get_id():
        return 'rie_bedroc'

    @staticmethod
    def get_name():
        return 'RIE and BEDROC'

    @staticmethod
    def get_parameters():
        parameters = list()
        parameters.append({'id': 'method_name', 'name': 'Method Name', 'type': str, 'default': None,
                           'description': 'Name of the evaluated method. Default: Partition name'})
        parameters.append({'id': 'alphas', 'name': 'Alphas', 'type': str,
                           'default': '20,100', 'regex': '([0-9]+(,[0-9]+)*)?',
                           'description': 'List of alphas. Default: 20, 100'})
        parameters.append({'id': 'shuffle', 'name': 'Shuffle', 'type': bool,
                           'default': True, 'description': 'Shuffles the data before evaluation to counter sorted data'
                                                           ' sets, which can be a problem in cases where the'
                                                           ' probability is equal. Default: True'})
        parameters.append({'id': 'partition', 'name': 'Partition', 'type': str, 'default': 'test',
                           'options': ['train', 'test', 'both'],
                           'description': 'The enrichment plot will be generated for the specified partition. Default:'
                                          ' test'})
        return parameters

    @staticmethod
    def check_prerequisites(global_parameters, local_parameters):
        data_validation.validate_target(global_parameters)
        data_validation.validate_partition(global_parameters)
        data_validation.validate_prediction(global_parameters)

    @staticmethod
    def execute(global_parameters, local_parameters):
        method_name = local_parameters['method_name']
        if method_name is None:
            method_name = local_parameters['partition'].title()
        alphas = []
        for alpha in local_parameters['alphas'].split(','):
            alphas.append(int(alpha))
        prediction_h5 = h5py.File(file_structure.get_prediction_file(global_parameters), 'r')
        predictions = prediction_h5[file_structure.Predictions.prediction][:]
        prediction_h5.close()
        target_h5 = h5py.File(file_structure.get_target_file(global_parameters), 'r')
        classes = target_h5[file_structure.Target.classes][:]
        target_h5.close()
        if local_parameters['partition'] == 'train' or local_parameters['partition'] == 'test':
            partition_h5 = h5py.File(file_structure.get_partition_file(global_parameters), 'r')
            if local_parameters['partition'] == 'train':
                partition = partition_h5[file_structure.Partitions.train][:]
                partition = numpy.unique(partition)
            else:
                partition = partition_h5[file_structure.Partitions.test][:]
            partition_h5.close()
            predictions = predictions[partition]
            classes = classes[partition]
        ries, bedrocs = rie_bedroc.stats(predictions, classes, alphas, shuffle=local_parameters['shuffle'],
                                         seed=global_parameters[constants.GlobalParameters.seed])
        csv_path = file_structure.get_evaluation_stats_file(global_parameters)
        csv = csv_file.CsvFile(csv_path)
        row = dict()
        for i in range(len(alphas)):
            row['rie' + str(alphas[i])] = ries[i]
            row['bedroc' + str(alphas[i])] = bedrocs[i]
        csv.add_row(method_name, row)
        csv.save()
