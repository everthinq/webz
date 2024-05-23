from typing import List

import requests
import re

base_url = 'https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-an'
content_regex = re.compile(r'<li class="notice.*?">(.*?)</ul>', re.DOTALL)


def main():
    # Fetch response from the url
    response = get_response(from_url=base_url)

    # Extract posts content into a list
    posts = content_regex.findall(response.text)

    # Write posts contents into a file
    write_posts(posts=posts, file_name='vbulletin.txt')


def get_response(from_url: str) -> requests.models.Response:
    return requests.get(url=from_url)


def write_posts(file_name: str, posts: List) -> None:
    # Extract text from each post and write it down
    with open(file_name, 'w+') as file:
        for index, post_html in enumerate(posts):
            post_text = re.sub(r'<br><br>', '\n', post_html)  # change <br> to new line
            post_text = re.sub(r'<.*?>', '', post_text)  # remove HTML tags
            post_text = re.sub(r'<div.*', '', post_text).strip()  # remove unclosed `<div` in the end specifically

            file.write(f"{index + 1}. [{post_text}]\n\n")
            print(f"{index + 1}. [{post_text}]\n")


if __name__ == "__main__":
    main()
