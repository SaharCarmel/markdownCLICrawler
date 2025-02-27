Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
By themselves, language models can't take actions - they just output text. A big use case for LangChain is creating **agents**. Agents are systems that use LLMs as reasoning engines to determine which actions to take and the inputs necessary to perform the action. After executing actions, the results can be fed back into the LLM to determine whether more actions are needed, or whether it is okay to finish. This is often achieved via tool-calling.
In this tutorial we will build an agent that can interact with a search engine. You will be able to ask this agent questions, watch it call the search tool, and have conversations with it.
## End-to-end agent​
The code snippet below represents a fully functional agent that uses an LLM to decide which tools to use. It is equipped with a generic search tool. It has conversational memory - meaning that it can be used as a multi-turn chatbot.
In the rest of the guide, we will walk through the individual components and what each part does - but if you want to just grab some code and get started, feel free to use this!
```
# Import relevant functionalityfrom langchain_anthropic import ChatAnthropicfrom langchain_community.tools.tavily_search import TavilySearchResultsfrom langchain_core.messages import HumanMessagefrom langgraph.checkpoint.memory import MemorySaverfrom langgraph.prebuilt import create_react_agent# Create the agentmemory = MemorySaver()model = ChatAnthropic(model_name="claude-3-sonnet-20240229")search = TavilySearchResults(max_results=2)tools =[search]agent_executor = create_react_agent(model, tools, checkpointer=memory)# Use the agentconfig ={"configurable":{"thread_id":"abc123"}}for chunk in agent_executor.stream({"messages":[HumanMessage(content="hi im bob! and i live in sf")]}, config):print(chunk)print("----")for chunk in agent_executor.stream({"messages":[HumanMessage(content="whats the weather where I live?")]}, config):print(chunk)print("----")
```

**API Reference:**ChatAnthropic | TavilySearchResults | HumanMessage | MemorySaver | create_react_agent
```
{'agent': {'messages': [AIMessage(content="Hello Bob! Since you didn't ask a specific question, I don't need to use any tools to respond. It's nice to meet you. San Francisco is a wonderful city with lots to see and do. I hope you're enjoying living there. Please let me know if you have any other questions!", response_metadata={'id': 'msg_01Mmfzfs9m4XMgVzsCZYMWqH', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 271, 'output_tokens': 65}}, id='run-44c57f9c-a637-4888-b7d9-6d985031ae48-0', usage_metadata={'input_tokens': 271, 'output_tokens': 65, 'total_tokens': 336})]}}----{'agent': {'messages': [AIMessage(content=[{'text': 'To get current weather information for your location in San Francisco, let me invoke the search tool:', 'type': 'text'}, {'id': 'toolu_01BGEyQaSz3pTq8RwUUHSRoo', 'input': {'query': 'san francisco weather'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}], response_metadata={'id': 'msg_013AVSVsRLKYZjduLpJBY4us', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'tool_use', 'stop_sequence': None, 'usage': {'input_tokens': 347, 'output_tokens': 80}}, id='run-de7923b6-5ee2-4ebe-bd95-5aed4933d0e3-0', tool_calls=[{'name': 'tavily_search_results_json', 'args': {'query': 'san francisco weather'}, 'id': 'toolu_01BGEyQaSz3pTq8RwUUHSRoo'}], usage_metadata={'input_tokens': 347, 'output_tokens': 80, 'total_tokens': 427})]}}----{'tools': {'messages': [ToolMessage(content='[{"url": "https://www.weatherapi.com/", "content": "{\'location\': {\'name\': \'San Francisco\', \'region\': \'California\', \'country\': \'United States of America\', \'lat\': 37.78, \'lon\': -122.42, \'tz_id\': \'America/Los_Angeles\', \'localtime_epoch\': 1717238643, \'localtime\': \'2024-06-01 3:44\'}, \'current\': {\'last_updated_epoch\': 1717237800, \'last_updated\': \'2024-06-01 03:30\', \'temp_c\': 12.0, \'temp_f\': 53.6, \'is_day\': 0, \'condition\': {\'text\': \'Mist\', \'icon\': \'//cdn.weatherapi.com/weather/64x64/night/143.png\', \'code\': 1030}, \'wind_mph\': 5.6, \'wind_kph\': 9.0, \'wind_degree\': 310, \'wind_dir\': \'NW\', \'pressure_mb\': 1013.0, \'pressure_in\': 29.92, \'precip_mm\': 0.0, \'precip_in\': 0.0, \'humidity\': 88, \'cloud\': 100, \'feelslike_c\': 10.5, \'feelslike_f\': 50.8, \'windchill_c\': 9.3, \'windchill_f\': 48.7, \'heatindex_c\': 11.1, \'heatindex_f\': 51.9, \'dewpoint_c\': 8.8, \'dewpoint_f\': 47.8, \'vis_km\': 6.4, \'vis_miles\': 3.0, \'uv\': 1.0, \'gust_mph\': 12.5, \'gust_kph\': 20.1}}"}, {"url": "https://www.timeanddate.com/weather/usa/san-francisco/historic", "content": "Past Weather in San Francisco, California, USA \\u2014 Yesterday and Last 2 Weeks. Time/General. Weather. Time Zone. DST Changes. Sun & Moon. Weather Today Weather Hourly 14 Day Forecast Yesterday/Past Weather Climate (Averages) Currently: 68 \\u00b0F. Passing clouds."}]', name='tavily_search_results_json', tool_call_id='toolu_01BGEyQaSz3pTq8RwUUHSRoo')]}}----{'agent': {'messages': [AIMessage(content='Based on the search results, the current weather in San Francisco is:\n\nTemperature: 53.6°F (12°C)\nConditions: Misty\nWind: 5.6 mph (9 kph) from the Northwest\nHumidity: 88%\nCloud Cover: 100% \n\nThe results provide detailed information like wind chill, heat index, visibility and more. It looks like a typical cool, foggy morning in San Francisco. Let me know if you need any other details about the weather where you live!', response_metadata={'id': 'msg_019WGLbaojuNdbCnqac7zaGW', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 1035, 'output_tokens': 120}}, id='run-1bb68bf3-b212-4ef4-8a31-10c830421c78-0', usage_metadata={'input_tokens': 1035, 'output_tokens': 120, 'total_tokens': 1155})]}}----
```

