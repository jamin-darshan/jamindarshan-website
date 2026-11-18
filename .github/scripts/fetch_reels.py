"""Pull the latest reels from the Jamin Darshan Instagram account (official Instagram Graph API)
and save them as insta/reels.json plus local thumbnails, so the website can show them."""
import json, os, re, urllib.request, urllib.parse

TOKEN, USER = os.environ.get('IG_TOKEN', '').strip(), os.environ.get('IG_USER_ID', '').strip()
OUT = 'insta'; os.makedirs(OUT, exist_ok=True)
if not TOKEN or not USER:
    print('IG_TOKEN / IG_USER_ID not set yet - keeping the reels section hidden'); raise SystemExit(0)

q = urllib.parse.urlencode({'fields': 'id,caption,media_type,media_product_type,thumbnail_url,permalink,timestamp', 'limit': 30, 'access_token': TOKEN})
data = json.load(urllib.request.urlopen(f'https://graph.facebook.com/v21.0/{USER}/media?{q}', timeout=60))
reels = []
for m in data.get('data', []):
    if m.get('media_type') != 'VIDEO' or not m.get('thumbnail_url'):
        continue
    thumb = f"{OUT}/{m['id']}.jpg"
    urllib.request.urlretrieve(m['thumbnail_url'], thumb)          # Instagram image links expire, so keep a copy
    first = (m.get('caption') or '').strip().splitlines()[0] if m.get('caption') else ''
    title = re.sub(r'[\U0001F000-\U0001FAFF☀-➿️]', '', first).strip()[:60]
    reels.append({'id': m['id'], 'permalink': m['permalink'], 'thumb': thumb, 'title': title, 'time': m.get('timestamp')})
    if len(reels) == 6:
        break
json.dump(reels, open(f'{OUT}/reels.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print('saved', len(reels), 'reels')
