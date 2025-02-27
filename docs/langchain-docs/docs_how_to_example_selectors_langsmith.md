Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
📚Prerequisites
  * Chat models
  * Few-shot-prompting
  * LangSmith


📦Compatibility
The code in this guide requires `langsmith>=0.1.101`, `langchain-core>=0.2.34`. Please ensure you have the correct packages installed.
LangSmith datasets have built-in support for similarity search, making them a great tool for building and querying few-shot examples.
In this guide we'll see how to use an indexed LangSmith dataset as a few-shot example selector.
## Setup​
Before getting started make sure you've created a LangSmith account and set your credentials:
```
import getpassimport osifnot os.environ.get("LANGSMITH_API_KEY"):  os.environ["LANGSMITH_API_KEY"]= getpass.getpass("Set LangSmith API key:\n\n")os.environ["LANGSMITH_TRACING"]="true"
```

```
Set LangSmith API key:········
```

We'll need to install the `langsmith` SDK. In this example we'll also make use of `langchain`, `langchain-openai`, and `langchain-benchmarks`:
```
%pip install -qU "langsmith>=0.1.101""langchain-core>=0.2.34" langchain langchain-openai langchain-benchmarks
```

Now we'll clone a public dataset and turn on indexing for the dataset. We can also turn on indexing via the LangSmith UI.
We'll clone the Multiverse math few shot example dataset.
This enables searching over the dataset and will make sure that anytime we update/add examples they are also indexed.
```
from langsmith import Client as LangSmithls_client = LangSmith()dataset_name ="multiverse-math-few-shot-examples-v2"dataset_public_url =("https://smith.langchain.com/public/620596ee-570b-4d2b-8c8f-f828adbe5242/d")ls_client.clone_public_dataset(dataset_public_url)dataset_id = ls_client.read_dataset(dataset_name=dataset_name).idls_client.index_dataset(dataset_id=dataset_id)
```

## Querying dataset​
Indexing can take a few seconds. Once the dataset is indexed, we can search for similar examples. Note that the input to the `similar_examples` method must have the same schema as the examples inputs. In this case our example inputs are a dictionary with a "question" key:
```
examples = ls_client.similar_examples({"question":"whats the negation of the negation of the negation of 3"},  limit=3,  dataset_id=dataset_id,)len(examples)
```

```
3
```

```
examples[0].inputs["question"]
```

```
'evaluate the negation of -100'
```

For this dataset, the outputs are the conversation that followed the question in OpenAI message format:
```
examples[0].outputs["conversation"]
```

```
[{'role': 'assistant', 'content': None, 'tool_calls': [{'id': 'toolu_01HTpq4cYNUac6F7omUc2Wz3',  'type': 'function',  'function': {'name': 'negate', 'arguments': '{"a": -100}'}}]}, {'role': 'tool', 'content': '-100.0', 'tool_call_id': 'toolu_01HTpq4cYNUac6F7omUc2Wz3'}, {'role': 'assistant', 'content': 'So the answer is 100.'}, {'role': 'user', 'content': '100 is incorrect. Please refer to the output of your tool call.'}, {'role': 'assistant', 'content': [{'text': "You're right, my previous answer was incorrect. Let me re-evaluate using the tool output:",  'type': 'text'}], 'tool_calls': [{'id': 'toolu_01XsJQboYghGDygQpPjJkeRq',  'type': 'function',  'function': {'name': 'negate', 'arguments': '{"a": -100}'}}]}, {'role': 'tool', 'content': '-100.0', 'tool_call_id': 'toolu_01XsJQboYghGDygQpPjJkeRq'}, {'role': 'assistant', 'content': 'The answer is -100.0'}, {'role': 'user', 'content': 'You have the correct numerical answer but are returning additional text. Please only respond with the numerical answer.'}, {'role': 'assistant', 'content': '-100.0'}]
```

## Creating dynamic few-shot prompts​
The search returns the examples whose inputs are most similar to the query input. We can use this for few-shot prompting a model like so:
```
from langchain.chat_models import init_chat_modelfrom langchain_benchmarks.tool_usage.tasks.multiverse_math import(  add,  cos,  divide,  log,  multiply,  negate,  pi,  power,  sin,  subtract,)from langchain_core.runnables import RunnableLambdafrom langsmith import AsyncClient as AsyncLangSmithasync_ls_client = AsyncLangSmith()defsimilar_examples(input_:dict)->dict:  examples = ls_client.similar_examples(input_, limit=5, dataset_id=dataset_id)return{**input_,"examples": examples}asyncdefasimilar_examples(input_:dict)->dict:  examples =await async_ls_client.similar_examples(    input_, limit=5, dataset_id=dataset_id)return{**input_,"examples": examples}defconstruct_prompt(input_:dict)->list:  instructions ="""You are great at using mathematical tools."""  examples =[]for ex in input_["examples"]:    examples.append({"role":"user","content": ex.inputs["question"]})for msg in ex.outputs["conversation"]:if msg["role"]=="assistant":        msg["name"]="example_assistant"if msg["role"]=="user":        msg["name"]="example_user"      examples.append(msg)return[{"role":"system","content": instructions},*examples,{"role":"user","content": input_["question"]},]tools =[add, cos, divide, log, multiply, negate, pi, power, sin, subtract]llm = init_chat_model("gpt-4o-2024-08-06")llm_with_tools = llm.bind_tools(tools)example_selector = RunnableLambda(func=similar_examples, afunc=asimilar_examples)chain = example_selector | construct_prompt | llm_with_tools
```

**API Reference:**init_chat_model | RunnableLambda
```
ai_msg =await chain.ainvoke({"question":"whats the negation of the negation of 3"})ai_msg.tool_calls
```

```
[{'name': 'negate', 'args': {'a': 3}, 'id': 'call_uMSdoTl6ehfHh5a6JQUb2NoZ', 'type': 'tool_call'}]
```

Looking at the LangSmith trace, we can see that relevant examples were pulled in in the `similar_examples` step and passed as messages to ChatOpenAI: https://smith.langchain.com/public/9585e30f-765a-4ed9-b964-2211420cd2f8/r/fdea98d6-e90f-49d4-ac22-dfd012e9e0d9.
#### Was this page helpful?
  * Setup
  * Querying dataset
  * Creating dynamic few-shot prompts


