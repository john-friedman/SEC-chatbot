import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from operator import itemgetter
from langchain import hub
from langchain.agents import AgentExecutor, create_tool_calling_agent
from lxml import etree as ET
from typing import Any

# put your key here
with open("../temp_keys/openai_api_key.txt", "r") as f:
    os.environ["OPENAI_API_KEY"] = f.read().strip()

dir_10k = "10K XML/"

@tool
def get_10k_files() -> list:
    """Get a list of all 10-K files in the Tech 10K directory."""
    return os.listdir(dir_10k)

def load_file(file):
    """Load the 10-K file, input is the file name."""
    with open(dir_10k + file, "r") as f:
        string = f.read()

    node =  ET.fromstring(string)
    # subset to first item
    node = node.find('.//item')
    return node

    
def get_title_tree(node,level=1):        
    tree_attrib = node.attrib.get('title','')
    for child in node:
        tree_attrib += '\n' + '|-' * level + get_title_tree(child, level + 1)

    return tree_attrib

@tool
def get_xml_file_tree(file):
    """Print the tree of the 10-K file, input is the file name."""

    xml = load_file(file)
    return get_title_tree(xml)

@tool
def get_section_text(file, title):
    """Get the text of a section in the 10-K file, input is the file name and the section title."""
    xml = load_file(file)
    node =  xml.find(f'.//*[@title="{title}"]')
    if node is None:
        return "Section not found. Try looking at the tree to find the correct title."
    else:
       return node.text

    


llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

tools = [get_10k_files,get_xml_file_tree,get_section_text]

# Construct the tool calling agent
prompt = hub.pull("hwchase17/openai-tools-agent")
agent = create_tool_calling_agent(llm, tools, prompt)

# Create an agent executor by passing in the agent and tools
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)



def main():
    print("Welcome to the 10-K Analysis Agent!")
    print("Type 'exit' to quit the program.")
    
    while True:
        user_input = input("\nEnter your question about the 10-K files: ")
        
        if user_input.lower() == 'exit':
            print("Thank you for using the 10-K Analysis Agent. Goodbye!")
            break
        
        response = agent_executor.invoke({"input": user_input})
        print("\nAgent's response:")
        print(response['output'])

if __name__ == "__main__":
    main()