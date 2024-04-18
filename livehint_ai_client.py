import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")
API_TIMEOUT=0.5

if API_BASE_URL is None:
    raise ValueError("API_BASE_URL is not defined")

if API_BEARER_TOKEN is None:
    raise ValueError("API_BEARER_TOKEN is not defined")


def get_problem_info(course, module, page, question):
    params = {
        "qr_course": course,
        "qr_module": module,
        "qr_page": page,
        "qr_question": question
    }
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}
    url = f"{API_BASE_URL}/problem-info"

    # Make problem-info GET request to LiveHint AI
    response = requests.get(url, headers=headers, params=params, timeout=API_TIMEOUT)
    response.raise_for_status()

    # Extract data from the response
    data = response.json()
    problem_id = data.get("problem_id")
    tutorbot = data.get("tutorbot")
    return problem_id, tutorbot


def create_session(problem_id, tutorbot):
    # Make session POST request to LiveHint AI
    session_id = "my_session_id"
    return session_id


def updated_session(session_id):
    # Make sessions/<session_id> PUT request to LiveHint AI
    return None


def init(course, module, page, question):
    problem_id, tutorbot = get_problem_info(course, module, page, question)
    session_id = create_session(problem_id, tutorbot)
    updated_session(session_id)
    return session_id


def get_chat_response(session_id, message):
    data = "response.json()"
    return data