import os, sys, json, subprocess, platform, tempfile, gc
from collections import defaultdict
from datetime import date
from itertools import chain

pydir = os.path.abspath(os.path.dirname(__file__))
otfccdump = os.path.join(pydir, 'otfcc/otfccdump')
otfccbuild = os.path.join(pydir, 'otfcc/otfccbuild')
if platform.system() in ('Mac', 'Darwin'):
    otfccdump += '1'
    otfccbuild += '1'
if platform.system() == 'Linux':
    otfccdump += '2'
    otfccbuild += '2'

def getmulchar(allch):
    s = str()
    with open(os.path.join(pydir, 'datas/Multi.txt'), 'r', encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if allch:
                s += line.strip('#').strip()
            elif not line.startswith('#'):
                s += line
    return s

def addvariants():
    with open(os.path.join(pydir, 'datas/Variants.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            vari = line.strip().split('\t')
            codein = 0
            for ch1 in vari:
                if ord(ch1) in fontcodes:
                    codein = ord(ch1)
                    break
            if codein != 0:
                for ch1 in vari:
                    if ord(ch1) not in fontcodes:
                        font['cmap'][str(ord(ch1))] = font['cmap'][str(codein)]
                        fontcodes.add(ord(ch1))

def transforme():
    with open(os.path.join(pydir, 'datas/Chars_tct.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and (usemulchar or not s in mulchar):
                addunicodest(ord(t), ord(s))

def addunicodest(tcunic, scunic):
    if tcunic not in fontcodes:
        return
    tcname = font['cmap'][str(tcunic)]
    if str(scunic) in font['cmap']:
        scgly.add(font['cmap'][str(scunic)])
    font['cmap'][str(scunic)] = tcname
    fontcodes.add(scunic)

def build_glyph_codes():
    glyph_codes = defaultdict(list)
    for codepoint, glyph_name in font['cmap'].items():
        glyph_codes[glyph_name].append(codepoint)
    return glyph_codes

def removeglyhps():
    isrm=set()
    if tc=='TC':
        for v1 in scgly:
            if len(glyph_codes[v1])<1:
                #print('移除', v1)
                isrm.add(v1)
                del glyph_codes[v1]
                try:
                    font['glyph_order'].remove(v1)
                except ValueError:
                    pass
                del font['glyf'][v1]
    else:
        s = set(chain(
            range(0x0000, 0x007E + 1),
            range(0x02B0, 0x02FF + 1),
            range(0x2002, 0x203B + 1),
            range(0x2E00, 0x2E7F + 1),
            range(0x2E80, 0x2EFF + 1),
            range(0x3000, 0x301C + 1),
            range(0x3100, 0x312F + 1),
            range(0x3190, 0x31BF + 1),
            range(0xFE10, 0xFE1F + 1),
            range(0xFE30, 0xFE4F + 1),
            range(0xFF01, 0xFF5E + 1),
            range(0xFF5F, 0xFF65 + 1),
        ))
        with open(os.path.join(pydir, 'datas/Hans.txt'),'r',encoding = 'utf-8') as f:
            for line in f.readlines():
                if line.strip() and not line.strip().startswith('#'):
                    s.add(ord(line.strip()))
        useg=set()
        cdsall=set(map(str, s))
        for gln in font['glyph_order']:
            if gln in ('.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'):
                useg.add(gln)
            elif len(set(glyph_codes[gln]).intersection(cdsall)) > 0:
                useg.add(gln)
        reget = set()
        if 'GSUB' in font:
            for lookup in font['GSUB']['lookups'].values():
                if lookup['type'] == 'gsub_single':
                    for subtable in lookup['subtables']:
                        for a, b in subtable.items():
                            if a in useg:
                                reget.add(b)
                elif lookup['type'] == 'gsub_alternate':
                    for subtable in lookup['subtables']:
                        for a, b1 in subtable.items():
                            if a in useg:
                                reget.update(b1)
                elif lookup['type'] == 'gsub_ligature':
                    for subtable in lookup['subtables']:
                        for item in subtable['substitutions']:
                            if set(item['from']).issubset(useg):
                                reget.add(item['to'])
        useg.update(reget)
        fgnames=set(font['glyf'].keys())
        for gln in fgnames:
            if gln not in useg:
                isrm.add(gln)
                for codepoint in glyph_codes[gln]:
                    del font['cmap'][codepoint]
                del glyph_codes[gln]
                try:
                    font['glyph_order'].remove(gln)
                except ValueError:
                    pass
                del font['glyf'][gln]
    print('Checking Lookup tables...')
    if 'GSUB' in font:
        for lookup in font['GSUB']['lookups'].values():
            if lookup['type'] == 'gsub_single':
                for subtable in lookup['subtables']:
                    for g1, g2 in list(subtable.items()):
                        if g1 in isrm or g2 in isrm:
                            del subtable[g1]
            elif lookup['type'] == 'gsub_alternate':
                for subtable in lookup['subtables']:
                    for item in set(subtable.keys()):
                        if item in isrm or len(set(subtable[item]).intersection(isrm))>0:
                            del subtable[item]
            elif lookup['type'] == 'gsub_ligature': 
                for subtable in lookup['subtables']:
                    s1=list()
                    for item in subtable['substitutions']:
                        if item['to'] not in isrm and len(set(item['from']).intersection(isrm))<1:
                            s1.append(item)
                    subtable['substitutions']=s1
            elif lookup['type'] == 'gsub_chaining':
                for subtable in lookup['subtables']:
                    for ls in subtable['match']:
                        for l1 in ls:
                            l1=list(set(l1).difference(isrm))
    if 'GPOS' in font:
        for lookup in font['GPOS']['lookups'].values():
            if lookup['type'] == 'gpos_single':
                for subtable in lookup['subtables']:
                    for item in list(subtable.keys()):
                        if item in isrm:
                            del subtable[item]
            elif lookup['type'] == 'gpos_pair':
                for subtable in lookup['subtables']:
                    for item in list(subtable['first'].keys()):
                        if item in isrm:
                            del subtable['first'][item]
                    for item in list(subtable['second'].keys()):
                        if item in isrm:
                            del subtable['second'][item]
            elif lookup['type'] == 'gpos_mark_to_base':
                nsb=list()
                for subtable in lookup['subtables']:
                    gs=set(subtable['marks'].keys()).union(set(subtable['bases'].keys()))
                    if len(gs.intersection(isrm))<1:
                        nsb.append(subtable)
                lookup['subtables']=nsb


def lookuptable():
    print('Building lookups...')
    if not 'GSUB' in font:
        print('Creating empty GSUB!')
        font['GSUB'] = {
                            'languages': 
                            {
                                'hani_DFLT': 
                                {
                                    'features': []
                                }
                            }, 
                            'features': {}, 
                            'lookups': {}, 
                            'lookupOrder': []
                        }
    if not 'hani_DFLT' in font['GSUB']['languages']:
        font['GSUB']['languages']['hani_DFLT'] = {'features': []}
    for table in font['GSUB']['languages'].values():
        table['features'].insert(0, 'liga_st')
    font['GSUB']['features']['liga_st'] = ['wordsc', 'stchars', 'wordtc']
    font['GSUB']['lookupOrder'].append('wordsc')
    font['GSUB']['lookupOrder'].append('stchars')
    font['GSUB']['lookupOrder'].append('wordtc')
    build_char_table()
    build_word_table()

def build_char_table():
    chartab = []
    with open(os.path.join(pydir, 'datas/Chars_tct.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and s in mulchar:
                codesc = ord(s)
                codetc = ord(t)
                if codesc in fontcodes and codetc in fontcodes:
                    chartab.append((s, t))
    with open(os.path.join(pydir, 'datas/Punctuation.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            if s and t and s != t:
                codesc = ord(s)
                codetc = ord(t)
                if codesc in fontcodes and codetc in fontcodes:
                    chartab.append((s, t))
    addlookupschar(chartab)

def addlookupschar(chtab):
    kt = dict()
    for s, t in chtab:
        gls=font['cmap'][str(ord(s))]
        glt=font['cmap'][str(ord(t))]
        if gls != glt:
            kt[gls] = glt
    font['GSUB']['lookups']['stchars'] = {
                                            'type': 'gsub_single',
                                            'flags': {},
                                            'subtables': [kt]
                                         }

def build_word_table():
    stword = list()
    with open(os.path.join(pydir, 'datas/STPhrases.txt'),'r',encoding = 'utf-8') as f:
        ls = list()
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            ls.append(line.strip().split(' ')[0])
        for line in ls:
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if not(s and t):
                continue
            codesc = tuple(ord(c) for c in s)
            codetc = tuple(ord(c) for c in t)
            if all(codepoint in fontcodes for codepoint in codesc) \
                    and all(codepoint in fontcodes for codepoint in codetc):
                stword.append((s, t))
    if len(stword) + len(font['glyph_order']) > 65535:
        nd=len(stword) + len(font['glyph_order']) - 65535
        raise RuntimeError('Not enough glyph space! You need ' + str(nd) + ' more glyph space!')
    if len(stword) > 0:
        addlookupword(stword)

def addlookupword(stword):
    stword.sort(key=lambda x:len(x[0]), reverse = True)
    subtablesl = list()
    subtablesm = list()
    i, j = 0, 0
    sbs = list()
    sbt = dict()
    wlen = len(stword[0][0])
    while True:
        wds = list()
        wdt = list()
        for s1 in stword[i][0]:
            wds.append(font['cmap'][str(ord(s1))])
        for t1 in stword[i][1]:
            wdt.append(font['cmap'][str(ord(t1))])
        newgname = 'ligast' + str(i)
        font['glyf'][newgname] = {
                                    'advanceWidth': 0, 
                                    'advanceHeight': 1000, 
                                    'verticalOrigin': 880
                                 }
        font['glyph_order'].append(newgname)
        sbs.append({'from': wds, 'to': newgname})
        sbt[newgname] = wdt
        if i >= len(stword) - 1:
            subtablesl.append({'substitutions': sbs})
            subtablesm.append(sbt)
            break
        j += len(stword[i][0] + stword[i][1])
        wlen2 = len(stword[i + 1][0])
        if j >= 20000 or wlen2 < wlen:
            j = 0
            wlen = wlen2
            subtablesl.append({'substitutions': sbs})
            subtablesm.append(sbt)
            sbs = list()
            sbt = dict()
        i += 1
    font['GSUB']['lookups']['wordsc'] = {
                                            'type': 'gsub_ligature',
                                            'flags': {},
                                            'subtables': subtablesl
                                        }
    font['GSUB']['lookups']['wordtc'] = {
                                            'type': 'gsub_multiple',
                                            'flags': {},
                                            'subtables': subtablesm
                                        }

def setinfo():
    newn=list()
    tc = sys.argv[3].upper()
    if tc=='TC':
        zhn=' 繁體'
    else:
        zhn=' 轉繁體'
    for nj in font['name']:
        nn=dict(nj)
        nn['nameString']=nn['nameString'].replace('Advocate Ancient Sans', 'Advocate Ancient Sans '+tc).replace('AdvocateAncientSans', 'AdvocateAncientSans'+tc).replace('Advocate Ancient Serif', 'Advocate Ancient Serif '+tc).replace('AdvocateAncientSerif', 'AdvocateAncientSerif'+tc).replace(' 香港', '').replace('尙古黑體','尙古黑體'+zhn).replace('尙古黑体','尙古黑體'+zhn).replace('尙古明體','尙古明體'+zhn).replace('尙古明体','尙古明體'+zhn)
        newn.append(nn)
    font['name']=newn

if len(sys.argv) > 2:
    print('Loading font...')
    tc = 'ST'
    if len(sys.argv) > 3:
        tc = sys.argv[3].upper()
    fin = sys.argv[1]
    font = json.loads(subprocess.check_output((otfccdump, '--no-bom', fin)).decode("utf-8", "ignore"))
    fontcodes = set(map(int, font['cmap']))
    print('Adding variants...')
    addvariants()
    print('Transforming codes...')
    usemulchar = tc == 'TC'
    mulchar = getmulchar(tc == 'ST')
    scgly=set()
    transforme()
    glyph_codes = build_glyph_codes()
    print('Removing glyghs...')
    removeglyhps()
    if tc == "ST":
        print('Manage GSUB...')
        print('Recycling variants...')
        fontcodes = set(map(int, font['cmap']))
        addvariants()
        print('Building lookup table...')
        fontcodes = set(map(int, font['cmap']))
        lookuptable()
    print('Setting font info...')
    setinfo()
    print('Generating font...')
    tmpfile = tempfile.mktemp('.json')
    with open(tmpfile, 'w', encoding='utf-8') as f:
        f.write(json.dumps(font))
    del font
    for x in set(locals().keys()):
        if x not in ('os', 'subprocess', 'otfccbuild', 'sys', 'tmpfile', 'gc'):
            del locals()[x]
    gc.collect()
    print('Creating font file...')
    subprocess.run((otfccbuild, '--keep-modified-time', '--keep-average-char-width', '-O3', '-q', '-o', sys.argv[2], tmpfile))
    os.remove(tmpfile)
    print('Finished!')
