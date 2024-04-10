from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Day, Meal, User, Product, SelectedDayId
from . import db
import json
from datetime import datetime
import sqlite3
from sqlalchemy import inspect


def loadJSON(file_path):
    with open(file_path) as json_file:
        file_contents = json_file.read()
    dict = json.loads(file_contents)
    return dict

data = loadJSON("website/foods.json")
foods = data["foods"]

for food in foods:
    constituents_dict = {} #Dict
    constituents_list = food["constituents"] #List


    for con in constituents_list:
        try:
            if con["unit"] == "mg":
                quantity = con["quantity"] / 1000
            elif con["unit"] == 'µg':
                quantity = con["quantity"] / 1000000
            else:
                quantity = con["quantity"]
            constituents_dict[con["nutrientId"]] = quantity
        except:
            constituents_dict[con["nutrientId"]] = 0

    protein = constituents_dict['Protein'] #Float
    fat = constituents_dict["Fett"] #Float
    carbs = constituents_dict["Karbo"] #Float
    sukker = constituents_dict['Sukker'] #Float

    flerum = constituents_dict["Flerum"] #Float
    stivel = constituents_dict["Stivel"] #Float
    alko = constituents_dict["Alko"] #Float
    niacin = constituents_dict['Niacin'] #Float
    vitE = constituents_dict['Vit E'] #Float
    vitB1 = constituents_dict["Vit B1"] #Float
    vitB12 = constituents_dict['Vit B12'] #Float
    vitA = constituents_dict["Vit A"] #Float
    vitD = constituents_dict["Vit D"] #Float
    vitB2 = constituents_dict["Vit B2"] #Float
    vitB6 = constituents_dict["Vit B6"] #Float
    vitC = constituents_dict["Vit C"] #Float
    fiber = constituents_dict["Fiber"] #Float
    retinol = constituents_dict["Retinol"] #Float
    fiber = constituents_dict["Fiber"] #Float
    omega6 = constituents_dict["Omega-6"] #Float
    vann = constituents_dict['Vann'] #Float


    kcal = food["calories"]["quantity"] #Float
    # kj = food["energy"]["quantity"] #Float
    portions = food["portions"] #List
    name = food["foodName"] #String

print(foods[0]["constituents"])




