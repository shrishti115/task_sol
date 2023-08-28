import random
import json


fragments = {
    "shape": {
        "cube": ["cube", "cubic", "cuboid", "cubes", "block", "blocks"],
        "sphere": ["sphere", "ball", "orb"],
        "cone": ["cone"],
        "plane": ["plane", "flat", "sheet"],
    },
    "action": {
        "create": ["create", "spawn", "add", "generate"],
        "delete": ["delete", "remove"],
    },
    "size": {
        "small": ["small", "tiny", "little"],
        "medium": ["medium", "average"],
        "large": ["large", "huge", "big"],
    },
    "color": {
        "red": ["red"],
        "blue": ["blue"],
        "green": ["green"],
        "yellow": ["yellow"],
        "white": ["white"],
        "black": ["black"],
    },
}


# creating a reverse lookup so that we can access the key of a value in the fragments object
def create_reverse_lookup_map(dictionary):
    reverse_lookup_map = {}
    for outer_key, inner_dict in dictionary.items():
        for inner_key, synonyms in inner_dict.items():
            for synonym in synonyms:
                reverse_lookup_map[synonym] = inner_key
    return reverse_lookup_map


reverse_lookup = create_reverse_lookup_map(fragments)


def generate_sentence():
    # select a random shape as well as a random value from the shape

    shape = random.choice(random.choice(list(fragments["shape"].values())))
    action = random.choice(random.choice(list(fragments["action"].values())))
    size = random.choice(random.choice(list(fragments["size"].values())))
    color = random.choice(random.choice(list(fragments["color"].values())))

    # return the sentence
    return f"{action} a {shape} of {size} size and {color} color"


# generating training data with a given amount of samples
def generate_training_data(amount):
    list_of_training_data = []
    for st in fragments["shape"]:
        for i in range(amount):
            sentence = generate_sentence()
            intent = reverse_lookup.get(sentence.split()[0])
            size = reverse_lookup.get(sentence.split()[4])
            color = reverse_lookup.get(sentence.split()[7])
            if intent == "create":
                list_of_training_data.append(
                    {
                        "sentence": sentence,
                        "intent": intent,
                        "entities": {
                            "shape": st,
                            "size": size,
                            "color": color,
                        },
                    }
                )

            else:
                list_of_training_data.append(
                    {
                        "sentence": sentence,
                        "intent": intent,
                        "entities": {
                            "name": st,
                        },
                    }
                )
    return list_of_training_data


training_data = generate_training_data(5)


# write the training data in a json file
with open("training_data.json", "w") as f:
    json.dump(training_data, f, indent=4)
