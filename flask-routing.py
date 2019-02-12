import json
import wikipedia
from flask import Flask
from flask import request
from flask import make_response

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    
    req_data = request.get_json()
    #print(req_data['queryText'])
    parameter = None
    response = None
    intent = req_data['queryResult']['intent']['displayName']
    if(intent == 'getInformation'):
        parameter = req_data['queryResult']['parameters']['placeToVisit']
        response = wikipedia.summary(parameter, sentences=1)
    else:
        parameter = req_data['queryResult']['parameters']['geo-country']
        response = countryRecommender(parameter)
    
    my_result =  {

    "fulfillmentText": response,
     "source": parameter
    }

    res = json.dumps(my_result, indent=4)

    r = make_response(res)

    r.headers['Content-Type'] = 'application/json'
    return r


def countryRecommender(country):
    answer = 'something'
    if(country.lower() == 'france'):
        answer = 'best places in France are: (1) eiffel tower, (2) louvre and (3) seine'
    elif(country.lower() == 'germany'):
        answer = 'best places in Germany are: (1) berlin, (2) frankfurt and (3) Niederwalddenkmal'
    elif(country.lower() == 'thailand'):
        answer = 'best places in Thailand are: (1) chiang mai, (2) phuket and (3) ko samui'
    elif(country.lower() == 'india'):
        answer = 'best places in India are: (1) taj mahal, (2) jaipur and (3) ganga'
    elif(country.lower() == 'singapore'):
        answer = 'best places in Singapore are: (1) marina bay, (2) sentosa and (3) universal studios singapore'
    elif(country.lower() == 'canada'):
        answer = 'best places in Canada are: (1) vancouver, (2) banff and (3) brock\'s monument'
    else:
        answer = 'Sorry, I haven\'t been trained for '+ country
        rv = wikipedia.summary(country, sentences=1) + '\n' + answer + '\n'
        return rv
    options = "Please select from any of the options to get more information aobut the place."
    rv = wikipedia.summary(country, sentences=1) + '\n' + options + answer + '\n' 
    return rv
    
@app.route('/test', methods=['GET'])
def test():
    return  "Successfully transmitting data from my laptop to my ChatBot"

@app.route('/', methods=['GET'])
def home():
    return  "Welcome to my local server"

if __name__ == '__main__':
    
    print("Running app on localhost port 5000")
    app.run(debug=True, port=5000)