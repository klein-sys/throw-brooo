# -*- coding: utf-8 -*-
import sys
import os

# Add builder to sys.path
sys.path.insert(0, os.path.dirname(__file__))

from html_head import HTML_HEAD
from html_ui import HTML_UI
from js_data import JS_DATA
from js_audio import JS_AUDIO
from js_calculus import JS_CALCULUS
from js_model_framework import JS_MODEL_FRAMEWORK
from animal_models import JS_ANIMAL_MODELS
from js_three import JS_THREE
from js_gameplay import JS_GAMEPLAY

full_html = HTML_HEAD + HTML_UI + "\n  <script>\n" + JS_DATA + JS_AUDIO + JS_CALCULUS + JS_MODEL_FRAMEWORK + JS_ANIMAL_MODELS + JS_THREE + JS_GAMEPLAY

workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
file1 = os.path.join(workspace_dir, "throw_food_for_animals_3d_calculus_edition.html")
file2 = os.path.join(workspace_dir, "index.html")

with open(file1, "w", encoding="utf-8") as f:
    f.write(full_html)

with open(file2, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"Successfully generated:\n- {file1} ({len(full_html)} bytes)\n- {file2} ({len(full_html)} bytes)")
