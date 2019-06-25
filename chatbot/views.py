import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from konlpy.tag import Kkma


#  ------------------------ Fill this with your page access token! -------------------------------
PAGE_ACCESS_TOKEN = "EAAEYZClBnc0YBALJOSz1ZCcJBtpca1IzKRVdbu5ivrdHQ6CZC0ZBBBCTbNPPjyuT3e3nBJMzi2bUZCR33YMhpEKitayYic9w7MT1whUDhER4igC1i4ZBMSop6esJbegEbdOk7Pkf2F1sTO2S3yogOLgWgJGvVZCf6Y7AzrYx8RWcEWltHTH6pkM"
VERIFY_TOKEN = "1234567890"


questions = {
        '기간': ["""2019.03 - 2020.02\n(1년 활동 후 수료증 발급)"""],
        '대상': ["""명지대 인문캠퍼스 재학생/휴학생 중 웹 서비스를 만들고 싶은 사람 누구나!!\n\n1년 동안 꾸준히, 열심히, 열정적으로 활동 할 수 있는 사람을 모집합니다!!"""],
        '모집': ["""1차 서류 접수 기간\n2019.02.20 – 2019.03.07\n2차 면접\n2019.03.09 – 2019.03.12\n결과 발표\n2019.03.13"""],
        '활동': ["""HTML & CSS (Bootstrap)\nPython\nDjango 를 이용한 웹사이트 개발\n주 1회 또는 2회 세션 진행"""],
        '지원': ["""지원 기간이 아닙니다."""],
        '문의': ["""자세한 문의는 카카오톡 플러스친구(@likelionmyongji)를 통해 주시면 감사하겠습니다."""],
        'mju': ["""■□□□■\n■■□■■\n■□■□■\n■□□□■\n■□□□■\n□□□□□\n□□□□■\n□□□□■\n□□□□■\n■□□□■\n□■■■□\n□□□□□\n■□□□■\n■□□□■\n■□□□■\n■□□□■\n□■■■□\n"""]
            }


# Helper function
def post_facebook_message(fbid, recevied_message):
    # Use KoNLPy
    kkma = Kkma()
    tokens = kkma.morphs(recevied_message)
    question_text = ''
    for token in tokens:
        if token in questions:
            question_ans = random.choice(questions[token])
            question_text += question_ans + "\n\n"
    if not question_text:
        question_text = "안녕하세요, 명지대학교(서울)\n멋쟁이 사자처럼 챗봇입니다.\n기간, 대상, 모집, 활동, 지원, 문의\n중에서 원하는 키워드를 넣어서\n질문해주세요."

    '''
    # 유저 이름 출력(오류 발생, 구현 예정)
    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN}
    user_details = requests.get(user_details_url, user_details_params).json()
    question_text = '질문 주셔서 감사합니다, '+user_details['first_name']+'님!' + question_text
    '''

    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":question_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())

# Create your views here.
class chatbotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle Facebook messages
    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    # Assuming the sender only sends text. Non-text messages like stickers, audio, pictures
                    # are sent as attachments and must be handled accordingly.
                    try:
                        post_facebook_message(message['sender']['id'], message['message']['text'])
                    except:
                        print("따봉")
        return HttpResponse()
