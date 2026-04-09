from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()


embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")


vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_rag",
    embedding=embedding_model,
)

# take the user input
user_query = input("Ask something --> ")

# perform similarity search - get relevant chunks from vector db.
search_results = vector_db.similarity_search(query=user_query)

context = "\n\n".join(
    [
        f"Page Content: {result.page_content}\nPage Number: {result.metadata['page_label']}\nFile Location: {result.metadata['source']}"
        for result in search_results
    ]
)

system_prompt = f"""
You are an helpful AI assistant who answers user query based on the available context retrieved from a PDF along with page contents and page number.

You should only answer the user based on the following context and navigate the user to open the right number to know more.

Context: 
 {context}
"""


client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ],
)

print(f"RESPONSE --> {response.choices[0].message.content}")
