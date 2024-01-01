from autogen import UserProxyAgent, ConversableAgent, config_list_from_json
import sys

def main():
    print("LOG: Starting conversation with chat GPT")
    # Load LLM inference endpoints from an env variable or a file
    # See https://microsoft.github.io/autogen/docs/FAQ#set-your-api-endpoints
    # and OAI_CONFIG_LIST_sample.
    # For example, if you have created a OAI_CONFIG_LIST file in the current working directory, that file will be used.
    config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")

    # Create the agent that uses the LLM.
    assistant = ConversableAgent("agent", llm_config={"config_list": config_list})

    # Create the agent that represents the user in the conversation.
    user_proxy = UserProxyAgent("user", code_execution_config=False)

    # Let the assistant start the conversation.  It will end when the user types exit.
    assistant.initiate_chat(user_proxy, message="How can I help you today?")

    for line in sys.stdin:
        print("LOG: Received text from app.js: " + line)
        sys.stdout.flush()


if __name__ == "__main__":
    main()