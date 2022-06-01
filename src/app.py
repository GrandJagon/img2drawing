import os

from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource, reqparse, abort
from werkzeug.datastructures import FileStorage

# Local imports from service classes
import services.cartoonify as cartoon
from services.hash import hash_filename
from services.storage import Storage


app = Flask(__name__)
api = Api(app)

# Retrieving global variables from server environmenbt variables
PORT = os.environ.get('PORT')
ID_HEADER_KEY = os.environ.get('IP_HEADER_KEY')


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Temporary folder to store raw images before processing
STORAGE_DIR_TEMP = APP_ROOT + '/temp/'

authorized_types = ['image/jpeg', 'image/png', 'application/octet-stream']

# Creating parser to make sure request are formatted the good way
# 'userId':string in headers and 'image':multipart-file in body
cartoon_post_args = reqparse.RequestParser()
cartoon_post_args.add_argument(ID_HEADER_KEY, type=str, location='headers', help="L'ID utilisateur doit être présent", required=True)
cartoon_post_args.add_argument('image', type=FileStorage, required=True, location='files', help="L'image est manquante")

# Function to check whether the image has the right type
def abort_if_wrong_type(img):
    if img.mimetype not in authorized_types:
        # HTTP response
        abort(400, message = "L'image doit-être au format PNG ou JPEG")

# Resource responsible for the endpoint /cartoon/
# Methods corresponding to request are coded in here
class Cartoon(Resource):
    def post(self):
        args = cartoon_post_args.parse_args()
        img = args['image']
        user_id = request.headers[ID_HEADER_KEY]
        abort_if_wrong_type(img)

        try:
            # Saves raw image in temp folder
            temp_path = STORAGE_DIR_TEMP + img.filename
            img.save(temp_path)

            # Gets the processed image 
            cartoon_img = cartoon.comicFromPath(temp_path)

            # Hashes the file name
            cartoon_img_hash = hash_filename(img.filename)

            # Creates a folder for user if first time
            if(Storage.checkIfFolderExist(user_id) == False):
                Storage.addFolder(user_id)
        
            folder = Storage.getFolderPath(user_id)
            final_path = os.path.join(folder, cartoon_img_hash)

            cartoon_img.save(final_path)

            os.remove(temp_path)

            return send_file(final_path, 'image/jpeg')

        except Exception as e:
            print(e.with_traceback())
            return "Internal server error, check the log"

        
# Tying Cartoon class to appropriate endpoint
api.add_resource(Cartoon, "/")


if __name__ == '__main__':
    app.run(port=PORT)
    
    
    