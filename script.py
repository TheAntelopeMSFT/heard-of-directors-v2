import sys
import autogen
from autogen import OpenAIWrapper
import json

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"],
    },
)

def echo_text(text):
    bot_text = "From Python: " + text
    print(bot_text)

if __name__ == "__main__":
    print("LOG: Starting conversation with chat GPT")

    # create a UserProxyAgent instance named "user_proxy"
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "work_dir": "coding",
            "use_docker": False,  # set to True or image name like "python:3" to use docker
        },
    )

    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={
            "seed": 42,  # seed for caching and reproducibility
            "config_list": config_list,  # a list of OpenAI API configurations
            "temperature": 0,  # temperature for sampling
        },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
    )

    # the assistant receives a message from the user_proxy, which contains the task description
    user_proxy.initiate_chat(
        recipient=assistant,
        message="Hi, I am a chatbot. I can help you with your tasks.",
    )

    # set the cache to True to speed up the inference
    autogen.Completion.set_cache(True)
    while True:
        # create context for the assistant if context.json file does not exist else, read the context from the file
        try:
            with open('context.json') as json_file:
                context = json.load(json_file)
        except:
            context = {}

        # read the text from the standard input in app.js file
        # line is the text which the user enetered
        for line in sys.stdin:
            print("LOG: Received text from app.js: " + line)
            # enter the user name into the context dictionary
            text = line.strip()
            user = text.split(':')[0]
            message = text.split(':')[1]

            # count the number of messages in the context dictionary
            count = len(context)

            # add the latest message to the context dictionary
            context[count] = (user, message)
            
            # save the context dictionary as json file
            with open('context.json', 'w') as fp:
                json.dump(context, fp)

            print("LOG: Context: " + str(context))
            
            if "hey dj," in text:
                # remove the "hey dj" from the message
                message = message.replace("hey dj,", "")

                # the assistant receives a message from the user_proxy, which contains the task description
                user_proxy.send(
                    recipient=assistant,
                    message=message,
                )

            if "follow up" in text:
                # remove the "follow up" from the message
                message2 = text.replace("follow up,", "")

                # the assistant receives a message from the user_proxy, which contains the task description
                user_proxy.send(
                    recipient=assistant,
                    message=message2,
                )
                
            
        sys.stdout.flush()