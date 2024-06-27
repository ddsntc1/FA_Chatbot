# main.py에 붙여넣을 부분

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from load_model_type_a import load_Auto
from llmteam.load_push import all_files
from llmteam.retriever import *
from llmteam.retrieve_docs import *
from llmteam.make_chain_model import make_chain_llm
from llmteam.make_answer import *
from transformers import TextStreamer

app = FastAPI()
model,tokenizer = load_Auto()
pinecone,bm25 = all_files('files')
retriever=retriever(pinecone,bm25)
# rag_chain = make_chain_llm(retriever,llm)

# 요청 바디
class QueryRequest(BaseModel):
    query: str


# 응답 바디
class QueryResponse(BaseModel):
    response: str

def invokes(text):
  PROMPT = '''Below is an instruction that describes a task. Write a response that appropriately completes the request.
  제시하는 context에서만 대답하고 context에 없는 내용은 모르겠다고 대답해. 모르는 답변을 임의로 생성하지마.
  '''
  instruction = text

  Context = search_results(retriever,instruction)


  messages = [
      {"role": "system", "content": f"{PROMPT}"},
      {'role': 'assistant','content':f"{Context}"},
      {"role": "user", "content": f"{instruction}"}
      ]

  input_ids = tokenizer.apply_chat_template(
      messages,
      add_generation_prompt=True,
      return_tensors="pt"
  ).to(model.device)

  terminators = [
      tokenizer.eos_token_id,
      tokenizer.convert_tokens_to_ids("<|eot_id|>")
  ]

  text_streamer = TextStreamer(tokenizer)
  out = model.generate(
      input_ids,
      max_new_tokens=4096,
      eos_token_id=terminators,
      do_sample=True,
      streamer = text_streamer,
      temperature=0.7,
      top_p=0.9,
      repetition_penalty = 1
  )
  return out



@app.post("/query", response_model=QueryResponse)
async def get_query_response(query_request: QueryRequest):
    try:
        # 쿼리 텍스트를 받아서 LLM 모델에 전달
        query_text = query_request.query
        response_text = invokes(query_text)
        return QueryResponse(response=response_text.split('\\nAnswer')[:-1])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

