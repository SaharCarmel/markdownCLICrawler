Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
Perhaps the most error-prone part of any SQL chain or agent is writing valid and safe SQL queries. In this guide we'll go over some strategies for validating our queries and handling invalid queries.
We will cover:
  1. Appending a "query validator" step to the query generation;
  2. Prompt engineering to reduce the incidence of errors.


## Setup​
First, get required packages and set environment variables:
```
%pip install --upgrade --quiet langchain langchain-community langchain-openai
```

```
# Uncomment the below to use LangSmith. Not required.# import os# os.environ["LANGSMITH_API_KEY"] = getpass.getpass()# os.environ["LANGSMITH_TRACING"] = "true"
```

The below example will use a SQLite connection with Chinook database. Follow these installation steps to create `Chinook.db` in the same directory as this notebook:
  * Save this file as `Chinook_Sqlite.sql`
  * Run `sqlite3 Chinook.db`
  * Run `.read Chinook_Sqlite.sql`
  * Test `SELECT * FROM Artist LIMIT 10;`


Now, `Chinook.db` is in our directory and we can interface with it using the SQLAlchemy-driven `SQLDatabase` class:
```
from langchain_community.utilities import SQLDatabasedb = SQLDatabase.from_uri("sqlite:///Chinook.db")print(db.dialect)print(db.get_usable_table_names())print(db.run("SELECT * FROM Artist LIMIT 10;"))
```

**API Reference:**SQLDatabase
```
sqlite['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track'][(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains'), (6, 'Antônio Carlos Jobim'), (7, 'Apocalyptica'), (8, 'Audioslave'), (9, 'BackBeat'), (10, 'Billy Cobham')]
```

## Query checker​
Perhaps the simplest strategy is to ask the model itself to check the original query for common mistakes. Suppose we have the following SQL query chain:
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
from langchain.chains import create_sql_query_chainchain = create_sql_query_chain(llm, db)
```

**API Reference:**create_sql_query_chain
And we want to validate its outputs. We can do so by extending the chain with a second prompt and model call:
```
from langchain_core.output_parsers import StrOutputParserfrom langchain_core.prompts import ChatPromptTemplatesystem ="""Double check the user's {dialect} query for common mistakes, including:- Using NOT IN with NULL values- Using UNION when UNION ALL should have been used- Using BETWEEN for exclusive ranges- Data type mismatch in predicates- Properly quoting identifiers- Using the correct number of arguments for functions- Casting to the correct data type- Using the proper columns for joinsIf there are any of the above mistakes, rewrite the query.If there are no mistakes, just reproduce the original query with no further commentary.Output the final SQL query only."""prompt = ChatPromptTemplate.from_messages([("system", system),("human","{query}")]).partial(dialect=db.dialect)validation_chain = prompt | llm | StrOutputParser()full_chain ={"query": chain}| validation_chain
```

**API Reference:**StrOutputParser | ChatPromptTemplate
```
query = full_chain.invoke({"question":"What's the average Invoice from an American customer whose Fax is missing since 2003 but before 2010"})print(query)
```

```
SELECT AVG(i.Total) AS AverageInvoiceFROM Invoice iJOIN Customer c ON i.CustomerId = c.CustomerIdWHERE c.Country = 'USA'AND c.Fax IS NULLAND i.InvoiceDate >= '2003-01-01' AND i.InvoiceDate < '2010-01-01'
```

Note how we can see both steps of the chain in the Langsmith trace.
```
db.run(query)
```

```
'[(6.632999999999998,)]'
```

The obvious downside of this approach is that we need to make two model calls instead of one to generate our query. To get around this we can try to perform the query generation and query check in a single model invocation:
```
system ="""You are a {dialect} expert. Given an input question, create a syntactically correct {dialect} query to run.Unless the user specifies in the question a specific number of examples to obtain, query for at most {top_k} results using the LIMIT clause as per {dialect}. You can order the results to return the most informative data in the database.Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Pay attention to use date('now') function to get the current date, if the question involves "today".Only use the following tables:{table_info}Write an initial draft of the query. Then double check the {dialect} query for common mistakes, including:- Using NOT IN with NULL values- Using UNION when UNION ALL should have been used- Using BETWEEN for exclusive ranges- Data type mismatch in predicates- Properly quoting identifiers- Using the correct number of arguments for functions- Casting to the correct data type- Using the proper columns for joinsUse format:First draft: <<FIRST_DRAFT_QUERY>>Final answer: <<FINAL_ANSWER_QUERY>>"""prompt = ChatPromptTemplate.from_messages([("system", system),("human","{input}")]).partial(dialect=db.dialect)defparse_final_answer(output:str)->str:return output.split("Final answer: ")[1]chain = create_sql_query_chain(llm, db, prompt=prompt)| parse_final_answerprompt.pretty_print()
```

```
================================[1m System Message [0m================================You are a [33;1m[1;3m{dialect}[0m expert. Given an input question, create a syntactically correct [33;1m[1;3m{dialect}[0m query to run.Unless the user specifies in the question a specific number of examples to obtain, query for at most [33;1m[1;3m{top_k}[0m results using the LIMIT clause as per [33;1m[1;3m{dialect}[0m. You can order the results to return the most informative data in the database.Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Pay attention to use date('now') function to get the current date, if the question involves "today".Only use the following tables:[33;1m[1;3m{table_info}[0mWrite an initial draft of the query. Then double check the [33;1m[1;3m{dialect}[0m query for common mistakes, including:- Using NOT IN with NULL values- Using UNION when UNION ALL should have been used- Using BETWEEN for exclusive ranges- Data type mismatch in predicates- Properly quoting identifiers- Using the correct number of arguments for functions- Casting to the correct data type- Using the proper columns for joinsUse format:First draft: <<FIRST_DRAFT_QUERY>>Final answer: <<FINAL_ANSWER_QUERY>>================================[1m Human Message [0m=================================[33;1m[1;3m{input}[0m
```

```
query = chain.invoke({"question":"What's the average Invoice from an American customer whose Fax is missing since 2003 but before 2010"})print(query)
```

```
SELECT AVG(i."Total") AS "AverageInvoice"FROM "Invoice" iJOIN "Customer" c ON i."CustomerId" = c."CustomerId"WHERE c."Country" = 'USA'AND c."Fax" IS NULLAND i."InvoiceDate" BETWEEN '2003-01-01' AND '2010-01-01';
```

```
db.run(query)
```

```
'[(6.632999999999998,)]'
```

## Human-in-the-loop​
In some cases our data is sensitive enough that we never want to execute a SQL query without a human approving it first. Head to the Tool use: Human-in-the-loop page to learn how to add a human-in-the-loop to any tool, chain or agent.
## Error handling​
At some point, the model will make a mistake and craft an invalid SQL query. Or an issue will arise with our database. Or the model API will go down. We'll want to add some error handling behavior to our chains and agents so that we fail gracefully in these situations, and perhaps even automatically recover. To learn about error handling with tools, head to the Tool use: Error handling page.
#### Was this page helpful?
  * Setup
  * Query checker
  * Human-in-the-loop
  * Error handling


