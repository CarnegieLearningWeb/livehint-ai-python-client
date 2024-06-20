from livehint_ai_client import init, start_chat, get_chat_response, API_DEFAULT_APP_CONTEXT, API_DEFAULT_MODEL, API_DEFAULT_TEMPERATURE, API_DEFAULT_STREAM

def main():
    course = "Algebra I"
    module = "M1"
    page = "101"
    question = "1"
    stream = API_DEFAULT_STREAM
    app_context = API_DEFAULT_APP_CONTEXT
    temperature = API_DEFAULT_TEMPERATURE
    model = API_DEFAULT_MODEL
    session_id = init(app_context, course, module, page, question, temperature, model)
    print("Session ID:", session_id)
    response1 = start_chat(session_id, stream)
    print("start_chat last response:", response1[-1])
    message = "sorry I don't quite understand the problem"
    response2 = get_chat_response(session_id, message)
    print("get_chat_response response:", response2)

if __name__ == "__main__":
    main()
