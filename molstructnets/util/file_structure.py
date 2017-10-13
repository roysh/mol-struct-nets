from util import file_util, constants


class DataSet:

    smiles = 'smiles'


class Target:

    classes = 'classes'


class Partitions:

    train = 'train'
    test = 'test'


class Preprocessed:

    preprocessed = 'preprocessed'
    preprocessed_training = 'preprocessed_training'
    preprocessed_training_references = 'preprocessed_training_references'


class Predictions:

    prediction = 'prediction'


class AttentionMap:

    substructure_atoms = 'substructure_atoms'
    attention_map_active = 'attention_map_active'
    attention_map_inactive = 'attention_map_inactive'
    attention_map_active_indices = 'attention_map_active_indices'
    attention_map_inactive_indices = 'attention_map_inactive_indices'


def get_root_from_experiment_file(experiment_file_path):
    return file_util.get_parent(file_util.get_parent(experiment_file_path))


def get_experiment_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'experiments')


def get_data_set_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'data_sets')


def get_data_set_file(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'data_sets',
                                     global_parameters[constants.GlobalParameters.data_set] + '.h5')


def get_target_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'data_sets',
                                     global_parameters[constants.GlobalParameters.data_set], 'targets')


def get_target_file(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'data_sets',
                                     global_parameters[constants.GlobalParameters.data_set], 'targets',
                                     global_parameters[constants.GlobalParameters.target] + '.h5')


def get_partition_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'data_sets',
                                     global_parameters[constants.GlobalParameters.data_set], 'targets',
                                     global_parameters[constants.GlobalParameters.target], 'partitions')


def get_preprocessed_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'data_sets',
                                     global_parameters[constants.GlobalParameters.data_set],
                                     'preprocessed')


def get_network_file(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'experiments',
                                     global_parameters[constants.GlobalParameters.experiment],
                                     global_parameters[constants.GlobalParameters.data_set],
                                     global_parameters[constants.GlobalParameters.target], 'network.h5')


def get_prediction_file(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'experiments',
                                     global_parameters[constants.GlobalParameters.experiment],
                                     global_parameters[constants.GlobalParameters.data_set],
                                     global_parameters[constants.GlobalParameters.target], 'predictions.h5')


def get_evaluation_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'experiments',
                                     global_parameters[constants.GlobalParameters.experiment],
                                     global_parameters[constants.GlobalParameters.data_set],
                                     global_parameters[constants.GlobalParameters.target], 'evaluation')


def get_interpretation_folder(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'experiments',
                                     global_parameters[constants.GlobalParameters.experiment],
                                     global_parameters[constants.GlobalParameters.data_set],
                                     global_parameters[constants.GlobalParameters.target], 'interpretation')

def get_attentionmap_file(global_parameters):
    return file_util.resolve_subpath(global_parameters[constants.GlobalParameters.root], 'experiments',
                                     global_parameters[constants.GlobalParameters.experiment],
                                     global_parameters[constants.GlobalParameters.data_set],
                                     global_parameters[constants.GlobalParameters.target], 'interpretation',
                                     'attention_map.h5')
