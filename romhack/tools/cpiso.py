import os,sys,time
R=os.path.expanduser('~/mnt/roms/')
src=R+'Dot Hack Part 1 - Infection (USA).iso'; dst=R+'Dot Hack Part 1 - Infection (FR).iso'
size=os.path.getsize(src); t=time.time()
done=min(os.path.getsize(dst),size) if os.path.exists(dst) else 0
done-=done%(1<<20)
with open(src,'rb') as f, open(dst,'r+b' if os.path.exists(dst) else 'wb') as g:
    f.seek(done); g.seek(done)
    while done<size and time.time()-t<150:
        buf=f.read(16<<20); g.write(buf); done+=len(buf)
print(done,size,'COMPLETE' if done>=size else 'partial')
