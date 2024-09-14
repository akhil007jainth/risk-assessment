import anthropic
import os
from PyPDF2 import PdfReader
import re
import json


def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


class PdfPromptExecutor:

    def __init__(self, pdf_content=None):
        self.pdf_content = pdf_content

    def user_prompt(self):
        user_prompt = f"""
        Please analyze the following PDF content and extract key information, and generate 13 questions that test understanding of the material provided. 
        For each question, provide four answers, all answers are correct but different weightage, so give questions and answers and all 13 questions score will be 100.

        example:
          1) first question
            a) answer 1, score = 5 > can be diff
            b) answer 2, score  = 3 > can be diff
            c) answer 3, score  = 9 > can be diff
            d) answer 4, score  = 5 > can be diff
          2) second question
            a) answer 1, score  = 5 > can be diff
            b) answer 2, score = 3 > can be diff
            c) answer 3, score = 9 > can be diff
            d) answer 4, score = 5 > can be diff

        ... and so on for all other questions. 

        in the end, provide these questions and answers in json like below

        [{{
        "question":"question 1",
        "answers":[
            {{"A":"option1", "score":5}},
            {{"B":"option2", "score":6}},
            {{"C":"option3", "score":9}},
            {{"D":"option4", "score":5}}
            ]
        }},

        {{
            "question":"question 2",
            "answers":[
                {{"A":"option1", "score":5}},
                {{"B":"option2", "score":6}},
                {{"C":"option3", "score":9}},
                {{"D":"option4", "score":5}}
            ]
        }}
        ]


        PDF Content:
        {self.pdf_content}
        """

        return user_prompt

    @staticmethod
    def system_prompt():
        system_prompt = """
        You are an expert in analyzing documents and creating insightful questions. Your task is to read the provided PDF content, extract key information, and generate questions that test understanding of the material. For each question, provide a concise answer and assign a score according to Rubric-Based Grading System (Total score = 100 marks)
        """
        return system_prompt

    @staticmethod
    def anthropic_client():
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
        return client

    @classmethod
    def execute(cls, pdf_content):
        obj = cls(pdf_content)

        message = obj.anthropic_client().messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            system=obj.system_prompt(),
            messages=[
                {"role": "user", "content": obj.user_prompt()}
            ]
        )
        generated_questions = message.content[0].text

        return obj.format_data(generated_questions)

    def format_data(self, generated_questions):
        data = re.findall(r"(\[.*)", generated_questions, re.DOTALL)[0]
        actual_data = json.loads(data)

        return actual_data


class CalculatePromptExecutor:

    def __init__(self, answers, questions):
        self.answers = answers
        self.questions = questions

    def user_prompt(self):
        user_prompt = f"""
        Please calculate the score on behalf of questions and answers we provide
        
        answers are provided with unique question_id key with answer option
        
        inputs:
        
        questions
        {self.questions}
        
        Answers
        {self.answers}
        
        please provide calculated score in json
        - total_score
        - max_score
        - percentage
        
        """

        return user_prompt

    @staticmethod
    def system_prompt():
        system_prompt = """
        You are an expert in analyzing documents and calculate insightful questions. Your task is to calculate the score on behave of answers and questions
        """
        return system_prompt

    @staticmethod
    def anthropic_client():
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
        return client

    @classmethod
    def execute(cls, answers, questions):
        obj = cls(answers, questions)

        message = obj.anthropic_client().messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=4000,
            system=obj.system_prompt(),
            messages=[
                {"role": "user", "content": obj.user_prompt()}
            ]
        )
        generated_questions = message.content[0].text

        return obj.format_data(generated_questions)

    def format_data(self, generated_questions):
        data = re.findall(r"\{.*?\}", generated_questions, re.DOTALL)[0]
        actual_data = json.loads(data)

        return actual_data


