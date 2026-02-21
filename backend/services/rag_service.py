from io import BytesIO
from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_experimental.text_splitter import SemanticChunker
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from typing import List

from core.config import settings
from services.qdrant_service import qdrant_service


class QdrantRetriever(BaseRetriever):
    """A custom retriever that uses the new qdrant-client query_points API."""

    collection_name: str
    embeddings: OpenAIEmbeddings
    k: int = 5

    def _get_relevant_documents(self, query: str) -> List[Document]:
        query_vector = self.embeddings.embed_query(query)
        results = qdrant_service.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=self.k,
        )
        docs = []
        for point in results.points:
            page_content = point.payload.get("page_content", "")
            metadata = point.payload.get("metadata", {})
            docs.append(Document(page_content=page_content, metadata=metadata))
        return docs


class RagService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        self.llm = ChatOpenAI(
            api_key=settings.OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0
        )

    def extract_text_from_pdf_bytes(self, pdf_bytes: bytes) -> str:
        """Extract text from uploaded PDF bytes."""
        reader = PdfReader(BytesIO(pdf_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)

    def chunk_text(self, text: str) -> list[str]:
        """Split text into semantic chunks."""
        splitter = SemanticChunker(
            embeddings=self.embeddings,
            breakpoint_threshold_type=settings.CHUNK_BREAKPOINT_THRESHOLD_TYPE,
        )
        documents = splitter.create_documents([text])

        chunks = []
        for doc in documents:
            content = doc.page_content.strip()
            if len(content) < settings.CHUNK_MIN_SIZE:
                continue
            if len(content) > settings.CHUNK_MAX_SIZE:
                for i in range(0, len(content), settings.CHUNK_MAX_SIZE):
                    sub = content[i : i + settings.CHUNK_MAX_SIZE].strip()
                    if len(sub) >= settings.CHUNK_MIN_SIZE:
                        chunks.append(sub)
            else:
                chunks.append(content)

        return chunks

    def process_document(
        self, collection_name: str, document_name: str, pdf_bytes: bytes
    ):
        """Extract, chunk, embed and insert PDF."""
        # 1. Extract
        text = self.extract_text_from_pdf_bytes(pdf_bytes)
        if not text.strip():
            raise ValueError(f"No text extracted from {document_name}")

        # 2. Chunk
        chunks = self.chunk_text(text)
        if not chunks:
            raise ValueError(f"No valid chunks for {document_name}")

        # 3. Clean existing document data logic is handled in the route
        # 4. Embed
        vectors = self.embeddings.embed_documents(chunks)

        # 5. Insert
        num_inserted = qdrant_service.upsert_vectors(
            collection_name, chunks, vectors, document_name
        )
        return num_inserted

    def get_answer(self, collection_name: str, query: str):
        """Retrieve context from Qdrant and generate answer using LangChain."""
        retriever = QdrantRetriever(
            collection_name=collection_name,
            embeddings=self.embeddings,
            k=5,
        )

        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Use three sentences maximum and keep the answer concise."
            "\n\n"
            "{context}"
        )
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)

        response = rag_chain.invoke({"input": query})
        return {
            "answer": response["answer"],
            "context": [doc.page_content for doc in response["context"]],
        }


rag_service = RagService()
