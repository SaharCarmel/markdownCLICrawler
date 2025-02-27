Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
important
This section will cover building with the legacy LangChain AgentExecutor. These are fine for getting started, but past a certain point, you will likely want flexibility and control that they do not offer. For working with more advanced agents, we'd recommend checking out LangGraph Agents or the migration guide
By themselves, language models can't take actions - they just output text. A big use case for LangChain is creating **agents**. Agents are systems that use an LLM as a reasoning engine to determine which actions to take and what the inputs to those actions should be. The results of those actions can then be fed back into the agent and it determines whether more actions are needed, or whether it is okay to finish.
In this tutorial, we will build an agent that can interact with multiple different tools: one being a local database, the other being a search engine. You will be able to ask this agent questions, watch it call tools, and have conversations with it.
## Concepts​
Concepts we will cover are:
  * Using language models, in particular their tool calling ability
  * Creating a Retriever to expose specific information to our agent
  * Using a Search Tool to look up things online
  * `Chat History`, which allows a chatbot to "remember" past interactions and take them into account when responding to follow-up questions.
  * Debugging and tracing your application using LangSmith


## Setup​
### Jupyter Notebook​
This guide (and most of the other guides in the documentation) uses Jupyter notebooks and assumes the reader is as well. Jupyter notebooks are perfect for learning how to work with LLM systems because oftentimes things can go wrong (unexpected output, API down, etc) and going through guides in an interactive environment is a great way to better understand them.
This and other tutorials are perhaps most conveniently run in a Jupyter notebook. See here for instructions on how to install.
### Installation​
To install LangChain run:
  * Pip
  * Conda


```
pip install langchain
```

```
conda install langchain -c conda-forge
```

For more details, see our Installation guide.
### LangSmith​
Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls. As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent. The best way to do this is with LangSmith.
After you sign up at the link above, make sure to set your environment variables to start logging traces:
```
export LANGSMITH_TRACING="true"export LANGSMITH_API_KEY="..."
```

Or, if in a notebook, you can set them with:
```
import getpassimport osos.environ["LANGSMITH_TRACING"]="true"os.environ["LANGSMITH_API_KEY"]= getpass.getpass()
```

## Define tools​
We first need to create the tools we want to use. We will use two tools: Tavily (to search online) and then a retriever over a local index we will create
### Tavily​
We have a built-in tool in LangChain to easily use Tavily search engine as tool. Note that this requires an API key - they have a free tier, but if you don't have one or don't want to create one, you can always ignore this step.
Once you create your API key, you will need to export that as:
```
export TAVILY_API_KEY="..."
```

```
from langchain_community.tools.tavily_search import TavilySearchResults
```

**API Reference:**TavilySearchResults
```
search = TavilySearchResults(max_results=2)
```

```
search.invoke("what is the weather in SF")
```

```
[{'url': 'https://www.weatherapi.com/', 'content': "{'location': {'name': 'San Francisco', 'region': 'California', 'country': 'United States of America', 'lat': 37.78, 'lon': -122.42, 'tz_id': 'America/Los_Angeles', 'localtime_epoch': 1714000492, 'localtime': '2024-04-24 16:14'}, 'current': {'last_updated_epoch': 1713999600, 'last_updated': '2024-04-24 16:00', 'temp_c': 15.6, 'temp_f': 60.1, 'is_day': 1, 'condition': {'text': 'Overcast', 'icon': '//cdn.weatherapi.com/weather/64x64/day/122.png', 'code': 1009}, 'wind_mph': 10.5, 'wind_kph': 16.9, 'wind_degree': 330, 'wind_dir': 'NNW', 'pressure_mb': 1018.0, 'pressure_in': 30.06, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 72, 'cloud': 100, 'feelslike_c': 15.6, 'feelslike_f': 60.1, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 5.0, 'gust_mph': 14.8, 'gust_kph': 23.8}}"}, {'url': 'https://www.weathertab.com/en/c/e/04/united-states/california/san-francisco/', 'content': 'San Francisco Weather Forecast for Apr 2024 - Risk of Rain Graph. Rain Risk Graph: Monthly Overview. Bar heights indicate rain risk percentages. Yellow bars mark low-risk days, while black and grey bars signal higher risks. Grey-yellow bars act as buffers, advising to keep at least one day clear from the riskier grey and black days, guiding ...'}]
```

