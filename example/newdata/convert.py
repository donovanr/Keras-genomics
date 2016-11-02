from os import system
import subprocess

def probedata(dataprefix):
    return int(subprocess.check_output('wc -l '+dataprefix, shell=True).split(' ')[0])



for dtype in ['train','test']:
    for l in ['pos','neg']:
        system(' '.join(['paste - - -d\'?\'','< data.shuffed.'+dtype+'.'+l+'.fa','>', 'data.shuffed.'+dtype+'.'+l+'.tsv']))
    posnum = probedata('data.shuffed.'+dtype+'.pos.tsv')
    negnum = probedata('data.shuffed.'+dtype+'.neg.tsv')
    target = ['1\t0']*posnum + ['0\t1']*negnum
    with open(dtype+'.target','w') as f:
        for x in target:
            f.write(x+'\n')
    system(' '.join(['cat','data.shuffed.'+dtype+'.pos.tsv','data.shuffed.'+dtype+'.neg.tsv','>',dtype+'.tsv']))


system(' '.join(['paste -d \'!\'','train.tsv','train.target','| shuf|','awk -v FS=\'!\' \'{print $1>"trainvalid.tsv.shuf" ; print $2>"trainvalid.target.shuf"}\'  ']))

for dtype in ['tsv','target']:
    system(' '.join(['head -n 1000 trainvalid.'+dtype+'.shuf > valid.'+dtype+'.shuf']))
    system(' '.join(['tail -n+1001 trainvalid.'+dtype+'.shuf > train.'+dtype+'.shuf']))

for dtype in ['train','valid','test']:
    suffix = '.shuf' if dtype !='test' else ''
    system(' '.join(['cp',dtype+'.target'+suffix,'../'+dtype+'.target']))
    with open(dtype+'.tsv'+suffix) as fin,open('../'+dtype+'.fa','w') as fout:
        for x in fin:
            line = x.split('?')
            fout.write(line[0]+'\n'+line[1])

