from chat import Chat

if __name__ == '__main__':
    chat = Chat(conversation_file=None, user="Console Tester", timestamp=None)
    while True:
        message = input("Escribe un mensaje: ")
        if message == "exit":
            print("Hasta luego! 👋")
            break
        print(chat.response_to(message)['content'])
