from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain ,  SequentialChain
from dotenv import load_dotenv
import os 

load_dotenv()

api_key = os.getenv("Groq_api_key")
if not api_key:
    raise ValueError("API key not found in environment variables")

model = 'openai/gpt-oss-20b'
llm = ChatGroq(model = model, groq_api_key = api_key,temperature=0.6)

from langchain_core.prompts import PromptTemplate


def get_president_info(country_name):
    prompt_template_name = PromptTemplate(
    input_variables=['country'],
    template = "What is the name of the president of {country}"
    )

    prompt_template_age = PromptTemplate(
        input_variables = ['president_name'],
        template = "What is the age of {president_name}"
    )

    name_chain = LLMChain(
    llm = llm,
    prompt = prompt_template_name,
    output_key = 'president_name'
    )

    age_chain = LLMChain(
        llm = llm,
        prompt = prompt_template_age,
        output_key = 'age'
    )

    sequential_chain = SequentialChain(
    chains = [name_chain, age_chain],
    input_variables = ['country'],
    output_variables = ['president_name', 'age']
    )

    response = sequential_chain.invoke({"country": country_name})
    return response
