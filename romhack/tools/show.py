import json,sys
recs=json.load(open('mails_en.json'))
a,b=int(sys.argv[1]),int(sys.argv[2])
for i in range(a,min(b,len(recs))):
    r=recs[i]; out=[]; cur=''
    for k,l in enumerate(r['lines'][1:] if r['lines'] and r['lines'][0]=='' else r['lines']):
        if l=='': out.append(cur); cur=''; continue
        if cur and (len(prev)<22 or l.startswith('#B%') or prev.startswith('#B%')): cur+=' | '+l
        else: cur=(cur+' '+l) if cur else l
        prev=l
    out.append(cur)
    print('@%d [%s] %s'%(i,r['sender'],r['subject'])); print('\n'.join(out))
