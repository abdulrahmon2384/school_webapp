from flask import render_template, flash, request, url_for, redirect, jsonify
from flask_login import login_user


def login_user_and_redirect(user, role, next_page):
    login_user(user, remember=True)
    if role == "head teacher":
        return redirect(url_for('admin'))
    return redirect(url_for(next_page))


def return_error() -> None:
    flash("Invalid username or password", "danger")
