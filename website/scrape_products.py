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

foods = loadJSON("website\foods.json")

for key, value in foods.items():
    print(key, value)