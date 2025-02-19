'''
pip install langchain-community pypdf
pip install -qU langchain-chroma

'''

import lang_smith_config
import os
from langchain_core.documents import Document

current_dir=os.path.dirname(os.path.abspath(__file__))
print("Current working directory:", current_dir)

# documents = [
#     Document(
#         page_content=" Dogs are great compnions, known for their loyalty and friendliness.",
#         metadata={"source","pets-doc"}
#     ),
#     Document(
#         page_content="Cats are independent pets that often enjoy their own space.",
#         metadata={"source","pets-doc"}
#     )
# ]


# from langchain_community.document_loaders import PyPDFLoader
# file_path=os.path.join(current_dir,"WhatisChatGPT.pdf")
# print(f"file_path: {file_path}")
# if not os.path.exists(file_path):
#     print(f"File {file_path} not found")
#     exit()
# else:
#     print(f"File {file_path} exists")

# loader = PyPDFLoader(file_path)
# docs = loader.load()
# print(len(docs))
# print(docs[0].metadata)

# from langchain_text_splitters import RecursiveCharacterTextSplitter
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=100,chunk_overlap=20,add_start_index=True)
# all_splits = text_splitter.split_documents(docs)
# print(len(all_splits))


from langchain_openai import OpenAIEmbeddings
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# vector1=embeddings.embed_query(all_splits[0].page_content)
# vector2=embeddings.embed_query(all_splits[1].page_content)
# assert len(vector1) == len(vector2)
# print(f"Generated vectors of length, vector1: {len(vector1)}\n")


from langchain_chroma import Chroma
from chromadb.config import Settings
v_store = Chroma(collection_name="learn-langchain",
                 embedding_function=embeddings,
                 client_settings=Settings(is_persistent=True),
                 persist_directory="./learn_langchain_chroma_db")


# ids = v_store.add_documents(documents=all_splits)
# print(ids)



results=v_store.similarity_search("what is the strength of ChatGPT")
print(results)

async def async_search():
    results = await v_store.asimilarity_search("what is the strength of ChatGPT")
    print(results)