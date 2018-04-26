import hashlib
import math
import numpy
from util import progressbar, logger
import humanize
import psutil


def hash_parameters(parameters):
    parameters = sorted(parameters.items())
    return hashlib.sha1(str(parameters).encode()).hexdigest()


def copy_dict_from_keys(dict_, keys):
    new_dict = {}
    for key in keys:
        new_dict[key] = dict_[key]
    return new_dict


def in_range(value, min_=None, max_=None):
    if min_ is not None and value < min_:
        return False
    if max_ is not None and value > max_:
        return False
    return True


def is_active(probabilities):
    return probabilities[0] > probabilities[1]


def chunk(number, number_chunks):
    chunks = []
    chunk_size = math.ceil(number / number_chunks)
    for i in range(number_chunks):
        start = chunk_size * i
        end = min(start + chunk_size, number) - 1
        size = end - start + 1
        chunks.append({'size': size, 'start': start, 'end': end})
    return chunks


def chunk_by_size(number, max_chunk_size):
    chunks = []
    number_chunks = math.ceil(number / max_chunk_size)
    for i in range(number_chunks):
        start = max_chunk_size * i
        end = min(start + max_chunk_size, number) - 1
        size = end - start + 1
        chunks.append({'size': size, 'start': start, 'end': end})
    return chunks


def max_in_memory_chunk_size(array, as_bool=False, use_swap=True, buffer=math.pow(1024,3)):
    if as_bool:
        target_type = numpy.dtype(bool)
    else:
        target_type = array.dtype
    shape = list(array.shape)
    shape[0] = 1
    shape = tuple(shape)
    single_size = numpy.zeros(shape, target_type).nbytes
    available_memory = psutil.virtual_memory().available
    if use_swap:
        available_memory += psutil.swap_memory().free
    available_memory -= buffer
    if available_memory < single_size:
        return 0
    else:
        return math.floor(available_memory/single_size)


def copy_into_memory(array, as_bool=False, use_swap=True, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1
    if isinstance(array, numpy.ndarray) and (not as_bool or array.dtype.name == 'bool'):
        return array[start:end+1]
    else:
        if as_bool:
            target_type = numpy.dtype(bool)
        else:
            target_type = array.dtype
        shape = list(array.shape)
        shape[0] = 1
        shape = tuple(shape)
        necessary_size = numpy.zeros(shape, target_type).nbytes
        necessary_size *= end - start + 1
        available_memory = psutil.virtual_memory().available
        if use_swap:
            available_memory += psutil.swap_memory().free
        if available_memory < necessary_size:
            logger.log('Available memory is ' + humanize.naturalsize(available_memory, binary=True)
                       + ' but necessary memory is ' + humanize.naturalsize(necessary_size, binary=True)
                       + '. Data will not be copied into memory.', logger.LogLevel.WARNING)
            if start == 0 and end == len(array) - 1:
                return array
            else:
                raise MemoryError('Out of memory')
        else:
            logger.log('Copying data with shape: ' + str(array.shape) + ', type: ' + str(target_type) + ' and size: '
                       + humanize.naturalsize(necessary_size, binary=True) + ' into memory.')
            if isinstance(array, numpy.ndarray):
                return array.astype(bool)[start:end+1]
            else:
                return copy_ndarray(array, as_bool, start=start, end=end)


def copy_ndarray(array, as_bool=False, log_level=logger.LogLevel.INFO, start=None, end=None):
    if start is None:
        start = 0
    if end is None:
        end = len(array) - 1
    if as_bool:
        new_array = numpy.zeros(array.shape, dtype=bool)
        with progressbar.ProgressBar(len(array), log_level) as progress:
            for i in range(start, end+1):
                new_array[i,:] = array[i,:].astype(bool)
                progress.increment()
        return new_array
    else:
        return array[start:end+1]


def substring_cut_from_middle(string, slices):
    removed = 0
    for slice_ in slices:
        cut_start = slice_[0] - removed
        cut_end = slice_[1] - removed
        string = string[:cut_start] + string[cut_end:]
        removed += slice_[1] - slice_[0]
    return string


def minimum(value_1, value_2):
    if value_1 is None:
        return value_2
    if value_2 is None:
        return value_1
    return min(value_1, value_2)


def maximum(value_1, value_2):
    if value_1 is None:
        return value_2
    if value_2 is None:
        return value_1
    return max(value_1, value_2)


def keys_in(keys, dict_):
    contained = True
    for key in keys:
        contained &= key in dict_
    return contained


def to_int(string):
    try:
        return int(string)
    except:
        return None


def normalize(values):
    offset = -values.min()
    factor = 1 / (values.max() + offset)
    for i in range(len(values)):
        values[i] = (values[i] + offset) * factor
