Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
A vector store retriever is a retriever that uses a vector store to retrieve documents. It is a lightweight wrapper around the vector store class to make it conform to the retriever interface. It uses the search methods implemented by a vector store, like similarity search and MMR, to query the texts in the vector store.
In this guide we will cover:
  1. How to instantiate a retriever from a vectorstore;
  2. How to specify the search type for the retriever;
  3. How to specify additional search parameters, such as threshold scores and top-k.


## Creating a retriever from a vectorstore​
You can build a retriever from a vectorstore using its .as_retriever method. Let's walk through an example.
First we instantiate a vectorstore. We will use an in-memory FAISS vectorstore:
```
from langchain_community.document_loaders import TextLoaderfrom langchain_community.vectorstores import FAISSfrom langchain_openai import OpenAIEmbeddingsfrom langchain_text_splitters import CharacterTextSplitterloader = TextLoader("state_of_the_union.txt")documents = loader.load()text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)texts = text_splitter.split_documents(documents)embeddings = OpenAIEmbeddings()vectorstore = FAISS.from_documents(texts, embeddings)
```

**API Reference:**TextLoader | FAISS | OpenAIEmbeddings | CharacterTextSplitter
We can then instantiate a retriever:
```
retriever = vectorstore.as_retriever()
```

This creates a retriever (specifically a VectorStoreRetriever), which we can use in the usual way:
```
docs = retriever.invoke("what did the president say about ketanji brown jackson?")
```

## Maximum marginal relevance retrieval​
By default, the vector store retriever uses similarity search. If the underlying vector store supports maximum marginal relevance search, you can specify that as the search type.
This effectively specifies what method on the underlying vectorstore is used (e.g., `similarity_search`, `max_marginal_relevance_search`, etc.).
```
retriever = vectorstore.as_retriever(search_type="mmr")
```

```
docs = retriever.invoke("what did the president say about ketanji brown jackson?")
```

## Passing search parameters​
We can pass parameters to the underlying vectorstore's search methods using `search_kwargs`.
### Similarity score threshold retrieval​
For example, we can set a similarity score threshold and only return documents with a score above that threshold.
```
retriever = vectorstore.as_retriever(  search_type="similarity_score_threshold", search_kwargs={"score_threshold":0.5})
```

```
docs = retriever.invoke("what did the president say about ketanji brown jackson?")
```

### Specifying top k​
We can also limit the number of documents `k` returned by the retriever.
```
retriever = vectorstore.as_retriever(search_kwargs={"k":1})
```

```
docs = retriever.invoke("what did the president say about ketanji brown jackson?")len(docs)
```

```
1
```

#### Was this page helpful?
  * Creating a retriever from a vectorstore
  * Maximum marginal relevance retrieval
  * Passing search parameters
    * Similarity score threshold retrieval
    * Specifying top k


