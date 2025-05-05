from enum import Enum

class VectorDBEnums(Enum):
    QDRANT = "QDRANT"
    PGVECTOR = "PGVECTOR"

class DistanceTypeEnum(Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT = "dot"

class PgVectorTableSchemeEnums(Enum):
    ID = 'id'
    TEXT = 'text'
    VECTOR = 'vector'
    CHUNK_ID = 'chunk_id'
    METADATA = 'metadata'
    SUMMARY = 'summary'
    SUMMARY_METADATA = 'summary_metadata'
    _PREFIX = 'pgvector'

class PgVectorDistanceMethodEnums(Enum):
    COSINE = "vector_cosine_ops"
    DOT = "vector_l2_ops"

class PgVectorIndexTypeEnums(Enum):
    HNSW = "hnsw"
    IVFFLAT = "ivfflat"