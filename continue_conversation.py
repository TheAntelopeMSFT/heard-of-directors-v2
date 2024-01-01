import sys
import autogen

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    filter_dict={
        "model": ["gpt-4-1106-preview"],
    },
)



if __name__ == "__main__":
    # echo_text(sys.argv[1])
    continue_conversation_with_chat_gpt(sys.argv[1])