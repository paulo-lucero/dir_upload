import typing
from dataclasses import dataclass
from pathlib import Path
import shutil

from app.schema import DIR_SCHEMA
from app.logger import DIR_LOGGER

from app.report import console_api



T = typing.TypeVar('T')
_TYPE_STR_PATH = str | Path


def _convert_to_deco(method_func: typing.Callable[[T], tuple[str, str]]):
    def converter(_: T, orig_file: _TYPE_STR_PATH):
        if isinstance(orig_file, Path):
            orig_file = str(orig_file.resolve())
        
        converted_root, orig_root = method_func(_)

        return (
            converted_root +
            orig_file[len(orig_root):]
        )
    
    return converter



@dataclass(frozen=True)
class DirInfo:
    final_dir: str
    request_dir: str
    no_files_until: int


    def __post_init__(self):
        DIR_SCHEMA.add_schema_dir(self.request_dir)


    @property
    def request_parent(self):
        return str(Path(self.request_dir).parent)


    @_convert_to_deco
    def to_request(self):
        return self.request_dir, self.final_dir


    @_convert_to_deco
    def to_final(self):
        return self.final_dir, self.request_dir
    

    def get_request_level(self, request_file: _TYPE_STR_PATH):
        if isinstance(request_file, Path):
            request_file = str(request_file)
        request_sub = request_file[len(self.request_dir):]
        return len(Path(request_sub).parts) - 1
    

    def is_file_at_final(self, request_file: _TYPE_STR_PATH):
        at_final = Path(self.to_final(request_file))

        return at_final.is_file()
    

    def is_dir_at_final(self, request_dir: _TYPE_STR_PATH):
        at_final = Path(self.to_final(request_dir))

        return at_final.is_dir()
    

    def is_request_allowed_file(self, request_file: _TYPE_STR_PATH):
        request_lvl = self.get_request_level(request_file)

        if request_lvl > self.no_files_until: return True

        return not Path(request_file).is_file()
    

    def _copy_to_request(self, dir_path: Path, dir_names: list[str]):
        for dir_name in dir_names:
            subdir_path = dir_path / dir_name
            request_dir = self.to_request(subdir_path)
            request_dir_path = Path(request_dir)

            if DIR_SCHEMA.is_schema(request_dir_path): continue
            if request_dir_path.is_dir(): continue

            request_dir_path.mkdir()
            print(f'Created : {request_dir}')
    

    def ready_request(self):
        for dir_path, dir_names, file_names in Path(self.final_dir).walk():
            self._copy_to_request(dir_path, dir_names)
    

    def _upload_file(self, request_path: Path):
        if request_path.is_dir(): return

        dest_file = self.to_final(request_path)
        orig_file = str(request_path)

        shutil.copy2(orig_file, dest_file)

        if Path(dest_file).is_file():
            request_path.unlink()
            console_api.print(f'[blue]Uploaded[/] : \'{orig_file}\'')
        else:
            raise FileNotFoundError(f'This \'{orig_file}\' isn\'t successfully uploaded')


    def upload_requests(self, dir_path: Path | None = None):
        if dir_path is None:
            dir_path = Path(self.request_dir)

        for content_path in dir_path.iterdir():
            DIR_LOGGER.incr()
            if not self.is_request_allowed_file(content_path):
                DIR_LOGGER.add_log(self.request_parent, 'NOT ALLOWED FILES', str(content_path))
                continue

            if self.is_file_at_final(content_path):
                DIR_LOGGER.add_log(self.request_parent, 'FILE ALREADY EXISTS', str(content_path))
                continue

            self._upload_file(content_path)

            if not content_path.is_dir(): continue

            if DIR_SCHEMA.is_schema(content_path):
                # DIR_LOGGER.add_log(self.request_parent, 'HAS SCHEMA', str(content_path))
                continue

            if not self.is_dir_at_final(content_path):
                DIR_LOGGER.add_log(self.request_parent, 'NOT PART OF SCHEMA', str(content_path))
                continue

            self.upload_requests(content_path)