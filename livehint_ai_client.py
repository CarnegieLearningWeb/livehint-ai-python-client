import os
import requests
from dotenv import load_dotenv
from enum import Enum
import json
from urllib.parse import quote

class APIExceptionType(Enum):
    TIMEOUT = 1
    HTTP_ERROR = 2
    CONNECTION_ERROR = 3
    REQUEST_ERROR = 4
    UNEXPECTED_ERROR = 5

class APIException(Exception):
    def __init__(self, exception_type, message):
        self.exception_type = exception_type
        self.message = message

    def __str__(self):
        return f"{self.exception_type.name}: {self.message}"

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")
API_TIMEOUT= 3
API_TUTORBOT_TYPE = "solver_bot"
API_VALID_APP_CONTEXTS = ["mathbook_tx", "mathstream"]
API_DEFAULT_APP_CONTEXT = "mathbook_tx"
API_SUPPORTED_MODELS = ["gpt-4o", "gpt-4-0125-preview", "gpt-4-1106-preview", "gpt-4-0613", "claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
API_DEFAULT_MODEL = "gpt-4-0613"
API_DEFAULT_TEMPERATURE = 0.3
API_DEFAULT_STREAM = True

if API_BASE_URL is None:
    raise ValueError("API_BASE_URL is not defined")

if API_BEARER_TOKEN is None:
    raise ValueError("API_BEARER_TOKEN is not defined")


def get_problem_info(app_context, course, module, page, question, item_id):
    params = {
        "app_context": app_context,
        "qr_course": course,
        "qr_module": module,
        "qr_page": page,
        "qr_question": question,
        "item_id": item_id
    }
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}
    url = f"{API_BASE_URL}/api/problem-info"

    # Make problem-info GET request to LiveHint AI
    try:
        response = requests.get(url, headers=headers, params=params, timeout=API_TIMEOUT)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        raise APIException(APIExceptionType.TIMEOUT, "Timeout occurred during API request")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error ({e.response.status_code}): {e.response.reason}")
        raise APIException(APIExceptionType.HTTP_ERROR, f"HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your network connection.")
        raise APIException(APIExceptionType.CONNECTION_ERROR, "Connection error during API request")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
        raise APIException(APIExceptionType.REQUEST_ERROR, f"Request error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise APIException(APIExceptionType.UNEXPECTED_ERROR, f"Unexpected error: {str(e)}")

    # Extract data from the response
    data = response.json()
    problem_id = data.get("problem_id")
    tutorbot = data.get("tutorbot")
    return problem_id, tutorbot


def create_session(app_context, problem_id, tutorbot):
    request_data = {
        "app_context": app_context,
        "problem_id": problem_id,
        "tutorbot": tutorbot
    }
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}
    url = f"{API_BASE_URL}/api/session"

    # Make session POST request to LiveHint AI
    try:
        response = requests.post(url, json=request_data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        raise APIException(APIExceptionType.TIMEOUT, "Timeout occurred during API request")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error ({e.response.status_code}): {e.response.reason}")
        raise APIException(APIExceptionType.HTTP_ERROR, f"HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your network connection.")
        raise APIException(APIExceptionType.CONNECTION_ERROR, "Connection error during API request")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
        raise APIException(APIExceptionType.REQUEST_ERROR, f"Request error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise APIException(APIExceptionType.UNEXPECTED_ERROR, f"Unexpected error: {str(e)}")

    # Extract data from the response
    data = response.json()
    session_id = data.get("session_id")
    return session_id


def update_session(session_id, model, temperature):
    request_data = {
        "model": model,
        "stream": False,
        "temperature": temperature,
        "tutorbot_type": API_TUTORBOT_TYPE
    }
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}
    url = f"{API_BASE_URL}/api/sessions/{session_id}"
    

    # Make sessions/<session_id> PUT request to LiveHint AI
    try:
        response = requests.put(url, json=request_data, headers=headers)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        raise APIException(APIExceptionType.TIMEOUT, "Timeout occurred during API request")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error ({e.response.status_code}): {e.response.reason}")
        raise APIException(APIExceptionType.HTTP_ERROR, f"HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your network connection.")
        raise APIException(APIExceptionType.CONNECTION_ERROR, "Connection error during API request")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
        raise APIException(APIExceptionType.REQUEST_ERROR, f"Request error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise APIException(APIExceptionType.UNEXPECTED_ERROR, f"Unexpected error: {str(e)}")

    return None

# helper function
def parse_stream_response(stream_content):
    result = []
    for line in stream_content.splitlines():
        if line:
            line = line.decode('utf-8')
            if line.startswith('data:'):
                data = line[5:].strip()
                try:
                    message_data = json.loads(data)
                    result.append(message_data)
                except json.JSONDecodeError:
                    print(f"Error decoding JSON: {data}")
            # normally wouldn't have lines below
            elif line.strip() == 'event: done':
                break

    return result

# called at the beginning; called once for each chat
def init(app_context, course=None, module=None, page=None, question=None, item_id=None, model=API_DEFAULT_MODEL, temperature=API_DEFAULT_TEMPERATURE):
    problem_id, tutorbot = get_problem_info(app_context, course, module, page, question, item_id)
    session_id = create_session(app_context, problem_id, tutorbot)
    update_session(session_id, model, temperature)
    return session_id

# called after session is updated; called once for each chat
def start_chat(session_id:str, stream=API_DEFAULT_STREAM) -> list:
    stream_str = "true" if stream else "false"
    params = {
        "system_prompt_num": "9",
        "stream": stream_str
    }
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}
    url = f"{API_BASE_URL}/api/chat-response/{session_id}"

    # GET /api/chat-response/<session_id>
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        raise APIException(APIExceptionType.TIMEOUT, "Timeout occurred during API request")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error ({e.response.status_code}): {e.response.reason}")
        raise APIException(APIExceptionType.HTTP_ERROR, f"HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your network connection.")
        raise APIException(APIExceptionType.CONNECTION_ERROR, "Connection error during API request")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
        raise APIException(APIExceptionType.REQUEST_ERROR, f"Request error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise APIException(APIExceptionType.UNEXPECTED_ERROR, f"Unexpected error: {str(e)}")
    
    # return list with single response if stream is false, otherwise return list with multiple responses
    response_data = [response.json()] if (not stream) else parse_stream_response(response.content)

    return response_data

# called whenever the user responds back to the tutorbot's message
def get_chat_response(session_id:str, message:str) -> list:
    params = {
        "content": message
    }
    headers = {"Authorization": f"Bearer {API_BEARER_TOKEN}"}
    url = f"{API_BASE_URL}/api/chat-response/{session_id}"


    # GET /api/chat-response/<session_id>
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
        raise APIException(APIExceptionType.TIMEOUT, "Timeout occurred during API request")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error ({e.response.status_code}): {e.response.reason}")
        raise APIException(APIExceptionType.HTTP_ERROR, f"HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your network connection.")
        raise APIException(APIExceptionType.CONNECTION_ERROR, "Connection error during API request")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
        raise APIException(APIExceptionType.REQUEST_ERROR, f"Request error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise APIException(APIExceptionType.UNEXPECTED_ERROR, f"Unexpected error: {str(e)}")

    response_data = [response.json()]

    return response_data