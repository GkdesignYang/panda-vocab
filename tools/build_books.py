#!/usr/bin/env python3
"""
重新生成 books/*.json 词库。

用法（在仓库根目录）：
    python3 tools/build_books.py

脚本会把原始词表下载到 tools/cache/（已在 .gitignore 里忽略），
然后输出 8 本词书到 books/。每个词条格式：
    [单词, 音标, 词性, 短释义(竹笋上显示), 完整释义]

数据来源（许可证见 THIRD_PARTY_NOTICES.md）：
  - KyleBing/english-vocabulary (BSD-3-Clause)：初中、高中、四级、六级、托福、SAT
  - skywind3000/ECDICT (MIT)：音标、雅思词表（tag=ielts）、PET 释义
  - 剑桥 B1 Preliminary Vocabulary List：PET 单词表（tools/pet_words.txt，仅单词）
"""
import csv
import json
import os
import re
import sys
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, 'tools', 'cache')
OUT = os.path.join(ROOT, 'books')
os.makedirs(CACHE, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

KYLE = 'https://raw.githubusercontent.com/KyleBing/english-vocabulary/master/json/'
ECDICT_URL = 'https://raw.githubusercontent.com/skywind3000/ECDICT/master/ecdict.csv'
KYLE_BOOKS = {
    'junior': '1-初中-顺序.json',
    'senior': '2-高中-顺序.json',
    'cet4': '3-CET4-顺序.json',
    'cet6': '4-CET6-顺序.json',
    'toefl': '6-托福-顺序.json',
    'sat': '7-SAT-顺序.json',
}


def fetch(url, name):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        print('下载', url)
        parts = urllib.parse.urlsplit(url)
        safe = urllib.parse.urlunsplit(parts._replace(path=urllib.parse.quote(parts.path)))
        with urllib.request.urlopen(safe, timeout=300) as r, open(path, 'wb') as f:
            f.write(r.read())
    return path


# ---------- ECDICT index ----------
csv.field_size_limit(sys.maxsize)
ec, ielts_rows = {}, []
with open(fetch(ECDICT_URL, 'ecdict.csv'), encoding='utf-8') as f:
    for row in csv.DictReader(f):
        k = row['word'].lower()
        if 'ielts' in row['tag'].split():
            ielts_rows.append(row)
        if k in ec and ec[k]['word'] == k:  # prefer the lowercase entry
            continue
        ec[k] = row

POS_MAP = {'a': 'adj', 'adj': 'adj', 'ad': 'adv', 'adv': 'adv', 'n': 'n', 'v': 'v', 'vt': 'v', 'vi': 'v',
           'prep': 'prep', 'conj': 'conj', 'pron': 'pron', 'num': 'num', 'art': 'art', 'int': 'int',
           'interj': 'int', 'aux': 'aux', 'abbr': 'abbr', 'phr': 'phr', 'modal': 'v', 'det': 'det'}
BAD = ('人名', '地名', '姓氏', '男子名', '女子名', '复数', '过去式', '过去分词', '现在分词', '第三人称', '比较级', '最高级')


def clean_segments(text):
    t = text.replace('　', ' ')
    t = re.sub(r'\[[^\]]*\]', '', t)
    t = re.sub(r'【[^】]*】', '', t)
    t = re.sub(r'（[^）]*）', '', t)
    t = re.sub(r'\([^)]*\)', '', t)
    t = re.sub(r'<[^>]*>', '', t)
    t = t.replace('◎', '').replace('“', '').replace('”', '').replace('"', '')
    out = []
    for s in re.split(r'[；;，,、/]', t):
        s = s.strip(' .…。:：')
        if not s or any(b in s for b in BAD):
            continue
        if re.search(r'[A-Za-z]', s) or not re.search(r'[一-鿿]', s):
            continue
        if s not in out:
            out.append(s)
    return out


def norm_pos(p):
    p = (p or '').strip().strip('.').lower()
    parts = [x.strip('. ') for x in re.split(r'[&/,]', p) if x.strip('. ')]
    parts = [POS_MAP.get(x, x if len(x) <= 5 else '') for x in parts]
    parts = [x for i, x in enumerate(parts) if x and x not in parts[:i]]
    return '/'.join(parts)


def norm_phonetic(p):
    return (p or '').replace('\n', ' ').replace('ә', 'ə').replace("'", 'ˈ').replace('.', 'ˌ').replace('ɡ', 'g').strip()


def make_entry(word, items):
    """items: [(pos, text), ...] in priority order"""
    groups = []
    for pos, text in items:
        if '人名' in text or '地名' in text:
            continue
        segs = clean_segments(text)
        if not segs:
            continue
        pos = norm_pos(pos)
        for g in groups:
            if g[0] == pos:
                g[1].extend(s for s in segs if s not in g[1])
                break
        else:
            groups.append((pos, segs))
    if not groups:
        return None
    pos0, segs0 = groups[0]
    short = next((s for s in segs0 if 1 <= len(s) <= 7), None)
    if short is None:
        short = min(segs0, key=len)
        if len(short) > 10:
            short = short[:9] + '…'
    full = '  '.join((pos + '. ' if pos else '') + '；'.join(segs[:3]) for pos, segs in groups[:3])
    if len(full) > 46:
        full = full[:45] + '…'
    row = ec.get(word.lower())
    return [word, norm_phonetic(row['phonetic'] if row else ''), pos0, short, full]


def ecdict_items(row):
    items = []
    for line in row['translation'].split('\\n'):
        line = line.strip()
        if not line or line.startswith('['):
            continue
        m = re.match(r'^([a-z]+)\.\s*(.*)$', line)
        items.append((m.group(1), m.group(2)) if m else ('', line))
    return items


def finish(name, entries):
    seen, out = set(), []
    for e in entries:
        if e is None:
            continue
        k = e[0].lower()
        if k in seen or len(k) < 2:
            continue
        seen.add(k)
        out.append(e)
    path = os.path.join(OUT, f'{name}.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print(f'{name:7s} {len(out):6d} 词  {os.path.getsize(path) // 1024} KB')
    return out


# ---------- KyleBing books ----------
kyle_data = {name: json.load(open(fetch(KYLE + fn, fn), encoding='utf-8')) for name, fn in KYLE_BOOKS.items()}


def kyle(data):
    merged, order = {}, []
    for x in data:
        w = x['word'].strip()
        k = w.lower()
        if k not in merged:
            merged[k] = [w, []]
            order.append(k)
        for t in x.get('translations', []):
            merged[k][1].append((t.get('type', ''), t.get('translation', '')))
    res = []
    for k in order:
        w, items = merged[k]
        e = make_entry(w, items)
        if e is None and k in ec:
            e = make_entry(w, ecdict_items(ec[k]))
        res.append(e)
    return res


for name, data in kyle_data.items():
    finish(name, kyle(data))

# ---------- IELTS: ECDICT words tagged "ielts", alphabetical ----------
ielts_rows.sort(key=lambda r: r['word'].lower())
finish('ielts', [make_entry(r['word'], ecdict_items(r)) for r in ielts_rows])

# ---------- PET: Cambridge B1 Preliminary headwords, meanings from ECDICT ----------
phrase_dict = {}
for data in kyle_data.values():
    for x in data:
        for p in x.get('phrases') or []:
            phrase_dict.setdefault(p['phrase'].strip().lower(), p['translation'])
MANUAL = {'app': ('n', '应用程序'), 'café': ('n', '咖啡馆'), 'cashpoint': ('n', '自动取款机'),
          'download': ('v', '下载'), 'extreme sport': ('n', '极限运动'), 'internet': ('n', '互联网'),
          'laptop': ('n', '笔记本电脑'), 'motor-racing': ('n', '赛车运动'), 'online': ('adj', '在线的；网上的'),
          'rainforest': ('n', '雨林'), 'recycling': ('n', '回收利用'), 'social media': ('n', '社交媒体'),
          'upload': ('v', '上传')}
pet, missing = [], []
for line in open(os.path.join(ROOT, 'tools', 'pet_words.txt'), encoding='utf-8'):
    for w in (x.strip() for x in line.split(',')):
        if not w:
            continue
        k = w.lower()
        e = make_entry(w, ecdict_items(ec[k])) if k in ec else None
        if e is None and k in phrase_dict:
            e = make_entry(w, [('', phrase_dict[k])])
        if e is None and k in MANUAL:
            e = make_entry(w, [MANUAL[k]])
        if e is None:
            missing.append(w)
        pet.append(e)
finish('pet', pet)
if missing:
    print('PET 未找到释义：', ', '.join(missing))
print('完成。若词数有变化，请同步修改 index.html 里 BOOKS 的 count。')
