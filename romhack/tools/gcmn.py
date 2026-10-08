"""Textes de GCMN.PRG : deplaces en fin de fichier (zone 0x730600 reservee par le decalage du tas)."""
import sys,struct,pickle,re,glob,os,importlib; sys.path.insert(0,'tools'); sys.path.insert(0,'.'); sys.path.insert(0,'tr')
import relocs,mails,strs,fontpatch as fp
B=0x400800; BSS=0x35d80; MAXBLOB=0x60000
W=(363,259)
CL={'Twin Blade':'Lame Jumelle','Blademaster':'Maître Lame','Heavy Blade':'Lame Lourde','Heavy Axeman':'Hache Lourde','Long Arm':'Longue Lance','Wavemaster':'Maître des Vagues'}
EL={'Earth':'Terre','Water':'Eau','Fire':'Feu','Wood':'Bois','Thunder':'Foudre','Darkness':'Ténèbres','None':'Aucun'}
ST={'Physical Attack':'Attaque physique','Physical Defense':'Défense physique','Physical Accuracy':'Précision physique','Physical Evasion':'Esquive physique','Magical Attack':'Attaque magique','Magical Defense':'Défense magique','Magical Accuracy':'Précision magique','Magical Evasion':'Esquive magique'}
ARM={'Head armor.':'Armure de tête.','Body armor.':'Armure de corps.','Hand armor.':'Armure de mains.','Leg armor.':'Armure de jambes.',
'Light head armor.':'Armure de tête légère.','Light body armor.':'Armure de corps légère.','Light hand armor.':'Armure de mains légère.','Light leg armor.':'Armure de jambes légère.',
'Heavy head armor.':'Armure de tête lourde.','Heavy body armor.':'Armure de corps lourde.','Heavy hand armor.':'Armure de mains lourde.','Heavy leg armor.':'Armure de jambes lourde.'}
L2={'':'','%B%C: Wavemaster':'%B%C : Maître des Vagues','%B%C: Twin Blade/Long Arm/Wavemaster':'%B%C : L. Jumelle/L. Lance/M. Vagues','Attack and magic are negative.':'Attaque et magie négatives.'}
def template(lines,SK):
    j=' / '.join(lines)
    m=re.match(r'^Lv\. (\d+)(#Y ?Rare#W)?: (.+)$',lines[0])
    if m and lines[-1].startswith('%6 button: view status of'):
        what=m.group(3)
        if what in ARM: w=ARM[what]
        else:
            c=re.match(r'Weapon for (.+)\.$',what)
            if not c or c.group(1) not in CL: return None
            w='Arme de %s.'%{'Maître des Vagues':'M. des Vagues'}.get(CL[c.group(1)],CL[c.group(1)])
        mid=[L2.get(l) for l in lines[1:-1]]
        if None in mid: return None
        return ['Nv. %s%s : %s'%(m.group(1),'#Y Rare#W' if m.group(2) else '',w)]+mid+['Touche %6 : statut de '+("l'arme." if 'weapon' in lines[-1] else "l'armure.")]
    m=re.match(r'^Lv\. (\d+) ([PM]): ([SR]): (\w+): (.+)$',lines[0])
    if m:
        d=SK.get(' / '.join(lines[1:]))
        if d is None or m.group(4) not in EL: return None
        return ['Nv. %s %s: %s: %s: %s'%(m.group(1),m.group(2),m.group(3),EL[m.group(4)],m.group(5))]+d
    m=re.match(r'^#Y(.+)#W parameter #Y([+-]\d+)#W\.$',j)
    if m:
        s=m.group(1); e=re.match(r'(\w+) Element$',s)
        fr=ST.get(s) or (e and 'Elément '+EL[e.group(1)])
        return ['#Y%s#W : paramètre #Y%s#W.'%(fr,m.group(2))] if fr else None
    m=re.match(r'^Select (BGM|Movie) (\d+) in desktop audio / player\.$',j)
    if m: return ['%s %s : à choisir dans le'%({'BGM':'BGM','Movie':'Vidéo'}[m.group(1)],m.group(2)),'lecteur du bureau.']
    m=re.match(r'^Select Image (\d+) in desktop / accessories\.$',j)
    if m: return ['Image %s : à choisir dans les'%m.group(1),'accessoires du bureau.']
    return None
def fit(text,N,T,ol):
    """texte -> N lignes exactement (complete par des vides) ; None si impossible"""
    if isinstance(text,list): return text if len(text)==N else None
    ls=None
    if '\n' in text:
        ls=text.split('\n')
        if len(ls)>N or any(mails.widths(l,T)[0]>W[0]*1.12 for l in ls): text=text.replace('\n',' '); ls=None
    if ls is not None: pass
    elif N==1: ls=[text]
    else:
        for k in (1.0,1.06,1.12):
            ls=mails.wrap(text,T,(int(W[0]*k),int(W[1]*k)))[1:]
            if len(ls)<=N: break
    if len(ls)>N: return None
    return ls+['']*(N-len(ls))
