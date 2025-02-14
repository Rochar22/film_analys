# Интеллектуальный анализ фильмов при помощи ИИ
## Задачи нейронной сети
Нейронная сеть умеет дать свою оценку фильму и на основе ваших оценок сможет подстроится и дать уникальный рейтинг подходящий вам в удобном и красивом интерфейсе
## Что использовалось для написании программы
Этот проект состоит из нескольких частей
### 1. Искусственный Интелект
ИИ создавался с помощью разных библиотек и технологий, но можно выделить несколько важных из них:
#### 1. Tensorflow Keras
Для создания самой нейронной сети
#### 2. SciKit-Learn
Для нормализации данных и использовании их в будущем
#### 3. Pandas
Для переобразования данных в удобном виде для нейронной сети
#### 4. OMDb API
Для поиска харастеристик фильмов на сайте IMDb 
### 2. GUI Приложение
GUI написан при помощи библиотеки tkinter и позволяет увидеть постер фильма, оценку с IMDb и оценку, составленную самой нейросетью.
# Как запустить?
## 1. Скачать версию python не менее 3.12
## 2. Создать виртуальное окружение в python и активировать его
```shell
python -m venv .venv
./.venv/Scripts/activate
```
## 3. Скачать библиотеки из requirements.txt
```
pip install -r requirements.txt
```
## 4. запустить файл gui.py
```
python gui.py
```
