import copy
import yaml

class RecognizerTestLoader(yaml.Loader):
    """
    A class for facilitating testing of recognizers.

    We would like to use the yaml library's functionality for turning
    strings into its internal representation, which is then fed into
    our recognizers. That way, the test input can be written as a yaml
    string, rather than having to be constructed by hand.

    The yaml.load function takes a Loader argument which expects a
    class to use instead of the standard unsafe loader. The library
    offers a couple of classes to choose from.

    This is a custom class that injects a recognizer call in the
    same way our parser does, assuming that you set the class'
    _test_recognizer member variable to some recognizer function.

    It saves the result into a result variable, so you can assert
    on it, and it overrides construct_object() to disable construction,
    since we're not testing the constructors here, and we don't want
    an exception because there aren't any.
    """
    def get_single_node(self):
        node = super().get_single_node()
        args = self.__class__.test_args
        kwargs = self.__class__.test_kwargs
        node = self.__class__.test_recognizer(node, *args, **kwargs)
        self.__class__.result = node
        return node

    def get_node(self):
        node = super().get_node()
        args = self.__class__.test_args
        kwargs = self.__class__.test_kwargs
        node = self.__class__.test_recognizer(node, *args, **kwargs)
        self.__class__.result = node
        return node

    def construct_object(self, node, deep=False):
        pass

def run_recognizer(test_recognizer, test_data, *args, **kwargs):
    """
    Run the given recognizer on the given YAML string, and return
    the result.

    Args:
        test_recognizer (function): The recognizer to be tested.
        test_data (str): A YAML string to feed it.

    Returns:
        (yaml.Node): The recognizer's output.
    """
    AdaptedTestLoader = copy.deepcopy(RecognizerTestLoader)
    AdaptedTestLoader.test_recognizer = test_recognizer
    AdaptedTestLoader.test_args = args
    AdaptedTestLoader.test_kwargs = kwargs
    yaml.load(test_data, Loader=AdaptedTestLoader)
    return AdaptedTestLoader.result
