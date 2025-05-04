from fastapi import APIRouter, Request,status
from fastapi.responses import JSONResponse
from helpers import get_settings, Settings
from controllers.NlpController import NlpController
from models import ResponseSignals
import logging
from .schema.nlp import PushRequest,SearchRequest,AnswerRequest
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_shemas import DataChunk
from tqdm.auto import tqdm

app_logger = logging.getLogger("uvicorn.error")

nlp_router = APIRouter(
    prefix="/api/v1/nlp",
    tags=["api_v1", "nlp"],
)

@nlp_router.post("/index/push/{project_id}")
async def index_project(request: Request,project_id: int,push_request: PushRequest):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

    # Check if the project exists in the database
    project = await project_model.get_project_or_create_one(project_id=project_id)

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignals.PROJECT_NOT_FOUND.value
                },
        )
    
    nlp_controller = NlpController(
        vector_db_client=request.app.vector_db_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client,
        template_parser=request.app.template_parser
    )
    
    has_records= True
    page_no = 1
    inserted_items_count = 0
    idx=0
    #check for collection
    collection_name=  nlp_controller.create_collection_name(project_id=project.project_id)
    _=  request.app.vector_db_client.create_collection(collection_name=collection_name,
                                                            embedding_dimension=request.app.embedding_client.embedding_size,
                                                            do_reset=push_request.do_reset)
    # setup batches by build progress bar
    total_chunks=await chunk_model.get_total_chunks_count(project_id=project.project_id)
    pbar=tqdm(total=total_chunks,desc=F"Vector indexing_{total_chunks}",position=0)

    while has_records:
        page_chunks= await chunk_model.get_all_project_chunks_by_project_id(project_id=project.project_id,page_no=page_no)
        if len (page_chunks):
            page_no+=1
        if len(page_chunks) ==0 or not page_chunks:
            has_records = False
            break
        # chunks_ids= list(range(idx,idx+len(page_chunks)))
        #for pgvector

        chunks_ids = [c.chunk_id   for c in page_chunks]
        idx+=len(page_chunks)
        is_inserted = await nlp_controller.index_into_vector_db(
            project=project,
            processed_chunks=page_chunks,
            chunks_ids=chunks_ids
            )
        
        if not is_inserted:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={
                    "signal": ResponseSignals.PROJECT_INDEX_FAIL.value
                    },
            )
        inserted_items_count += len(page_chunks)
        pbar.update(inserted_items_count)
        return JSONResponse(
                content={
                "signal": ResponseSignals.PROJECT_INDEX_SUCCESS.value,
                "inserted_items_count": inserted_items_count,
            },
        )
    
        
@nlp_router.get("/index/info/{project_id}")
async def get_index_project_info(request: Request,project_id: int):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)


    # Check if the project exists in the database
    project = await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller = NlpController(
        vector_db_client=request.app.vector_db_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client,
        template_parser=request.app.template_parser
    )

    collection_info = await nlp_controller.get_vector_db_collection_info(
        project=project,
    )
    return JSONResponse(
        content={
            "signal": ResponseSignals.PROJECT_INDEX_INFO_SUCCESS.value,
            "collection_info": collection_info,
            },
        )
@nlp_router.post("/index/search/{project_id}")
async def search_index(request: Request,project_id: int,search_request: SearchRequest):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)


    # Check if the project exists in the database
    project = await project_model.get_project_or_create_one(project_id=project_id)

    nlp_controller = NlpController(
        vector_db_client=request.app.vector_db_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client,
        template_parser=request.app.template_parser
    )
    search_results = await nlp_controller.search_vector_db_collection(
        project=project,
        text=search_request.text,
        limit=search_request.limit
    )
    
    if search_results:
        return JSONResponse(
            content={
                "signal": ResponseSignals.VECTOR_DB__SEARCH_SUCCESS.value,
                "search_Results": [
                    result.dict()
                    for result in search_results
                ]
                },
            )
    else:
        return JSONResponse(
            content={
                "signal": ResponseSignals.VECTOR_DB__SEARCH_ERROR.value,
                },
            )


@nlp_router.post("/index/answer/{project_id}")
async def search_index(request: Request,project_id: int,answer_request: AnswerRequest):

    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)


    # Check if the project exists in the database
    project = await project_model.get_project_or_create_one(project_id=project_id)
    nlp_controller = NlpController(
        vector_db_client=request.app.vector_db_client,
        embedding_client=request.app.embedding_client,
        generation_client=request.app.generation_client,
        template_parser=request.app.template_parser
    )

    answer,full_prompt,chat_history= await nlp_controller.answer_rag_questions(
        project=project,
        query=answer_request.query,
        limit=answer_request.limit
    )
    if answer and full_prompt and chat_history:
        return JSONResponse(
            content={
                "signal": ResponseSignals.GENERATION_SUCCESS.value,
                "answer": answer,
                "full_prompt": full_prompt,
                "chat_history": chat_history,
         
            },
        )
    else:
        return JSONResponse(
            content={
                "signal": ResponseSignals.GENERATION_ERROR.value,
                },
            )
    