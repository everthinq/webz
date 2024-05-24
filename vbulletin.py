from typing import List

import requests
import re

base_url = 'https://forum.vbulletin.com/forum/vbulletin-3-8/vbulletin-3-8-questions-problems-and-troubleshooting/414325-www-vs-non-www-url-causing-site-not-to-login'
content_regex = re.compile(r'<div class="js-post__content-text restore h-wordwrap" itemprop="text">(.*?)</div>', re.DOTALL)


def main():
    # Fetch response from the url
    response = get_response(from_url=base_url)

    # Extract posts content into a list
    posts = content_regex.findall(response.text)

    # Write posts contents into a file
    write_posts(posts=posts, file_name='vbulletin.txt', response=response)


def get_response(from_url: str) -> requests.models.Response:
    return requests.get(url=from_url)


def write_posts(file_name: str, posts: List, response: requests.models.Response) -> None:
    # Extract text from each post and write it down
    with open(file_name, 'w+') as file:
        for index, post_html in enumerate(posts):
            post_text = re.sub(r'<br><br>', '\n', post_html)  # change <br> to new line
            post_text = re.sub(r'&quot;', '"', post_text)  # change &quot; to "
            post_text = re.sub(r'<.*?>', '', post_text).strip()  # remove HTML tags

            # Process posts with quoting blocks
            if 'class="bbcode_container"' in post_html:
                quotes_regex = re.compile(
                    r'<div class="js-post__content-text restore h-wordwrap" itemprop="text">(.*?)<div class="b-post__footer h-hide--on-preview">',
                    re.DOTALL
                )
                quotes_posts = quotes_regex.findall(response.text)

                post_text = re.sub(r'<.*?>', '', quotes_posts[index])  # remove HTML tags
                post_text = re.sub(r'</?(a|span)[^>]*>', '', post_text)  # remove the remaining HTML tags
                post_text = re.sub(r'&quot;', '"', post_text)  # change &quot; to "
                post_text = re.sub(r'<br>', '\n', post_text)  # change <br> to new line
                post_text = re.sub(r'&#91;', '[', post_text)  # change &#91; to [
                post_text = re.sub(r'&#93;', ']', post_text)  # change &#93; to ]
                post_text = re.sub(r'\s+', ' ', post_text).strip()  # replace a bunch of spaces with a single space

            file.write(f"{index + 1}. [{post_text}]\n\n")
            print(f"{index + 1}. [{post_text}]\n")


if __name__ == "__main__":
    main()
