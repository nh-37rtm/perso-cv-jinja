
from dataclasses import dataclass, is_dataclass

import typing as t
import inspect

T= t.TypeVar('T')

# https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
def is_optional(field):
    return t.get_origin(field) is t.Union and \
           type(None) in t.get_args(field)

def deep_map_from_raw(source: dict|list, destination_type: t.Type[T]) -> T:


    if is_optional(destination_type):
            return deep_map_from_raw(source, t.get_args(destination_type)[0])           

    common_destination_type = t.get_origin(destination_type)
    is_generic_type = True
    
    if common_destination_type is None:
        common_destination_type = destination_type
        is_generic_type = False
    
    generic_args = None
    
    if is_generic_type:
        generic_args = t.get_args(destination_type)
            
    while True:
        
        if issubclass( common_destination_type, list) and \
            isinstance(source, list) :
            
            sub_destination_type: t.Type = list
            
            if is_generic_type and len(generic_args) > 0:
                sub_destination_type, = generic_args
                
            return [
                deep_map_from_raw(value, sub_destination_type) 
                for value in source ]    
                

        if isinstance(source, dict) :
            
            destination_dict = source
                
            if issubclass( common_destination_type, dict):
                sub_destination_value_type: t.Type = dict
            
                if is_generic_type and len(generic_args) > 0:
                    _, sub_destination_value_type = generic_args
                
                return dict([
                    (key, deep_map_from_raw(value, sub_destination_value_type))
                    for key, value in destination_dict.items() ])

            if is_dataclass( common_destination_type ):

                result_dict = dict()
                result_instance = None

                for field_name, field in common_destination_type.__dataclass_fields__.items():
                    # assert(field_name in source)
                    if not field_name in source:
                        continue

                    # setattr(result_instance, field_name, 
                    #         deep_map_from_raw( source[field_name], field.type) )

                    destination_type = None
                    
                    if inspect.isclass(field.type):
                        destination_type = field.type
                    else:
                        destination_type = field.type
                    result_dict[field_name] = deep_map_from_raw( source[field_name], destination_type)

                    
                    
                result_instance = common_destination_type(**result_dict)
                
                return result_instance

        # source type is not supported or final type : return as is
        return source
            
        break
