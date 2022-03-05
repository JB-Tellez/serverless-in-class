from http.server import BaseHTTPRequestHandler
from datetime import date
from peewee import PostgresqlDatabase, Model, CharField, DateField
from urllib import parse


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        url_components = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_components.query)
        dic = dict(query_string_list)

        if "person" in dic:

            init_db()
            info = str(get_list())

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            message = info
            self.wfile.write(message.encode())


db = PostgresqlDatabase(
    "qqvxpcad",  # Required by Peewee.
    user="qqvxpcad",
    password="L4uSFU8WWvMB-BYTPnFshZ8hSDTMDjVb",
    host="kashin.db.elephantsql.com",
)


class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db

    def __repr__(self):
        return f"Person: name={self.name}, birthday={self.birthday}"

    def __str__(self):
        return f"{self.name}: {self.birthday}"


def init_db():
    db.connect()
    db.create_tables([Person])


def get_list():
    people = [person for person in Person.select()]
    return people


def get_one(id):
    # people = Person.select().where(Person.name == name).get()
    # people = Person.get(Person.name == name)
    people = Person.get_by_id(id)
    return people


def update_one(id, name):
    q = Person.update({Person.name: name}).where(Person.id == id)
    result = q.execute()
    return result


def delete_one(id):
    result = Person.delete_by_id(id)
    print(result)


def create(name, yyyy, m, d):
    person = Person(name=name, birthday=date(yyyy, m, d))
    return person.save()
