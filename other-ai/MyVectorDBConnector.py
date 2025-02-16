from TextToEmbeddings import get_embeddings
import chromadb
from chromadb.config import Settings
import shortuuid
from MyLogger import logger
import sys
class MyVectorDBConnector:
    def __init__(self,collection_name,embedding_fn):
        #内存模式
        # chroma_client = chromadb.Client(Settings(allow_reset=True))
        #数据持久化
        chroma_client = chromadb.PersistentClient(path="./chroma_db",settings=Settings(allow_reset=True))
        # 清空数据库
        #chroma_client.reset()
        self.collection = chroma_client.get_or_create_collection(name=collection_name)
        self.embedding_fn = embedding_fn
    def add_documents(self,documents,bizCode="ALL"):
        ''' 向 collection 中添加 documents '''
        embeddings = self.embedding_fn(documents)
        #print(embeddings)
        #ids = [f"id{i}" for i in range(len(documents))]
        #print(ids)
        ids = [shortuuid.uuid() for i in range(len(documents))]
        metadatas = [{"len": len(doc),"bizCode":bizCode} for doc in documents]
        self.collection.add(
            documents=documents,
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )
        logger.debug(f"VectorDB add_documents length: {len(documents)}")
    def search(self,query,top_n,where=None):
        #where={"len": {"$gt": min_length}}  # 过滤条件：长度大于 min_length
        ''' 检索向量数据库 '''
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n,
            where=where
        ) 
        logger.debug(f"VectorDB search text >>>>>>>>>: {query} \n VectorDB search results >>>>>>>>>>>>>>: \n{results}\n<<<<<<<<<<<<<<<<<<<")  
        return results
    def get_all_items(self):
        all_items = self.collection.get(include=['metadatas', 'documents'])
        logger.debug(f"get_all_items from chromadb >>>>>>>>>>")
        logger.debug(all_items)
        logger.debug("<<<<<<<<<<<<<<<<<<<")
        return all_items
    def delete_by_ids(self,ids):
        self.collection.delete(ids=ids)
        logger.debug(f"VectorDB delete_documents with ids: {ids}")

    def clear_collection(self):
        # where条件指定删除id不等于a的文档，因为没有文档id是a，所以表示全部删除collection中的文档，清空collection
        self.collection.delete(where={"id": {"$ne": "a"}})
        logger.debug("VectorDB collection cleared")


if __name__ == "__main__":
    # paragraphs1 = extract_text_from_pdf("docs/WhatisChatGPT.pdf",min_line_length=10)
    # paragraphs1 = extract_text_from_pdf("docs/财务业务中台项目概况.pdf",min_line_length=10)
    # paragraphs1 = extract_text_from_pdf("docs/财务中台微服务开发规范V1.2.pdf",min_line_length=10)
    vector_db = MyVectorDBConnector("rag_demo",get_embeddings)
    #vector_db.clear_collection()
    # vector_db.add_documents(paragraphs1)
    #user_query = "Llama 2有多少个参数"
    #user_query = "what is the Advantages and disadvantages of chatgpt"
    #user_query = "目录名最大多少位"
    user_query = "财务中台建设过程有哪些"
    vector_db.get_all_items()
    #vector_db.delete_by_ids(['id0', 'id1'])
    #sys.exit()
    #where={"len": {"$gt": 100},"bizCode":{"$eq":"CWZT"}}
    # 使用多个条件进行搜索
    where = {
        "$and": [
            {"len": {"$gt": 100}},
            {"bizCode": {"$eq": "CWZT"}}
        ]
    }
    results = vector_db.search(user_query,2,where)

    # for para in results['documents'][0]:
    #     print(para,"\n")