import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from urllib.parse import unquote, urlparse


def load_books(file_path):
    with open(file_path, 'r') as file:
        books = json.loads(file.read())
    add_filename_books(books)
    return books


def parse_filename(url):
    file_path = unquote(urlparse(url).path)
    return os.path.basename(file_path)


def add_filename_books(books):
    for book in books:
        book['cover_filename'] = parse_filename(book['image_url'])


def rebuild_site():

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    books = load_books('library.json')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    print('Site rebuild')


def main():
    server = Server()
    rebuild_site()
    server.watch('template.html', rebuild_site)
    server.serve(root='.')


if __name__ == '__main__':
    main()
