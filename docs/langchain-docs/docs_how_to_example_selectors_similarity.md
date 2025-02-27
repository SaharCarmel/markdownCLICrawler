Skip to main content
**Join us at Interrupt: The Agent AI Conference by LangChain on May 13 & 14 in San Francisco!**
![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)![Open on GitHub](https://img.shields.io/badge/Open%20on%20GitHub-grey?logo=github&logoColor=white)
This object selects examples based on similarity to the inputs. It does this by finding the examples with the embeddings that have the greatest cosine similarity with the inputs.
```
from langchain_chroma import Chromafrom langchain_core.example_selectors import SemanticSimilarityExampleSelectorfrom langchain_core.prompts import FewShotPromptTemplate, PromptTemplatefrom langchain_openai import OpenAIEmbeddingsexample_prompt = PromptTemplate(  input_variables=["input","output"],  template="Input: {input}\nOutput: {output}",)# Examples of a pretend task of creating antonyms.examples =[{"input":"happy","output":"sad"},{"input":"tall","output":"short"},{"input":"energetic","output":"lethargic"},{"input":"sunny","output":"gloomy"},{"input":"windy","output":"calm"},]
```

**API Reference:**SemanticSimilarityExampleSelector | FewShotPromptTemplate | PromptTemplate | OpenAIEmbeddings
```
example_selector = SemanticSimilarityExampleSelector.from_examples(# The list of examples available to select from.  examples,# The embedding class used to produce embeddings which are used to measure semantic similarity.  OpenAIEmbeddings(),# The VectorStore class that is used to store the embeddings and do a similarity search over.  Chroma,# The number of examples to produce.  k=1,)similar_prompt = FewShotPromptTemplate(# We provide an ExampleSelector instead of examples.  example_selector=example_selector,  example_prompt=example_prompt,  prefix="Give the antonym of every input",  suffix="Input: {adjective}\nOutput:",  input_variables=["adjective"],)
```

```
# Input is a feeling, so should select the happy/sad exampleprint(similar_prompt.format(adjective="worried"))
```

```
Give the antonym of every inputInput: happyOutput: sadInput: worriedOutput:
```

```
# Input is a measurement, so should select the tall/short exampleprint(similar_prompt.format(adjective="large"))
```

```
Give the antonym of every inputInput: tallOutput: shortInput: largeOutput:
```

```
# You can add new examples to the SemanticSimilarityExampleSelector as wellsimilar_prompt.example_selector.add_example({"input":"enthusiastic","output":"apathetic"})print(similar_prompt.format(adjective="passionate"))
```

```
Give the antonym of every inputInput: enthusiasticOutput: apatheticInput: passionateOutput:
```

#### Was this page helpful?
