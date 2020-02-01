# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 20:00:29 2019

@author: Olaitan
"""
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import routes
