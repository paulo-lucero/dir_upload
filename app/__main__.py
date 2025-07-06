def _generate_dir_infos():
    from app.info import DirInfo
    from app.py_ext import stringify_downloads_path

    return [
        DirInfo(
            final_dir=stringify_downloads_path(r"FINAL\FOLDER 1"),
            request_dir=stringify_downloads_path(r"UPLOAD REQUESTS\FOLDER 1"),
            no_files_until=2
        ),
        DirInfo(
            final_dir=stringify_downloads_path(r"FINAL\FOLDER 1\PROJECT 1\TOOLS"),
            request_dir=stringify_downloads_path(r"UPLOAD REQUESTS\FOLDER 1\PROJECT 1\TOOLS"),
            no_files_until=0
        ),
        DirInfo(
            final_dir=stringify_downloads_path(r"FINAL\FOLDER 2"),
            request_dir=stringify_downloads_path(r"UPLOAD REQUESTS\FOLDER 2"),
            no_files_until=3
        ),
    ]


def upload_requests():
    from app.logger import DIR_LOGGER

    for dir_info in _generate_dir_infos():
        dir_info.upload_requests()
    #     DIR_LOGGER.add_counts_log(dir_info.request_dir)
    # DIR_LOGGER.produce_counts_log()
    DIR_LOGGER.produce_logs()


def ready_requests():
    for dir_info in _generate_dir_infos():
        dir_info.ready_request()


# ready_requests()
upload_requests()