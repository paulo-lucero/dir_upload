from dataclasses import (
    dataclass,
    field
)
from pathlib import Path

from app.py_ext import create_instance



@create_instance
@dataclass(frozen=True)
class DIR_SCHEMA:
    schema_dirs: list[str] = field(default_factory=lambda : [])


    def add_schema_dir(self, requested_dir: str):
        if requested_dir in self.schema_dirs:
            raise Exception(f'This dir schema \'{requested_dir}\' is already exist')
        
        self.schema_dirs.append(requested_dir)


    def is_schema(self, dir_path: Path):
        return str(dir_path) in self.schema_dirs