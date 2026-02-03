import feedparser
import json
from bs4 import BeautifulSoup

# List of RSS feed URLs
urls = [
    "https://sckr.si/?show=1000&format=feed&type=rss",
    "https://sckr.si/sts/124-aktualno?format=feed&type=rss",
    "https://sckr.si/sts/?format=feed&type=rss"
]

def getNews():
    data = []
    for url in urls:
        try:
            feed = feedparser.parse(url)
            feed_data = {
                'title': getattr(feed.feed, 'title', ''),
                'description': getattr(feed.feed, 'description', ''),
                'link': getattr(feed.feed, 'link', ''),
                'language': getattr(feed.feed, 'language', ''),
                'lastBuildDate': getattr(feed.feed, 'updated', ''),
                'entries': []
            }
            for entry in feed.entries:
                entry_data = {
                    'title': getattr(entry, 'title', ''),
                    'link': getattr(entry, 'link', ''),
                    'guid': getattr(entry, 'guid', ''),
                    'description': getattr(entry, 'description', ''),
                    'author': getattr(entry, 'author', ''),
                    'category': getattr(entry, 'category', ''),
                    'pubDate': getattr(entry, 'published', ''),
                    'images': []
                }
                # Parse description for cleaning HTML and extracting images
                if entry_data['description']:
                    soup = BeautifulSoup(entry_data['description'], 'html.parser')
                    # Clean description to text only
                    entry_data['description'] = soup.get_text()
                    # Extract images
                    imgs = soup.find_all('img')
                    for img in imgs:
                        img_data = {
                            'src': img.get('src', ''),
                            'alt': img.get('alt', ''),
                            'width': img.get('width', ''),
                            'height': img.get('height', ''),
                            'style': img.get('style', '')
                        }
                        entry_data['images'].append(img_data)
                else:
                    entry_data['description'] = ''
                feed_data['entries'].append(entry_data)
            data.append(feed_data)
        except Exception as e:
            print(f"Error parsing {url}: {e}")
    return data

if __name__ == "__main__":
    data = getNews()
    print(json.dumps(data, indent=4, ensure_ascii=False))