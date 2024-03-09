from flask import render_template, flash, request, url_for, redirect, jsonify
from flask_login import login_user



def return_error() -> None:
    flash("Invalid username or password", "danger")