COV=[]
def build(prg):
    T=mails.tabs(); orig=bytes(prg); prg=bytearray(prg)
    import gcmn_keys,hashlib
    hk=lambda x: hashlib.sha1(x.encode('utf-8')).hexdigest()[:12]
    uniq=gcmn_keys.K
    G={}; SK={}; M={}
    for f in sorted(glob.glob('tr/gcmn_*.py')):
        m=importlib.import_module(os.path.basename(f)[:-3]); G.update(getattr(m,'G',{})); SK.update(getattr(m,'SK',{})); M.update(getattr(m,'M',{}))
    byen={uniq[i]:v for i,v in G.items()}
    rev={h:i for i,h in enumerate(uniq)}
    import gcmn_menu,names_items,names_weapons,names_misc as nx
    NM=dict(names_items.NAMES); NM.update(names_weapons.NAMES)
    NR=((0x6b1b18,0x6b2180),(0x6b85e0,0x6bec20),(0x6d0100,0x6dfe00))
    I2=dict(NM); I2.update(nx.ITEM2)
    ZONES=((0x6aec00,0x6b0c00,nx.MON),(0x6b0c00,0x6b2200,nx.NPC),(0x6b2180,0x6b85e0,nx.SKILL),(0x6b1b18,0x6b2180,NM),(0x6b85e0,0x6bec70,I2),(0x6d0100,0x6dfe00,NM))
    def name(a,j):
        for a0,a1,dd in ZONES:
            if a0<=a<a1 and j in dd: return dd[j]
        if 0x6b2180<=a<0x6b85e0:
            m=re.fullmatch(r'(\S+) +(\w+)',j)
            if m and m.group(2) in nx.SUFFIX: return nx.SUFFIX[m.group(2)]+' '+m.group(1)
        return None
    byen.update({hk(k):v for k,v in nx.GT.items()})
    for a,fr in nx.INPLACE_A.items():
        k=a-B; e=orig.index(b'\0',k); n=e
        while orig[n]==0: n+=1
        enc=fp.encode(fr); assert len(enc)<=n-k-1,(hex(a),fr,len(enc),n-k-1)
        prg[k:n]=enc.ljust(n-k,b'\0'); COV.append((a,B+n))
    for old,fr in getattr(gcmn_menu,'INPLACE',{}).items():
        k=orig.find(old+b'\0'); assert k>0 and orig.find(old+b'\0',k+1)<0,old
        n=k+len(old)
        while orig[n]==0: n+=1
        enc=fp.encode(fr); assert len(enc)<=n-k-1,(old,fr,n-k-1); prg[k:n]=enc.ljust(n-k,b'\0'); COV.append((B+k,B+n))
    blob=bytearray(); base=B+len(prg)+BSS; n=tp=0; bad=[]; left=0
    for t in strs.targets('gcmn.prg',orig):
        j=' / '.join(t['lines']); N=len(t['lines'])
        fr=template(t['lines'],SK)
        if t['a'] in M and N==1: fr=[M[t['a']]]
        elif N==1 and hk(j) not in byen and name(t['a'],j) is not None: fr=[name(t['a'],j)]
        elif fr is not None: tp+=1
        elif hk(j) in byen:
            fr=fit(byen[hk(j)],N,T,t['lines'])
            if fr is None: bad.append((rev.get(hk(j),-1),N,byen[hk(j)])); continue
        else:
            left+=1; continue
        lens=[len(l.encode('latin1','replace')) for l in t['lines']]
        enc=[fp.encode(l) for l in fr]
        pad=[e_.count(b'%F')+e_.count(b'%G') for e_ in enc]   # o/u circonflexes = 2 octets : la boite compte un caractere de moins
        if len(set(lens))==1 and N>1 and any(l.endswith(' ') for l in t['lines']):
            if any(len(e)>L for e,L in zip(enc,lens)): bad.append((rev.get(hk(j),-1),N,fr)); continue
            enc=[e.ljust(L,b' ') for e,L in zip(enc,lens)]
        else: enc=[e_+b' '*k for e_,k in zip(enc,pad)]
        a=base+len(blob); blob.extend(b'\0'.join(enc)+b'\0\0\0\0')
        while len(blob)%4: blob.append(0)
        for s in t['sites']: relocs.repoint(prg,s,a)
        COV.append((t['a'],t['a']+t['slot']))
        n+=1
    assert len(blob)<=MAXBLOB,hex(len(blob))
    struct.pack_into('<I',prg,0x14,0)      # bss deja dans le fichier (zeros) : pas de memset apres coup
    print('GCMN: %d textes deplaces (dont %d par modele), %d octets ; a revoir: %d'%(n,tp,len(blob),len(bad)))
    for b_ in bad[:60]: print('  ! idx %s (%d lignes): %s'%b_)
    return bytes(prg)+bytes(BSS)+bytes(blob)
