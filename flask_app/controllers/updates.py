from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models import user, report, city