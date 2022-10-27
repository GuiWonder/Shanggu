import os, sys, json, subprocess, platform, tempfile, gc
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
                if str(ord(ch1)) in font['cmap']:
                    codein = ord(ch1)
                    break
            if codein != 0:
                for ch1 in vari:
                    if str(ord(ch1)) not in font['cmap']:
                        font['cmap'][str(ord(ch1))] = font['cmap'][str(codein)]

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
                if str(ord(t)) in font['cmap']:
                    font['cmap'][str(ord(s))] = font['cmap'][str(ord(t))]

def removeglyhps():
    usedg=set()
    if tc=='TT':
        usedg.update(set(font['cmap'].values()))
        if 'cmap_uvs' in font:
            for k in font['cmap_uvs'].keys():
                c, v=k.split(' ')
                if c in font['cmap']:
                    usedg.add(font['cmap_uvs'][k])
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
        cdsall=set(map(str, s))
        nmap=set(font['cmap'].keys()).intersection(cdsall)
        for mp in nmap:
            usedg.add(font['cmap'][mp])
    if 'GSUB' in font:
        for lkn in font['GSUB']['lookupOrder']:
            if lkn in font['GSUB']['lookups']:
                lookup=font['GSUB']['lookups'][lkn]
                if lookup['type'] == 'gsub_single':
                    for subtable in lookup['subtables']:
                        for g1, g2 in list(subtable.items()):
                            if g1 in usedg:
                                usedg.add(g2)
                elif lookup['type'] == 'gsub_alternate':
                    for subtable in lookup['subtables']:
                        for item in set(subtable.keys()):
                            if item in usedg:
                                usedg.update(set(subtable[item]))
                elif lookup['type'] == 'gsub_ligature': 
                    for subtable in lookup['subtables']:
                        for item in subtable['substitutions']:
                            if set(item['from']).issubset(usedg):
                                usedg.add(item['to'])
                elif lookup['type'] == 'gsub_chaining':
                    for subtable in lookup['subtables']:
                        for ls in subtable['match']:
                            for l1 in ls:
                                usedg.update(set(l1))
    unusegl=set()
    unusegl.update(set(font['glyph_order']))
    notg={'.notdef', '.null', 'nonmarkingreturn', 'NULL', 'NUL'}
    unusegl.difference_update(notg)
    unusegl.difference_update(usedg)
    for ugl in unusegl:
        font['glyph_order'].remove(ugl)
        del font['glyf'][ugl]
    
    print('Checking cmap tables...')
    for cod in set(font['cmap'].keys()):
        if font['cmap'][cod] in unusegl:
            del font['cmap'][cod]
    if 'cmap_uvs' in font:
        for uvk in set(font['cmap_uvs'].keys()):
            if font['cmap_uvs'][uvk] in unusegl:
                del font['cmap_uvs'][uvk]
    print('Checking Lookup tables...')
    if 'GSUB' in font:
        for lookup in font['GSUB']['lookups'].values():
            if lookup['type'] == 'gsub_single':
                for subtable in lookup['subtables']:
                    for g1, g2 in list(subtable.items()):
                        if g1 in unusegl or g2 in unusegl:
                            del subtable[g1]
            elif lookup['type'] == 'gsub_alternate':
                for subtable in lookup['subtables']:
                    for item in set(subtable.keys()):
                        if item in unusegl or len(set(subtable[item]).intersection(unusegl))>0:
                            del subtable[item]
            elif lookup['type'] == 'gsub_ligature': 
                for subtable in lookup['subtables']:
                    s1=list()
                    for item in subtable['substitutions']:
                        if item['to'] not in unusegl and len(set(item['from']).intersection(unusegl))<1:
                            s1.append(item)
                    subtable['substitutions']=s1
            elif lookup['type'] == 'gsub_chaining':
                for subtable in lookup['subtables']:
                    for ls in subtable['match']:
                        for l1 in ls:
                            l1=list(set(l1).difference(unusegl))
    if 'GPOS' in font:
        for lookup in font['GPOS']['lookups'].values():
            if lookup['type'] == 'gpos_single':
                for subtable in lookup['subtables']:
                    for item in list(subtable.keys()):
                        if item in unusegl:
                            del subtable[item]
            elif lookup['type'] == 'gpos_pair':
                for subtable in lookup['subtables']:
                    for item in list(subtable['first'].keys()):
                        if item in unusegl:
                            del subtable['first'][item]
                    for item in list(subtable['second'].keys()):
                        if item in unusegl:
                            del subtable['second'][item]
            elif lookup['type'] == 'gpos_mark_to_base':
                nsb=list()
                for subtable in lookup['subtables']:
                    gs=set(subtable['marks'].keys()).union(set(subtable['bases'].keys()))
                    if len(gs.intersection(unusegl))<1:
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
    kt = dict()
    with open(os.path.join(pydir, 'datas/Chars_tct.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            s = s.strip()
            t = t.strip()
            if s and t and s != t and s in mulchar:
                if str(ord(s)) in font['cmap'] and str(ord(t)) in font['cmap']:
                    kt[font['cmap'][str(ord(s))]] = font['cmap'][str(ord(t))]
    with open(os.path.join(pydir, 'datas/Punctuation.txt'),'r',encoding = 'utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith('#') or '\t' not in line:
                continue
            s, t = line.strip().split('\t')
            if s and t and s != t:
                if str(ord(s)) in font['cmap'] and str(ord(t)) in font['cmap']:
                    kt[font['cmap'][str(ord(s))]] = font['cmap'][str(ord(t))]
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
            codesc = tuple(str(ord(c)) for c in s)
            codetc = tuple(str(ord(c)) for c in t)
            if all(codepoint in font['cmap'] for codepoint in codesc) \
                    and all(codepoint in font['cmap'] for codepoint in codetc):
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
    cfg=json.load(open(os.path.join(pydir, 'config.json'), 'r', encoding = 'utf-8'))
    fnm=cfg['fontName']
    fnp=fnm.replace(' ', '')
    newn=list()
    if tc=='TT':
        zhn=' 繁體'
    else:
        zhn=' 轉繁體'
    for nj in font['name']:
        nn=dict(nj)
        nn['nameString']=nn['nameString'].replace(fnm+' Sans', fnm+' Sans '+tc).replace(fnp+'Sans', fnp+'Sans'+tc).replace(fnm+' Serif', fnm+' Serif '+tc).replace(fnp+'Serif', fnp+'Serif'+tc).replace('黑體','黑體'+zhn).replace('黑体','黑體'+zhn).replace('明體','明體'+zhn).replace('明体','明體'+zhn)
        newn.append(nn)
    font['name']=newn

if len(sys.argv) > 2:
    print('Loading font...')
    tc = 'ST'
    if len(sys.argv) > 3:
        tc = sys.argv[3].upper()
    fin = sys.argv[1]
    font = json.loads(subprocess.check_output((otfccdump, '--no-bom', fin)).decode("utf-8", "ignore"))
    print('Adding variants...')
    addvariants()
    print('Transforming codes...')
    usemulchar = tc == 'TT'
    mulchar = getmulchar(tc == 'ST')
    transforme()
    print('Removing glyghs...')
    removeglyhps()
    if tc == "ST":
        print('Checking GSUB...')
        print('Checking variants...')
        addvariants()
        print('Building lookup table...')
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
