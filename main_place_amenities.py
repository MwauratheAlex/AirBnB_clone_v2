#!/usr/bin/python3
""" Test link Many-To-Many Place <> Amenity
"""
from models import *
from models.state import State

# creation of a State
state = State(name="California")
state.save()

print("OK")
