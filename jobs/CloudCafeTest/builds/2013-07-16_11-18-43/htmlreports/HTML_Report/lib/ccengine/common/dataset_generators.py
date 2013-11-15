class Dataset(object):
    def __init__(self, name, data_dict):
        """Defines a set of data to be used as input for a data driven test.

        data_dict should be a dictionary with keys matching the keyword
        arguments defined in test method that consumes the dataset.

        name should be a string describing the dataset.
        """

        self.name = name
        self.data = data_dict


class BaseDatasetGenerator(list):
    """Specialized list that holds Dataset objects"""

    def append(self, dataset):
        if not isinstance(dataset, Dataset):
            raise TypeError(
                "append() argument must be type Dataset, not {0}".format(
                    type(dataset)))

        super(BaseDatasetGenerator, self).append(dataset)

    def append_new_dataset(self, name,  data_dict):
        """Creates and appends a new Dataset"""
        self.append(Dataset(name, data_dict))


class TestMultiplier(BaseDatasetGenerator):
    """Does not generate datasets, but instead creates num_range number of
    copies of the source test, and names the new tests numerically.
    """

    def __init__(self, num_range):
        for num in range(num_range):
            name = "{0}".format(num)
            self.append_new_dataset(name, dict())


class DatasetGenerator(BaseDatasetGenerator):
    """Generates Datasets from a list of dictionaries, which are named
    numericaly according to the source dictionary's order in the source list.
    If a base_dataset_name is provided, that is used as the base name postfix
    for all tests before they are numbered.
    """

    def __init__(self, list_of_dicts, base_dataset_name=None):
        count = 0
        for kwdict in list_of_dicts:
            test_name = "{0}_{1}".format(base_dataset_name or "dataset", count)
            self.append_new_dataset(test_name, kwdict)
            count += 1