### Retriever​
We will also create a retriever over some data of our own. For a deeper explanation of each step here, see this tutorial.
```
from langchain_community.document_loaders import WebBaseLoaderfrom langchain_community.vectorstores import FAISSfrom langchain_openai import OpenAIEmbeddingsfrom langchain_text_splitters import RecursiveCharacterTextSplitterloader = WebBaseLoader("https://docs.smith.langchain.com/overview")docs = loader.load()documents = RecursiveCharacterTextSplitter(  chunk_size=1000, chunk_overlap=200).split_documents(docs)vector = FAISS.from_documents(documents, OpenAIEmbeddings())retriever = vector.as_retriever()
```

**API Reference:**WebBaseLoader | FAISS | OpenAIEmbeddings | RecursiveCharacterTextSplitter
```
retriever.invoke("how to upload a dataset")[0]
```

```
Document(page_content='# The data to predict and grade over  evaluators=[exact_match], # The evaluators to score the results  experiment_prefix="sample-experiment", # The name of the experiment  metadata={   "version": "1.0.0",   "revision_id": "beta"  },)import { Client, Run, Example } from \'langsmith\';import { runOnDataset } from \'langchain/smith\';import { EvaluationResult } from \'langsmith/evaluation\';const client = new Client();// Define dataset: these are your test casesconst datasetName = "Sample Dataset";const dataset = await client.createDataset(datasetName, {  description: "A sample dataset in LangSmith."});await client.createExamples({  inputs: [    { postfix: "to LangSmith" },    { postfix: "to Evaluations in LangSmith" },  ],  outputs: [    { output: "Welcome to LangSmith" },    { output: "Welcome to Evaluations in LangSmith" },  ],  datasetId: dataset.id,});// Define your evaluatorconst exactMatch = async ({ run, example }: { run: Run; example?:', metadata={'source': 'https://docs.smith.langchain.com/overview', 'title': 'Getting started with LangSmith | \uf8ffü¶úÔ∏è\uf8ffüõ†Ô∏è LangSmith', 'description': 'Introduction', 'language': 'en'})
```

Now that we have populated our index that we will do doing retrieval over, we can easily turn it into a tool (the format needed for an agent to properly use it)
```
from langchain.tools.retriever import create_retriever_tool
```

**API Reference:**create_retriever_tool
```
retriever_tool = create_retriever_tool(  retriever,"langsmith_search","Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",)
```

### Tools​
Now that we have created both, we can create a list of tools that we will use downstream.
```
tools =[search, retriever_tool]
```

## Using Language Models​
Next, let's learn how to use a language model by to call tools. LangChain supports many different language models that you can use interchangably - select the one you want to use below!
Select chat model:
Groq▾
* Groq
* OpenAI
* Anthropic
* Azure
* Google Vertex
* AWS
* Cohere
* NVIDIA
* Fireworks AI
* Mistral AI
* Together AI
* IBM watsonx
* Databricks
```
pip install -qU "langchain[groq]"
```

```
import getpassimport osifnot os.environ.get("GROQ_API_KEY"): os.environ["GROQ_API_KEY"]= getpass.getpass("Enter API key for Groq: ")from langchain.chat_models import init_chat_modelmodel = init_chat_model("llama3-8b-8192", model_provider="groq")
```

You can call the language model by passing in a list of messages. By default, the response is a `content` string.
```
from langchain_core.messages import HumanMessageresponse = model.invoke([HumanMessage(content="hi!")])response.content
```

**API Reference:**HumanMessage
```
'Hello! How can I assist you today?'
```

We can now see what it is like to enable this model to do tool calling. In order to enable that we use `.bind_tools` to give the language model knowledge of these tools
```
model_with_tools = model.bind_tools(tools)
```

