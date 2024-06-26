# main.py에 붙여넣을 부분

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from load_model_type_a import load_Auto
from llmteam.load_push import all_files
from llmteam.retriever import *
from llmteam.retrieve_docs import *
from llmteam.make_chain_model import make_chain_llm
from llmteam.make_answer import *

app = FastAPI()
llm = load_Auto()
pinecone,bm25 = all_files('files')
retriever=retriever(pinecone,bm25)
rag_chain = make_chain_llm(retriever,llm)

# 요청 바디
class QueryRequest(BaseModel):
    query: str


# 응답 바디
class QueryResponse(BaseModel):
    response: str


@app.post("/query", response_model=QueryResponse)
async def get_query_response(query_request: QueryRequest):
    try:
        # 쿼리 텍스트를 받아서 LLM 모델에 전달
        query_text = query_request.query
        response_text = rag_chain.invoke(query_text)
        return QueryResponse(response=response_text.split('\\nAnswer')[:-1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

