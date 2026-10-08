"""Reponses de Kite (DESKTOP.PRG) : enregistrements {ptr sujet, ptr nom, nb lignes, ptr corps, 0}."""
import sys,struct,json,re,glob,os,importlib; sys.path.insert(0,'tools'); sys.path.insert(0,'.'); sys.path.insert(0,'tr')
import relocs,mails
B=0x400800
def records(prg):
    tg=relocs.sites('desktop.prg',prg); s2t={s[1]:t for t,ss in tg.items() for s in ss if s[0]=='w'}
    out=[]
    for fo in sorted(s2t):
        if fo-12 in s2t and fo-8 in s2t and s2t[fo-8]==0x431258:
            n,=struct.unpack_from('<I',prg,fo-4); body=s2t[fo]
            raw=prg[body-B:body-B+4000].split(b'\0')[:n]
            while raw and raw[-1]==b'': raw.pop()
            out.append(dict(fo=fo,subject=mails.dec(mails.cstr(prg,s2t[fo-12])),lines=[mails.dec(l) for l in raw],n=n))
    return out
def norm(s): return re.sub(r'[^a-z0-9]','',s.lower())
def automatch(recs):
    """reprend sujets et citations deja traduits dans les mails 'RE:'"""
    men=json.load(open('mails_en.json')); fr={}
    for f in sorted(glob.glob('tr/mails_*.py')): fr.update(importlib.import_module(os.path.basename(f)[:-3]).M)
    subj={}; body={}
    for i,m in enumerate(men):
        if m['subject'].upper().startswith('RE:') and i in fr:
            es=m['subject'][3:].strip(); fs=fr[i]['subject'][3:].strip()
            subj[norm(es)]=fs
            q=' '.join(l[1:] for l in m['lines'] if l.startswith('>'))
            fq='\n'.join(l[1:] for l in fr[i]['body'].split('\n') if l.startswith('>'))
            if q: body[norm(q)]=fq
    return subj,body
if __name__=='__main__':
    prg=open('DESKTOP.PRG','rb').read(); recs=records(prg)
    json.dump(recs,open('replies_en.json','w'),ensure_ascii=False,indent=0)
    subj,body=automatch(recs); ns=nb=0
    for i,r in enumerate(recs):
        s=subj.get(norm(r['subject'])); b=body.get(norm(' '.join(r['lines'])))
        ns+=s is not None; nb+=b is not None
        print('@%d %s%s | %s%s'%(i,'' if s is None else '=',r['subject'],'' if b is None else '=',' '.join(l for l in r['lines'] if l)))
    print(len(recs),'reponses ; sujets auto',ns,'corps auto',nb)

def insert(prg,add,add_block,T,report):
    """traduit les reponses ; add(bytes)->adresse d'une chaine, add_block(lines)->adresse d'un corps"""
    import replies_fr as R
    recs=records(bytes(prg)); subj,body=automatch(recs); miss=[]
    for i,r in enumerate(recs):
        fo=r['fo']
        fs=R.SUBJ.get(r['subject'])
        fb=R.BODY.get(i)
        if fb is None:
            b=body.get(norm(' '.join(r['lines'])))
            if b is not None: fb='\n\n'.join(' '.join(p.split('\n')) for p in re.split(r'\n\s*\n',b))
        if fs is None or fb is None: miss.append((i,r['subject'],fs is None,fb is None)); continue
        w=mails.widths(fs,T); assert w[0]<=mails.MAXSUBJ[0]+8,('sujet',fs,w)
        lines=mails.wrap(fb,T)
        struct.pack_into('<I',prg,fo-12,add(mails.fp.encode(fs)))
        struct.pack_into('<I',prg,fo,add_block(lines)); struct.pack_into('<I',prg,fo-4,len(lines)+1)
    report.append('reponses traduites: %d / %d'%(len(recs)-len(miss),len(recs)))
    return miss
