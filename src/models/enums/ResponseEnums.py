from enum import Enum
class ResponseSignals(Enum):

    FILE_UPLOAD_SUCCESS = "file_uploaded_successfully"
    FILE_UPLOAD_FAIL = "file_failed_to_upload"
    FILE_SIZE_EXCEEDEDD = "file_size_exceeded"
    FILE_TYPE_NOT_SUPPORTED = "file_type_npt_supported"
    FILE_VALIDATE_SUCCESS = "file_validated_successfully"
