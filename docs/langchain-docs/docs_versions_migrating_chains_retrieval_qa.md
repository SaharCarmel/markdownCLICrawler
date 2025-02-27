Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
The `RetrievalQA` chain performed natural-language question answering over a data source using retrieval-augmented generation.
Some advantages of switching to the LCEL implementation are:
  * Easier customizability. Details such as the prompt and how documents are formatted are only configurable via specific parameters in the `RetrievalQA` chain.
  * More easily return source documents.
  * Support for runnable methods like streaming and async operations.


Now let's look at them side-by-side. We'll use the following ingestion code to load a blog post by Lilian Weng on autonomous agents into a local vector store:
## Shared setup​
For both versions, we'll need to load the data with the `WebBaseLoader` document loader, split it with `RecursiveCharacterTextSplitter`, and add it to an in-memory `FAISS` vector store.
We will also instantiate a chat model to use.
```
%pip install --upgrade --quiet langchain-community langchain langchain-openai faiss-cpu beautifulsoup4
```

```
import osfrom getpass import getpassif"OPENAI_API_KEY"notin os.environ:  os.environ["OPENAI_API_KEY"]= getpass()
```

```
# Load docsfrom langchain_community.document_loaders import WebBaseLoaderfrom langchain_community.vectorstores import FAISSfrom langchain_openai.chat_models import ChatOpenAIfrom langchain_openai.embeddings import OpenAIEmbeddingsfrom langchain_text_splitters import RecursiveCharacterTextSplitterloader = WebBaseLoader("https://lilianweng.github.io/posts/2023-06-23-agent/")data = loader.load()# Splittext_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)all_splits = text_splitter.split_documents(data)# Store splitsvectorstore = FAISS.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())# LLMllm = ChatOpenAI()
```

**API Reference:**WebBaseLoader | FAISS | ChatOpenAI | OpenAIEmbeddings | RecursiveCharacterTextSplitter
## Legacy​
Details
```
from langchain import hubfrom langchain.chains import RetrievalQA# See full prompt at https://smith.langchain.com/hub/rlm/rag-promptprompt = hub.pull("rlm/rag-prompt")qa_chain = RetrievalQA.from_llm(  llm, retriever=vectorstore.as_retriever(), prompt=prompt)qa_chain("What are autonomous agents?")
```

**API Reference:**hub | RetrievalQA
```
{'query': 'What are autonomous agents?', 'result': 'Autonomous agents are LLM-empowered agents capable of handling autonomous design, planning, and performance of complex scientific experiments. These agents can browse the Internet, read documentation, execute code, call robotics experimentation APIs, and leverage other LLMs. They can generate reasoning steps, such as developing a novel anticancer drug, based on requested tasks.'}
```

## LCEL​
Details
```
from langchain import hubfrom langchain_core.output_parsers import StrOutputParserfrom langchain_core.runnables import RunnablePassthrough# See full prompt at https://smith.langchain.com/hub/rlm/rag-promptprompt = hub.pull("rlm/rag-prompt")defformat_docs(docs):return"\n\n".join(doc.page_content for doc in docs)qa_chain =({"context": vectorstore.as_retriever()| format_docs,"question": RunnablePassthrough(),}| prompt| llm| StrOutputParser())qa_chain.invoke("What are autonomous agents?")
```

**API Reference:**hub | StrOutputParser | RunnablePassthrough
```
'Autonomous agents are agents empowered by large language models (LLMs) that can handle autonomous design, planning, and performance of complex tasks such as scientific experiments. These agents can use tools to browse the Internet, read documentation, execute code, call robotics experimentation APIs, and leverage other LLMs for their tasks. The model can come up with reasoning steps when given a specific task, such as developing a novel anticancer drug.'
```

