"""Ajoute les accents francais dans les deux polices du jeu (ef8x16 / ef12x20, dans l'ELF)."""
import struct, sys
sys.path.insert(0,'.')
SMALL=dict(addr=0x2f5600,gw=8,gh=16,ofs=0x2fb5f0)
LARGE=dict(addr=0x2f2180,gw=12,gh=20,ofs=0x2fb4f0)
# caractere FR -> (index de glyphe remplace, octets a ecrire dans le texte)
ACC={'é':(91,b'{'),'è':(93,b'}'),'à':(59,b'['),'ê':(61,b']'),'ç':(92,b'|'),
     'ù':(64,b'`'),'â':(94,b'~'),'î':(60,b'\\'),'ô':(110,b'%F'),'û':(111,b'%G')}
BASE={'é':'e','è':'e','ê':'e','à':'a','â':'a','ç':'c','ù':'u','û':'u','î':'i','ô':'o'}
KIND={'é':'acute','è':'grave','à':'grave','ù':'grave','ê':'circ','â':'circ','î':'circ','ô':'circ','û':'circ','ç':'ced'}

class Sheet:
    def __init__(s,buf,fo,gw,gh): s.b=buf; s.fo=fo; s.gw=gw; s.gh=gh; s.stride=16*gw//2
    def get(s,idx):
        r,c=divmod(idx,16); out=[]
        for y in range(s.gh):
            row=[]
            for x in range(s.gw):
                X=c*s.gw+x; by=s.b[s.fo+(r*s.gh+y)*s.stride+X//2]
                row.append(by>>4 if X&1 else by&15)
            out.append(row)
        return out
    def put(s,idx,g):
        r,c=divmod(idx,16)
        for y in range(s.gh):
            for x in range(s.gw):
                X=c*s.gw+x; o=s.fo+(r*s.gh+y)*s.stride+X//2; by=s.b[o]
                s.b[o]=(by&0x0f)|(g[y][x]<<4) if X&1 else (by&0xf0)|g[y][x]

def ink(g): return [[v if v>=9 else 0 for v in row] for row in g]
def finish(g,large):
    """recalcule ombre (petite police: decalee +1,+1) ou contour (grande police: 4-voisins)."""
    h=len(g); w=len(g[0]); out=[row[:] for row in g]
    for y in range(h):
        for x in range(w):
            if g[y][x]:
                nb=[(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if large else [(x+1,y+1)]
                for X,Y in nb:
                    if 0<=X<w and 0<=Y<h and not g[Y][X]: out[Y][X]=4
    return out
def setp(g,pts):
    for x,y,v in pts:
        if 0<=y<len(g) and 0<=x<len(g[0]): g[y][x]=max(g[y][x],v)

def make(sh,ch,large):
    base=sh.get(ord(BASE[ch])-32); k=KIND[ch]; w=sh.gw
    if BASE[ch]=='i':   # i sans point, decale pour loger le circonflexe
        g=[[0]*w for _ in range(sh.gh)]
        if large:
            for y in range(6,16): g[y][3]=9; g[y][4]=15
            L=3
        else:
            for y in range(4,12): g[y][1]=15
            setp(g,[(1,1,15),(0,2,15),(2,2,15)]); return finish(g,large)
    else:
        g=ink(base)
        body=range(6,16) if large else range(4,12)
        xs=[x for y in body for x in range(w) if g[y][x]]
        L=(min(xs)+max(xs))//2
    if large:
        if k=='circ':  setp(g,[(L-1,1,9),(L,1,15),(L+1,1,15),(L+2,1,9),(L-2,2,9),(L-1,2,15),(L,2,9),(L+1,2,9),(L+2,2,15),(L+3,2,9),(L-2,3,15),(L-1,3,9),(L+2,3,9),(L+3,3,15)])
        if k=='acute': setp(g,[(L+1,1,9),(L+2,1,15),(L,2,9),(L+1,2,15),(L-1,3,9),(L,3,15)])
        if k=='grave': setp(g,[(L-1,1,15),(L,1,9),(L,2,15),(L+1,2,9),(L+1,3,15),(L+2,3,9)])
        if k=='ced':   setp(g,[(L,16,9),(L+1,16,15),(L+1,17,9),(L+2,17,15),(L-1,18,15),(L,18,15),(L+1,18,9)])
    else:
        if k=='circ':  setp(g,[(L,1,15),(L+1,1,15),(L-1,2,15),(L+2,2,15)])
        if k=='acute': setp(g,[(L+1,1,15),(L+2,1,9),(L,2,15)])
        if k=='grave': setp(g,[(L,1,15),(L-1,1,9),(L+1,2,15)])
        if k=='ced':   setp(g,[(L+1,12,15),(L,13,15),(L+1,13,9)])
    return finish(g,large)

def patch(elf,v2o):
    for F,large in ((SMALL,False),(LARGE,True)):
        sh=Sheet(elf,v2o(F['addr']),F['gw'],F['gh']); to=v2o(F['ofs'])
        for ch,(idx,_) in ACC.items():
            sh.put(idx,make(sh,ch,large))
            if BASE[ch]=='i': o=4
            else: o,=struct.unpack_from('<h',elf,to+2*(ord(BASE[ch])-32))
            struct.pack_into('<h',elf,to+2*idx,o)

def encode(s):
    """texte francais -> octets du jeu"""
    rep={'É':'E','È':'E','Ê':'E','À':'A','Â':'A','Ç':'C','Ô':'O','Î':'I','Û':'U','Ù':'U','œ':'oe','Œ':'OE','ï':'i','ë':'e','ü':'u','«':'"','»':'"','’':"'",'…':'...',' ':' ',' ':' '}
    out=b''
    import re as _re
    m=_re.search(r'<([0-9a-f]{4})>',s)
    if m: return encode(s[:m.start()])+bytes.fromhex(m.group(1))+encode(s[m.end():])
    for c in s:
        if c in ACC: out+=ACC[c][1]
        elif c in rep: out+=rep[c].encode()
        else:
            o=c.encode('ascii')
            if o in (b'{',b'}',b'[',b']',b'|',b'`',b'~',b'\\'): raise ValueError('caractere reserve aux accents: '+c)
            out+=o
    return out
