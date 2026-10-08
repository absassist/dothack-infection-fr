"""Chaines referencees (cibles de relocations) d'un PRG, hors zones deja traitees."""
import sys,re,struct; sys.path.insert(0,'tools'); sys.path.insert(0,'.')
import relocs, mails
B=0x400800
def targets(prgname,prg,B=B,dstart=None,dend=None):
    tg=relocs.sites(prgname,prg,B); ts=sorted(tg)
    if dstart is None: hdr=struct.unpack('<8I',prg[:32]); dstart=hdr[3]+0x40
    if dend is None: dend=len(prg)
    out=[]
    for i,t in enumerate(ts):
        o=t-B
        if not (dstart<=o<dend): continue
        nxt=min(ts[i+1]-B if i+1<len(ts) else dend, o+4000)
        raw=prg[o:nxt]; body=raw.rstrip(b'\0')
        if not body or b'\0'*1 in body and False: continue
        if not re.fullmatch(rb'[\x20-\x7e\x81-\x83\x99\x9a\x9b\xa0-\xb6\x00\x65\x7e]+',body): continue
        if not re.search(rb'[A-Za-z]{2}',body): continue
        out.append(dict(a=t,o=o,slot=nxt-o,lines=[mails.dec(l) for l in body.split(b'\0')],sites=tg[t]))
    return out
if __name__=='__main__':
    name=sys.argv[1]; prg=open(name.upper()+'.PRG','rb').read()
    T=targets(name+'.prg',prg)
    print(len(T),'cibles texte', sum(len(l)+1 for t in T for l in t['lines']),'octets')
    import pickle; pickle.dump(T,open(name+'_targets.pkl','wb'))