## Setup​
### Jupyter Notebook​
This guide (and most of the other guides in the documentation) uses Jupyter notebooks and assumes the reader is as well. Jupyter notebooks are perfect interactive environments for learning how to work with LLM systems because oftentimes things can go wrong (unexpected output, API down, etc), and observing these cases is a great way to better understand building with LLMs.
This and other tutorials are perhaps most conveniently run in a Jupyter notebook. See here for instructions on how to install.
### Installation​
To install LangChain run:
```
%pip install -U langchain-community langgraph langchain-anthropic tavily-python langgraph-checkpoint-sqlite
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

### Tavily​
We will be using Tavily (a search engine) as a tool. In order to use it, you will need to get and set an API key:
```
export TAVILY_API_KEY="..."
```

Or, if in a notebook, you can set it with:
```
import getpassimport osos.environ["TAVILY_API_KEY"]= getpass.getpass()
```

## Define tools​
We first need to create the tools we want to use. Our main tool of choice will be Tavily - a search engine. We have a built-in tool in LangChain to easily use Tavily search engine as tool.
```
from langchain_community.tools.tavily_search import TavilySearchResultssearch = TavilySearchResults(max_results=2)search_results = search.invoke("what is the weather in SF")print(search_results)# If we want, we can create other tools.# Once we have all the tools we want, we can put them in a list that we will reference later.tools =[search]
```

**API Reference:**TavilySearchResults
```
[{'url': 'https://www.weatherapi.com/', 'content': "{'location': {'name': 'San Francisco', 'region': 'California', 'country': 'United States of America', 'lat': 37.78, 'lon': -122.42, 'tz_id': 'America/Los_Angeles', 'localtime_epoch': 1717238703, 'localtime': '2024-06-01 3:45'}, 'current': {'last_updated_epoch': 1717237800, 'last_updated': '2024-06-01 03:30', 'temp_c': 12.0, 'temp_f': 53.6, 'is_day': 0, 'condition': {'text': 'Mist', 'icon': '//cdn.weatherapi.com/weather/64x64/night/143.png', 'code': 1030}, 'wind_mph': 5.6, 'wind_kph': 9.0, 'wind_degree': 310, 'wind_dir': 'NW', 'pressure_mb': 1013.0, 'pressure_in': 29.92, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 88, 'cloud': 100, 'feelslike_c': 10.5, 'feelslike_f': 50.8, 'windchill_c': 9.3, 'windchill_f': 48.7, 'heatindex_c': 11.1, 'heatindex_f': 51.9, 'dewpoint_c': 8.8, 'dewpoint_f': 47.8, 'vis_km': 6.4, 'vis_miles': 3.0, 'uv': 1.0, 'gust_mph': 12.5, 'gust_kph': 20.1}}"}, {'url': 'https://www.wunderground.com/hourly/us/ca/san-francisco/date/2024-01-06', 'content': 'Current Weather for Popular Cities . San Francisco, CA 58 ° F Partly Cloudy; Manhattan, NY warning 51 ° F Cloudy; Schiller Park, IL (60176) warning 51 ° F Fair; Boston, MA warning 41 ° F ...'}]
```

## Using Language Models​
Next, let's learn how to use a language model to call tools. LangChain supports many different language models that you can use interchangably - select the one you want to use below!
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
'Hi there!'
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
ContentString: Hello!ToolCalls: []
```

