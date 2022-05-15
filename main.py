# users.csv содержит: user_id, age
# products.csv содержит: product_id, category_id
# purchases.csv содержит: product_id, user_id, product_cost, num_units

import csv


# age_groupS - кортеж, который содержит в себе возрастные группы

age_groups = tuple(tuple(str(k) for k in range(i, i + 5)) for i in range(18, 86, 5))

# product_category - содержит в себе категории продуктов

product_category = ('Laptop', 'Smartphone', 'Printer', 'PC')

array_users = [1, 2]  # список, который будет хранить в себе введенные id пользователей


def menu():
    """
    отвечает за меню интерфейса
    """
    print("0 - Выход из программы")
    print("1 - Получить информацию о тратах каждой возрастной группы по каждой категории товара")
    print("2 - Рекомендация товаров для каждой группы пользователей")


def information_input():
    """
    запрашивает ввод id пользователей
    """
    while True:
        try:
            print('Введите id покупателей:\nДля завершения ввода напишите 0')
            num_user = int(input())
            if num_user == 0:
                break
            array_users.append(num_user)
        except ValueError:
            print('Ошибка! Введеные символы не могут быть определены как id покупателя, попробуйте снова.')


def main_dialog():
    """
    отвечает за интерфейс пользователя
    """
    information_input()
    menu()
    key = 0
    try:
        key = int(input())
    except ValueError:
        print("Ошибка! Введенные символы не соответствуют заданным командам, попробуйте снова.")
    while key:
        if key == 1:
            result_total_costs_by_category(array_users)
        elif key == 2:
            result_output(array_users)
        else:
            print("Такой команды не существует, попробуйте еще раз.")
        menu()
        try:
            key = int(input())
        except ValueError:
            print("Ошибка! Введенные символы не соответствуют заданным командам, попробуйте снова.")


def array_users_for_age(temp_array_users):
    """
    получает масив пользователей с возрастом, на основе введенных значений
    сюда помещаются id пользователей, на выходе получается список [[id, age]]
    """
    with open('users.csv') as file_users:
        reader = csv.reader(file_users)
        next(reader)
        temp_array_users_age = []
        for i in reader:
            for j in temp_array_users:
                if str(j) == i[0]:
                    temp_array_users_age.append(i)
    return temp_array_users_age


def getting_age_match(temp_array_users_age):
    """
    получает словарь соответствия каждого пользователя его возрастной группе
    на вход подается массив [[id, age]], на выходе получается словарь {id: (age, age, age, age, age)}
    """
    dictionary_users = {}
    for age_group in age_groups:
        for j in temp_array_users_age:
            if j[1] in age_group:
                dictionary_users[j[0]] = age_group
    return dictionary_users


def selection_of_goods_for_the_age_group(temp_age):
    """
    получает масив с поокупками конкретного возраста
    на вход подается age, на выходе получаем массив из purchases, соответствующий возрасту
    """
    with open('users.csv') as file_users:
        reader = csv.reader(file_users)
        next(reader)
        list_group = []
        for i in reader:
            if str(temp_age) == i[1]:
                list_group.append(i)
    with open('purchases.csv') as file_purchases:
        reader_1 = csv.reader(file_purchases)
        next(reader_1)
        list_purchases_for_group = []
        for i in reader_1:
            for j in list_group:
                if i[1] == j[0]:
                    list_purchases_for_group.append(i)
    return list_purchases_for_group


def method_of_recommendation(temp_array_users):
    """
    выводит рекомендации по 5 продуктов, в него передается array_users
    """
    temp_dict = getting_age_match(array_users_for_age(temp_array_users))
    resulting_dictionary = {}
    for i in temp_dict:
        temp_purchases = []
        for j in temp_dict[i]:
            for k in selection_of_goods_for_the_age_group(j):
                temp_purchases.append(k)
        temp_purchases_2 = sorted(temp_purchases, key=lambda x: int(x[3]), reverse=True)
        temp = []
        for key in temp_purchases_2:
            temp.append(key[0])
        resulting_dictionary[i] = temp[:5]
    return resulting_dictionary


def result_output(temp_array_users):
    """
    вывод данных для рекомендации
    """
    temp_dict = method_of_recommendation(temp_array_users)
    for i in temp_dict:
        print("User_id: ", i, " : products: ", temp_dict[i])


def total_costs_by_category(temp_array_users):
    """
    расчитывает словарь для возрастной группы по каждой категори товара
    """
    temp_dict = getting_age_match(array_users_for_age(temp_array_users))
    resulting_dictionary = {}
    for i in temp_dict:
        temp_purchases = []
        for j in temp_dict[i]:
            for k in selection_of_goods_for_the_age_group(j):
                temp_purchases.append(k)
        temp_purchases_2 = sorted(temp_purchases, key=lambda x: int(x[3]), reverse=True)
        resulting_dictionary[i] = temp_purchases_2
    with open('products.csv') as file_product:
        reader = csv.reader(file_product)
        next(reader)
        temp_products_dict = {}
        temp_reader = []
        for i in reader:
            temp_reader.append(i)
        for i in resulting_dictionary:
            temp = []
            for j in resulting_dictionary[i]:
                for k in temp_reader:
                    if j[1] == k[0]:
                        temp.append(list([k[1], j[2]]))
            temp_products_dict[i] = temp
    return temp_products_dict


def result_total_costs_by_category(temp_array_users):
    """
    расчитывает сумму трат для каждой категории по возрастной группе
    """
    dict_users_product = total_costs_by_category(temp_array_users)
    temp_dict = {}
    for i in dict_users_product:
        dict_category_temp = {}
        for j in product_category:
            count = 0
            for k in dict_users_product[i]:
                if j == k[0]:
                    count += int(k[1])
            dict_category_temp[j] = count
        temp_dict[i] = dict_category_temp
    for i in temp_dict:
        print("User_id: ", i, " : products: ", temp_dict[i])


# начинается выполнения программы
if __name__ == "__main__":
    main_dialog()

