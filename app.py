from flask import Flask, render_template, request, jsonify
import requests
import json
import random

app = Flask(__name__)

# Free Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_HEADERS = {
    "Authorization": "Bearer hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your free HF token
}

from flask import Flask, render_template, request, jsonify
import requests
import json
import random
import re
from datetime import datetime

app = Flask(__name__)

# Free APIs for enhanced features
NUTRITION_API_URL = "https://api.api-ninjas.com/v1/nutrition/"
NUTRITION_HEADERS = {
    "X-Api-Key": "YOUR_FREE_API_NINJAS_KEY"  # Get free from api.api-ninjas.com
}

# Enhanced recipe generation with more AI-like features
def calculate_nutrition_estimate(ingredients):
    """Estimate basic nutrition info"""
    nutrition_data = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0
    }
    
    # Basic estimation logic
    ingredient_calories = {
        'potato': 77, 'bread': 265, 'rice': 130, 'onion': 40,
        'tomato': 18, 'paneer': 265, 'oil': 884, 'butter': 717,
        'egg': 155, 'chicken': 165, 'milk': 42, 'cheese': 113
    }
    
    for ingredient in ingredients.lower().split(','):
        ingredient = ingredient.strip()
        for key, cal in ingredient_calories.items():
            if key in ingredient:
                nutrition_data['calories'] += cal
                nutrition_data['protein'] += cal * 0.1
                nutrition_data['carbs'] += cal * 0.5
                nutrition_data['fat'] += cal * 0.3
                break
    
    return nutrition_data

def generate_cooking_tips(recipe_type, ingredients):
    """Generate cooking tips based on ingredients"""
    tips = []
    
    if 'potato' in ingredients.lower():
        tips.append("💡 Tip: Soak potatoes in cold water for 30 minutes to remove excess starch for crispier results!")
    
    if 'onion' in ingredients.lower():
        tips.append("💡 Tip: Chill onions in the fridge before cutting to reduce tears!")
        
    if 'tomato' in ingredients.lower():
        tips.append("💡 Tip: Score an 'X' on tomatoes and blanch in hot water for easy peeling!")
    
    if recipe_type == 'curry':
        tips.append("💡 Tip: Toast your spices for 30 seconds before adding liquids for enhanced flavor!")
    
    if 'rice' in ingredients.lower():
        tips.append("💡 Tip: Rinse rice until water runs clear for fluffy, separate grains!")
    
    return tips[:2]  # Return max 2 tips

def generate_difficulty_and_time(recipe_type, ingredients):
    """Estimate cooking difficulty and time"""
    difficulty_map = {
        'sandwich': {'level': 'Easy', 'time': '10-15 minutes', 'icon': '⭐'},
        'stir_fry': {'level': 'Easy', 'time': '15-20 minutes', 'icon': '⭐⭐'},
        'curry': {'level': 'Medium', 'time': '25-35 minutes', 'icon': '⭐⭐⭐'}
    }
    
    return difficulty_map.get(recipe_type, {'level': 'Easy', 'time': '15-20 minutes', 'icon': '⭐⭐'})

def generate_alternative_suggestions(main_ingredient):
    """Suggest recipe variations"""
    alternatives = {
        'potato': ['Try making potato chips', 'Make loaded potato skins', 'Create potato gnocchi'],
        'bread': ['Make bread pudding', 'Create stuffed French toast', 'Try bread pizza'],
        'rice': ['Make rice pudding', 'Create fried rice', 'Try rice paper rolls'],
        'default': ['Add herbs for extra flavor', 'Try different cooking methods', 'Experiment with spice combinations']
    }
    
    for key in alternatives:
        if key in main_ingredient.lower():
            return random.choice(alternatives[key])
    
    return random.choice(alternatives['default'])

