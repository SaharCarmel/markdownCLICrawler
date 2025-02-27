Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
Prerequisites
This guide assumes familiarity with the following concepts:
  * LangChain Tools
  * Function/tool calling
  * Using chat models to call tools
  * Defining custom tools


Some models are capable of **tool calling** - generating arguments that conform to a specific user-provided schema. This guide will demonstrate how to use those tool calls to actually call a function and properly pass the results back to the model.
![Diagram of a tool call invocation](https://python.langchain.com/assets/images/tool_invocation-7f277888701ee431a17607f1a035c080.png)
![Diagram of a tool call result](https://python.langchain.com/assets/images/tool_results-71b4b90f33a56563c102d91e7821a993.png)
First, let's define our tools and our model:
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
import getpassimport osifnot os.environ.get("GROQ_API_KEY"): os.environ["GROQ_API_KEY"]= getpass.getpass("Enter API key for Groq: ")from langchain.chat_models import init_chat_modelllm = init_chat_model("llama3-8b-8192", model_provider="groq")
```

```
from langchain_core.tools import tool@tooldefadd(a:int, b:int)->int:"""Adds a and b."""return a + b@tooldefmultiply(a:int, b:int)->int:"""Multiplies a and b."""return a * btools =[add, multiply]llm_with_tools = llm.bind_tools(tools)
```

**API Reference:**tool
Now, let's get the model to call a tool. We'll add it to a list of messages that we'll treat as conversation history:
```
from langchain_core.messages import HumanMessagequery ="What is 3 * 12? Also, what is 11 + 49?"messages =[HumanMessage(query)]ai_msg = llm_with_tools.invoke(messages)print(ai_msg.tool_calls)messages.append(ai_msg)
```

**API Reference:**HumanMessage
```
[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_GPGPE943GORirhIAYnWv00rK', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_dm8o64ZrY3WFZHAvCh1bEJ6i', 'type': 'tool_call'}]
```

Next let's invoke the tool functions using the args the model populated!
Conveniently, if we invoke a LangChain `Tool` with a `ToolCall`, we'll automatically get back a `ToolMessage` that can be fed back to the model:
Compatibility
This functionality was added in `langchain-core == 0.2.19`. Please make sure your package is up to date.
If you are on earlier versions of `langchain-core`, you will need to extract the `args` field from the tool and construct a `ToolMessage` manually.
```
for tool_call in ai_msg.tool_calls:  selected_tool ={"add": add,"multiply": multiply}[tool_call["name"].lower()]  tool_msg = selected_tool.invoke(tool_call)  messages.append(tool_msg)messages
```

```
[HumanMessage(content='What is 3 * 12? Also, what is 11 + 49?'), AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_loT2pliJwJe3p7nkgXYF48A1', 'function': {'arguments': '{"a": 3, "b": 12}', 'name': 'multiply'}, 'type': 'function'}, {'id': 'call_bG9tYZCXOeYDZf3W46TceoV4', 'function': {'arguments': '{"a": 11, "b": 49}', 'name': 'add'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 50, 'prompt_tokens': 87, 'total_tokens': 137}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_661538dc1f', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-e3db3c46-bf9e-478e-abc1-dc9a264f4afe-0', tool_calls=[{'name': 'multiply', 'args': {'a': 3, 'b': 12}, 'id': 'call_loT2pliJwJe3p7nkgXYF48A1', 'type': 'tool_call'}, {'name': 'add', 'args': {'a': 11, 'b': 49}, 'id': 'call_bG9tYZCXOeYDZf3W46TceoV4', 'type': 'tool_call'}], usage_metadata={'input_tokens': 87, 'output_tokens': 50, 'total_tokens': 137}), ToolMessage(content='36', name='multiply', tool_call_id='call_loT2pliJwJe3p7nkgXYF48A1'), ToolMessage(content='60', name='add', tool_call_id='call_bG9tYZCXOeYDZf3W46TceoV4')]
```

And finally, we'll invoke the model with the tool results. The model will use this information to generate a final answer to our original query:
```
llm_with_tools.invoke(messages)
```

```
AIMessage(content='The result of \\(3 \\times 12\\) is 36, and the result of \\(11 + 49\\) is 60.', response_metadata={'token_usage': {'completion_tokens': 31, 'prompt_tokens': 153, 'total_tokens': 184}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_661538dc1f', 'finish_reason': 'stop', 'logprobs': None}, id='run-87d1ef0a-1223-4bb3-9310-7b591789323d-0', usage_metadata={'input_tokens': 153, 'output_tokens': 31, 'total_tokens': 184})
```

Note that each `ToolMessage` must include a `tool_call_id` that matches an `id` in the original tool calls that the model generates. This helps the model match tool responses with tool calls.
Tool calling agents, like those in LangGraph, use this basic flow to answer queries and solve tasks.
## Related​
  * LangGraph quickstart
  * Few shot prompting with tools
  * Stream tool calls
  * Pass runtime values to tools
  * Getting structured outputs from models


#### Was this page helpful?
  * Related


