import json
from dataclasses import dataclass
from pathlib import Path
from time import sleep

from langchain import OpenAI, ConversationChain
from datetime import datetime

from langchain.chat_models import ChatOpenAI

from datasets import Dataset
from core import PoT, PoT_original, CoT_original, CP_rendezvous, digit2alph, CP_rendezvous_d2a, _compare_single_token, \
    _compare_permutation, digit2alph_CoT

# Load SVAMP dataset
svamp = Dataset(Path("data/SVAMP.json"))

# Load LlamaCpp
#llm = OpenAI(temperature=0.0)
llm = ChatOpenAI(temperature=0.0)

@dataclass
class Result:
    passage: str
    question: str
    answer: float
    cache: str
    openai: str


def dataclass_to_dict(obj):
    if isinstance(obj, list):
        return [dataclass_to_dict(value) for value in obj]
    elif isinstance(obj, dict):
        return {key: dataclass_to_dict(value) for key, value in obj.items()}
    elif isinstance(obj, Result):
        return {"passage": obj.passage, "question": obj.question, "answer": obj.answer,
                "cache": obj.cache, "openai": obj.openai}
    else:
        return obj


def prompting_test():
    try:
        outputs = []
        test_name = "d2e_CoT_ChatOpenAI"
        #cot_filepath = "results/result_cot_original.json"
        for i, problem in enumerate(svamp):
            sleep(1)
            pot_cache, pot_output = digit2alph_CoT(llm=llm, problem=problem)

            print(f"Question {i+1}---")
            outputs.append(Result(passage=problem.passage, question=problem.question,
                                  answer=problem.answer, cache=pot_cache, openai=pot_output))

            break

    finally:
        # Convert dataclass objects to dictionaries
        outputs = dataclass_to_dict(outputs)

        # Get current date and time
        now = datetime.now()

        # Save result json
        with open(Path(f"results/{test_name}_{now.strftime('%m%d_%H%M')}.json"), 'w') as f:
            json.dump({
                "Results": outputs,
            }, f, indent=4)


def compare_single_token():
    try:
        outputs = []
        test_name = "compare_one_token"

        for i in range(1000):
            sleep(1)
            output = _compare_single_token(llm=llm, n=2)

            print(f"Question {i+1}---")
            outputs.append(output)

            break

    finally:
        # Get current date and time
        now = datetime.now()

        # Save result json
        with open(Path(f"results/{test_name}_{now.strftime('%m%d_%H%M')}.json"), 'w') as f:
            json.dump({
                "Results": outputs,
            }, f, indent=4)


def compare_permutation(filepath):
    try:
        outputs = []
        test_name = "compare_permutation_2"

        with open(filepath, 'r') as f:
            results = json.load(f)

            for i, result in enumerate(results['Results']):
                sleep(1)
                nums = result.split()

                if nums:
                    wrong = False
                    buf = -1
                    for num in nums:
                        if buf > int(num):
                            wrong = True
                            break
                    if not wrong:
                        output = _compare_permutation(llm=llm, sources=nums)

                print(f"Question {i + 1}---")
                outputs.append(output)

                break

    finally:
        # Get current date and time
        now = datetime.now()

        # Save result json
        with open(Path(f"results/{test_name}_{now.strftime('%m%d_%H%M')}.json"), 'w') as f:
            json.dump({
                "Results": outputs,
            }, f, indent=4)


def comparing_numbers(option='single', filepath=""):
    if option == 'single':
        compare_single_token()
    else:
        compare_permutation(filepath)


if __name__ == '__main__':
    #prompting_test()
    comparing_numbers(option='permute', filepath='results/compare_one_token_2_0606_2143.json')
    #comparing_numbers(option='single')
