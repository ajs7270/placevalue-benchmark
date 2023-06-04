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


def num_to_words(num):
    under_20 = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
                'Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen',
                'Nineteen']
    tens = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
    above_100 = {100: 'Hundred', 1000: 'Thousand', 1000000: 'Million', 1000000000: 'Billion'}

    if num < 20:
        return under_20[int(num)]

    if num < 100:
        return tens[int(num / 10) - 2] + ('' if num % 10 == 0 else ' ' + under_20[int(num) % 10])

    pivot = max([key for key in above_100.keys() if key <= num])

    return num_to_words(int(num / pivot)) + ' ' + above_100[pivot] + (
        '' if num % pivot == 0 else ' ' + num_to_words(num % pivot))


def float_to_words(float_num):
    if '.' not in str(float_num):
        return num_to_words(int(float_num))

    integer_part, fractional_part = str(float_num).split('.')

    words = num_to_words(int(integer_part))
    words += ' point'
    for digit in fractional_part:
        words += ' ' + num_to_words(int(digit))
    return words


def convert_digit2alph(problem):

    passage = problem.passage
    question = problem.question

    passage_idxs = [idx for idx in re.finditer(r"\d+\.\d+|\d+", passage)]
    question_idxs = [idx for idx in re.finditer(r"\d+\.\d+|\d+", question)]

    for idx in reversed(passage_idxs):
        num = problem.passage[idx.start(): idx.end()]
        alph_num = float_to_words(num)
        passage = passage[:idx.start()] + alph_num + passage[idx.end():]

    for idx in reversed(question_idxs):
        num = problem.question[idx.start(): idx.end()]
        alph_num = float_to_words(num)
        question = question[:idx.start()] + alph_num + question[idx.end():]

    return passage, question


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


def scale_up_nums(target: str, amount):

    idxs = [idx for idx in re.finditer(r"\d+\.\d+|\d+", target)]
    scaled = target

    for idx in reversed(idxs):
        num = target[idx.start(): idx.end()]
        num = float(num)

        if num.is_integer():
            num = int(num)

        num_scaled = num * amount

        scaled = scaled[:idx.start()] + str(num_scaled) + scaled[idx.end():]

    return scaled


def calc_scaled_result(equation: str, amount):
    idxs = [idx for idx in re.finditer(r"\d+\.\d+|\d+", equation)]
    scaled = equation

    for idx in reversed(idxs):
        num = equation[idx.start(): idx.end()]
        num = float(num)

        if num.is_integer():
            num = int(num)

        num_scaled = num * amount

        scaled = scaled[:idx.start()] + str(num_scaled) + scaled[idx.end():]

    scaled_result = eval(scaled)

    return scaled_result


def scale_up_dataset(filepath, amount=1000):
    new_data = []
    with open(filepath, "r") as f:
        data = json.load(f)
        for i, problem in enumerate(data):
            new_data.append(problem)
            new_data[i]['Body'] = scale_up_nums(new_data[i]['Body'], amount)
            new_data[i]['Question'] = scale_up_nums(new_data[i]['Question'], amount)
            new_data[i]['Answer'] = calc_scaled_result(new_data[i]['Equation'], amount)

    with open(f"data/SVAMP_scaled_{amount}.json", "w") as f:
        json.dump(new_data, f, indent=4)


