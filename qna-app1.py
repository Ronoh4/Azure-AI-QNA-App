import streamlit as st
from dotenv import load_dotenv
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient

# Get Configuration Settings
load_dotenv()
ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
ai_key = os.getenv('AI_SERVICE_KEY')
ai_project_name = os.getenv('QA_PROJECT_NAME')
ai_deployment_name = os.getenv('QA_DEPLOYMENT_NAME')

# Create client using endpoint and key
credential = AzureKeyCredential(ai_key)
ai_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)

def get_answer(user_question):
    try:
        # Submit a question and get the answer
        response = ai_client.get_answers(question=user_question,
                                        project_name=ai_project_name,
                                        deployment_name=ai_deployment_name)
        answers = []
        for candidate in response.answers:
            answers.append({
                'answer': candidate.answer,
                'confidence': candidate.confidence,
                'source': candidate.source
            })
        return answers
    except Exception as ex:
        st.write(str(ex))

def main():
    st.title('Question Answering App')
    user_question = st.text_input('Enter your question here:')
    if st.button('Send'):
        if user_question:
            answers = get_answer(user_question)
            for answer in answers:
                st.write(f"Answer: {answer['answer']}")
                st.write(f"Confidence: {answer['confidence']}")
                st.write(f"Source: {answer['source']}")
        else:
            st.write('Please enter a question.')

if __name__ == "__main__":
    main()
