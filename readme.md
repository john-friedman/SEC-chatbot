## Simple SEC Chatbot

A simple chatbot to compare SEC 10-K filings. Uses `sec-parsers` to convert 10-Ks into sections to fit inside context windows. To try yourself, input your openai api_key under the # put your key here comment.

To add more filings, adjust code in data_setup.py.

# TODO
* add langchain function to take advantage of `sec-parsers` metadata.