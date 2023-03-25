import openai

openai_api_key = ""

openai.api_key = openai_api_key

admin_setting = {"role": "system", "content": "你现在是一个活泼可爱的直播机器人，你将接收到观众的弹幕，请友好风趣的回应他们吧，你不用回应所有弹幕，但请挑比较有趣的回复。"}

messages = []

# Function to send a message to ChatGPT and get a response
def chatgpt_response(prompt):
    message = compose_message(prompt)
    print(message)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.5,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )
    new_message = response.choices[0].message
    add_message(new_message)
    return new_message.content

def add_message(new_message):
    global messages
    messages.append(new_message)

def compose_message(prompt):
    global messages
    messages.append(
        {"role": "user","content":prompt}
    )
    return [admin_setting] + messages


if __name__ == "__main__":
    print(chatgpt_response("BuibuibuiOOOOO: 测试"))

