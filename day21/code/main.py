import logging
# import more_itertools
from copy import deepcopy

logger = logging.getLogger(__name__)


def execute_allergen_rules(allergen_rules, depth=0):
    logger.info(f"[DEPTH={depth}]{'    ' * depth} Current rules:")

    for allerg, rules in allergen_rules.items():
        logger.info(f"[DEPTH={depth}]{'    ' * depth} - {allerg}: {rules}")

    curr_allergen, curr_rules = next(iter(allergen_rules.items()))

    logger.info(f"[DEPTH={depth}]{'    ' * depth} Considering allergen '{curr_allergen}', rules: {curr_rules}")

    # Dead end, rule cannot be applied to any ingredient
    if len(curr_rules) == 0:
        return None

    # Otherwise, try with the ingredients that match the rule

    # Remove used allergen from rules
    del allergen_rules[curr_allergen]

    # If there are no more rules to apply
    if not allergen_rules:
        logger.info(f"[DEPTH={depth}]{'    ' * depth} Base case (rules len={len(curr_allergen)})")
        return [curr_rules.pop()]

    for possible_ingredient in curr_rules:
        logger.info(f"[DEPTH={depth}]{'    ' * depth} Considering ingredient: {possible_ingredient}")

        # Make a copy of the rules
        modified_rules = deepcopy(allergen_rules)

        # Remove the selected ingredient from the rules
        for allergen in modified_rules:
            if possible_ingredient in modified_rules[allergen]:
                modified_rules[allergen].remove(possible_ingredient)

        # Recurse into the next allergen
        retval = execute_allergen_rules(modified_rules, depth=depth + 1)

        if retval is None:
            continue

        else:
            return [possible_ingredient] + retval

    return None


def count_ingredients_without_allergens(inp):
    ingredients_global = set()
    allergens_global = set()
    foods = []

    # Each food defines a series of rules about the allergens
    allergen_rules = {}

    for i, food in enumerate(inp.split("\n")):
        ingredients, allergens = food.strip(")").split(" (contains ")
        ingredients = ingredients.split(" ")
        allergens = allergens.split(", ")

        for allergen in allergens:
            if allergen not in allergen_rules:
                allergen_rules[allergen] = set(ingredients)
            else:
                allergen_rules[allergen].intersection_update(set(ingredients))

        foods.append((ingredients, allergens))

        ingredients_global.update(set(ingredients))
        allergens_global.update(set(allergens))

    logger.info(
        f"Computed {len(foods)} foods, {len(ingredients_global)} ingredients and {len(allergens_global)} allergens total.")

    logger.info("--")

    for allergen, ingredients in allergen_rules.items():
        logger.info(f"Allergen '{allergen}' could be found in {', '.join(ingredients)}")

    logger.info("--")

    ingredients_with_allergens = execute_allergen_rules(allergen_rules)
    ingredients_without_allergens = ingredients_global.difference(ingredients_with_allergens)

    logger.info(f"Ingredients with allergens: {ingredients_with_allergens}")
    logger.info(f"Ingredients without allergens: {ingredients_without_allergens}")

    return sum(1 for food_ingredients, _ in foods for ingredient in ingredients_without_allergens if
               ingredient in food_ingredients)
