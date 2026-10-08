import sys
iso=sys.argv[1]
want={'SLUS_202.67':(371,19223388),'DATA.BIN':(12463,136665088),'GCMN.PRG':(10349,3121280),'DESKTOP.PRG':(10138,432128),'TOPPAGE.PRG':(11874,172800),'DEMO.PRG':(10107,61568),'OUTSIDE.BIN':(1268309,1048576),'ICON.BIN':(11959,1032192)}
f=open(iso,'rb')
for n,(l,s) in want.items():
    f.seek(l*2048); open(n,'wb').write(f.read(s))

# scene de l'Epitaphe (membre gzip de STR1E.BIN, LBA 837295, position 188416)
f.seek(837295*2048+188416); open('str0001e.gz.orig','wb').write(f.read(844995))
