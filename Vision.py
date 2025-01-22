from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import cv2
import numpy as np
import pytesseract as pt


class Vision:
    def __init__(self,image_path):
        self.image = image_path

    def change_image(self,new_image_path):
        self.image = new_image_path

    def extract_food(self):
        try:
            image = load_img(self.image, target_size=(224, 224))
            image = img_to_array(image)
            image = np.expand_dims(image, axis=0)
            image = preprocess_input(image)

            model = MobileNetV2(weights='imagenet', include_top=False)
            predictions = model.predict(image)
            results = decode_predictions(predictions)

            food_lables = [label for (_,label, _) in results[0]]
            return food_lables
        except Exception as e:
            print(e)

    def extract_text(self):
        try:
            img = cv2.imread(self.image)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            text = pt.image_to_string(thresh, lang='eng')
            return text
        except Exception as e:
            print(e)


