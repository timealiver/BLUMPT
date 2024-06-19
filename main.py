import cv2
import numpy as np
import pyautogui
import mss
import time

# Загружаем шаблоны (искомые изображения)
templates = [cv2.imread(f'template{i}.png', cv2.IMREAD_COLOR) for i in range(1, 5)]
template_hs = [template.shape[0] for template in templates]
template_ws = [template.shape[1] for template in templates]

# Область экрана, которую будет захватывать программа
monitor = {"top": 230, "left": 710, "width": 480, "height": 660}
sct = mss.mss()

def find_and_click_image(templates, template_hs, template_ws):
    # Делаем скриншот экрана
    screen = np.array(sct.grab(monitor))

    # Преобразуем изображения в оттенки серого для поиска шаблона
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    for i, template in enumerate(templates):
        gray_template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Ищем шаблон на экране
        res = cv2.matchTemplate(gray_screen, gray_template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Порог соответствия шаблона
        #print(res)
        loc = np.where(res >= threshold)

        # Нажимаем на первое найденное совпадение
        for pt in zip(*loc[::-1]):
            x, y = pt
            pyautogui.click(x + monitor["left"] + template_ws[i] // 2, y + monitor["top"] + template_hs[i] // 2)
            return True

    return False

while True:
    if find_and_click_image(templates, template_hs, template_ws):
        time.sleep(0.03)  # Задержка между нажатиями (0.03 секунды)
