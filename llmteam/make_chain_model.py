from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

def make_chain_llm(retriever,llm):
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    template = "\"```\" Below is an instruction that describes a task. Write a response that appropriately completes the request."\
    "제시하는 context에서만 대답하고 context에 없는 내용은 생성하지마"\
    "make answer in korean. 한국어로 대답하세요"\
    "\n\nContext:\n{context}\n;"\
    "Question: {question}"\
    "\n\nAnswer:"

    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = (
    {"context": retriever| format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
    )

    return rag_chain
