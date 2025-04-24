import subprocess
import tempfile
import os
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI

class ResponseFormatter(BaseModel):
    """Always use this tool to structure your response to the user."""
    thinking: str = Field(description="Plan step by step in detail to answer the user's question such that when executed the code will give the answer, code that does not need to be edited by the user, this code will directly be executed ")
    answer: str = Field(description="Answer by only giving the code to achive the user's request and nothing else, only write code that does not need to be edited by the user, write code that doesnt require things like api keys and no user input")
    Depenecies: str = Field(description="Give all the required packages to run this code, only give commands (ex- pip install numpy) and nothing else, make this comma separated (Leave this empty if no dependency command is required)")

def execute_code_in_conda_env(env_name: str, dependencies: str, code: str) -> str:
    try:
        if dependencies == "" or dependencies == " ":
            install_command = f"conda activate {env_name}"
        else:
            install_command = f"conda activate {env_name} && {dependencies.replace(',', ' && ')}"
        print(install_command)
        install_result = subprocess.run(
            install_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print(install_result.stdout)
        if install_result.returncode != 0:
            return f"Dependency installation failed:\n{install_result.stderr}"

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_script:
            temp_script.write(code.encode('utf-8'))
            script_path = temp_script.name

        run_command = f"conda activate {env_name} && python {script_path}"
        print(run_command)
        run_result = subprocess.run(
            run_command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        os.remove(script_path)

        if run_result.returncode == 0:
            return run_result.stdout
        else:
            return f"Code execution failed:\n{run_result.stderr}"

    except Exception as e:
        return f"Unexpected error: {e}"

model = ChatOpenAI(model="gpt-4", temperature=0)
model_with_tools = model.bind_tools([ResponseFormatter])

query = input("Ask a question: ")

query = query + "(use the correct formate to answer and write code to achive this, you can do everything)"

ai_msg = model_with_tools.invoke(query)

print(ai_msg)

thinking = ai_msg.tool_calls[0]["args"]["thinking"]
code = ai_msg.tool_calls[0]["args"]["answer"].replace("```python", "").replace("```", "")
dependencies = ai_msg.tool_calls[0]["args"]["Depenecies"]

print("Thinking:", thinking)
print("Code:", code)
print("Dependencies:", dependencies)

output = execute_code_in_conda_env(env_name="TestCode", dependencies=dependencies, code=code)
print("Output:", output)


