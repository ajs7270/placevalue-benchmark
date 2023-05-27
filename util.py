import json
import numbers
import re

import func_timeout


def convert_and_caching_prob(problem, inplace=False):

    passage = problem.passage
    question = problem.question

    passage_idxs = [idx for idx in re.finditer(r"\d+\.\d+|\d+", passage)]
    question_idxs = [idx for idx in re.finditer(r"\d+\.\d+|\d+", question)]

    if not inplace:
        cnt = len(passage_idxs) - 1
        for idx in reversed(passage_idxs):
            passage = passage[:idx.start()] + f'number{cnt}' + passage[idx.end():]
            cnt -= 1
        cnt = len(passage_idxs) + len(question_idxs) - 1
        for idx in reversed(question_idxs):
            question = question[:idx.start()] + f'number{cnt}' + question[idx.end():]
            cnt -= 1
    else:
        cnt = len(passage_idxs) - 1
        for idx in reversed(passage_idxs):
            num = problem.passage[idx.start(): idx.end()]
            passage = passage[:idx.start()] + f'{num}(number{cnt})' + passage[idx.end():]
            cnt -= 1
        cnt = len(passage_idxs) + len(question_idxs) - 1
        for idx in reversed(question_idxs):
            num = problem.question[idx.start(): idx.end()]
            question = question[:idx.start()] + f'{num}(number{cnt})' + question[idx.end():]
            cnt -= 1

    cache = ''
    cnt = 0
    for idx in passage_idxs:
        num = problem.passage[idx.start():idx.end()]
        cache += f'number{cnt} = {num}\n'
        cnt += 1
    for idx in question_idxs:
        num = problem.question[idx.start():idx.end()]
        cache += f'number{cnt} = {num}\n'
        cnt += 1

    return passage, question, cache


def safe_execute(code_string: str):
    def execute(x):
        try:
            exec(x)
            locals_ = locals()

            r = re.compile("^ans[0-9]*$")
            ans_candidate = []
            for key in locals_.keys():
                if r.match(key):
                    if len(key) == 3:
                        ans_candidate.append(0)
                    else:
                        ans_candidate.append(int(key[3:]))

            ans_var = 'ans'
            last_num = sorted(ans_candidate)[-1]
            if last_num != 0:
                ans_var += f'{last_num}'

            return locals_[ans_var]
        except Exception:
            return None
    try:
        ans = func_timeout.func_timeout(5, execute, args=(code_string,))
    except func_timeout.FunctionTimedOut:
        ans = None

    return ans


def PoT_calc_accuracy(filepath):
    correct_cnt = 0
    with open(filepath, 'r') as f:
        results = json.load(f)
        nan_cnt = 0
        for i, result in enumerate(results["Results"]):
            code = result["cache"] + result["openai"]

            ans = safe_execute(code)
            #print(ans)
            if isinstance(ans, numbers.Number):
                ans = float(ans)
                if ans.is_integer():
                    ans = int(ans)

                if ans == result["answer"]:
                    correct_cnt += 1
                else:
                    print("--------")
                    print("Wrong guess:")
                    print(f"Problem {i}")
                    print("Code:")
                    print(code)
                    print("Answer:")
                    print(result["answer"])
                    print("Guess:")
                    print(ans)
                    print("--------")
            else:
                nan_cnt += 1

    print("Total right count:")
    print(correct_cnt)
    print("Total nan count:")
    print(nan_cnt)


def CoT_calc_accuracy(filepath):
    correct_cnt = 0
    with open(filepath, 'r') as f:
        results = json.load(f)
        nan_cnt = 0
        for i, result in enumerate(results["Results"]):
            nums_in_output = re.findall(r"\d+\.\d+|\d+", result["openai"])

            if nums_in_output:
                ans = float(nums_in_output[-1])
                if ans.is_integer():
                    ans = int(ans)

                if ans == result["answer"]:
                    correct_cnt += 1
                else:
                    print("--------")
                    print("Wrong guess:")
                    print(f"Problem {i}")
                    print("Code:")
                    print(result["openai"])
                    print("Answer:")
                    print(result["answer"])
                    print("Guess:")
                    print(ans)
                    print("--------")
            else:
                nan_cnt += 1

    print("Total right count:")
    print(correct_cnt)
    print("Total nan count:")
    print(nan_cnt)
