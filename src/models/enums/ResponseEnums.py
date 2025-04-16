from enum import Enum


class ResponseSignals(Enum):

    FILE_UPLOAD_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOAD_FAIL = "file_failed_to_upload"
    FILE_SIZE_EXCEEDEDD = "file_size_exceeded"
    FILE_TYPE_NOT_SUPPORTED = "file_type_npt_supported"
    FILE_VALIDATE_SUCCESS = "file_validated_successfully"
    FILE_PROCESSING_FAIL = "file_processing_failed"
    FILE_PROCESSING_SUCCESS = "file_processed_successfully"
    NO_FILES_ERROR = "no_files_to_process"
    FILE_NOT_FOUND = "no_file_id_not_found"
