from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "QDRANT"


class DistanceTypeEnum(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"
