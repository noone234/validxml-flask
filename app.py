import os

# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, Response, send_from_directory
from werkzeug import secure_filename
from lxml import etree

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


# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']

    # Check if the file is one of the allowed types/extensions
    if file:
        if allowed_file(file.filename):

            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)

            # Move the file from the temporal folder to
            # the upload folder we setup
            saved_filename = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_filename)

            # Validate the file.
            return validate_xml_file(saved_filename)

        elif file.filename == '':
            return render_template('nofile.html')

        else:
            return render_template('badfiletype.html')


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
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
        port=int("5000"),
        debug=True
    )

