from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from pathlib import Path
from llama_index import download_loader
CJKPDFReader = download_loader("CJKPDFReader")

from file import get_index_filepath, get_index_name_from_file_name, check_index_file_exists
from llm import get_index_by_index_name
from prompt import get_prompt, get_trans_prompt
import googletrans
from googletrans import Translator

def check_llama_index_exists(file_name):
    index_name = get_index_name_from_file_name(file_name)
    return check_index_file_exists(index_name)



def create_llama_index(filepath):
    index_name = get_index_name_from_file_name(filepath)
    documents = SimpleDirectoryReader(input_files=[filepath]).load_data()
    # loader = CJKPDFReader()
    # documents = loader.load_data(file=filepath)
    index = GPTSimpleVectorIndex.from_documents(documents)

    index.save_to_disk(get_index_filepath(index_name))
    return index_name


def get_answer_from_llama_index(text, index_name):
    index = get_index_by_index_name(index_name)
    answer = index.query(text, text_qa_template=get_prompt())
    return answer
