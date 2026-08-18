# solution.py

import requests


def weather():
    print("=== Task 1: Погода ===")

    city_name = "Belgorod"
    api_key = "d55eef5dba5f71c22df51c6462a1cce2"

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        print(f"Погода в городе {city_name}:")
        print("Температура:", data["main"]["temp"], "°C")
        print("Влажность:", data["main"]["humidity"], "%")
        print("Давление:", data["main"]["pressure"], "гПа")
        print("Погода:", data["weather"][0]["description"])
        print("Скорость ветра:", data["wind"]["speed"], "м/с")

    else:
        print("Ошибка OpenWeatherMap API:", response.status_code)


def rick_and_morty():
    print("\n=== Task 2: Rick and Morty API ===")

    character_name = input(
        "Введите имя персонажа на английском: "
    ).strip()

    url = "https://rickandmortyapi.com/api/character"

    params = {
        "name": character_name
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            characters = data["results"]

            character = characters[0]

            print("\nИнформация о персонаже:")
            print("Имя:", character["name"])
            print("Статус:", character["status"])
            print("Вид:", character["species"])
            print("Тип:", character["type"] or "Не указан")
            print("Пол:", character["gender"])
            print(
                "Происхождение:",
                character["origin"]["name"]
            )
            print(
                "Местоположение:",
                character["location"]["name"]
            )
            print(
                "Количество эпизодов:",
                len(character["episode"])
            )

        elif response.status_code == 404:
            print("Персонаж не найден.")
            print("Введите имя на английском, например Rick.")

        else:
            print(
                "Ошибка Rick and Morty API:",
                response.status_code
            )
            print(response.text)

    except requests.exceptions.RequestException as error:
        print("Ошибка подключения:", error)

if __name__ == "__main__":
    weather()
    rick_and_morty()