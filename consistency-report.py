import json
import re
import sys

filename = sys.argv[1]


def get_user(meta):
    if 'createdByUser' in meta:
        user_info = meta['createdByUser']
        if 'name' in user_info:
            return user_info['name']


def log_problem(e, msg):
    print('https://www.zotero.org/groups/2480461/ag-gipp/items/' + e['data'][
        'key'] + "/item-details " + msg + ' (' + get_user(e['meta']) + ')')


def parse_extra_field(d, ent):
    extra = d.split('\n')
    extra_dictionary = {}
    for e in extra:
        if len(e.strip()) > 0:
            parts = e.split(':', 1)
            if len(parts) == 2:
                extra_dictionary[parts[0].strip()] = parts[1].strip()
            else:
                log_problem(ent, 'unlabeled extra information: ' + e)
    return extra_dictionary


with open(filename) as f:
    bibtex = json.loads(f.read())
    file_pat = re.compile('--[a-zA-Z]{2,}--')
    for entry in bibtex:
        data = entry['data']
        tags = data['tags']
        biblatex = entry['biblatex']
        if len(tags) == 0 and len(biblatex) > 3:
            log_problem(entry, "has no tags")
        if 'extra' in data:
            edict = parse_extra_field(data['extra'], entry)
            if 'Citation Key' in edict:
                cite_key = edict['Citation Key']
                if len(cite_key) < 4:
                    log_problem(entry, cite_key + ' is too short as citation key.')
        if 'filename' in data:
            fname = data['filename']
            if not file_pat.search(fname):
                log_problem(entry, "does not comply with naming convention:" + fname)
