import os
import yaml

def has_key(node, key):
    """
    Returns True iff the node has the given key.

    Args:
        node (yaml.MappingNode): A node to check.
        key (Any): The desired key object.

    Returns:
        (bool): True iff the key is present.
    """
    return any([kv_pair
            for kv_pair in node.value
            if kv_pair[0].value == key])

def get_by_key(node, key):
    """
    Returns the node representing the value for the given key.

    Args:
        node (yaml.MappingNode): A node.
        key (Any): The desired key object.

    Returns:
        (yaml.Node): The node for the given key.
    """
    matches = [kv_pair[1]
            for kv_pair in node.value
            if kv_pair[0].value == key]
    return matches[0]

def set_by_key(node, key, value_node):
    """
    Sets the node representing the value for the given key.

    Args:
        node (yaml.MappingNode): A node.
        key (str): The desired key.
        value_node (yaml.Node): A value node to insert for the given \
                key.
    """
    matches = [i
            for i, kv_pair in enumerate(node.value)
            if kv_pair[0].value == key]
    if len(matches) == 0:
        key_node = yaml.ScalarNode('tag:yaml.org,2002:str', key)
        node.value.append((key_node, value_node))
    else:
        node.value[matches[0]] = (node.value[matches[0]][0], value_node)

def update_key(node, key, recognizer, *args, **kwargs):
    set_by_key(node, key, recognizer(get_by_key(node, key), *args, **kwargs))

def set_key_default(node, key, default_value):
    if has_key(node, key):
        return

    if isinstance(default_value, str):
        value_node = yaml.ScalarNode('tag:yaml.org,2002:str', default_value)
    elif isinstance(default_value, list):
        value_node = yaml.SequenceNode('tag:yaml.org,2002:seq', default_value)
    elif isinstance(default_value, dict):
        # TODO BUG should be a list of (yaml.Node, yaml.Node) made from dict
        # Do we have anything other than empty lists and scalars for default values?
        value_node = yaml.MappingNode('tag:yaml.org,2002:map', default_value)
    elif isinstance(default_value, bool):
        value_node = yaml.ScalarNode('tag:yaml.org,2002:bool', default_value)
    elif default_value is None:
        value_node = None   # TODO: is that right? See when we construct things

    set_by_key(node, key, value_node)

def rename_key(node, key, new_name):
    """
    Renames a key in the given mapping.

    If the new name already exists in the given mapping, raises an
    error.

    Args:
        node (yaml.MappingNode): A node containing the given key
        key (str): The key to rename
        new_name (str): The new name for the key

    Raises:
        RuntimeError: The mapping already has a key with the new name.
    """
    require_keys(node, [key])

    if has_key(node, new_name):
        raise RuntimeError("{}{}Invalid input: invalid key {}".format(
            node.start_mark, os.linesep, new_name))

    matches = [i
            for i, kv_pair in enumerate(node.value)
            if kv_pair[0].value == key]
    new_key = yaml.ScalarNode('tag:yaml.org,2002:str', new_name)
    node.value[matches[0]] = (new_key, node.value[matches[0]][1])

def require_keys(node, keys):
    """Checks that the node is a mapping and has the given keys."""
    if not isinstance(node, yaml.MappingNode):
        raise RuntimeError("{}{}Invalid input: expected a mapping with keys {}".format(
            node.start_mark, os.linesep, keys))

    for key in keys:
        if not has_key(node, key):
            raise RuntimeError("{}{}Invalid input: missing key '{}' of expected keys {}".format(
                node.start_mark, os.linesep, key, keys))

def require_type(node, tag):
    if not isinstance(node, yaml.ScalarNode):
        raise RuntimeError('{}{}Invalid input: expected a scalar value of type {}'.format(
            node.start_mark, os.linesep, tag))

    if node.tag != tag:
        raise RuntimeError('{}{}Invalid input: expected a scalar value of type {}, found one of type {}'.format(
            node.start_mark, os.linesep, node.tag, tag))

def interpret_as_bool(node):
    """Converts a ScalarNode containing a boolean value to have
    a bool type value. Does nothing if the node is not a boolean
    scalar node.

    Args:
        node (yaml.ScalarNode): The node to change
    """
    if isinstance(node, yaml.ScalarNode):
        if node.tag == 'tag:yaml.org,2002:bool':
            if node.value == 'false':
                node.tag = 'tag:yaml.org,2002:bool'
                node.value = False
            if node.value == 'true':
                node.tag = 'tag:yaml.org,2002:bool'
                node.value = True

