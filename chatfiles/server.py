import os
from flask import Flask, request, make_response
from chat import create_llama_index, get_answer_from_llama_index, check_llama_index_exists
from file import get_index_name_without_json_extension
from file import get_index_path, get_index_name_from_file_name, check_index_file_exists, \
    get_index_name_with_json_extension
from difflib import SequenceMatcher
from googletrans import Translator


app = Flask(__name__)



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Please send a POST request with a file", 400
    filepath = None
    try:
        uploaded_file = request.files["file"]

        filename = uploaded_file.filename
        filepath = os.path.join(get_index_path(), os.path.basename(filename))

        if check_llama_index_exists(filepath) is True:
            return get_index_name_without_json_extension(get_index_name_from_file_name(filepath))

        uploaded_file.save(filepath)

        index_name = create_llama_index(filepath)

        # cleanup temp file
        if filepath is not None and os.path.exists(filepath):
            os.remove(filepath)

        return get_index_name_without_json_extension(index_name)
    except Exception as e:
        # cleanup temp file
        if filepath is not None and os.path.exists(filepath):
            os.remove(filepath)
        return "Error: {}".format(str(e)), 500

# @app.route('/upload', methods=['POST'])
# def batch_upload_files():
#     if 'files' not in request.files:
#         return "Please send a POST request with files", 400
#     filepaths = []
#     try:
#         files = request.files.getlist("files")
#         for uploaded_file in files:
#             filename = uploaded_file.filename
#             filepath = os.path.join(get_index_path(), os.path.basename(filename))
#             if check_llama_index_exists(filepath) is True:
#                 filepaths.append(get_index_name_without_json_extension(get_index_name_from_file_name(filepath)))
#                 continue

#             uploaded_file.save(filepath)
#             index_name = create_llama_index(filepath)

#             # cleanup temp file
#             if filepath is not None and os.path.exists(filepath):
#                 os.remove(filepath)
#             filepaths.append(get_index_name_without_json_extension(index_name))

#         return filepaths
#     except Exception as e:
#         # cleanup temp files
#         for filepath in filepaths:
#             if filepath is not None and os.path.exists(filepath):
#                 os.remove(filepath)
#         return "Error: {}".format(str(e)), 500




@app.route('/query', methods=['GET'])
def query_from_llama_index():
    try:
        message = request.args.get('message')
        index_name = request.args.get('indexName')
        index_name = get_index_name_with_json_extension(index_name)

        if check_index_file_exists(index_name) is False:
            return "Index file does not exist", 404

        answer = get_answer_from_llama_index(message, index_name)
        
        
        pre_set_answers = []   
        pre_set_answers.append({'요구사항': '첫급여 우리적금의 금리는 얼마야?','답변': '첫급여 우리적금의 최고금리는 세금납부 전 연 3.40%이며, 기본금리(연2.3%)와 우대금리(연1.1%p)로 구성됩니다. 우대금리는 급여이체실적 충족월이 9개월 이상일 경우에 1.1%p까지 적용됩니다. 단, 자세한 우대금리 요건은 적립식 상품의 세부설명서를 확인하시기 바랍니다. (참조: 2022.03.02. 준법감시인 -1956-2 심의필 본문)',})
        pre_set_answers.append({'요구사항': '첫급여 우리적금의 급여이체실적 충족 기준은 뭐야?', '답변': '첫급여 우리적금의 급여이체실적 충족 기준은 아래와 같습니다.\n\n 1. 고객이 지정한 이체일 기준으로 50만원 이상 입금한 경우 \n 2. 적요란의 문구에 “급여”, “월급”, “급료”, “수당”이 인쇄된 이체실적이 월 50만원 이상인 경우 \n 3. 적요란의 문구에 고객기본정보의 직장명과 동일하게 인쇄된 이체실적이 월 50만원 이상인 경우 \n 감사합니다.'})
        pre_set_answers.append({'요구사항': '첫급여 우리적금의 중도 해지 이율은 얼마야?', '답변': '첫급여 우리적금의 중도해지이율은 예치기간에 따라 적용되며, 예치기간이 3개월 미만인 경우는 연 0.1%, 예치기간이 3개월 이상 ~ 6개월 미만인 경우에는 기본이율의 50%에 해당하는 이율이 적용됩니다. 예치기간이 6개월 이상 ~ 9개월 미만인 경우는 연 0.15%, 예치기간이 9개월 이상 ~ 11개월 미만인 경우는 기본이율이 적용됩니다. 예치기간이 11개월 이상인 경우에는 기본이율의 90%×보유일수/계약일수에 해당하는 이율이 적용됩니다.(참고:4/8페이지)'})
        # message의 charactor들을 pre_set_answers의 요구사항과 비교해서 80% 이상 일치하면 정해진 pre_set_answers를 return
        # space는 삭제하고 비교
        # 80% 미만이면 answer를 return
        
        for pre_set_answer in pre_set_answers:
            if is_similar(message, pre_set_answer['요구사항']):
                print('pre_set_answer: ', pre_set_answer['답변'])
                return pre_set_answer['답변'], 200
  
        ret_message = str(answer.response)
        print('answer: ', ret_message)
        # 한국어가 아닌지 체크 후 번역
        tr = Translator( )
        if tr.detect(ret_message).lang != 'ko':
            ret_message = tr.translate(ret_message, src='en', dest='ko').text
        return make_response(ret_message), 200
    except Exception as e:
        return "Error: {}".format(str(e)), 500

# 문자열이 space를 제외하고 80% 이상 일치하는지 확인
def is_similar(str1, str2):
    str1 = str1.replace(' ', '')
    str2 = str2.replace(' ', '')
    if len(str1) > len(str2):
        print('sequence macher',SequenceMatcher(None, str1, str2).ratio())
        return SequenceMatcher(None, str1, str2).ratio() > 0.8
    else:
        print('sequence macher',SequenceMatcher(None, str2, str1).ratio())
        return SequenceMatcher(None, str2, str1).ratio() > 0.8

if __name__ == '__main__':
    if not os.path.exists('./documents'):
        os.makedirs('./documents')
    if (os.environ.get('CHAT_FILES_MAX_SIZE') is not None):
        app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('CHAT_FILES_MAX_SIZE'))
    app.run(port=5001, host='0.0.0.0')
