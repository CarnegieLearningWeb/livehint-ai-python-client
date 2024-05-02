from livehint_ai_client import init, start_chat, get_chat_response

def main():
    course = "Algebra I"
    module = "M1"
    page = "101"
    question = "1"
    stream = True
    session_id = init(course, module, page, question)
    print("Session ID:", session_id)
    response1 = start_chat(session_id, stream)
    print("start_chat last response:", response1[-1])
    message = "sorry I don't quite understand the problem"
    response2 = get_chat_response(session_id, message)
    print("get_chat_response response:", response2)

if __name__ == "__main__":
    main()
