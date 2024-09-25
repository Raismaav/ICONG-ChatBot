from chat import Chat

if __name__ == '__main__':
    chat = Chat(conversation_file='conversations/042a8bd64e5f_conversación_general.json')
    while True:
        message = input("Escribe un mensaje: ")
        if message == "exit":
            print("Hasta luego! 👋")
            break
        print(chat.response_to(message)['content'])