The LCEL implementation exposes the internals of what's happening around retrieving, formatting documents, and passing them through a prompt to the LLM, but it is more verbose. You can customize and wrap this composition logic in a helper function, or use the higher-level `create_retrieval_chain` and `create_stuff_documents_chain` helper method:
```
from langchain import hubfrom langchain.chains import create_retrieval_chainfrom langchain.chains.combine_documents import create_stuff_documents_chain# See full prompt at https://smith.langchain.com/hub/langchain-ai/retrieval-qa-chatretrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")combine_docs_chain = create_stuff_documents_chain(llm, retrieval_qa_chat_prompt)rag_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain)rag_chain.invoke({"input":"What are autonomous agents?"})
```

**API Reference:**hub | create_retrieval_chain | create_stuff_documents_chain
```
{'input': 'What are autonomous agents?', 'context': [Document(metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'title': "LLM Powered Autonomous Agents | Lil'Log", 'description': 'Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as AutoGPT, GPT-Engineer and BabyAGI, serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.\nAgent System Overview In a LLM-powered autonomous agent system, LLM functions as the agent’s brain, complemented by several key components:', 'language': 'en'}, page_content='Boiko et al. (2023) also looked into LLM-empowered agents for scientific discovery, to handle autonomous design, planning, and performance of complex scientific experiments. This agent can use tools to browse the Internet, read documentation, execute code, call robotics experimentation APIs and leverage other LLMs.\nFor example, when requested to "develop a novel anticancer drug", the model came up with the following reasoning steps:'), Document(metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'title': "LLM Powered Autonomous Agents | Lil'Log", 'description': 'Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as AutoGPT, GPT-Engineer and BabyAGI, serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.\nAgent System Overview In a LLM-powered autonomous agent system, LLM functions as the agent’s brain, complemented by several key components:', 'language': 'en'}, page_content='Weng, Lilian. (Jun 2023). “LLM-powered Autonomous Agents”. Lil’Log. https://lilianweng.github.io/posts/2023-06-23-agent/.'), Document(metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'title': "LLM Powered Autonomous Agents | Lil'Log", 'description': 'Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as AutoGPT, GPT-Engineer and BabyAGI, serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.\nAgent System Overview In a LLM-powered autonomous agent system, LLM functions as the agent’s brain, complemented by several key components:', 'language': 'en'}, page_content='Fig. 1. Overview of a LLM-powered autonomous agent system.\nComponent One: Planning#\nA complicated task usually involves many steps. An agent needs to know what they are and plan ahead.\nTask Decomposition#'), Document(metadata={'source': 'https://lilianweng.github.io/posts/2023-06-23-agent/', 'title': "LLM Powered Autonomous Agents | Lil'Log", 'description': 'Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as AutoGPT, GPT-Engineer and BabyAGI, serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.\nAgent System Overview In a LLM-powered autonomous agent system, LLM functions as the agent’s brain, complemented by several key components:', 'language': 'en'}, page_content='Or\n@article{weng2023agent,\n title  = "LLM-powered Autonomous Agents",\n author = "Weng, Lilian",\n journal = "lilianweng.github.io",\n year  = "2023",\n month  = "Jun",\n url   = "https://lilianweng.github.io/posts/2023-06-23-agent/"\n}\nReferences#\n[1] Wei et al. “Chain of thought prompting elicits reasoning in large language models.” NeurIPS 2022\n[2] Yao et al. “Tree of Thoughts: Dliberate Problem Solving with Large Language Models.” arXiv preprint arXiv:2305.10601 (2023).')], 'answer': 'Autonomous agents are entities capable of operating independently to perform tasks or make decisions without direct human intervention. In the context provided, autonomous agents empowered by Large Language Models (LLMs) are used for scientific discovery, including tasks like autonomous design, planning, and executing complex scientific experiments.'}
```

## Next steps​
Check out the LCEL conceptual docs for more background information on the LangChain expression language.
#### Was this page helpful?
  * Shared setup
  * Legacy
  * LCEL
  * Next steps


