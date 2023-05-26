from langchain import PromptTemplate, LLMChain
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

PoT_org_template = """
Read the following passages to answer questions with Python code, store the result as a 'ans' variable:

# Passage: James bought 93 red and 10 blue stickers, he used 31 red sticker on his fridge and 7 blue stickers on his laptop.
# Question: How many red stickers does James have?
original_red_stickers = 93
used_red_stickers = 31
ans = original_red_stickers - used_red_stickers

# Passage: Allen went to supermarket to buy eggs, each egg costs 80 dollars, if the discount is 29 dollars.
# Question: How much do you have to pay to buy for each egg?
original_egg_price_in_dollars = 80
discount_dollars = 29
ans = original_egg_price_in_dollars - discount_dollars

# Passage: Dianna collects both cases and books. He bought 22 cases and 5 books from the store. Now he has 57 cases and 25 books.
# Question: How many books did danny have at first?
num_books_bought_at_store = 5
num_books_now = 25
ans = num_books_now - num_books_bought_at_store

# Passage: There were 108 chickens and 20 sheeps at the farm, some of chickens and sheeps were sold. There are 87 chickens and 18 sheeps left now.
# Question: How many chickens were sold?
num_chicken_before = 108
num_chicken_now = 87
ans = num_chicken_before - num_chicken_now

# Passage: Katty scored 2 goals on monday, 8 goals on tuesday and 9 goals on wednesday.
# Question: How many did Katty score on monday and wednesday?
num_goals_on_monday = 2
num_goals_on_wednesday = 9
ans = num_goals_on_monday + num_goals_on_wednesday

# Passage: There are 5 girls and 4 boys in the Masquerade, 12 more girls and 7 more boys joined. 
# Question: How many more girls than boys are in the Masquerade?
num_girls_before = 5
num_girls_joined = 12
num_boys_before = 4
num_boys_joined = 7
total_girls = num_girls_before + num_girls_joined
total_boys = num_boys_before + num_boys_joined
ans = total_girls - total_boys

# Passage: Joseph and Getty went to buy ice creams, they together bought 36 ice creams. On the way back, Joseph ate 12 of the ice creasm, and he has 2 ice creams left now. 
# Question: How much ice cream did Getty purchase?
num_ice_creams_bought_by_joseph = 2 + 12
total_ice_creams = 36
ans = total_ice_creams - num_ice_creams_bought_by_joseph

# Passage: {passage}
# Question : {question}
"""


def PoT(llm, problem, inplace=False):

    if not inplace:
        prompt = PromptTemplate(template=PoT_template, input_variables=["passage", "question", "cache"])
    else:
        prompt = PromptTemplate(template=PoT_template_inplace, input_variables=["passage", "question", "cache"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    passage, question, cache = convert_and_caching_prob(problem, inplace=inplace)

    print("problem:")
    print(prompt.format(passage=passage, question=question, cache=cache))

    output = llm_chain.run(passage=passage, question=question, cache=cache)

    print("output:")
    print(cache + output)

    return cache, output


def PoT_original(llm, problem):

    prompt = PromptTemplate(template=PoT_org_template, input_variables=["passage", "question"])

    llm_chain = LLMChain(prompt=prompt, llm=llm)

    print("problem:")
    print(prompt.format(passage=problem.passage, question=problem.question))

    output = llm_chain.run(passage=problem.passage, question=problem.question)

    print("output:")
    print(output)

    return "", output
