import numpy as np
import matplotlib as plt
import pickle as pkl

items = pkl.load(open("items.pkl", "rb"))


def separate_number_from_str(data):
    number = None
    for i in data:
        for word in i["kcal"].split():
            if word.isdigit():
                number = int(word)
        i["kcal"] = number
    return data


"""
function that generate:
random days of usability of the product
random weight of the product.
"""


def add_random_date_and_weight(data, days_spectrum, grams_100_spectrum, randomise_type="uniform"):
    if randomise_type == "uniform":
        for i in data:
            i["date"] = int(np.random.uniform(0.0, 1.0) * days_spectrum + 1)  # in days
            i["weight"] = int(100 * (grams_100_spectrum * np.random.uniform(0.0, 1.0) + 1))  # in grams 100g-1000g
    elif randomise_type == "normal":
        for i in data:
            i["date"] = int(np.random.normal(0.0, 1.0) * days_spectrum + 1)  # in days
            i["weight"] = int(100 * (grams_100_spectrum * np.random.normal(0.0, 1.0) + 1))  # in grams 100g-1000g
    return data


# example of usage
items = add_random_date_and_weight(items, 24, 9)
for i in items:
    print(i["date"], "days left,", i["weight"], "grams")

"""
we can use it to randomise number of calories of the product by 
the given percent ratio
"""


def randomise_calories(data, percent, randomise_type="uniform"):
    sum_of_calories = 0
    percent = percent / 100
    data = separate_number_from_str(data)
    for i in data:
        sum_of_calories += i["kcal"]
    mean_of_calories = sum_of_calories / len(data)
    if randomise_type == "uniform":
        for i in data:
            new_percent = percent * np.random.uniform(0.0, 1.0)
            loss = np.random.uniform(0.0, 1.0)
            if loss > .5:
                i["kcal"] = int(i["kcal"] - mean_of_calories * new_percent)
            else:
                i["kcal"] = int(i["kcal"] + mean_of_calories * new_percent)
    elif randomise_type == "normal":
        for i in data:
            new_percent = percent * np.random.normal(0.0, 1.0)
            loss = np.random.normal(0.0, 1.0)
            if loss > .5:
                i["kcal"] = int(i["kcal"] - mean_of_calories * new_percent)
            else:
                i["kcal"] = int(i["kcal"] + mean_of_calories * new_percent)
    return data


# example of usage
items = randomise_calories(items, 5)
for i in items:
    print(i["kcal"], "new calories number")

"""
function to transfer from dictionary to list
"""


def dict_to_list(data):
    list = []
    for i in data:
        list.append(i)
    return list


""""
Function for making batches, we need to provide a dataset
converted to list, also number of batches we want to produce
and size of each batch, both parameters are determined by numbers.
"""


def make_batches(data_in_list, number_of_batches, size_per_batch):
    dict_of_batches = {}
    for i in range(number_of_batches):
        batch_list = []
        for j in range(size_per_batch):
            batch_list.append(data_in_list[int(np.random.uniform(0.0, len(data_in_list)))])
        dict_of_batches[f"batch{i + 1}"] = batch_list
    return dict_of_batches


# simple usage

items_list = dict_to_list(items)
dict_of_batches = make_batches(items_list, 1000, 25)
for i in dict_of_batches:
    print(dict_of_batches[i])
