import requests
import difflib
from bs4 import BeautifulSoup

class QuizletParser():
    def __init__(self, url, query):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.content, "html.parser")
        q, qA = self.parse(soup)
        self.match(q, qA, query)

    def parse(self, soup):
        job_elems = soup.find_all('div', class_='SetPageTerms-term')
        questions = []
        questionsAnswers = {}
        for i in job_elems:
            question = i.find('a', class_='SetPageTerm-wordText').find('span').decode_contents().replace("<br/>","\n")
            answer = i.find('a', class_='SetPageTerm-definitionText').find('span').decode_contents().replace("<br/>","\n")
            questions.append(question)
            questionsAnswers[question] = answer
        return questions,questionsAnswers

    def match(self, q, qA, query):
        matches = difflib.get_close_matches(query, q)
        print(query)
        for i in matches:
            print("Question")
            print(i)
            print("Answer")
            print(qA[i])

qp = QuizletParser("https://quizlet.com/71390125/chapter-2-flash-cards/", "1) Every financial market performs the following function:A) It determines the level of interest rates.B) It allows common stock to be traded.C) It allows loans to be made.D) It channels funds from lenders-savers to borrowers-spenders.")



