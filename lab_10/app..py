import json
import queue
import random
import os
import requests
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from PIL import Image
from io import BytesIO



q = queue.Queue()

model_path = os.path.join(os.path.dirname(__file__), "model")
model = Model(model_path)
recognizer = KaldiRecognizer(model, 16000)

current_character = None


def callback(indata, frames, time, status):
    if status:
        print(status)

    q.put(bytes(indata))


def get_random_character():
    global current_character

    try:
        character_id = random.randint(1, 826)

        url = f"https://rickandmortyapi.com/api/character/{character_id}"

        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            current_character = response.json()

            name = current_character["name"]
            status = current_character["status"]
            species = current_character["species"]

            print()
            print("Персонаж:", name)
            print("Статус:", status)
            print("Вид:", species)
            print()

        else:
            print("Ошибка запроса к API.")

    except requests.RequestException:
        print("Ошибка подключения к интернету.")


def show_character():
    if current_character is None:
        print("Сначала скажите команду 'случайный'.")
        return

    try:
        image_url = current_character["image"]

        response = requests.get(image_url, timeout=10)

        image = Image.open(BytesIO(response.content))
        image.show()

        print("Показан персонаж:", current_character["name"])

    except requests.RequestException:
        print("Ошибка при загрузке изображения.")


def save_character():
    if current_character is None:
        print("Сначала скажите команду 'случайный'.")
        return

    try:
        image_url = current_character["image"]

        response = requests.get(image_url, timeout=10)

        name = current_character["name"]
        safe_name = name.replace(" ", "_").replace("/", "_")

        filename = safe_name + ".jpg"

        with open(filename, "wb") as file:
            file.write(response.content)

        print("Изображение сохранено:", filename)

    except requests.RequestException:
        print("Ошибка при сохранении изображения.")


def character_info():
    if current_character is None:
        print("Сначала скажите команду 'случайный'.")
        return

    print()
    print("Имя:", current_character["name"])
    print("Статус:", current_character["status"])
    print("Вид:", current_character["species"])
    print("Пол:", current_character["gender"])
    print("Местоположение:", current_character["location"]["name"])
    print()


def show_commands():
    print()
    print("Доступные команды:")
    print("случайный - получить случайного персонажа")
    print("показать - открыть изображение персонажа")
    print("сохранить - сохранить изображение")
    print("информация - показать данные персонажа")
    print("команды - показать список команд")
    print("стоп - завершить программу")
    print()


show_commands()
sd.default.device = 2

try:
    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):

        print()
        print("Голосовой ассистент запущен.")
        print("Скажите команду...")
        print()

        while True:
            data = q.get()

            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())

                text = result["text"]

                if text == "":
                    continue

                print("Вы сказали:", text)

                if "случайный" in text:
                    get_random_character()

                elif "показать" in text:
                    show_character()

                elif "сохранить" in text:
                    save_character()

                elif "информация" in text:
                    character_info()

                elif "команды" in text:
                    show_commands()

                elif "стоп" in text:
                    print("Работа программы завершена.")
                    break

                else:
                    print("Команда не распознана.")

except Exception as error:
    print("Произошла ошибка:")
    print(error)