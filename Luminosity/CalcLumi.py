import os, sys, math
out_fold = 'lumiInput'
os.system('mkdir '+out_fold)
crab_fold=sys.argv[1]
listfolders = [f for f in os.listdir(crab_fold)]
'''for fold1 in listfolders:
    print("Report of "+fold1+"\n")
    os.system("crab report "+crab_fold+"/"+fold1)
os.system('export PATH=$HOME/.local/bin:/cvmfs/cms-bril.cern.ch/brilconda/bin:$PATH')
for fold1 in listfolders:
     os.system("brilcalc lumi -b \"STABLE BEAMS\" -i "+crab_fold+"/"+fold1+"/results/processedLumis.json > "+out_fold+"/"+fold1+".txt")
     print("Integrated luminosity for  "+fold1+"\n")'''

list_fold=[f for f in os.listdir(out_fold)]
calc_Lumi=[]
for file in list_fold:
    if 'MET' in file:
        f=open(out_fold+'/'+file, 'r')
        for line in f:
            if 'nfill' in line:
                for lf in list(f):
                    if '|' in lf:
                        calc_Lumi.append(lf.split('|')[-2])
lumi_array_float=[]
for calc in calc_Lumi:
    lumi_array_float.append(float(calc))
total_lumi=sum(lumi_array_float)*(10**-9)

##py2tex(str(round(total_lumi,4))+'*fb**-1')
print (str(total_lumi)+'fb^-1')
