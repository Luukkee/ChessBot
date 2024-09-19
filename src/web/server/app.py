from routes import *
from flask_cors import CORS
CORS(app)

#Run application
if __name__ == '__main__': 
    with app.app_context():
        db.create_all()   
    app.run(debug=True, port = 5001)
