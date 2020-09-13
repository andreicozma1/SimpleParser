import difflib
from bs4 import BeautifulSoup
import requests

class QuizletParser():
    def __init__(self, url, query):
        print("###############################################")
        print("URL: ", url)
        print("Query: ", query)

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
            question = i.find('a', class_='SetPageTerm-wordText').find('span').decode_contents().replace("<br/>","")
            answer = i.find('a', class_='SetPageTerm-definitionText').find('span').decode_contents().replace("<br/>","")
            questions.append(question)
            questionsAnswers[question] = answer
        return questions,questionsAnswers

    def match(self, q, qA, query):
        matches = difflib.get_close_matches(query, q, True, 0.02)
        print("Matching Queries: ", len(matches))

        for i in matches:
            print("############")
            print("    Question:")
            print("       = ", i)
            print("    Answer:")
            print("       = ", qA[i])

        print("############")
        print()


# reads a question from stdin and returns it as a string
def getQuestion(prompt=""):
    print(prompt, end='')

    # read until there a line is only a new line and append to query str
    question = ''
    while True:
        line = input()
        if len(line.split()) == 0:
            break
        line = line.replace('\n', '')
        question += ' ' + line
    question = question.split(" ")

    # delete any words in query less than 4 characters
    for w in question:
        if len(w) < 4:
            question.remove(w)
    question = ' '.join([str(elem) for elem in question])
    return question


# takes a string and queries google then returns a list of tuples with the link and question
def getGoogleResults(query, accepted_sites):
    # search google
    req = requests.get('http://google.com/search?q='+query)
    soup = BeautifulSoup(req.content, 'html.parser')
    a = soup.find_all('a', href=True)

    # gather all of the links
    links = []
    for l in a:
        links.append(l.get('href').replace("/url?q=", ''))

    # parse the links for accepted sites
    sites = []
    for l in links:
        for a in accepted_sites:
            if a in l:
                sites.append(l)

    return sites, query


# get list of relevant sites

while True:
    sites, query = getGoogleResults(getQuestion(), ['quizlet'])

    for s in sites:
        qp = QuizletParser(s, query)
    print("###############################################")
    print("###############################################")
    print("###############################################")



