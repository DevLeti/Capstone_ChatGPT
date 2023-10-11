import dotenv
import os
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import ChatPromptTemplate
import getArticle

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# User keyword
'''
추후 Keyword Generation 매칭 필요
'''
user_keyword = input()

# getArticles
search_result = getArticle.searchArticle(user_keyword)
article_links = getArticle.getOnlyNaverLinks(search_result)
article_list = getArticle.getArticleDetailBulk(article_links)
article_string = ""
for article in article_list:
    article_string += article
    article_string += ", "
article_string = article_string[:-1]

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