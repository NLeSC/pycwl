from .common import *

import os

def recognize_type_definition(node):
    return node

def recognize_type(node):
    return node

def recognize_type_description(node):
    pass

def recognize_file_type_description(node):
    pass

def recognize_array_type_description(node):
    require_keys(node, ['itemType'])
    update_key(node, 'itemType', recognize_type)
    node.tag = '!ArrayTypeDescription'
    return node

def recognize_enum_type_description(node):
    require_keys(node, ['symbols'])
    symbols = get_by_key(node, 'symbols')
    if not isinstance(symbols, yaml.SequenceNode):
        raise RuntimeError('{}{}Expected a list of symbols'.format(
                node.start_mark, os.linesep))

    for symbol in symbols.value:
        require_type(symbol, 'tag:yaml.org,2002:str')

    node.tag = '!EnumTypeDescription'
    return node

def recognize_record_type_description(node):
    require_keys(node, ['record'])
    rename_key(node, 'record', 'fields')

    update_key(node, 'fields', mapping_to_sequence, 'name')
    fields = get_by_key(node, 'fields')
    update_each_item(fields, recognize_record_field_description)

    node.tag = '!RecordTypeDescription'
    return node

def recognize_record_field_description(node):
    require_keys(node, ['name', 'type'])
    update_key(node, 'type', recognize_type)
    node.tag = '!RecordFieldDescription'
    return node
