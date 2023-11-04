import dotenv
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
from langchain.prompts import PromptTemplate
import getArticle

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# User keyword
'''
추후 Keyword Generation 매칭 필요
'''
user_keyword = input()

my_template = """아래의 질문을 몇가지 키워드로 요약해줘.
질문: {question}"""

prompt = PromptTemplate.from_template(my_template)
prompt.format(question="아이유 몇살이야?")

api_key = os.environ["OPENAI_API_CD"]
chat_model = ChatOpenAI(openai_api_key=api_key)
keyword = chat_model.predict(prompt.format(question=user_keyword))
print(keyword)

# getArticles
search_result = getArticle.searchArticle(user_keyword)
article_links = getArticle.getOnlyNaverLinks(search_result)
article_list = getArticle.getArticleDetailBulk(article_links)
article_string = ""
# for article in article_list:
#     article_string += article
#     article_string += ", "
for i in range (0,len(article_list)):
    article_string += f"\n{i+1}번째 기사:"
    article_string += article_list[i].strip('\n')
    article_string += "\n"
print(article_string)

print("GET ARTICLE COMPLETE")

# LLMs: this is a language model which takes a string as input and returns a string
llm = OpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])
# ChatModels: this is a language model which takes a list of messages as input and returns a message
chat_model = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"])

# TODO: Template 작성
template = "당신은 주어진 articles를 기반으로 question을 답해야 합니다.\
            답할 수 있는 경우 답과 함께 근거 article를 붙여 서술하고,\
            알 수 없는 경우 '모르겠습니다.'라고 답변하세요."
human_template = "articles: {articles},\n" \
                  "question: {question_keyword}"

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", template),
    ("human", human_template),
])

chain = chat_prompt | chat_model

# content='나는 프로그래밍을 사랑합니다.' additional_kwargs={} example=False
result = chain.invoke({"articles":article_string[0:3500],"question_keyword":user_keyword})
print(result.content)