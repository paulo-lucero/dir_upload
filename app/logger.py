import typing
from dataclasses import (
    dataclass,
    field
)
from pathlib import Path

import pandas as pd

from app.py_ext import create_instance
from app.report import (
    console_api,
    to_log_excel
)



@create_instance
@dataclass
class DIR_LOGGER:
    content_count = 0

    logs: dict[
        typing.Literal[
            'NOTES',
            'SCHEMA',
            'PATHS'
        ],
        list[str]
    ] = field(default_factory=lambda : {
        'NOTES': [],
        'SCHEMA': [],
        'PATHS': []
    })

    count_logs: dict[
        typing.Literal[
            'REQUEST ROOT',
            'RECURSIVE COUNT',
            'WALK COUNT',
            'IS SAME'
        ],
        list[str | int | bool]
    ] = field(default_factory=lambda : {
        'REQUEST ROOT': [],
        'RECURSIVE COUNT': [],
        'WALK COUNT': [],
        'IS SAME': []
    })


    def incr(self):
        self.content_count += 1


    def add_counts_log(self, request_dir: str):
        current_count = 0
        for dir_path, dirnames, file_names in Path(request_dir).walk():
            current_count += (len(dirnames) + len(file_names))

        self.count_logs['REQUEST ROOT'].append(request_dir)
        self.count_logs['RECURSIVE COUNT'].append(self.content_count)
        self.count_logs['WALK COUNT'].append(current_count)
        self.count_logs['IS SAME'].append(self.content_count == current_count)
        
        self.content_count = 0


    def produce_counts_log(self):
        count_logs = self.count_logs

        if len(count_logs['REQUEST ROOT']) == 0:
            console_api.print(f'[bold green]No Count Logs Found[/]')
            return

        count_log_df = pd.DataFrame(self.count_logs)
        count_log_file = to_log_excel(count_log_df, 'File_Manager_Counts')

        console_api.print(f'[blue]INFO[/] : count logs on \'{count_log_file}\'')
   

    def add_log(self, request_parent: str, note: str, file_path: str):
        self.logs['NOTES'].append(note)
        self.logs['SCHEMA'].append(file_path[len(request_parent):])
        self.logs['PATHS'].append(file_path)
    

    def produce_logs(self):
        header = '\n\n'
        logs = self.logs

        if len(logs['NOTES']) == 0:
            console_api.print(f'{header}[bold green]No Logs Found[/]')
            return
        
        logs_df = pd.DataFrame(logs)
        log_file =  to_log_excel(logs_df, 'File_Manager_Logs')

        console_api.print(f'{header}[bold red]WARNING[/] : \'{log_file}\'')