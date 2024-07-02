import os
from dotenv import load_dotenv
from langchain.retrievers import BM25Retriever, EnsembleRetriever
from kiwipiepy import Kiwi
load_dotenv()

kiwi = Kiwi()

def kiwi_tokenize(text):
    return [token.form for token in kiwi.tokenize(text)]
 

def retriever(pc, bm25):
    pcretriever = pc.as_retriever(search_kwargs={'k':4})
    kiwi_bm25 = BM25Retriever.from_documents(bm25,preprocess_func=kiwi_tokenize)
    kiwi_bm25.k=4
    
    kiwibm25_pc_37 = EnsembleRetriever(
        retrievers=[kiwi_bm25, pcretriever], 
        weights=[0.3, 0.7],  
        search_type="mmr", 
    ) 
    return kiwibm25_pc_37