We can now call the model. Let's first call it with a normal message, and see how it responds. We can look at both the `content` field as well as the `tool_calls` field.
```
response = model_with_tools.invoke([HumanMessage(content="Hi!")])print(f"ContentString: {response.content}")print(f"ToolCalls: {response.tool_calls}")
```

```
ContentString: Hello! How can I assist you today?ToolCalls: []
```

Now, let's try calling it with some input that would expect a tool to be called.
```
response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])print(f"ContentString: {response.content}")print(f"ToolCalls: {response.tool_calls}")
```

```
ContentString: ToolCalls: [{'name': 'tavily_search_results_json', 'args': {'query': 'current weather in San Francisco'}, 'id': 'call_4HteVahXkRAkWjp6dGXryKZX'}]
```

We can see that there's now no content, but there is a tool call! It wants us to call the Tavily Search tool.
This isn't calling that tool yet - it's just telling us to. In order to actually calll it, we'll want to create our agent.
## Create the agent​
Now that we have defined the tools and the LLM, we can create the agent. We will be using a tool calling agent - for more information on this type of agent, as well as other options, see this guide.
We can first choose the prompt we want to use to guide the agent.
If you want to see the contents of this prompt and have access to LangSmith, you can go to:
https://smith.langchain.com/hub/hwchase17/openai-functions-agent
```
from langchain import hub# Get the prompt to use - you can modify this!prompt = hub.pull("hwchase17/openai-functions-agent")prompt.messages
```

**API Reference:**hub
```
[SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template='You are a helpful assistant')), MessagesPlaceholder(variable_name='chat_history', optional=True), HumanMessagePromptTemplate(prompt=PromptTemplate(input_variables=['input'], template='{input}')), MessagesPlaceholder(variable_name='agent_scratchpad')]
```

Now, we can initialize the agent with the LLM, the prompt, and the tools. The agent is responsible for taking in input and deciding what actions to take. Crucially, the Agent does not execute those actions - that is done by the AgentExecutor (next step). For more information about how to think about these components, see our conceptual guide.
Note that we are passing in the `model`, not `model_with_tools`. That is because `create_tool_calling_agent` will call `.bind_tools` for us under the hood.
```
from langchain.agents import create_tool_calling_agentagent = create_tool_calling_agent(model, tools, prompt)
```

**API Reference:**create_tool_calling_agent
Finally, we combine the agent (the brains) with the tools inside the AgentExecutor (which will repeatedly call the agent and execute tools).
```
from langchain.agents import AgentExecutoragent_executor = AgentExecutor(agent=agent, tools=tools)
```

