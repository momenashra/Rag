APP_NAME ="RAG_App"
APP_VERSION="0.1"
GIT_TOKEN=""

FILE_ALLOWED_EXTENSIONS = ["text/plain","application/pdf"]
FILE_MAX_SIZE=10
FILE_CHUNK_SIZE=512000 #512KB

POSTGRES_USERNAME="postgres"
POSTGRES_PASSWORD="postgres_password"
POSTGRES_HOST="pgvector"
POSTGRES_PORT=5432
POSTGRES_MAIN_DATABASE="rag"





# ==============================================LLM CONFIG ============================================================ #

GENERATION_BACKEND="COHERE"
EMBEDDING_BACKEND="COHERE"


OPENAI_API_KEY=""

                        # for local openai server
OPENAI_API_URL_LITERAL=["http://localhost:11434/v1/","https://ca8d-34-87-49-26.ngrok-free.app/v1/"]
OPENAI_API_URL="" # for local openai server using ngrok

COHERE_API_KEY="E"


GENERATION_MODLE_ID_LITERAL=["gpt-3.5-turbo-0125","gpt-4","command-a-03-2025","qwen2.5:14b-instruct-q3_K_M"]
GENERATION_MODLE_ID="command-a-03-2025"

EMBEDDING_MODLE_ID_LITERAL=["embed-multilingual-light-v3.0","text-embedding-ada-002","nomic-embed-text"]
EMBEDDING_MODLE_ID="embed-multilingual-light-v3.0"

EMBEDDING_MODLE_SIZE=384

INPUT_DEFAULT_MAX_CARACTERS=1024        
GENERATION_DEFAULT_MAX_TOKENS=200
GENERATION_DEFAULT_TEMPRATURE=0.1


# ==============================================Vector DB CONFIG ============================================================ #
VECTOR_DB_BACKEND_LITERAL=["QDRANT","PGVECTOR"]
VECTOR_DB_BACKEND="PGVECTOR"
VECTOR_DB_PATH="qdrant_db"
VECTOR_DB_DISTANCE_METRIC="cosine"
VECTOR_DB_PGVEC_INDEX_THRESHOLD=100
# ==============================================Templates CONFIG ============================================================ #

PRIMARY_LANGUAGE="en"
DEFAULT_LANGUAGE="en"