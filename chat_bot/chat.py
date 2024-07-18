import openai, os, requests
from openai import AzureOpenAI
from extract_trajectories_helpers.extract_helpers import print_to_file


class Chat:

    def __init__(self,debug=False):
        """
        Sets up the api necessary to communicate with open AI
        """
        self.debug = debug
        # Open AI information
        self._openai_deployment = "gpt4oNice"  # newVersionUpdate
        self._openai_version = "2024-02-15-preview"  # newVersionUpdate
        self._openai_key = os.getenv("AZURE_OPENAI_API_KEY")
        self._openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self._openai_client = AzureOpenAI(
            azure_endpoint=self._openai_endpoint,
            api_key=self._openai_key,
            api_version=self._openai_version
        )

        # Azure AI Search setup
        self._search_key = os.getenv("SEARCH_KEY")
        self._search_endpoint = os.getenv("SEARCH_ENDPOINT")
        self._search_index_name = "7-16data"  # newVersionUpdate
        # self._search_index_name = "vector-nice1"  # newVersionUpdate

        # Setup the messaging
        self._message_system = open('system_message.txt', 'r').read()
        self._message_latest = None
        self._message_history = [{"role": "system", "content": self._message_system}]

        self._setup_api()

    def _setup_api(self):
        # Azure API information
        openai.api_type = "azure"
        openai.api_version = self._openai_version

        # Azure OpenAI setup
        openai.api_base = self._openai_endpoint
        openai.api_key = self._openai_key

    def send_message(self, message=None):
        if self.debug:
            print("Message Received")
        if message is None:
            return "Not a valid Message. Try again"

        self._message_history.append({"role": "user", "content": message})
        self._message_latest = dict(self._communicate())
        if self.debug:
            print("Message Processing")
        return self._process_message()

    def _communicate(self):
        return self._openai_client.chat.completions.create(
            messages=self._message_history,
            model=self._openai_deployment,
            extra_body={
                "data_sources": [  # camelCase is intentional, as this is the format the API expects
                    {
                        "type": "azure_search",
                        "parameters": {
                            "endpoint": self._search_endpoint,
                            "index_name": self._search_index_name,
                            "semantic_configuration": self._search_index_name + "-semantic-configuration",
                            "query_type": "vectorSemanticHybrid",
                            "fields_mapping": {
                                "content_fields_separator": "\n",
                                "content_fields": [
                                    "chunk"
                                ],
                                "filepath_field": "title",
                                "title_field": "file_name",
                                "url_field": "experiment_id",
                                "vector_fields": [
                                    "text_vector"
                                ]
                            },
                            "in_scope": True,
                            "role_information": self._message_system,
                            "filter": None,
                            "strictness": 2,
                            "top_n_documents": 5,
                            "authentication": {
                                "type": "api_key",
                                "key": self._search_key
                            },
                            "embedding_dependency": {
                                "type": "deployment_name",
                                "deployment_name": "text-embedding-ada-002"
                            },
                            "key": self._search_key,
                            "indexName": self._search_index_name
                        }
                    }
                ],
            },
            temperature=0,
            top_p=1,
            max_tokens=800,
            stop=None,
        )

    def get_sources(self, fancy=True, check_valid=False):
        cite = self.current_message.get("context", {})
        cite = cite.get("citations", None)

        if cite is None:
            return None
        if not fancy:
            return cite
        else:
            if check_valid:
                return "True"
            index = 0
            ret_str = ""
            for content in cite:
                file_name = content.get("title", "null")
                file_path = content.get("filepath", "null")
                url = content.get("url", "null")
                ret_str += (f"\n\n\nSource #{index}: \nProcessed File Name: {file_name} \n"
                            f"File Path:{file_path}\n Experiment ID:{url}")
                ret_str += "\n" + content.get("content", "\n")
                index += 1
            return ret_str

    def clear_chat(self):
        self._message_history = [{"role": "system", "content": self._message_system}]

    def _process_message(self):
        self.current_message = dict(self._message_latest.get("choices", {})[0])
        self.current_message = dict(self.current_message.get("message", {}))
        llm_response = self.current_message.get("content", {})
        if llm_response is None:
            return "Message Formatted improperly"
        self._message_history.append({"role": "assistant", "content": llm_response})
        return str(llm_response)
