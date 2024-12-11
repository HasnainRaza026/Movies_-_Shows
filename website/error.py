from flask import Blueprint, render_template, current_app

error = Blueprint('error', __name__)

# Error handler for 404 (Page Not Found)
@error.app_errorhandler(404)  # Use @app_errorhandler instead of @error.errorhandler
def page_not_found(e):
    current_app.logger.error(f"Page not found: {e}")
    return render_template("error.html", message="Page not found."), 404

# Error handler for 500 (Internal Server Error)
@error.app_errorhandler(500)
def internal_server_error(e):
    current_app.logger.error(f"Internal server error: {e}")
    return render_template("error.html", message="Internal server error occurred."), 500

# General error handler for uncaught exceptions
@error.app_errorhandler(Exception)
def handle_exception(e):
    current_app.logger.error(f"Unhandled exception: {e}")
    return render_template("error.html", message="An unexpected error occurred."), 500
