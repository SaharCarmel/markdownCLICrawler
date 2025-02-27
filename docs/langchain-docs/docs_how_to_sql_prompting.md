Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
On this page
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
In this guide we'll go over prompting strategies to improve SQL query generation using create_sql_query_chain. We'll largely focus on methods for getting relevant database-specific information in your prompt.
We will cover:
  * How the dialect of the LangChain SQLDatabase impacts the prompt of the chain;
  * How to format schema information into the prompt using `SQLDatabase.get_context`;
  * How to build and select few-shot examples to assist the model.


## Setup​
First, get required packages and set environment variables:
```
%pip install --upgrade --quiet langchain langchain-community langchain-experimental langchain-openai
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
from langchain_community.utilities import SQLDatabasedb = SQLDatabase.from_uri("sqlite:///Chinook.db", sample_rows_in_table_info=3)print(db.dialect)print(db.get_usable_table_names())print(db.run("SELECT * FROM Artist LIMIT 10;"))
```

**API Reference:**SQLDatabase
```
sqlite['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice', 'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track'][(1, 'AC/DC'), (2, 'Accept'), (3, 'Aerosmith'), (4, 'Alanis Morissette'), (5, 'Alice In Chains'), (6, 'Antônio Carlos Jobim'), (7, 'Apocalyptica'), (8, 'Audioslave'), (9, 'BackBeat'), (10, 'Billy Cobham')]
```

## Dialect-specific prompting​
One of the simplest things we can do is make our prompt specific to the SQL dialect we're using. When using the built-in create_sql_query_chain and SQLDatabase, this is handled for you for any of the following dialects:
```
from langchain.chains.sql_database.prompt import SQL_PROMPTSlist(SQL_PROMPTS)
```

```
['crate', 'duckdb', 'googlesql', 'mssql', 'mysql', 'mariadb', 'oracle', 'postgresql', 'sqlite', 'clickhouse', 'prestodb']
```

