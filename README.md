# validxml

Validates an XML file against a Schema using Python and Flask.

This app assumes that you have an XML schema which other people, companies,
or organizations want to comply with.  The app helps them confirm that their
XML file (1) is valid and (2) complies with your schema.  This can save you
a whole lot of time as it has for me, because it can delegate XML validation
tasks from you to a web app.

**Status: beta**
This application works, therefore it is in beta status.

**Configuring the XML Validator**

After downloading this Git repository, search the source code for all
occurences of "schema.xsd" and "/path/to/schema.xsd".  Replace those with
your XML schema.