**API Reference:**AgentExecutor
## Run the agent​
We can now run the agent on a few queries! Note that for now, these are all **stateless** queries (it won't remember previous interactions).
First up, let's how it responds when there's no need to call a tool:
```
agent_executor.invoke({"input":"hi!"})
```

```
{'input': 'hi!', 'output': 'Hello! How can I assist you today?'}
```

In order to see exactly what is happening under the hood (and to make sure it's not calling a tool) we can take a look at the LangSmith trace
Let's now try it out on an example where it should be invoking the retriever
```
agent_executor.invoke({"input":"how can langsmith help with testing?"})
```

```
{'input': 'how can langsmith help with testing?', 'output': 'LangSmith is a platform that aids in building production-grade Language Learning Model (LLM) applications. It can assist with testing in several ways:\n\n1. **Monitoring and Evaluation**: LangSmith allows close monitoring and evaluation of your application. This helps you to ensure the quality of your application and deploy it with confidence.\n\n2. **Tracing**: LangSmith has tracing capabilities that can be beneficial for debugging and understanding the behavior of your application.\n\n3. **Evaluation Capabilities**: LangSmith has built-in tools for evaluating the performance of your LLM. \n\n4. **Prompt Hub**: This is a prompt management tool built into LangSmith that can help in testing different prompts and their responses.\n\nPlease note that to use LangSmith, you would need to install it and create an API key. The platform offers Python and Typescript SDKs for utilization. It works independently and does not require the use of LangChain.'}
```

Let's take a look at the LangSmith trace to make sure it's actually calling that.
Now let's try one where it needs to call the search tool:
```
agent_executor.invoke({"input":"whats the weather in sf?"})
```

```
{'input': 'whats the weather in sf?', 'output': 'The current weather in San Francisco is partly cloudy with a temperature of 16.1°C (61.0°F). The wind is coming from the WNW at a speed of 10.5 mph. The humidity is at 67%. [source](https://www.weatherapi.com/)'}
```

We can check out the LangSmith trace to make sure it's calling the search tool effectively.
## Adding in memory​
As mentioned earlier, this agent is stateless. This means it does not remember previous interactions. To give it memory we need to pass in previous `chat_history`. Note: it needs to be called `chat_history` because of the prompt we are using. If we use a different prompt, we could change the variable name
```
# Here we pass in an empty list of messages for chat_history because it is the first message in the chatagent_executor.invoke({"input":"hi! my name is bob","chat_history":[]})
```

```
{'input': 'hi! my name is bob', 'chat_history': [], 'output': 'Hello Bob! How can I assist you today?'}
```

```
from langchain_core.messages import AIMessage, HumanMessage
```

**API Reference:**AIMessage | HumanMessage
```
agent_executor.invoke({"chat_history":[      HumanMessage(content="hi! my name is bob"),      AIMessage(content="Hello Bob! How can I assist you today?"),],"input":"what's my name?",})
```

```
{'chat_history': [HumanMessage(content='hi! my name is bob'), AIMessage(content='Hello Bob! How can I assist you today?')], 'input': "what's my name?", 'output': 'Your name is Bob. How can I assist you further?'}
```

If we want to keep track of these messages automatically, we can wrap this in a RunnableWithMessageHistory. For more information on how to use this, see this guide.
```
from langchain_community.chat_message_histories import ChatMessageHistoryfrom langchain_core.chat_history import BaseChatMessageHistoryfrom langchain_core.runnables.history import RunnableWithMessageHistorystore ={}defget_session_history(session_id:str)-> BaseChatMessageHistory:if session_id notin store:    store[session_id]= ChatMessageHistory()return store[session_id]
```

**API Reference:**ChatMessageHistory | BaseChatMessageHistory | RunnableWithMessageHistory
Because we have multiple inputs, we need to specify two things:
  * `input_messages_key`: The input key to use to add to the conversation history.
  * `history_messages_key`: The key to add the loaded messages into.


```
agent_with_chat_history = RunnableWithMessageHistory(  agent_executor,  get_session_history,  input_messages_key="input",  history_messages_key="chat_history",)
```

```
agent_with_chat_history.invoke({"input":"hi! I'm bob"},  config={"configurable":{"session_id":"<foo>"}},)
```

```
{'input': "hi! I'm bob", 'chat_history': [], 'output': 'Hello Bob! How can I assist you today?'}
```

```
agent_with_chat_history.invoke({"input":"what's my name?"},  config={"configurable":{"session_id":"<foo>"}},)
```

```
{'input': "what's my name?", 'chat_history': [HumanMessage(content="hi! I'm bob"), AIMessage(content='Hello Bob! How can I assist you today?')], 'output': 'Your name is Bob.'}
```

Example LangSmith trace: https://smith.langchain.com/public/98c8d162-60ae-4493-aa9f-992d87bd0429/r
## Conclusion​
That's a wrap! In this quick start we covered how to create a simple agent. Agents are a complex topic, and there's lot to learn!
important
This section covered building with LangChain Agents. They are fine for getting started, but past a certain point you will likely want flexibility and control which they do not offer. To develop more advanced agents, we recommend checking out LangGraph
If you want to continue using LangChain agents, some good advanced guides are:
  * How to use LangGraph's built-in versions of `AgentExecutor`
  * How to create a custom agent
  * How to stream responses from an agent
  * How to return structured output from an agent


#### Was this page helpful?
  * Concepts
  * Setup
    * Jupyter Notebook
    * Installation
    * LangSmith
  * Define tools
    * Tavily
    * Retriever
    * Tools
  * Using Language Models
  * Create the agent
  * Run the agent
  * Adding in memory
  * Conclusion


