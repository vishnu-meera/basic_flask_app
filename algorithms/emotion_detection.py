from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import requests
import json
import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt  
import cv2

class EmotionAl(Resource):
   
    def rgb2gray(self,rgb):
        return np.dot(rgb[...,:3], [0.299, 0.587, 0.114])

    def resize_img(self,img):
        img = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_AREA)
        img.resize((1, 1, 64, 64))
        return img

    def preprocess(self,img):
        if img.shape == (64, 64):
            img.resize((1, 1, 64, 64))
            return img
        grayscale = self.rgb2gray(img)
        processed_img = self.resize_img(grayscale)
        return processed_img

    def post(self):
        ret = ""
        print("here")
        print(request.files)
        for upload in request.files.getlist("file"):
            print("xxxx")
            img = mpimg.imread(upload)
            img = self.preprocess(img)
            scoring_uri = 'http://7a38107b-75de-4cc2-9611-3a74ec05c9e0.eastus.azurecontainer.io/score'
            input_data = json.dumps({'data': img.tolist()})
            headers = {'Content-Type': 'application/json'}
            ret = requests.post(scoring_uri, input_data, headers=headers)
            print(ret)
        return ret.text
