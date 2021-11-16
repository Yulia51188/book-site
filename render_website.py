import json
import os
from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from urllib.parse import unquote, urlparse


BOOKS_ON_PAGE = 10
COL_NUM = 2


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
    paged_books = chunked(books, BOOKS_ON_PAGE)

    for page_index, books_on_page in enumerate(paged_books, start=1):
        rendered_page = template.render(
            book_sets=list(chunked(books_on_page, COL_NUM)),
        )
        
        os.makedirs('pages', exist_ok=True)
        html_path = os.path.join('pages', f'index{page_index}.html')
        with open(html_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    server = Server()
    rebuild_site()
    server.watch('template.html', rebuild_site)
    server.serve(root='./pages')


if __name__ == '__main__':
    main()
