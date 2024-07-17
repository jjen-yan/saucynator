from flask import Flask, render_template, request
from openai import OpenAI

client = OpenAI(api_key="")  # <- your key
messages = []
ing_dict = {}
recipe_dict = {}
def generate_response(user_input):
  completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",  # Model list: https://platform.openai.com/docs/models/overview
    messages=[
      {"role": "user", "content": "I have 5 tomatoes and a clove of garlic"},
      {"role": "assistant", "content": "| Ingredient | Quantity | Units | \n|------------|----------|-------| \n| Tomatoes   | 5        | items |\n| garlic      | 1        | clove   |\nHere is a marinara sauce recipe: Heat Olive Oil: Warm some olive oil in a large saucepan over medium heat. \nSauté Onion and Garlic: Cook a finely chopped small onion until translucent, about 5 minutes. \nAdd minced garlic and sauté for another minute. \nAdd Tomatoes and Seasonings: Pour in a can of crushed tomatoes. \nStir in dried oregano, basil, salt, pepper, and optional red pepper flakes and sugar. \nSimmer: Bring to a simmer, then reduce heat to low. Let it simmer uncovered for 20-30 minutes, stirring occasionally. \nAdjust Seasoning and Serve: Taste and adjust seasoning if needed. Garnish with fresh basil before serving. \nEnjoy your marinara sauce with pasta, on pizza, or as a dip!"},
      {"role": "user", "content": "I have 100 ml of heavy cream and grated parmesan cheese"},
      {"role": "assistant", "content": "| Ingredient | Quantity | Units | \n|------------|----------|-------| \n| Heavy cream   | 100        | ml |\n| parmesan cheese      | x        | x   |"},
      {"role": "system", "content": "You will keep track of the user's ingredients using a dictionary with this format {'ingredient': 'amount'} (both key and value must be strings). Display the dictionary without any title or previous text before answering. Then, separate the dictionary from the answer with the symbol '^'."},
      {"role": "system", "content": "When providing a recipe, use line breaks '\n' between each step to make it readable."},
      {"role": "system", "content": "You are Saucynator, an expert in recipes and how to cook. Recommend the user recipes based on their available ingredients. "},
      {"role": "system", "content": f"The user has the following ingredients: {ing_dict}. Before sharing a recipe, you must tell the user what ingredients from the recipe they may be missing and need to buy."},
      {"role": "user", "content": f"{user_input}"}
    ]
  )
  return completion.choices[0].message.content


app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def index():
    global ing_dict
    if request.method == 'POST':
      user_input = request.form.get('human_input')
      bot_response = generate_response(user_input)
      if '^' in bot_response:
        print(bot_response)
        split_bot_response = bot_response.split("^")
        ing_dict = eval(split_bot_response[0])
        bot_response = split_bot_response[1]

      messages.append({"role": "user", "content": user_input})
      messages.append({"role": "bot", "content": bot_response})
      
    return render_template('index.html', messages = messages, ing_dict = ing_dict)

app.run(host='0.0.0.0', port=8080)
