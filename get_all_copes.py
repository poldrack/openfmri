f=open('copelist','r')
l=f.readlines()
f.close()

for line in l:
    line_split=line.strip().split('/')
    new_name=line.strip().replace('/','_').replace('.gfeat','').replace('.feat','').replace('model','').replace('stats','').replace('__zstat1','')
    print 'cp %s all_copes/%s'%(line.strip(),new_name)