For example, using our current DB we can see that we'll get a SQLite-specific prompt.
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
from langchain.chains import create_sql_query_chainchain = create_sql_query_chain(llm, db)chain.get_prompts()[0].pretty_print()
```

**API Reference:**create_sql_query_chain
```
You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Pay attention to use date('now') function to get the current date, if the question involves "today".Use the following format:Question: Question hereSQLQuery: SQL Query to runSQLResult: Result of the SQLQueryAnswer: Final answer hereOnly use the following tables:[33;1m[1;3m{table_info}[0mQuestion: [33;1m[1;3m{input}[0m
```

## Table definitions and example rows​
In most SQL chains, we'll need to feed the model at least part of the database schema. Without this it won't be able to write valid queries. Our database comes with some convenience methods to give us the relevant context. Specifically, we can get the table names, their schemas, and a sample of rows from each table.
Here we will use `SQLDatabase.get_context`, which provides available tables and their schemas:
```
context = db.get_context()print(list(context))print(context["table_info"])
```

```
['table_info', 'table_names']CREATE TABLE "Album" (	"AlbumId" INTEGER NOT NULL, 	"Title" NVARCHAR(160) NOT NULL, 	"ArtistId" INTEGER NOT NULL, 	PRIMARY KEY ("AlbumId"), 	FOREIGN KEY("ArtistId") REFERENCES "Artist" ("ArtistId"))/*3 rows from Album table:AlbumId	Title	ArtistId1	For Those About To Rock We Salute You	12	Balls to the Wall	23	Restless and Wild	2*/CREATE TABLE "Artist" (	"ArtistId" INTEGER NOT NULL, 	"Name" NVARCHAR(120), 	PRIMARY KEY ("ArtistId"))/*3 rows from Artist table:ArtistId	Name1	AC/DC2	Accept3	Aerosmith*/CREATE TABLE "Customer" (	"CustomerId" INTEGER NOT NULL, 	"FirstName" NVARCHAR(40) NOT NULL, 	"LastName" NVARCHAR(20) NOT NULL, 	"Company" NVARCHAR(80), 	"Address" NVARCHAR(70), 	"City" NVARCHAR(40), 	"State" NVARCHAR(40), 	"Country" NVARCHAR(40), 	"PostalCode" NVARCHAR(10), 	"Phone" NVARCHAR(24), 	"Fax" NVARCHAR(24), 	"Email" NVARCHAR(60) NOT NULL, 	"SupportRepId" INTEGER, 	PRIMARY KEY ("CustomerId"), 	FOREIGN KEY("SupportRepId") REFERENCES "Employee" ("EmployeeId"))/*3 rows from Customer table:CustomerId	FirstName	LastName	Company	Address	City	State	Country	PostalCode	Phone	Fax	Email	SupportRepId1	Luís	Gonçalves	Embraer - Empresa Brasileira de Aeronáutica S.A.	Av. Brigadeiro Faria Lima, 2170	São José dos Campos	SP	Brazil	12227-000	+55 (12) 3923-5555	+55 (12) 3923-5566	luisg@embraer.com.br	32	Leonie	Köhler	None	Theodor-Heuss-Straße 34	Stuttgart	None	Germany	70174	+49 0711 2842222	None	leonekohler@surfeu.de	53	François	Tremblay	None	1498 rue Bélanger	Montréal	QC	Canada	H2G 1A7	+1 (514) 721-4711	None	ftremblay@gmail.com	3*/CREATE TABLE "Employee" (	"EmployeeId" INTEGER NOT NULL, 	"LastName" NVARCHAR(20) NOT NULL, 	"FirstName" NVARCHAR(20) NOT NULL, 	"Title" NVARCHAR(30), 	"ReportsTo" INTEGER, 	"BirthDate" DATETIME, 	"HireDate" DATETIME, 	"Address" NVARCHAR(70), 	"City" NVARCHAR(40), 	"State" NVARCHAR(40), 	"Country" NVARCHAR(40), 	"PostalCode" NVARCHAR(10), 	"Phone" NVARCHAR(24), 	"Fax" NVARCHAR(24), 	"Email" NVARCHAR(60), 	PRIMARY KEY ("EmployeeId"), 	FOREIGN KEY("ReportsTo") REFERENCES "Employee" ("EmployeeId"))/*3 rows from Employee table:EmployeeId	LastName	FirstName	Title	ReportsTo	BirthDate	HireDate	Address	City	State	Country	PostalCode	Phone	Fax	Email1	Adams	Andrew	General Manager	None	1962-02-18 00:00:00	2002-08-14 00:00:00	11120 Jasper Ave NW	Edmonton	AB	Canada	T5K 2N1	+1 (780) 428-9482	+1 (780) 428-3457	andrew@chinookcorp.com2	Edwards	Nancy	Sales Manager	1	1958-12-08 00:00:00	2002-05-01 00:00:00	825 8 Ave SW	Calgary	AB	Canada	T2P 2T3	+1 (403) 262-3443	+1 (403) 262-3322	nancy@chinookcorp.com3	Peacock	Jane	Sales Support Agent	2	1973-08-29 00:00:00	2002-04-01 00:00:00	1111 6 Ave SW	Calgary	AB	Canada	T2P 5M5	+1 (403) 262-3443	+1 (403) 262-6712	jane@chinookcorp.com*/CREATE TABLE "Genre" (	"GenreId" INTEGER NOT NULL, 	"Name" NVARCHAR(120), 	PRIMARY KEY ("GenreId"))/*3 rows from Genre table:GenreId	Name1	Rock2	Jazz3	Metal*/CREATE TABLE "Invoice" (	"InvoiceId" INTEGER NOT NULL, 	"CustomerId" INTEGER NOT NULL, 	"InvoiceDate" DATETIME NOT NULL, 	"BillingAddress" NVARCHAR(70), 	"BillingCity" NVARCHAR(40), 	"BillingState" NVARCHAR(40), 	"BillingCountry" NVARCHAR(40), 	"BillingPostalCode" NVARCHAR(10), 	"Total" NUMERIC(10, 2) NOT NULL, 	PRIMARY KEY ("InvoiceId"), 	FOREIGN KEY("CustomerId") REFERENCES "Customer" ("CustomerId"))/*3 rows from Invoice table:InvoiceId	CustomerId	InvoiceDate	BillingAddress	BillingCity	BillingState	BillingCountry	BillingPostalCode	Total1	2	2021-01-01 00:00:00	Theodor-Heuss-Straße 34	Stuttgart	None	Germany	70174	1.982	4	2021-01-02 00:00:00	Ullevålsveien 14	Oslo	None	Norway	0171	3.963	8	2021-01-03 00:00:00	Grétrystraat 63	Brussels	None	Belgium	1000	5.94*/CREATE TABLE "InvoiceLine" (	"InvoiceLineId" INTEGER NOT NULL, 	"InvoiceId" INTEGER NOT NULL, 	"TrackId" INTEGER NOT NULL, 	"UnitPrice" NUMERIC(10, 2) NOT NULL, 	"Quantity" INTEGER NOT NULL, 	PRIMARY KEY ("InvoiceLineId"), 	FOREIGN KEY("TrackId") REFERENCES "Track" ("TrackId"), 	FOREIGN KEY("InvoiceId") REFERENCES "Invoice" ("InvoiceId"))/*3 rows from InvoiceLine table:InvoiceLineId	InvoiceId	TrackId	UnitPrice	Quantity1	1	2	0.99	12	1	4	0.99	13	2	6	0.99	1*/CREATE TABLE "MediaType" (	"MediaTypeId" INTEGER NOT NULL, 	"Name" NVARCHAR(120), 	PRIMARY KEY ("MediaTypeId"))/*3 rows from MediaType table:MediaTypeId	Name1	MPEG audio file2	Protected AAC audio file3	Protected MPEG-4 video file*/CREATE TABLE "Playlist" (	"PlaylistId" INTEGER NOT NULL, 	"Name" NVARCHAR(120), 	PRIMARY KEY ("PlaylistId"))/*3 rows from Playlist table:PlaylistId	Name1	Music2	Movies3	TV Shows*/CREATE TABLE "PlaylistTrack" (	"PlaylistId" INTEGER NOT NULL, 	"TrackId" INTEGER NOT NULL, 	PRIMARY KEY ("PlaylistId", "TrackId"), 	FOREIGN KEY("TrackId") REFERENCES "Track" ("TrackId"), 	FOREIGN KEY("PlaylistId") REFERENCES "Playlist" ("PlaylistId"))/*3 rows from PlaylistTrack table:PlaylistId	TrackId1	34021	33891	3390*/CREATE TABLE "Track" (	"TrackId" INTEGER NOT NULL, 	"Name" NVARCHAR(200) NOT NULL, 	"AlbumId" INTEGER, 	"MediaTypeId" INTEGER NOT NULL, 	"GenreId" INTEGER, 	"Composer" NVARCHAR(220), 	"Milliseconds" INTEGER NOT NULL, 	"Bytes" INTEGER, 	"UnitPrice" NUMERIC(10, 2) NOT NULL, 	PRIMARY KEY ("TrackId"), 	FOREIGN KEY("MediaTypeId") REFERENCES "MediaType" ("MediaTypeId"), 	FOREIGN KEY("GenreId") REFERENCES "Genre" ("GenreId"), 	FOREIGN KEY("AlbumId") REFERENCES "Album" ("AlbumId"))/*3 rows from Track table:TrackId	Name	AlbumId	MediaTypeId	GenreId	Composer	Milliseconds	Bytes	UnitPrice1	For Those About To Rock (We Salute You)	1	1	1	Angus Young, Malcolm Young, Brian Johnson	343719	11170334	0.992	Balls to the Wall	2	2	1	U. Dirkschneider, W. Hoffmann, H. Frank, P. Baltes, S. Kaufmann, G. Hoffmann	342562	5510424	0.993	Fast As a Shark	3	2	1	F. Baltes, S. Kaufman, U. Dirkscneider & W. Hoffman	230619	3990994	0.99*/
```

When we don't have too many, or too wide of, tables, we can just insert the entirety of this information in our prompt:
```
prompt_with_context = chain.get_prompts()[0].partial(table_info=context["table_info"])print(prompt_with_context.pretty_repr()[:1500])
```

```
You are a SQLite expert. Given an input question, first create a syntactically correct SQLite query to run, then look at the results of the query and return the answer to the input question.Unless the user specifies in the question a specific number of examples to obtain, query for at most 5 results using the LIMIT clause as per SQLite. You can order the results to return the most informative data in the database.Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.Pay attention to use date('now') function to get the current date, if the question involves "today".Use the following format:Question: Question hereSQLQuery: SQL Query to runSQLResult: Result of the SQLQueryAnswer: Final answer hereOnly use the following tables:CREATE TABLE "Album" (	"AlbumId" INTEGER NOT NULL, 	"Title" NVARCHAR(160) NOT NULL, 	"ArtistId" INTEGER NOT NULL, 	PRIMARY KEY ("AlbumId"), 	FOREIGN KEY("ArtistId") REFERENCES "Artist" ("ArtistId"))/*3 rows from Album table:AlbumId	Title	ArtistId1	For Those About To Rock We Salute You	12	Balls to the Wall	23	Restless and Wild	2*/CREATE TABLE "Artist" (	"ArtistId" INTEGER NOT NULL, 	"Name" NVARCHAR(120)
```

When we do have database schemas that are too large to fit into our model's context window, we'll need to come up with ways of inserting only the relevant table definitions into the prompt based on the user input. For more on this head to the Many tables, wide tables, high-cardinality feature guide.
## Few-shot examples​
Including examples of natural language questions being converted to valid SQL queries against our database in the prompt will often improve model performance, especially for complex queries.
Let's say we have the following examples:
```
examples =[{"input":"List all artists.","query":"SELECT * FROM Artist;"},{"input":"Find all albums for the artist 'AC/DC'.","query":"SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",},{"input":"List all tracks in the 'Rock' genre.","query":"SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",},{"input":"Find the total duration of all tracks.","query":"SELECT SUM(Milliseconds) FROM Track;",},{"input":"List all customers from Canada.","query":"SELECT * FROM Customer WHERE Country = 'Canada';",},{"input":"How many tracks are there in the album with ID 5?","query":"SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",},{"input":"Find the total number of invoices.","query":"SELECT COUNT(*) FROM Invoice;",},{"input":"List all tracks that are longer than 5 minutes.","query":"SELECT * FROM Track WHERE Milliseconds > 300000;",},{"input":"Who are the top 5 customers by total purchase?","query":"SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",},{"input":"Which albums are from the year 2000?","query":"SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",},{"input":"How many employees are there","query":'SELECT COUNT(*) FROM "Employee"',},]
```

We can create a few-shot prompt with them like so:
```
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplateexample_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")prompt = FewShotPromptTemplate(  examples=examples[:5],  example_prompt=example_prompt,  prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",  suffix="User input: {input}\nSQL query: ",  input_variables=["input","top_k","table_info"],)
```

**API Reference:**FewShotPromptTemplate | PromptTemplate
```
print(prompt.format(input="How many artists are there?", top_k=3, table_info="foo"))
```

```
You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than 3 rows.Here is the relevant table info: fooBelow are a number of examples of questions and their corresponding SQL queries.User input: List all artists.SQL query: SELECT * FROM Artist;User input: Find all albums for the artist 'AC/DC'.SQL query: SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');User input: List all tracks in the 'Rock' genre.SQL query: SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');User input: Find the total duration of all tracks.SQL query: SELECT SUM(Milliseconds) FROM Track;User input: List all customers from Canada.SQL query: SELECT * FROM Customer WHERE Country = 'Canada';User input: How many artists are there?SQL query:
```

## Dynamic few-shot examples​
If we have enough examples, we may want to only include the most relevant ones in the prompt, either because they don't fit in the model's context window or because the long tail of examples distracts the model. And specifically, given any input we want to include the examples most relevant to that input.
We can do just this using an ExampleSelector. In this case we'll use a SemanticSimilarityExampleSelector, which will store the examples in the vector database of our choosing. At runtime it will perform a similarity search between the input and our examples, and return the most semantically similar ones.
We default to OpenAI embeddings here, but you can swap them out for the model provider of your choice.
```
from langchain_community.vectorstores import FAISSfrom langchain_core.example_selectors import SemanticSimilarityExampleSelectorfrom langchain_openai import OpenAIEmbeddingsexample_selector = SemanticSimilarityExampleSelector.from_examples(  examples,  OpenAIEmbeddings(),  FAISS,  k=5,  input_keys=["input"],)
```

**API Reference:**FAISS | SemanticSimilarityExampleSelector | OpenAIEmbeddings
```
example_selector.select_examples({"input":"how many artists are there?"})
```

```
[{'input': 'List all artists.', 'query': 'SELECT * FROM Artist;'}, {'input': 'How many employees are there', 'query': 'SELECT COUNT(*) FROM "Employee"'}, {'input': 'How many tracks are there in the album with ID 5?', 'query': 'SELECT COUNT(*) FROM Track WHERE AlbumId = 5;'}, {'input': 'Which albums are from the year 2000?', 'query': "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';"}, {'input': "List all tracks in the 'Rock' genre.", 'query': "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');"}]
```

To use it, we can pass the ExampleSelector directly in to our FewShotPromptTemplate:
```
prompt = FewShotPromptTemplate(  example_selector=example_selector,  example_prompt=example_prompt,  prefix="You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than {top_k} rows.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries.",  suffix="User input: {input}\nSQL query: ",  input_variables=["input","top_k","table_info"],)
```

```
print(prompt.format(input="how many artists are there?", top_k=3, table_info="foo"))
```

```
You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run. Unless otherwise specificed, do not return more than 3 rows.Here is the relevant table info: fooBelow are a number of examples of questions and their corresponding SQL queries.User input: List all artists.SQL query: SELECT * FROM Artist;User input: How many employees are thereSQL query: SELECT COUNT(*) FROM "Employee"User input: How many tracks are there in the album with ID 5?SQL query: SELECT COUNT(*) FROM Track WHERE AlbumId = 5;User input: Which albums are from the year 2000?SQL query: SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';User input: List all tracks in the 'Rock' genre.SQL query: SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');User input: how many artists are there?SQL query:
```

Trying it out, we see that the model identifies the relevant table:
```
chain = create_sql_query_chain(llm, db, prompt)chain.invoke({"question":"how many artists are there?"})
```

```
'SELECT COUNT(*) FROM Artist;'
```

#### Was this page helpful?
  * Setup
  * Dialect-specific prompting
  * Table definitions and example rows
  * Few-shot examples
  * Dynamic few-shot examples


