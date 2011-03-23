import httplib
import urllib
import json
import re

PLAYLIST_STATIC = {
    "key": "sdf883jsdf22",
    "path": "www.playlist.com",
    "searchTracks": "/async/searchbeta/tracks?searchfor=%s&page=%s"
}

def requestSongs(query, page=1):
    results = {
        "total": 0,
        "tracks": []
    }
    
    if len(query.strip()) == 0:
        return results
    
    conn = httplib.HTTPConnection(PLAYLIST_STATIC["path"])
    conn.request("GET", PLAYLIST_STATIC["searchTracks"] % (urllib.quote(query.encode('utf8')), page))
    res = conn.getresponse()

    if res.status == 200:
        resdata = re.compile(
            ".*PPL.search.trackdata = ([^\n]+);.*PPL.search.track_count = \"([^\n]+)\";.*", re.MULTILINE|re.DOTALL
        ).match(res.read())
        
        results["total"] = resdata.groups()[1]
        tracks = json.loads(resdata.groups()[0])
        
        for track in tracks:
            results["tracks"].append({
                "album": urllib.unquote(track["album"]),
                "artist": urllib.unquote(track["artist"]),
                "title": urllib.unquote(track["title"]),
                "songURL": rc4crypt(track["song_url"].decode('hex'), PLAYLIST_STATIC["key"]),
                "duration": track["duration"],
                "status": track["status"]
            })
                
    return results
    
# http://code.activestate.com/recipes/576736-rc4-arc4-arcfour-algorithm/
def rc4crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))

    return ''.join(out)