import os
import openai
from langchain.chat_models import ChatOpenAI
from llama_index import LLMPredictor, GPTSimpleVectorIndex, ServiceContext

from file import check_index_file_exists, get_index_filepath
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

llm_predictor = LLMPredictor(llm=ChatOpenAI(
    temperature=0.0, model_name="gpt-3.5-turbo"))
service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)


def get_index_by_index_name(index_name):
    if check_index_file_exists(index_name) is False:
        return None
    index_filepath = get_index_filepath(index_name)
    index = GPTSimpleVectorIndex.load_from_disk(index_filepath, service_context=service_context)
    return index
