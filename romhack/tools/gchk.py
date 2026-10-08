import sys,pickle,glob,os,importlib;sys.path.insert(0,'tools');sys.path.insert(0,'tr')
import mails,gcmn
def english():
    """textes anglais de GCMN.PRG, dans l'ordre de tr/gcmn_keys.py (retrouves par empreinte dans la copie du jeu)"""
    if os.path.exists('gcmn_uniq.pkl'): return list(pickle.load(open('gcmn_uniq.pkl','rb')))
    import strs,hashlib,gcmn_keys
    by={}
    for t in strs.targets('gcmn.prg',open('GCMN.PRG','rb').read()):
        j=' / '.join(t['lines']); by.setdefault(hashlib.sha1(j.encode('utf-8')).hexdigest()[:12],j)
    return [by.get(h,'') for h in gcmn_keys.K]
u=english();T=mails.tabs()
LIM=int(sys.argv[2]) if len(sys.argv)>2 else 363
m=importlib.import_module(sys.argv[1]);n=0
for i,v in sorted(m.G.items()):
    en=u[i].split(' / ');N=len(en)
    try: fr=gcmn.fit(v,N,T,en)
    except Exception as e: print('ERR',i,e);continue
    if fr is None: print('LINES',i,N,v);continue
    ew=max(mails.widths(l,T,True)[0] for l in en)
    for l in fr:
        w=mails.widths(l,T)[0]
        if w>max(LIM,ew): print('WIDE',i,w,ew,l);n+=1
print('ok',len(m.G),'wide',n)
