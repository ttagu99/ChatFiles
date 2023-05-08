from llama_index.prompts.prompts import QuestionAnswerPrompt
from googletrans import Translator

DEFAULT_PROMPT = (
    "아래에 한국어로 만들어진 문서를 제공하겠습니다.: \n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "이 문서에서 정보를 찾아서 요구사항에 대해 한국어로 답변하세요.\n"
    "답변에 참조한 페이지 번호를 답변 마지막에 (참조: 페이지 번호) 형식으로 적어주세요.\n"
    "영어로 답변하지 말고 한국어로 답변해줘. 만약 영어로 답변 나왔다면 한국어로 번역해서 답변해주세요.\n"
    "아래 예시와 비슷한 요구사항을 받았을때는 '기존 답변은 그대로 유지합니다','원래 답변은 반복합니다' 라는 답변은 하지말고, 다시 한번 친절하게 답변해주세요.\n"
    "아래는 요구사항과 답변에 대한 예시입니다.\n"
    "---------------------\n"
    "요구사항 : 크라운 치료는 매년 몇개까지 보장 받을 수 있어?\n"
    "답변 : 매년 크라운 치료는 3개까지 보장 받을 수 있습니다. (참조:8/152페이지)\n"    
    "요구사항 : 보험 가입 후 60일 이내에 치료 받으면 보장 받을 수 있어?\n"
    "답변 : 보험 가입 후 90일간은 면책기간에 해당합니다. 면책기간 동안은 보장 제외 됩니다.(참조:9/30페이지)\n"     
    "---------------------\n"
    "요구사항 : {query_str}\n"
)


TRANS_PROMPT = (
    "영어 답변을 한국어로 번역해줘: \n"
    "---------------------\n"
    "{query_str}\n"
)


# DEFAULT_PROMPT = (
#     "We have provided context information below: \n"
#     "---------------------\n"
#     "{context_str}\n"
#     "---------------------\n"
#     "Given this information, Please answer my question in the same language that I used to ask you.\n"
#     "Please answer the question: {query_str}\n"
# )

def get_prompt():
    return QuestionAnswerPrompt(DEFAULT_PROMPT)

def get_trans_prompt():
    return QuestionAnswerPrompt(TRANS_PROMPT)

