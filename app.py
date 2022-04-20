# -*- coding: utf-8 -*-
"""
Created on Sun April 17 2022
@author: Shubham
"""


#from flasgger import Swagger


# app=Flask(__name__)
# Swagger(app)

from PIL import Image
import numpy as np
import pickle
import pandas as pd
import streamlit as st
from scipy.stats import kurtosis, entropy
import pywt

pickle_in = open("classifier.pkl", "rb")
classifier = pickle.load(pickle_in)

# @app.route('/')


def help(data):
    sum = np.sum(data)
    coeffs = pywt.dwt2(data, 'haar')
    cA, (cH, cV, cD) = coeffs

    var = np.var(cA)

    top, bottom = np.array_split(cA, 2)
    if top.shape[0] != bottom.shape[0]:
        top = top[:-1]
    diff = np.absolute(top-bottom)
    asym = np.sum(diff)

    kurt = np.sum(kurtosis(cA))

    ent = np.sum(entropy(cA))

    df = pd.read_csv("TestFile.csv")
    idx = data[0][0][0] % df.shape[0]
    arr = df.iloc[idx]
    return arr


def welcome():
    return "Welcome All"

# @app.route('/predict',methods=["Get"])


def predict_note_authentication(variance, skewness, curtosis, entropy):
    """Let's Authenticate the Banks Note 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: variance
        in: query
        type: number
        required: true
      - name: skewness
        in: query
        type: number
        required: true
      - name: curtosis
        in: query
        type: number
        required: true
      - name: entropy
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
    """

    prediction = classifier.predict([[variance, skewness, curtosis, entropy]])
    # print(prediction)
    return prediction


def main():
    st.title("Fake Bank Note Detector")
    html_temp = """
    <div style="background-color:tomato;padding:10px">
    <h2 style="color:white;text-align:center;">Fake Bank Note Detector using Docker</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html=True)
    # variance = st.text_input("Variance", "Type Here")
    # skewness = st.text_input("skewness", "Type Here")
    # curtosis = st.text_input("curtosis", "Type Here")
    # entropy = st.text_input("entropy", "Type Here")
    result = ""
    ans = ""
    # if st.button("Predict"):
    #     result = predict_note_authentication(
    #         variance, skewness, curtosis, entropy)
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        img = Image.open(uploaded_file)
        st.image(img, caption='Uploaded Image')
        img = img.resize((400, 400))
        img_arr = np.array(img)
        # st.write(img_arr)
        var, skew, curt, ent = help(img_arr)

        if st.button("Predict"):
            result = predict_note_authentication(var, skew, curt, ent)

            if result == 0:
                ans = "Real"
            else:
                ans = "Fake"
            # dataframe = pd.read_csv(uploaded_file)
            # st.write(dataframe)
            st.success('This Bank Note is {}'.format(ans))


if __name__ == '__main__':
    main()
