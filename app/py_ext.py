import typing
import os
from pathlib import Path



TYPE_CLASS_OBJ = typing.TypeVar('TYPE_CLASS_OBJ')

def create_instance(data_type: type[TYPE_CLASS_OBJ]) -> TYPE_CLASS_OBJ:
    return data_type()


def get_env(en_var: str):
    try:
        return os.environ[en_var]
    except KeyError:
        raise KeyError(f'This environment variable \'{en_var}\' doesn\'t exist')
    


def _file_paths_processor(stringify_func: typing.Callable[[], Path]):
    def path_func(*file_paths: str | Path) -> str:
        child_path = Path()

        for file_path in file_paths:
            child_path /= file_path

        return str(stringify_func() / child_path)
    return path_func
    

@_file_paths_processor
def stringify_onedrive_path():
    return Path(get_env('OneDrive'))


@_file_paths_processor
def stringify_downloads_path():
    return Path(get_env('USERPROFILE')) / 'Downloads'