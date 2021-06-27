from flask_cors import CORS
from flask import Flask, request
from newspaper import Article
from flask_restful import Api, Resource
from transformers  import pipeline
import json
import os

#dont change until the lambda AWS is ready
apikey = "000000abc1234ABC"

app = Flask(__name__)
api = Api(app)

#habilita la conexion y resuelve problemas de CORS
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#USE Transformer/Hugginface BERT API
nlp = pipeline(
    'question-answering',
    model='mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
    tokenizer=(
        'mrm8488/distill-bert-base-spanish-wwm-cased-finetuned-spa-squad2-es',
        {"use_fast": False}
    )
)

#class for serving bert api
class Bert(Resource):
    @staticmethod
    def post():
        y = request.get_json()
        if y["apikey"] == apikey:
            #responde con el texto de una pagina web solicitada.
            article = Article(y["url"], language="es")
            article.download()
            article.parse()
            contexto = article.text
            answer = nlp({'question':y["question"], 'context':contexto})
            out = {'Prediction': answer['answer'] }
            return out, 201
        else:
            return "{'msg':'error este no es el origen'", 404

api.add_resource(Bert,  '/api/v1/bert')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, threaded=True)