def generate_enhanced_recipe(ingredients):
    """Enhanced recipe generation with AI-like features"""
    
    # Recipe templates with more detail
    recipe_templates = {
        'curry': {
            'name': 'Aromatic {main} Curry',
            'funny_name': 'The "Spice-Wizard\'s-Magic-Potion" {main} Extravaganza',
            'cuisine': 'Indian',
            'steps': [
                '🔥 Heat 2 tbsp oil in a heavy-bottom pan over medium heat',
                '🧅 Add 1 large chopped onion and sauté until golden brown (5-7 mins)',
                '🧄 Add 1 tsp ginger-garlic paste and cook until fragrant (2 mins)',
                '🍅 Add 2 chopped tomatoes and cook until they break down completely',
                '🥘 Add {main} and cook for 5-7 minutes, stirring occasionally',
                '🌶️ Add ½ tsp turmeric, 1 tsp chili powder, 1 tsp garam masala',
                '💧 Add ½ cup water and bring to a gentle simmer',
                '⏰ Cover and cook for 15-20 minutes until {main} is tender',
                '🧂 Season with salt to taste and garnish with fresh cilantro',
                '🍽️ Serve hot with steamed rice or warm naan bread'
            ]
        },
        'stir_fry': {
            'name': 'Vibrant {main} Stir Fry',
            'funny_name': 'The "Wok-This-Way" {main} Symphony',
            'cuisine': 'Asian Fusion',
            'steps': [
                '🔥 Heat 1 tbsp oil in a wok or large skillet over high heat',
                '🥘 Add {main} and stir-fry for 3-4 minutes until lightly colored',
                '🥕 Add any available vegetables (carrots, bell peppers, etc.)',
                '🥄 Stir continuously for 2-3 minutes to maintain crispness',
                '🌶️ Season with salt, pepper, and available spices',
                '💧 Add a splash of water or soy sauce if available',
                '⏰ Cook for another 3-5 minutes until everything is tender-crisp',
                '🌿 Garnish with chopped green onions or herbs if available',
                '🍽️ Serve immediately while hot over steamed rice'
            ]
        },
        'sandwich': {
            'name': 'Gourmet {main} Sandwich',
            'funny_name': 'The "Between-Two-Slices-of-Heaven" {main} Creation',
            'cuisine': 'International',
            'steps': [
                '🍞 Toast 2 slices of bread until golden brown',
                '🧈 Spread butter or available spread on one side of each slice',
                '🥘 Layer the {main} evenly on one slice',
                '🥬 Add any available vegetables (lettuce, tomato, cucumber)',
                '🧂 Season with salt, pepper, and available spices',
                '🍅 Add condiments like ketchup or mustard if available',
                '🥪 Close the sandwich and press gently',
                '🔪 Cut diagonally for better presentation',
                '🍽️ Serve with a side of chips or fresh fruit'
            ]
        }
    }
    
    # Determine recipe details
    ingredients_lower = ingredients.lower()
    main_ingredient = 'mixed vegetables'
    recipe_type = 'stir_fry'
    
    if 'potato' in ingredients_lower:
        main_ingredient = 'Potato'
    elif 'bread' in ingredients_lower:
        main_ingredient = 'Bread'
        recipe_type = 'sandwich'
    elif 'rice' in ingredients_lower:
        main_ingredient = 'Rice'
    elif 'paneer' in ingredients_lower:
        main_ingredient = 'Paneer'
    
    if any(spice in ingredients_lower for spice in ['turmeric', 'haldi', 'garam masala', 'curry']):
        recipe_type = 'curry'
    
    template = recipe_templates[recipe_type]
    difficulty_info = generate_difficulty_and_time(recipe_type, ingredients)
    nutrition = calculate_nutrition_estimate(ingredients)
    tips = generate_cooking_tips(recipe_type, ingredients)
    alternative = generate_alternative_suggestions(main_ingredient)
    
    # Generate enhanced recipe
    recipe_name = template['name'].format(main=main_ingredient)
    funny_name = template['funny_name'].format(main=main_ingredient)
    steps = [step.format(main=main_ingredient.lower()) for step in template['steps']]
    
    recipe = f"""
🍽️ **{recipe_name}**
😄 *{funny_name}*

📊 **Recipe Info:**
🌍 Cuisine: {template['cuisine']}
{difficulty_info['icon']} Difficulty: {difficulty_info['level']}
⏱️ Cooking Time: {difficulty_info['time']}
📈 Estimated Calories: {nutrition['calories']:.0f} kcal

📝 **Step-by-Step Instructions:**
"""
    
    for i, step in enumerate(steps, 1):
        recipe += f"{i:2d}. {step}\n"
    
    recipe += f"\n📊 **Nutritional Estimate (per serving):**"
    recipe += f"\n🔥 Calories: {nutrition['calories']:.0f} kcal"
    recipe += f"\n🥩 Protein: {nutrition['protein']:.1f}g"
    recipe += f"\n🍞 Carbs: {nutrition['carbs']:.1f}g"
    recipe += f"\n🥑 Fat: {nutrition['fat']:.1f}g"
    
    if tips:
        recipe += f"\n\n💡 **Chef's Tips:**"
        for tip in tips:
            recipe += f"\n{tip}"
    
    recipe += f"\n\n🔄 **Try This Next:** {alternative}"
    
    # Add fun facts
    fun_facts = [
        "Did you know? The average person spends 37 minutes per day cooking!",
        "Fun fact: Cooking at home can save you up to $3000 per year!",
        "Amazing: There are over 10,000 different varieties of tomatoes worldwide!",
        "Cool fact: Onions were once used as currency in ancient Egypt!",
        "Interesting: The word 'curry' comes from the Tamil word 'kari' meaning sauce!",
        "Did you know? Potatoes were the first vegetable grown in space!"
    ]
    
    recipe += f"\n\n🎉 **Fun Fact:** {random.choice(fun_facts)}"
    
    return recipe

