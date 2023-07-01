# validxml

Validates an XML file against a schema using Python and Flask.

This app assumes that you have an XML schema which other people, companies,
or organizations want to comply with. The app helps them confirm that their
XML file (1) is valid and (2) complies with your schema. This can save you
a whole lot of time as it has for me, because it can delegate XML validation
tasks from you to a web app.

## Status: beta

This application works, therefore it is in beta status.

## Prerequisites

Python 3

## Installation

Clone this Git repository.

    git clone https://github.com/noone234/validxml-flask.git

Run the following commands.

    cd validxml-flask
    python3 -m venv env
    . env/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

## Setup

Edit `app/__init__.py` in your favorite text editor.
Search for `XML_SCHEMA_PATH`.
Change that to your desired .xsd file and path.

## Usage

In the `validxml` directory, run `python manage.py`.
Flask will then start listening on port 5000 for requests.

People may direct their web browser to your server's port 5000, e.g.

    http://yourserver.com:5000/

...to use the XML Validator.

## Advanced Setup

In many cases, the above approach is powerful enough to meet your needs.
However you may wish to run this Flask application in a more powerful
web server like nginx. You may also wish to run this Flask application
in a Docker container. Such setups are documented well outside of this
project, and I wish you luck with them.
