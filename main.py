import json
from dataclasses import dataclass
from pathlib import Path
from time import sleep

from langchain import OpenAI, ConversationChain
from datetime import datetime

from datasets import Dataset
from core import PoT

# Load SVAMP dataset
svamp = Dataset(Path("data/SVAMP.json"))

# Load LlamaCpp
llm = OpenAI(temperature=0.7)

@dataclass
class Result:
    passage: str
    question: str
    answer: float
    openai: str

def dataclass_to_dict(obj):
    if isinstance(obj, list):
        return [dataclass_to_dict(value) for value in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, Result):
        return {"passage": obj.passage, "question": obj.question, "answer": obj.answer, "openai": obj.openai}
    else:
        return obj

PoT_correct = 0
outputs = []
for i, problem in enumerate(svamp):
    sleep(1)
    pot_output = PoT(llm=llm, problem=problem)

    if pot_output == problem.answer:
        PoT_correct += 1

    outputs.append(pot_output)

    print(f"current corrects PoT: {PoT_correct}")
    outputs.append(Result(passage=problem.passage, question=problem.question, answer=problem.answer, openai=pot_output))

# Convert dataclass objects to dictionaries
outputs = dataclass_to_dict(outputs)

# Get current date and time
now = datetime.now()

# Save result json
with open(Path(f"result_{now.strftime('%m%d_%H%M')}.json"), 'w') as f:
    json.dump({
        "PoT correct": PoT_correct,
        "Results": outputs,
    }, f, indent=4)
