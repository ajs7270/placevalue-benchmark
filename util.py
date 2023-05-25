import re


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