def generate_bread_recipe(ingredients):
    """Special handler for bread-based recipes"""
    bread_recipes = [
        {
            'name': 'Ultimate Stuffed Bread Toast',
            'funny_name': 'The "Carb-Loading-Champion" Special',
            'steps': [
                'Take 2 slices of bread and make a pocket by cutting from one side',
                'Mix available vegetables with spices',
                'Stuff the mixture into the bread pocket',
                'Heat oil in a pan',
                'Cook the stuffed bread on both sides until golden',
                'Serve hot with ketchup or chutney'
            ],
            'fun_fact': 'Bread is over 14,000 years old and was first made by ancient Egyptians!'
        },
        {
            'name': 'Crispy Bread Pakora',
            'funny_name': 'The "Rainy-Day-Comfort" Bread Transformation',
            'steps': [
                'Cut bread into small cubes',
                'Make a batter with available flour and spices',
                'Dip bread cubes in the batter',
                'Deep fry until golden and crispy',
                'Drain on paper towels',
                'Serve hot with tea or coffee'
            ],
            'fun_fact': 'Pakoras are believed to have originated in the Indian subcontinent during the Mughal era!'
        }
    ]
    
    recipe = random.choice(bread_recipes)
    
    result = f"""🍞 {recipe['name']}
😄 {recipe['funny_name']}

📝 Instructions:
"""
    
    for i, step in enumerate(recipe['steps'], 1):
        result += f"{i}. {step}\n"
    
    result += f"\n🎉 Fun Fact: {recipe['fun_fact']}"
    
    return result

def query_huggingface_api(ingredients):
    """
    Query Hugging Face API for recipe generation
    """
    try:
        prompt = f"Create a recipe using these ingredients: {ingredients}. Include a funny name and cooking steps."
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 500,
                "temperature": 0.7,
                "do_sample": True
            }
        }
        
        response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload, timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get('generated_text', '')
                # Clean up the response
                if generated_text and len(generated_text) > len(prompt):
                    return generated_text[len(prompt):].strip()
        
        return None
        
    except Exception as e:
        print(f"API Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_recipe():
    try:
        ingredients = request.form.get('components', '').strip()
        
        if not ingredients:
            return jsonify({'error': 'Please provide some ingredients'}), 400
        
        # Add common Indian spices to the ingredients
        enhanced_ingredients = f"{ingredients}, turmeric (haldi), chili powder, tomato ketchup, water, garam masala, oil"
        
        # Try API first, fallback to local logic
        recipe = query_huggingface_api(enhanced_ingredients)
        
        if not recipe:
            # Use local recipe generation logic
            recipe = generate_recipe_with_local_logic(enhanced_ingredients)
        
        return recipe
        
    except Exception as e:
        print(f"Error generating recipe: {e}")
        return generate_enhanced_recipe(ingredients or "basic ingredients")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)