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
    PROJECT_NOT_FOUND = "project_id_not_found"
    PROJECT_INDEX_FAIL = "project_index_failed"
    PROJECT_INDEX_SUCCESS = "project_indexed_successfully"
    PROJECT_INDEX_INFO_FAILED = "project_index_info_failed"
    PROJECT_INDEX_INFO_SUCCESS = "project_index_info_retrived_successfully"
    VECTOR_DB__SEARCH_ERROR = "vector_db_search_error"
    VECTOR_DB__SEARCH_SUCCESS = "vector_db_search_success"