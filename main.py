import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl
from math import floor

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
# for i in items:
#     print(i["date"], "days left,", i["weight"], "grams")

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
                if i["kcal"] - mean_of_calories * new_percent > 0:
                    i["kcal"] = int(i["kcal"] - mean_of_calories * new_percent)
                else:
                    i["kcal"] = int(i["kcal"] + mean_of_calories * new_percent)
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


def delete_zeros(data):
    delete_list = []
    for i in range(len(data)):
        if data[i]["kcal"] <= 0:
            delete_list.append(i)
    for i in range(len(delete_list)):
        del data[delete_list[i] - i]
    return data


# example of usage
# for i in items:
#     print(i["kcal"], "new calories number")

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


def weight_counting(ip, cp, ipt):
    p = (ip * cp) / (100 * (ipt + 1))
    return p


def weight_counting_for_simulation(batches_dict):
    dictionary_of_parameters_in_all_batches = []
    for i in batches_dict:
        placeholder_dict = {}
        for j in range(len(batches_dict[i])):
            placeholder_dict[batches_dict[i][j]["name"]] = {
                "parameter": round(weight_counting(batches_dict[i][j]["weight"],
                                                   batches_dict[i][j]["kcal"],
                                                   floor(batches_dict[i][j]["date"] / 7)
                                                   ), 2), "kcal": batches_dict[i][j]["kcal"],
                "weight": batches_dict[i][j]["weight"],
                "date": batches_dict[i][j]["date"]}
        dictionary_of_parameters_in_all_batches.append(placeholder_dict)
    return dictionary_of_parameters_in_all_batches


def max_value(batch, waste):
    max_value_ = 0
    kcal = 0
    weight = 0
    name = None
    list_to_delete = []
    for date_food in batch:
        if batch[date_food]['date'] <= 0:
            waste += (batch[date_food]['parameter'])
            list_to_delete.append(date_food)
    for i in range(len(list_to_delete)):
        del batch[list_to_delete[i]]
    for food in batch:
        if batch[food]['parameter'] > max_value_:
            max_value_ = batch[food]['parameter']
            kcal = batch[food]['kcal']
            weight = batch[food]['weight']
            name = food
    return batch, waste, [max_value_, kcal, weight, name]


def date_substract(batch):
    for date in batch:
        batch[date]['date'] -= 1
    return batch


def greedy_algorithm(kcal_limit, lenght_of_simulation, dict_):
    dict_with_info = {}
    for i in range(len(dict_)):
        waste = 0
        days_starving = 0
        for k in range(lenght_of_simulation):
            actual_kcal = 0
            while kcal_limit > actual_kcal:

                if len(dict_[i]) == 0:
                    actual_kcal = kcal_limit
                else:
                    dict_[i], waste, chosen_food = max_value(dict_[i], waste)
                    # print(f"actual: {actual_kcal}, max: {kcal_limit}, dlugosc: {len(dict_[i])}, chosen: {dict_[i]}")
                if len(dict_[i]) == 0:
                    actual_kcal = kcal_limit
                    days_starving += 1
                if (kcal_limit - actual_kcal != 0) and (
                        kcal_limit - actual_kcal < chosen_food[1] * (chosen_food[2] / 100)):
                    new_weight = chosen_food[1] * (chosen_food[2] / 100) - (kcal_limit - actual_kcal)
                    new_weight = (new_weight / chosen_food[1]) * 100
                    actual_kcal = kcal_limit
                    dict_[i][chosen_food[3]]['weight'] = new_weight
                elif (kcal_limit - actual_kcal > 0) and (chosen_food[1] != 0):
                    actual_kcal += chosen_food[1] * (chosen_food[2] / 100)
                    del dict_[i][chosen_food[3]]

            dict_[i] = date_substract(dict_[i])
        dict_with_info[i] = {'waste': round(waste, 2), 'left': dict_[i], "days_starving": days_starving}
    return dict_with_info


# simple usage
items = add_random_date_and_weight(items, 15, 5)
items = randomise_calories(items, 5)
items = delete_zeros(items)
items_list = dict_to_list(items)
# first parameter is number of batches, second parameter is size per batch
dict_of_batches = make_batches(items_list, 1000, 20)
dict_with_parameters = weight_counting_for_simulation(dict_of_batches)
results = greedy_algorithm(2500, 10, dict_with_parameters)
list1 = []
list2 = []
list3 = []
for i in results:
    print(f"simulation number: {i}         waste: {results[i]['waste']},          days starving: {results[i]['days_starving']}")
    list1.append(i)
    list2.append(results[i]['waste'])
    list3.append(results[i]['days_starving'])


plt.hist(list2)
plt.title("100-500g, 1-15 days, 2000kcal -> waste")
plt.show()
plt.hist(list3)
plt.title("100-500g, 1-15 days, 2000kcal -> days starving")
plt.show()

