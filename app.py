
# importing the necessary dependencies
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import pickle

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            pclass = request.form['PassengerClass']
            
            Age=float(request.form['Age'])
            SibSp = request.form['SibSp']
            Parch = request.form['Parch']

            Fare = float(request.form['Fare'])
            Gender = request.form['Gender']
            if(Gender=='Female'):
                female=1
                male=0
            else:
                female=0
                male=1

            Embarked = request.form['Embarked']
            if(Embarked=='C'):
                C=1
                Q=0
                S=0
            elif (Embarked=='Q'):
                C=0
                Q=1
                S=0
            else:
                C=0
                Q=0
                S=1
            
            filename = 'model.pkl'
            model = pickle.load(open(filename, 'rb')) # loading the model file from the storage
            # predictions using the loaded model file
            prediction=model.predict([[pclass , Age, SibSp, Parch, Fare, female, male, C, Q, S]])
            print('prediction is', prediction)
            # showing the prediction results in a UI
            
            if prediction[0]== 1:
                return render_template('results.html',prediction='You would survive the Titanic')
            else:
                return render_template('results.html',prediction='Unfortunately, you wouldnt survive the Titanic')

            
            #return render_template('results.html',prediction=round(100*prediction[0]))
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')
    else:
        return render_template('index.html')



if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True) # running the app