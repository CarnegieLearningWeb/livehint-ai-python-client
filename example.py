import requests
import livehint_ai_client as lh_ai_client

def main():
    try:
        course = "Algebra I"
        module = "M1"
        page = "101"
        question = "1"
        session_id = lh_ai_client.init(course, module, page, question)
        print("Session ID:", session_id)
    except requests.exceptions.Timeout:
        print("The request timed out. Please try again later.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error ({e.response.status_code}): {e.response.reason}")
    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your network connection.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during the request: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
