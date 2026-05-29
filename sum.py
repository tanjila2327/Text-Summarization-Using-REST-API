from flask import Flaask, request, jsonify, render_template
from flask_cors import CORS  # Import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask_restx import Api, Resource, fields

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Secret key for encoding the JWT token
app.config['JWT_SECRET_KEY'] = "a#jghjh$"

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Your MySQL username
app.config['MYSQL_PASSWORD'] = 'tanzila@123'  # Your MySQL password
app.config['MYSQL_DB'] = 'summary'  # Use the summary database

# Initialize the JWT Manager and MySQL
jwt = JWTManager(app)
mysql = MySQL(app)

# Initialize Flask-RESTX for Swagger
api = Api(app, version='1.0', title='Summerizer API', description='A simple API for managing summaries')
ns = api.namespace('summaries', description='Operations related to summaries')

# Define the input/output models
summary_model = api.model('Summary', {
    'id': fields.Integer(readonly=True, description='The unique identifier of a summary'),
    'original_text': fields.String(required=True, description='The original text to be summarized'),
    'summary': fields.String(required=True, description='The summary of the original text')
})

# Define the login response model for Swagger
login_model = api.model('Login', {
    'username': fields.String(required=True, description='The username'),
    'password': fields.String(required=True, description='The password')
})

# Serve the login page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')  # Make sure login.html is in the templates folder

# Define the login route (for API) - Handles the POST request for login
@app.route('/login', methods=['POST'])
def login():
    # Get the request data
    data = request.get_json()

    # Extract the username and password from the data
    username = data['username']
    password = data['password']

    # Check if the credentials match
    if username == 'admin' and password == 'admin123':
        # Create an access token for the user
        access_token = create_access_token(identity=username)

        # Return the token as a JSON response
        return jsonify(access_token=access_token), 200
    else:
        # Return an error response if credentials are invalid
        return jsonify({"msg": "Invalid credentials"}), 401

# Add Swagger documentation for login
@ns.route('/login')
class Login(Resource):
    @api.doc('login_user')
    @api.expect(login_model)  # Expect data in login_model format
    def post(self):
        """Login the user and return a JWT token"""
        return {"msg": "Please log in to get a token"}, 200

# CREATE: Add new record
@ns.route('/create')
class CreateSummary(Resource):
    @api.doc('create_summary')
    @api.expect(summary_model)  # Expect data in summary_model format
    def post(self):
        data = request.get_json()  # This retrieves the data sent from Swagger
        original_text = data['original_text']
        summary_text = data['summary']

        # Connecting to the database and inserting the new record
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO summaries (original_text, summary) VALUES (%s, %s)', (original_text, summary_text))
        mysql.connection.commit()  # Commit the changes to the database
        cursor.close()  # Close the cursor after the operation

        # Return success response
        return jsonify({"msg": "Record created successfully!"}), 201


# READ: Get all records
@app.route('/summaries')
def show_summaries():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM summaries')  # Fetch all records from the summaries table
    summaries = cursor.fetchall()  # Get all the records as a list of dictionaries
    cursor.close()

    # Render the HTML page and pass the fetched data to the template
    return render_template('summaries.html', summaries=summaries)


# UPDATE: Update a record
@ns.route('/update/<int:id>')
class UpdateSummary(Resource):
    @api.doc('update_summary')
    @api.expect(summary_model)  # Expect data in summary_model format
    def put(self, id):  # Use PUT for updating data
        """
        Update the summary record with the provided ID.
        This method will update the original_text and summary of an existing record.
        """
        data = request.get_json()

        # Extract original_text and summary from the request data
        original_text = data['original_text']
        summary_text = data['summary']

        # Connecting to the database and updating the existing record
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE summaries SET original_text=%s, summary=%s WHERE id=%s', (original_text, summary_text, id))
        mysql.connection.commit()  # Commit the changes to the database
        cursor.close()

        return jsonify({"msg": "Record updated successfully!"}), 200


# DELETE: Delete a record
@ns.route('/delete')
class DeleteSummary(Resource):
    @api.doc('delete_summary')
    @api.expect(api.model('DeleteID', {'id': fields.Integer(required=True, description='The ID of the summary to delete')}))
    def delete(self):  # Use DELETE method for deleting
        data = request.get_json()
        summary_id = data['id']

        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM summaries WHERE id=%s', (summary_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({"msg": "Record deleted successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=3000)  # Run the Flask app on port 3000
