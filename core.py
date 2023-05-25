from langchain import PromptTemplate, LLMChain
import func_timeout
from collections import defaultdict
from util import convert_and_caching_prob


PoT_template = """
Read the following passages to answer questions with Python code, store the result as a 'ans' variable:

# Passage: James bought number0 red and number1 blue stickers, he used number2 red sticker on his fridge and number3 blue stickers on his laptop.
# Question: How many red stickers does James have?
number0 = 93
number1 = 10
number2 = 31
number3 = 7
ans = number0 - number2

# Passage: Allen went to supermarket to buy eggs, each egg costs number0 dollars, if the discount is number1 dollars.
# Question: How much do you have to pay to buy for each egg?
number0 = 80
number1 = 29
ans = number0 - number1

# Passage: Dianna collects both cases and books. He bought number0 cases and number1 books from the store. Now he has number2 cases and number3 books.
# Question: How many books did danny have at first?
number0 = 22
number1 = 5
number2 = 57
number3 = 25
ans = number3 - number1

# Passage: There were number0 chickens and number1 sheeps at the farm, some of chickens and sheeps were sold. There are number2 chickens and number3 sheeps left now.
# Question: How many chickens were sold?
number0 = 108
number1 = 20
number2 = 87
number3 = 18
ans = number0 - number2

# Passage: Katty scored number0 goals on monday, number1 goals on tuesday and number2 goals on wednesday.
# Question: How many did Katty score on monday and wednesday?
number0 = 2
number1 = 8
number2 = 9
ans = number0 + number2

# Passage: There are number0 girls and number1 boys in the Masquerade, number2 more girls and number3 more boys joined. 
# Question: How many more girls than boys are in the Masquerade?
number0 = 5
number1 = 4
number2 = 12
number3 = 7
total_girls = number0 + number1
total_boys = number2 + number3
ans = total_girls - total_boys

# Passage: Joseph and Getty went to buy ice creams, they together bought number0 ice creams. On the way back, Joseph ate number1 of the ice creasm, and he has number2 ice creams left now. 
# Question: How much ice cream did Getty purchase?
number0 = 36
number1 = 12
number2 = 2
num_ice_creams_bought_by_joseph = number2 + number1
ans = number0 - num_ice_creams_bought_by_joseph

# Passage: {passage}
# Question : {question}
{cache}
"""


PoT_template_inplace = """
Read the following passages to answer questions with Python code, store the result as a 'ans' variable:

# Passage: James bought 93(number0) red and 10(number1) blue stickers, he used 31(number2) red sticker on his fridge and 7(number3) blue stickers on his laptop.
# Question: How many red stickers does James have?
number0 = 93
number1 = 10
number2 = 31
number3 = 7
ans = number0 - number2

# Passage: Allen went to supermarket to buy eggs, each egg costs 80(number0) dollars, if the discount is 29(number1) dollars.
# Question: How much do you have to pay to buy for each egg?
number0 = 80
number1 = 29
ans = number0 - number1

# Passage: Dianna collects both cases and books. He bought 22(number0) cases and 5(number1) books from the store. Now he has 57(number2) cases and 25(number3) books.
# Question: How many books did danny have at first?
number0 = 22
number1 = 5
number2 = 57
number3 = 25
ans = number3 - number1

# Passage: There were 108(number0) chickens and 20(number1) sheeps at the farm, some of chickens and sheeps were sold. There are 87(number2) chickens and 18(number3) sheeps left now.
# Question: How many chickens were sold?
number0 = 108
number1 = 20
number2 = 87
number3 = 18
ans = number0 - number2

# Passage: Katty scored 2(number0) goals on monday, 8(number1) goals on tuesday and 9(number2) goals on wednesday.
# Question: How many did Katty score on monday and wednesday?
number0 = 2
number1 = 8
number2 = 9
ans = number0 + number2

# Passage: There are 5(number0) girls and 4(number1) boys in the Masquerade, 12(number2) more girls and 7(number3) more boys joined. 
# Question: How many more girls than boys are in the Masquerade?
number0 = 5
number1 = 4
number2 = 12
number3 = 7
total_girls = number0 + number1
total_boys = number2 + number3
ans = total_girls - total_boys

# Passage: Joseph and Getty went to buy ice creams, they together bought 36(number0) ice creams. On the way back, Joseph ate 12(number1) of the ice creasm, and he has 2(number2) ice creams left now. 
# Question: How much ice cream did Getty purchase?
number0 = 36
number1 = 12
number2 = 2
num_ice_creams_bought_by_joseph = number2 + number1
ans = number0 - num_ice_creams_bought_by_joseph

# Passage: {passage}
# Question : {question}
{cache}
"""


def safe_execute(code_string: str, keys=None):
    def execute(x):
        try:
            exec(x)
            locals_ = locals()
            if keys is None:
                return locals_.get('ans', None)
            else:
                return [locals_.get(k, None) for k in keys]
        except Exception:
            return None
    try:
        ans = func_timeout.func_timeout(5, execute, args=(code_string,))
    except func_timeout.FunctionTimedOut:
        ans = None

    return ans


def PoT(llm, problem, inplace=False, n=1):

    if not inplace:
        prompt = PromptTemplate(template=PoT_template, input_variables=["passage", "question", "cache"])
    else:
        prompt = PromptTemplate(template=PoT_template_inplace, input_variables=["passage", "question", "cache"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    passage, question, cache = convert_and_caching_prob(problem, inplace=inplace)

    print("problem:")
    print(prompt.format(passage=passage, question=question, cache=cache))

    answers = defaultdict(int)
    for i in range(n):
        output = llm_chain.run(passage=passage, question=question, cache=cache)
        output = cache + output
        print("output:")
        print(output)
        ans = safe_execute(output) #TODO should check output
        if ans:
            ans = float(ans)
            answers[ans] += 1
        print(answers)

    if not answers:
        return None

    ans = sorted(answers.items(), key=lambda x: x[1], reverse=True)[0][0]

    if ans.is_integer():
        return int(ans)

    return ans
