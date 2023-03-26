import time
from bilidm import get_dm_history
from chat import chatgpt_response, self_talk
from gtts_audio import synthesize_text

first_time = True
if __name__=="__main__":
    last_res_time = time.time()
    while True:
        messages = get_dm_history()
        print(messages)
        if first_time: 
            messages = []
            first_time = False
        if messages: 
            response_ai = chatgpt_response(messages)
            print(response_ai)
            synthesize_text(response_ai)
            last_res_time = time.time()
        else:
            if time.time() - last_res_time > 10:
                response_ai = self_talk()
                print(response_ai)
                synthesize_text(response_ai)
                last_res_time = time.time()

        time.sleep(5)
