import time
from bilidm import get_dm_history
from chat import chatgpt_response
from gtts_audio import synthesize_text

if __name__=="__main__":
    last_res_time = time.time()
    while True:
        messages = get_dm_history()
        print(messages)
        if messages: 
            response_ai = chatgpt_response(messages)
            print(response_ai)
            synthesize_text(response_ai)
            last_res_time = time.time()

        time.sleep(5)