def get_by_index(node, index):
    """Returns the node at the given index in a sequence.

    Args:
        node (yaml.SequenceNode): The sequence to index
        index (int): The item to retrieve

    Returns:
        (yaml.Node): The node at that item
    """
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Invalid input: expected a sequence'.format(
            node.start_mark, os.linesep))
    return node.value[index]

def mapping_to_sequence(node, key):
    """
    Converts a mapping of keys to mappings to a list of mappings.

    The keys of the outer mapping are added to the corresponding inner \
    mapping as a value under the specified key, unless there is a value \
    there already.

    This function modifies the original mappings and reuses them in the \
    result.

    Args:
        node (yaml.Node): A mapping whose values are also \
                yaml.MappingNodes, or some other kind of node.
        key (Union[str, list, dict]): A key to store the original key \
                under.

    Returns:
        (yaml.SequenceNode): A sequence containing the inner objects, \
                with the additional keys, or the original node if it \
                was not a mapping.
    """
    if not isinstance(node, yaml.MappingNode):
        return node

    object_list = []
    for k, v in node.value:
        set_by_key(v, key, k)
        object_list.append(v)
    return yaml.SequenceNode(u'tag:yaml.org,2002:seq', object_list)

def pairs_to_sequence(node, key_key, value_key, merge_value):
    """
    Converts a mapping to a list of mappings with keys and values as
    members.

    The arguments specify the names of the keys in the newly created
    mappings under which the key and value are stored.

    Returns the original node unchanged if it is already a mapping.

    Args:
        node (yaml.Node): A mapping node.
        key_key (str): A key to store the original key under.
        value_key (str): A key to store the original value under.

    Returns:
        (yaml.SequenceNode): A sequence containing mappings containing \
                the original pairs.
    """
    if not isinstance(node, yaml.MappingNode):
        return node

    key_tag = yaml.ScalarNode('tag:yaml.org,2002:str', key_key)
    value_tag = yaml.ScalarNode('tag:yaml.org,2002:str', value_key)

    object_list = []
    for k, v in node.value:
        if isinstance(v, yaml.MappingNode) and merge_value:
            new_node = v
            new_node.value.append((key_tag, k))
        else:
            new_node = yaml.MappingNode('tag:yaml.org,2002:map', [
                    (key_tag, k), (value_tag, v)])
        object_list.append(new_node)
    return yaml.SequenceNode('tag:yaml.org,2002:seq', object_list)

def update_each_item(node, recognizer, *args, **kwargs):
    """
    Applies the recognizer to each subnode in a sequence node.

    The subnode will be replaced with the recognizer's result.

    Args:
        node (yaml.SequenceNode): A SequenceNode.
        recognizer (Callable): A recognizer function to call.
        args: Additional arguments to pass to the recognizer.
        kwargs: Additional keyword arguments to pass to the recognizer.
    """
    new_subnodes = []
    if not isinstance(node, yaml.SequenceNode):
        raise RuntimeError('{}{}Invalid input: sequence expected.'.format(
            node.start_mark, os.linesep))

    for subnode in node.value:
        new_subnodes.append(recognizer(subnode, *args, **kwargs))

    node.value = new_subnodes

def update_each_value(node, recognizer, *args, **kwargs):
    """
    Applies the recognizer to each value in a mapping node.

    The value will be replaced with the recognizer's result.

    Args:
        node (yaml.MappingNode): A MappingNode.
        recognizer (Callable): A recognizer function to call.
        args: Additional arguments to pass to the recognizer.
        kwargs: Additional keyword arguments to pass to the recognizer.
    """
    new_kv_pairs = []

    if not isinstance(node, yaml.MappingNode):
        raise RuntimeError('{}{}Invalid input: mapping expected.'.format(
            node.start_mark, os.linesep))

    for kv_pair in node.value:
        new_kv_pairs.append((kv_pair[0], recognizer(kv_pair[1], *args, **kwargs)))

    node.value = new_kv_pairs

def optionally(recognizer, node):
    try:
        return recognizer(node)
    except RuntimeError as e:
        return node

def was_recognized(node):
    if not isinstance(node, yaml.MappingNode):
        return False
    if node.tag == 'tag:yaml.org,2002:map':
        return False
    return True

