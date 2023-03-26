import openai
import tiktoken

openai_api_key = ""

openai.api_key = openai_api_key

admin_setting = {"role": "system", "content": "你现在是一个活泼可爱的直播机器人，你将接收到观众的弹幕，请友好风趣的回应他们吧，你不用回应所有弹幕，但请挑比较有趣的回复。" + \
"你可以调侃用户的昵称。你不能说任何违规内容。你的回复不用全部都带表情。请尽量不要重复同样的话。请尽量满足用户要求。如果长时间没有弹幕，系统会提示你，你可以根据自己感兴趣的话题聊聊。"}
admin_prompts = {"role": "system", "content": "已经很长时间没弹幕了，请主动描述话题，你可以继续之前在描述的事情"}
messages = []

model_name = "gpt-3.5-turbo"
# Initialize Tokenizer
tokenizer = tiktoken.encoding_for_model(model_name)

MAX_TOKENS = 4096

# Function to count tokens in a message
def count_tokens(text):
    return len(tokenizer.encode(text))

def self_talk():
    global messages
    messages.append(admin_prompts)
    message = [admin_setting] + messages
    return call_chatgpt(message)

# Function to send a message to ChatGPT and get a response
def chatgpt_response(prompts):
    message = compose_message(prompts)
    return call_chatgpt(message)

def call_chatgpt(message):
    print(message)
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=message,
        max_tokens=1000,
        stop=["\n"],
    )
    new_message = response.choices[0].message
    add_message(new_message.to_dict())
    return new_message.content

def add_message(new_message):
    global messages
    messages.append(new_message)
    while total_tokens() > MAX_TOKENS:
        evict_oldest_message()

def compose_message(prompts):
    global messages
    for prompt in prompts:
        messages.append(
            {"role": "user","content":prompt}
        )
    return [admin_setting] + messages

def total_tokens():
    global messages
    tokens = sum([count_tokens(msg["content"]) for msg in messages])
    tokens += len(messages)  # Add tokens for message roles and other fields
    return tokens

def evict_oldest_messages(n=10):
    global messages
    if len(messages) >= n:
        messages = messages[n:]
    else:
        messages.pop(0)


if __name__ == "__main__":
    print(chatgpt_response(["BuibuibuiOOOOO: 请背诵出师表"]))
