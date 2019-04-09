params = {
    1: 0.001,  # Курсор
    2: 0.003,  # Видеокарта
    3: 0.01,  # Стойка видеокарт
    4: 0.03,  # Суперкомпьютер
    5: 0.1,  # Сервер ВКонтакте
    6: 0.5,  # Квантовый компьютер
    7: 1  # Датацентр
}
price = {
    1: 106.929,
    2: 119.948,
    3: 146.313,
    4: 511.878,
    5: 2559.322,
    6: 13308.350,
    7: 24134.045
}
name = {
    1: 'Курсор',
    2: 'Видеокарта',
    3: 'Стойка видеокарт',
    4: 'Суперкомпьютер',
    5: 'Сервер ВКонтакте',
    6: 'Квантовый компьютер',
    7: 'Датацентр'
}
while True:
    data = [price[x] / params[x] for x in range(1, 8)]
    recommend = data.index(min(data)) + 1
    print('Рекомендуется к покупке {} по цене {}/1vk'.format(name[recommend], data[recommend - 1]))
    new_price = float(input('Новая цена товара: '))
    price[recommend] = new_price