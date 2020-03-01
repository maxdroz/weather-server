from http.server import BaseHTTPRequestHandler
import pymongo
import json
import os


class Server(BaseHTTPRequestHandler):
    password = os.getenv("mongoPswd", "794613718293")
    client = pymongo.MongoClient(
        'mongodb+srv://admin:{}@weatherdata-etum5.mongodb.net/test?retryWrites=true&w=majority'.format(password))
    db = client['weather']
    collection = db['data']

    def do_HEAD(self):
        return

    def do_POST(self):
        self.respond()
        return

    def do_GET(self):
        return

    def respond(self):
        context = self.handle_http(200, 'application/json')
        self.wfile.write(context)

    def handle_http(self, status, content_type):
        self.send_response(status)
        self.send_header('Content-Type', content_type)
        self.end_headers()
        return bytes(self.get_from_db(self.headers['from_ts'], self.headers['to_ts']), 'UTF-8')

    def get_from_db(self, from_timestamp, to_timestamp):
        if from_timestamp is not None and to_timestamp is not None:
            res = self.collection.find(
                {
                    '$and': [
                        {'timestamp': {'$gt': int(from_timestamp)}},
                        {'timestamp': {'$lt': int(to_timestamp)}}
                    ]
                }
            )
        elif from_timestamp is None and to_timestamp is not None:
            res = self.collection.find(
                {'timestamp': {'$lt': int(to_timestamp)}}
            )
        elif from_timestamp is not None and to_timestamp is None:
            res = self.collection.find(
                {'timestamp': {'$gt': int(from_timestamp)}}
            )
        else:
            res = self.collection.find()
        ans = []
        for entry in res:
            js = {
                "temperature": entry["temperature"],
                "humidity": entry["humidity"],
                "pressure": entry["pressure"],
                "altitude": entry["altitude"],
                "timestamp": entry["timestamp"],
            }
            ans.append(js)
        return json.dumps(ans)