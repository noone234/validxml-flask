"""
This Flask application validates an XML file against a schema.
"""

import os
from flask import Flask, render_template, request, Response, send_from_directory
from werkzeug import secure_filename
from lxml import etree

__author__ = "Christopher Wolfe"
__copyright__ = "Copyright 2018, Christopher Wolfe"
__license__ = "MIT"
__maintainer__ = "Christopher Wolfe"
__email__ = "noone234@gmail.com"
__status__ = "Development"

# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads/'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['xml','XML'])
# This is the path to the XML schema used for validation.
app.config['XML_SCHEMA_PATH'] = '/u/scs_layout/tools/inc/product.xsd'

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

def validate_xml_file(xmlfilename):
    try:
        doc = etree.parse(xmlfilename)
        xsd = etree.parse(app.config['XML_SCHEMA_PATH'])

        xmlschema = etree.XMLSchema(xsd)
        xmlschema.assertValid(doc)
    
        print("%s validates" % xmlfilename)
        return render_template('valid.html', xmlfilename=xmlfilename)

    # So many exceptions, so little time...
    except etree.XMLSyntaxError as e:
        print("%s doesn't validate" % xmlfilename)
        print("PARSING ERROR", e)
        return render_template('invalid.html', xmlfilename=xmlfilename, error_summary='It is not even valid XML.')
    except etree.DocumentInvalid as e:
        print("%s doesn't validate" % xmlfilename)
        print("INVALID DOCUMENT", e)
        return render_template('invalid.html', xmlfilename=xmlfilename, error_summary="It does not comply with product.xsd; the XML schema", error_log=xmlschema.error_log)
    except AssertionError as e:
        print("%s doesn't validate" % xmlfilename)
        print("INVALID DOCUMENT", e)
        return render_template('invalid.html', xmlfilename=xmlfilename, error_summary='Invalid Document', error_log=xmlschema.error_log)


@app.route('/')
def index():
    # Prompt the user to upload an XML file.
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']

    # Check if the file is one of the allowed types/extensions
    if not file:
        return render_template('nofile.html')
    elif file.filename == '':
        return render_template('nofile.html')
    elif not allowed_file(file.filename):
        return render_template('badfiletype.html')
    else:
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)

        # Move the file from the temporal folder to
        # the upload folder we setup
        saved_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(saved_filename)

        # Validate the file.
        return validate_xml_file(saved_filename)


# This route expects a parameter containing the name of a file.
# Then it will locate that file in the upload directory
# and show it on the browser.  So if the user uploads
# an image, that image can be shown after the upload.
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/schema.xsd')
def xml_schema():
    return Response(open(app.config['XML_SCHEMA_PATH']).read(), mimetype='text/xml')

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