Now, let's try calling it with some input that would expect a tool to be called.
```
response = model_with_tools.invoke([HumanMessage(content="What's the weather in SF?")])print(f"ContentString: {response.content}")print(f"ToolCalls: {response.tool_calls}")
```

```
ContentString: ToolCalls: [{'name': 'tavily_search_results_json', 'args': {'query': 'weather san francisco'}, 'id': 'toolu_01VTP7DUvSfgtYxsq9x4EwMp'}]
```

We can see that there's now no text content, but there is a tool call! It wants us to call the Tavily Search tool.
This isn't calling that tool yet - it's just telling us to. In order to actually call it, we'll want to create our agent.
## Create the agent​
Now that we have defined the tools and the LLM, we can create the agent. We will be using LangGraph to construct the agent. Currently, we are using a high level interface to construct the agent, but the nice thing about LangGraph is that this high-level interface is backed by a low-level, highly controllable API in case you want to modify the agent logic.
Now, we can initialize the agent with the LLM and the tools.
Note that we are passing in the `model`, not `model_with_tools`. That is because `create_react_agent` will call `.bind_tools` for us under the hood.
```
from langgraph.prebuilt import create_react_agentagent_executor = create_react_agent(model, tools)
```

**API Reference:**create_react_agent
## Run the agent​
We can now run the agent with a few queries! Note that for now, these are all **stateless** queries (it won't remember previous interactions). Note that the agent will return the **final** state at the end of the interaction (which includes any inputs, we will see later on how to get only the outputs).
First up, let's see how it responds when there's no need to call a tool:
```
response = agent_executor.invoke({"messages":[HumanMessage(content="hi!")]})response["messages"]
```

```
[HumanMessage(content='hi!', id='a820fcc5-9b87-457a-9af0-f21768143ee3'), AIMessage(content='Hello!', response_metadata={'id': 'msg_01VbC493X1VEDyusgttiEr1z', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 264, 'output_tokens': 5}}, id='run-0e0ddae8-a85b-4bd6-947c-c36c857a4698-0', usage_metadata={'input_tokens': 264, 'output_tokens': 5, 'total_tokens': 269})]
```

In order to see exactly what is happening under the hood (and to make sure it's not calling a tool) we can take a look at the LangSmith trace
Let's now try it out on an example where it should be invoking the tool
```
response = agent_executor.invoke({"messages":[HumanMessage(content="whats the weather in sf?")]})response["messages"]
```

```
[HumanMessage(content='whats the weather in sf?', id='1d6c96bb-4ddb-415c-a579-a07d5264de0d'), AIMessage(content=[{'id': 'toolu_01Y5EK4bw2LqsQXeaUv8iueF', 'input': {'query': 'weather in san francisco'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}], response_metadata={'id': 'msg_0132wQUcEduJ8UKVVVqwJzM4', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'tool_use', 'stop_sequence': None, 'usage': {'input_tokens': 269, 'output_tokens': 61}}, id='run-26d5e5e8-d4fd-46d2-a197-87b95b10e823-0', tool_calls=[{'name': 'tavily_search_results_json', 'args': {'query': 'weather in san francisco'}, 'id': 'toolu_01Y5EK4bw2LqsQXeaUv8iueF'}], usage_metadata={'input_tokens': 269, 'output_tokens': 61, 'total_tokens': 330}), ToolMessage(content='[{"url": "https://www.weatherapi.com/", "content": "{\'location\': {\'name\': \'San Francisco\', \'region\': \'California\', \'country\': \'United States of America\', \'lat\': 37.78, \'lon\': -122.42, \'tz_id\': \'America/Los_Angeles\', \'localtime_epoch\': 1717238703, \'localtime\': \'2024-06-01 3:45\'}, \'current\': {\'last_updated_epoch\': 1717237800, \'last_updated\': \'2024-06-01 03:30\', \'temp_c\': 12.0, \'temp_f\': 53.6, \'is_day\': 0, \'condition\': {\'text\': \'Mist\', \'icon\': \'//cdn.weatherapi.com/weather/64x64/night/143.png\', \'code\': 1030}, \'wind_mph\': 5.6, \'wind_kph\': 9.0, \'wind_degree\': 310, \'wind_dir\': \'NW\', \'pressure_mb\': 1013.0, \'pressure_in\': 29.92, \'precip_mm\': 0.0, \'precip_in\': 0.0, \'humidity\': 88, \'cloud\': 100, \'feelslike_c\': 10.5, \'feelslike_f\': 50.8, \'windchill_c\': 9.3, \'windchill_f\': 48.7, \'heatindex_c\': 11.1, \'heatindex_f\': 51.9, \'dewpoint_c\': 8.8, \'dewpoint_f\': 47.8, \'vis_km\': 6.4, \'vis_miles\': 3.0, \'uv\': 1.0, \'gust_mph\': 12.5, \'gust_kph\': 20.1}}"}, {"url": "https://www.timeanddate.com/weather/usa/san-francisco/hourly", "content": "Sun & Moon. Weather Today Weather Hourly 14 Day Forecast Yesterday/Past Weather Climate (Averages) Currently: 59 \\u00b0F. Passing clouds. (Weather station: San Francisco International Airport, USA). See more current weather."}]', name='tavily_search_results_json', id='37aa1fd9-b232-4a02-bd22-bc5b9b44a22c', tool_call_id='toolu_01Y5EK4bw2LqsQXeaUv8iueF'), AIMessage(content='Based on the search results, here is a summary of the current weather in San Francisco:\n\nThe weather in San Francisco is currently misty with a temperature of around 53°F (12°C). There is complete cloud cover and moderate winds from the northwest around 5-9 mph (9-14 km/h). Humidity is high at 88%. Visibility is around 3 miles (6.4 km). \n\nThe results provide an hourly forecast as well as current conditions from a couple different weather sources. Let me know if you need any additional details about the San Francisco weather!', response_metadata={'id': 'msg_01BRX9mrT19nBDdHYtR7wJ92', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 920, 'output_tokens': 132}}, id='run-d0325583-3ddc-4432-b2b2-d023eb97660f-0', usage_metadata={'input_tokens': 920, 'output_tokens': 132, 'total_tokens': 1052})]
```

We can check out the LangSmith trace to make sure it's calling the search tool effectively.
## Streaming Messages​
We've seen how the agent can be called with `.invoke` to get a final response. If the agent executes multiple steps, this may take a while. To show intermediate progress, we can stream back messages as they occur.
```
for chunk in agent_executor.stream({"messages":[HumanMessage(content="whats the weather in sf?")]}):print(chunk)print("----")
```

```
{'agent': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_50Kb8zHmFqPYavQwF5TgcOH8', 'function': {'arguments': '{\n "query": "current weather in San Francisco"\n}', 'name': 'tavily_search_results_json'}, 'type': 'function'}]}, response_metadata={'token_usage': {'completion_tokens': 23, 'prompt_tokens': 134, 'total_tokens': 157}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-042d5feb-c2cc-4c3f-b8fd-dbc22fd0bc07-0', tool_calls=[{'name': 'tavily_search_results_json', 'args': {'query': 'current weather in San Francisco'}, 'id': 'call_50Kb8zHmFqPYavQwF5TgcOH8'}])]}}----{'action': {'messages': [ToolMessage(content='[{"url": "https://www.weatherapi.com/", "content": "{\'location\': {\'name\': \'San Francisco\', \'region\': \'California\', \'country\': \'United States of America\', \'lat\': 37.78, \'lon\': -122.42, \'tz_id\': \'America/Los_Angeles\', \'localtime_epoch\': 1714426906, \'localtime\': \'2024-04-29 14:41\'}, \'current\': {\'last_updated_epoch\': 1714426200, \'last_updated\': \'2024-04-29 14:30\', \'temp_c\': 17.8, \'temp_f\': 64.0, \'is_day\': 1, \'condition\': {\'text\': \'Sunny\', \'icon\': \'//cdn.weatherapi.com/weather/64x64/day/113.png\', \'code\': 1000}, \'wind_mph\': 23.0, \'wind_kph\': 37.1, \'wind_degree\': 290, \'wind_dir\': \'WNW\', \'pressure_mb\': 1019.0, \'pressure_in\': 30.09, \'precip_mm\': 0.0, \'precip_in\': 0.0, \'humidity\': 50, \'cloud\': 0, \'feelslike_c\': 17.8, \'feelslike_f\': 64.0, \'vis_km\': 16.0, \'vis_miles\': 9.0, \'uv\': 5.0, \'gust_mph\': 27.5, \'gust_kph\': 44.3}}"}, {"url": "https://world-weather.info/forecast/usa/san_francisco/april-2024/", "content": "Extended weather forecast in San Francisco. Hourly Week 10 days 14 days 30 days Year. Detailed \\u26a1 San Francisco Weather Forecast for April 2024 - day/night \\ud83c\\udf21\\ufe0f temperatures, precipitations - World-Weather.info."}]', name='tavily_search_results_json', id='d88320ac-3fe1-4f73-870a-3681f15f6982', tool_call_id='call_50Kb8zHmFqPYavQwF5TgcOH8')]}}----{'agent': {'messages': [AIMessage(content='The current weather in San Francisco, California is sunny with a temperature of 17.8°C (64.0°F). The wind is coming from the WNW at 23.0 mph. The humidity is at 50%. [source](https://www.weatherapi.com/)', response_metadata={'token_usage': {'completion_tokens': 58, 'prompt_tokens': 602, 'total_tokens': 660}, 'model_name': 'gpt-4', 'system_fingerprint': None, 'finish_reason': 'stop', 'logprobs': None}, id='run-0cd2a507-ded5-4601-afe3-3807400e9989-0')]}}----
```

## Streaming tokens​
In addition to streaming back messages, it is also useful to stream back tokens. We can do this with the `.astream_events` method.
important
This `.astream_events` method only works with Python 3.11 or higher.
```
asyncfor event in agent_executor.astream_events({"messages":[HumanMessage(content="whats the weather in sf?")]}, version="v1"):  kind = event["event"]if kind =="on_chain_start":if(      event["name"]=="Agent"):# Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`print(f"Starting agent: {event['name']} with input: {event['data'].get('input')}")elif kind =="on_chain_end":if(      event["name"]=="Agent"):# Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`print()print("--")print(f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}")if kind =="on_chat_model_stream":    content = event["data"]["chunk"].contentif content:# Empty content in the context of OpenAI means# that the model is asking for a tool to be invoked.# So we only print non-empty contentprint(content, end="|")elif kind =="on_tool_start":print("--")print(f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}")elif kind =="on_tool_end":print(f"Done tool: {event['name']}")print(f"Tool output was: {event['data'].get('output')}")print("--")
```

```
--Starting tool: tavily_search_results_json with inputs: {'query': 'current weather in San Francisco'}Done tool: tavily_search_results_jsonTool output was: [{'url': 'https://www.weatherapi.com/', 'content': "{'location': {'name': 'San Francisco', 'region': 'California', 'country': 'United States of America', 'lat': 37.78, 'lon': -122.42, 'tz_id': 'America/Los_Angeles', 'localtime_epoch': 1714427052, 'localtime': '2024-04-29 14:44'}, 'current': {'last_updated_epoch': 1714426200, 'last_updated': '2024-04-29 14:30', 'temp_c': 17.8, 'temp_f': 64.0, 'is_day': 1, 'condition': {'text': 'Sunny', 'icon': '//cdn.weatherapi.com/weather/64x64/day/113.png', 'code': 1000}, 'wind_mph': 23.0, 'wind_kph': 37.1, 'wind_degree': 290, 'wind_dir': 'WNW', 'pressure_mb': 1019.0, 'pressure_in': 30.09, 'precip_mm': 0.0, 'precip_in': 0.0, 'humidity': 50, 'cloud': 0, 'feelslike_c': 17.8, 'feelslike_f': 64.0, 'vis_km': 16.0, 'vis_miles': 9.0, 'uv': 5.0, 'gust_mph': 27.5, 'gust_kph': 44.3}}"}, {'url': 'https://www.weathertab.com/en/c/e/04/united-states/california/san-francisco/', 'content': 'San Francisco Weather Forecast for Apr 2024 - Risk of Rain Graph. Rain Risk Graph: Monthly Overview. Bar heights indicate rain risk percentages. Yellow bars mark low-risk days, while black and grey bars signal higher risks. Grey-yellow bars act as buffers, advising to keep at least one day clear from the riskier grey and black days, guiding ...'}]--The| current| weather| in| San| Francisco|,| California|,| USA| is| sunny| with| a| temperature| of| |17|.|8|°C| (|64|.|0|°F|).| The| wind| is| blowing| from| the| W|NW| at| a| speed| of| |37|.|1| k|ph| (|23|.|0| mph|).| The| humidity| level| is| at| |50|%.| [|Source|](|https|://|www|.weather|api|.com|/)|
```

## Adding in memory​
As mentioned earlier, this agent is stateless. This means it does not remember previous interactions. To give it memory we need to pass in a checkpointer. When passing in a checkpointer, we also have to pass in a `thread_id` when invoking the agent (so it knows which thread/conversation to resume from).
```
from langgraph.checkpoint.memory import MemorySavermemory = MemorySaver()
```

**API Reference:**MemorySaver
```
agent_executor = create_react_agent(model, tools, checkpointer=memory)config ={"configurable":{"thread_id":"abc123"}}
```

```
for chunk in agent_executor.stream({"messages":[HumanMessage(content="hi im bob!")]}, config):print(chunk)print("----")
```

```
{'agent': {'messages': [AIMessage(content="Hello Bob! It's nice to meet you again.", response_metadata={'id': 'msg_013C1z2ZySagEFwmU1EsysR2', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 1162, 'output_tokens': 14}}, id='run-f878acfd-d195-44e8-9166-e2796317e3f8-0', usage_metadata={'input_tokens': 1162, 'output_tokens': 14, 'total_tokens': 1176})]}}----
```

```
for chunk in agent_executor.stream({"messages":[HumanMessage(content="whats my name?")]}, config):print(chunk)print("----")
```

```
{'agent': {'messages': [AIMessage(content='You mentioned your name is Bob when you introduced yourself earlier. So your name is Bob.', response_metadata={'id': 'msg_01WNwnRNGwGDRw6vRdivt6i1', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 1184, 'output_tokens': 21}}, id='run-f5c0b957-8878-405a-9d4b-a7cd38efe81f-0', usage_metadata={'input_tokens': 1184, 'output_tokens': 21, 'total_tokens': 1205})]}}----
```

Example LangSmith trace
If you want to start a new conversation, all you have to do is change the `thread_id` used
```
config ={"configurable":{"thread_id":"xyz123"}}for chunk in agent_executor.stream({"messages":[HumanMessage(content="whats my name?")]}, config):print(chunk)print("----")
```

```
{'agent': {'messages': [AIMessage(content="I'm afraid I don't actually know your name. As an AI assistant without personal information about you, I don't have a specific name associated with our conversation.", response_metadata={'id': 'msg_01NoaXNNYZKSoBncPcLkdcbo', 'model': 'claude-3-sonnet-20240229', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 267, 'output_tokens': 36}}, id='run-c9f7df3d-525a-4d8f-bbcf-a5b4a5d2e4b0-0', usage_metadata={'input_tokens': 267, 'output_tokens': 36, 'total_tokens': 303})]}}----
```

## Conclusion​
That's a wrap! In this quick start we covered how to create a simple agent. We've then shown how to stream back a response - not only with the intermediate steps, but also tokens! We've also added in memory so you can have a conversation with them. Agents are a complex topic with lots to learn!
For more information on Agents, please check out the LangGraph documentation. This has it's own set of concepts, tutorials, and how-to guides.
#### Was this page helpful?
  * End-to-end agent
  * Setup
    * Jupyter Notebook
    * Installation
    * LangSmith
    * Tavily
  * Define tools
  * Using Language Models
  * Create the agent
  * Run the agent
  * Streaming Messages
  * Streaming tokens
  * Adding in memory
  * Conclusion


