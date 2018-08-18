from ROOT import TGraph, TFile, TGraphAsymmErrors
from array import array
import os
import glob,math
import matplotlib.pyplot as plt

path_sig_ll='ll/sig/*Output_pseudo_NLO_Mchi-1_Mphi*.root'
path_bkg_ll='ll/bkg/*.root'

Mphi=['50','100','350','400','500','1000']
mchi=['1']
pT_cuts=[50,55,60,65,70]    # pt cut for leading jet
pT_cuts_add=[30,35,40,45,50]  #pT cut for additional jets

bkgsr1_ll=['jet1_pT_sr1','jet2_pT_sr1']
bkgsr2_ll=['jet1_pT_sr2','jet2_pT_sr2','jet3_pT_sr2']

# Xrange=1000  # range of pt [0,1000]
# Totalbins=200
# perbin=(Xrange)/(Totalbins)
# print (perbin)
# setbins=[]   # set first bin for leading jet
# setbins_add=[]  # set first bin for additional jet
#
# for i in pT_cuts:
#     setbins.append((i)/(perbin))
#     print (i/(perbin))
#
# for i in pT_cuts_add:
#     setbins_add.append((i)/(perbin))
#     print (i/(perbin))



mphi50_sr1_jet1_ll=[]
mphi50_sr1_jet2_ll=[]
mphi50_sr2_jet1_ll=[]
mphi50_sr2_jet2_ll=[]
mphi50_sr2_jet3_ll=[]

mphi100_sr1_jet1_ll=[]
mphi100_sr1_jet2_ll=[]
mphi100_sr2_jet1_ll=[]
mphi100_sr2_jet2_ll=[]
mphi100_sr2_jet3_ll=[]

mphi350_sr1_jet1_ll=[]
mphi350_sr1_jet2_ll=[]
mphi350_sr2_jet1_ll=[]
mphi350_sr2_jet2_ll=[]
mphi350_sr2_jet3_ll=[]

mphi400_sr1_jet1_ll=[]
mphi400_sr1_jet2_ll=[]
mphi400_sr2_jet1_ll=[]
mphi400_sr2_jet2_ll=[]
mphi400_sr2_jet3_ll=[]

mphi500_sr1_jet1_ll=[]
mphi500_sr1_jet2_ll=[]
mphi500_sr2_jet1_ll=[]
mphi500_sr2_jet2_ll=[]
mphi500_sr2_jet3_ll=[]

mphi1000_sr1_jet1_ll=[]
mphi1000_sr1_jet2_ll=[]
mphi1000_sr2_jet1_ll=[]
mphi1000_sr2_jet2_ll=[]
mphi1000_sr2_jet3_ll=[]

sr1_jet1_ll=[]
sr1_jet2_ll=[]
sr2_jet1_ll=[]
sr2_jet2_ll=[]
sr2_jet3_ll=[]



files_bkg_ll = sorted(glob.glob(path_bkg_ll))
# print ("total files")
# print (files_bkg)
for file in files_bkg_ll:
    f=TFile.Open(file,'read')
    print ("selected file");f

    for i in bkgsr1_ll:
        if i in file.split('/')[-1]:
            if i==bkgsr1_ll[0]:
                # print (file)
                bkgsum=f.Get("bkgSum")
                sr1_jet1_ll.append(bkgsum.Integral())
            if i==bkgsr1_ll[1]:
                bkgsum=f.Get("bkgSum")
                sr1_jet2_ll.append(bkgsum.Integral())
    for i in bkgsr2_ll:
        if i in file.split('/')[-1]:
            if i==bkgsr2_ll[0]:
                bkgsum=f.Get("bkgSum")
                sr2_jet1_ll.append(bkgsum.Integral())
            if i==bkgsr2_ll[1]:
                bkgsum=f.Get("bkgSum")
                sr2_jet2_ll.append(bkgsum.Integral())
            if i==bkgsr2_ll[2]:
                bkgsum=f.Get("bkgSum")
                sr2_jet3_ll.append(bkgsum.Integral())





files = sorted(glob.glob(path_sig_ll))
print ("total files");files
for file in files:
    f=TFile.Open(file,'read')
    htotal=f.Get('h_total')
    print(htotal.Integral())
    print ("selected file")
    #print (f)
    sr1_jet1_pT_ll=f.Get('h_jet1_pT_sr1_')
    sr1_jet2_pT_ll=f.Get('h_jet2_pT_sr1_')
    sr2_jet1_pT_ll=f.Get('h_jet1_pT_sr2_')
    sr2_jet2_pT_ll=f.Get('h_jet2_pT_sr2_')
    sr2_jet3_pT_ll=f.Get('h_jet3_pT_sr2_')

    for i in Mphi:
        #print (file.split('/')[-1])
        if '_Mphi-'+i+'.root' in file.split('/')[-1]:
            #print ("entering")
            if i==Mphi[0]:
                    mphi50_sr1_jet1_ll.append(sr1_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet1_ll.append(sr2_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet2_ll.append(sr2_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi50_sr1_jet2_ll.append(sr1_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet3_ll.append(sr2_jet3_pT_ll.Integral()/(htotal.Integral()))



            if i==Mphi[1]:
                    mphi100_sr1_jet1_ll.append(sr1_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet1_ll.append(sr2_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet2_ll.append(sr2_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi100_sr1_jet2_ll.append(sr1_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet3_ll.append(sr2_jet3_pT_ll.Integral()/(htotal.Integral()))

            if i==Mphi[2]:
                    mphi350_sr1_jet1_ll.append(sr1_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet1_ll.append(sr2_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet2_ll.append(sr2_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi350_sr1_jet2_ll.append(sr1_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet3_ll.append(sr2_jet3_pT_ll.Integral()/(htotal.Integral()))

            if i==Mphi[3]:
                    mphi400_sr1_jet1_ll.append(sr1_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet1_ll.append(sr2_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet2_ll.append(sr2_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi400_sr1_jet2_ll.append(sr1_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet3_ll.append(sr2_jet3_pT_ll.Integral()/(htotal.Integral()))

            if i==Mphi[4]:
                    mphi500_sr1_jet1_ll.append(sr1_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet1_ll.append(sr2_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet2_ll.append(sr2_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi500_sr1_jet2_ll.append(sr1_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet3_ll.append(sr2_jet3_pT_ll.Integral()/(htotal.Integral()))


            if i==Mphi[5]:
                    mphi1000_sr1_jet1_ll.append(sr1_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet1_ll.append(sr2_jet1_pT_ll.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet2_ll.append(sr2_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi1000_sr1_jet2_ll.append(sr1_jet2_pT_ll.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet3_ll.append(sr2_jet3_pT_ll.Integral()/(htotal.Integral()))



EffMassSr1jet1_ll=[]
EffMassSr1jet2_ll=[]
EffMassSr2jet1_ll=[]
EffMassSr2jet2_ll=[]
EffMassSr2jet3_ll=[]

EffMassSr1jet1_ll.append(mphi50_sr1_jet1_ll)
EffMassSr1jet1_ll.append(mphi100_sr1_jet1_ll)
EffMassSr1jet1_ll.append(mphi350_sr1_jet1_ll)
EffMassSr1jet1_ll.append(mphi400_sr1_jet1_ll)
EffMassSr1jet1_ll.append(mphi500_sr1_jet1_ll)
EffMassSr1jet1_ll.append(mphi1000_sr1_jet1_ll)


EffMassSr1jet2_ll.append(mphi50_sr1_jet2_ll)
EffMassSr1jet2_ll.append(mphi100_sr1_jet2_ll)
EffMassSr1jet2_ll.append(mphi350_sr1_jet2_ll)
EffMassSr1jet2_ll.append(mphi400_sr1_jet2_ll)
EffMassSr1jet2_ll.append(mphi500_sr1_jet2_ll)
EffMassSr1jet2_ll.append(mphi1000_sr1_jet2_ll)


EffMassSr2jet1_ll.append(mphi50_sr2_jet1_ll)
EffMassSr2jet1_ll.append(mphi100_sr2_jet1_ll)
EffMassSr2jet1_ll.append(mphi350_sr2_jet1_ll)
EffMassSr2jet1_ll.append(mphi400_sr2_jet1_ll)
EffMassSr2jet1_ll.append(mphi500_sr2_jet1_ll)
EffMassSr2jet1_ll.append(mphi1000_sr2_jet1_ll)

EffMassSr2jet2_ll.append(mphi50_sr2_jet2_ll)
EffMassSr2jet2_ll.append(mphi100_sr2_jet2_ll)
EffMassSr2jet2_ll.append(mphi350_sr2_jet2_ll)
EffMassSr2jet2_ll.append(mphi400_sr2_jet2_ll)
EffMassSr2jet2_ll.append(mphi500_sr2_jet2_ll)
EffMassSr2jet2_ll.append(mphi1000_sr2_jet2_ll)

EffMassSr2jet3_ll.append(mphi50_sr2_jet3_ll)
EffMassSr2jet3_ll.append(mphi100_sr2_jet3_ll)
EffMassSr2jet3_ll.append(mphi350_sr2_jet3_ll)
EffMassSr2jet3_ll.append(mphi400_sr2_jet3_ll)
EffMassSr2jet3_ll.append(mphi500_sr2_jet3_ll)
EffMassSr2jet3_ll.append(mphi1000_sr2_jet3_ll)


all_srJets=[EffMassSr2jet1_ll,EffMassSr2jet2_ll,EffMassSr1jet1_ll,EffMassSr1jet2_ll,EffMassSr2jet3_ll]
all_BRjets=[sr2_jet1_ll,sr2_jet2_ll,sr1_jet1_ll,sr1_jet2_ll,sr2_jet3_ll]
label=['Sr2_jet1_ll','Sr2_jet2_ll','Sr1_jet1_ll','Sr1_jet2_ll','Sr2_jet3_ll']



y=[]
for i in range(len(EffMassSr1jet1_ll)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr1jet1_ll[i])[0])*100000/(math.sqrt((sr1_jet1_ll[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr1_jet_ll')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR1: Loose Working Point")
plt.savefig('sr1_jet1_ll.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')

y=[]
for i in range(len(EffMassSr2jet1_ll)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr2jet1_ll[i])[0])*100000/(math.sqrt((sr2_jet1_ll[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr2_jet1')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Loose Working Point")
plt.savefig('sr2_jet1_ll.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')


y=[]
for i in range(len(EffMassSr2jet2_ll)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr2jet2_ll[i])[0])*100000/(math.sqrt((sr2_jet2_ll[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr2_jet2')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Loose Working Point")
plt.savefig('sr2_jet2_ll.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')

path_sig_mm='mm/sig/*Output_pseudo_NLO_Mchi-1_Mphi*.root'
path_bkg_mm='mm/bkg/*.root'

Mphi=['50','100','350','400','500','1000']
mchi=['1']
pT_cuts=[50,55,60,65,70]    # pt cut for leading jet
pT_cuts_add=[30,35,40,45,50]  #pT cut for additional jets

bkgsr1_mm=['jet1_pT_sr1','jet2_pT_sr1']
bkgsr2_mm=['jet1_pT_sr2','jet2_pT_sr2','jet3_pT_sr2']

# Xrange=1000  # range of pt [0,1000]
# Totalbins=200
# perbin=(Xrange)/(Totalbins)
# print (perbin)
# setbins=[]   # set first bin for leading jet
# setbins_add=[]  # set first bin for additional jet
#
# for i in pT_cuts:
#     setbins.append((i)/(perbin))
#     print (i/(perbin))
#
# for i in pT_cuts_add:
#     setbins_add.append((i)/(perbin))
#     print (i/(perbin))



mphi50_sr1_jet1_mm=[]
mphi50_sr1_jet2_mm=[]
mphi50_sr2_jet1_mm=[]
mphi50_sr2_jet2_mm=[]
mphi50_sr2_jet3_mm=[]

mphi100_sr1_jet1_mm=[]
mphi100_sr1_jet2_mm=[]
mphi100_sr2_jet1_mm=[]
mphi100_sr2_jet2_mm=[]
mphi100_sr2_jet3_mm=[]

mphi350_sr1_jet1_mm=[]
mphi350_sr1_jet2_mm=[]
mphi350_sr2_jet1_mm=[]
mphi350_sr2_jet2_mm=[]
mphi350_sr2_jet3_mm=[]

mphi400_sr1_jet1_mm=[]
mphi400_sr1_jet2_mm=[]
mphi400_sr2_jet1_mm=[]
mphi400_sr2_jet2_mm=[]
mphi400_sr2_jet3_mm=[]

mphi500_sr1_jet1_mm=[]
mphi500_sr1_jet2_mm=[]
mphi500_sr2_jet1_mm=[]
mphi500_sr2_jet2_mm=[]
mphi500_sr2_jet3_mm=[]

mphi1000_sr1_jet1_mm=[]
mphi1000_sr1_jet2_mm=[]
mphi1000_sr2_jet1_mm=[]
mphi1000_sr2_jet2_mm=[]
mphi1000_sr2_jet3_mm=[]

sr1_jet1_mm=[]
sr1_jet2_mm=[]
sr2_jet1_mm=[]
sr2_jet2_mm=[]
sr2_jet3_mm=[]



files_bkg_mm = sorted(glob.glob(path_bkg_mm))
# print ("total files")
# print (files_bkg)
for file in files_bkg_mm:
    f=TFile.Open(file,'read')
    print ("selected file");f

    for i in bkgsr1_mm:
        if i in file.split('/')[-1]:
            if i==bkgsr1_mm[0]:
                # print (file)
                bkgsum=f.Get("bkgSum")
                sr1_jet1_mm.append(bkgsum.Integral())
            if i==bkgsr1_mm[1]:
                bkgsum=f.Get("bkgSum")
                sr1_jet2_mm.append(bkgsum.Integral())
    for i in bkgsr2_mm:
        if i in file.split('/')[-1]:
            if i==bkgsr2_mm[0]:
                bkgsum=f.Get("bkgSum")
                sr2_jet1_mm.append(bkgsum.Integral())
            if i==bkgsr2_mm[1]:
                bkgsum=f.Get("bkgSum")
                sr2_jet2_mm.append(bkgsum.Integral())
            if i==bkgsr2_mm[2]:
                bkgsum=f.Get("bkgSum")
                sr2_jet3_mm.append(bkgsum.Integral())





files = sorted(glob.glob(path_sig_mm))
print ("total files");files
for file in files:
    f=TFile.Open(file,'read')
    htotal=f.Get('h_total')
    print(htotal.Integral())
    print ("selected file")
    #print (f)
    sr1_jet1_pT_mm=f.Get('h_jet1_pT_sr1_')
    sr1_jet2_pT_mm=f.Get('h_jet2_pT_sr1_')
    sr2_jet1_pT_mm=f.Get('h_jet1_pT_sr2_')
    sr2_jet2_pT_mm=f.Get('h_jet2_pT_sr2_')
    sr2_jet3_pT_mm=f.Get('h_jet3_pT_sr2_')

    for i in Mphi:
        #print (file.split('/')[-1])
        if '_Mphi-'+i+'.root' in file.split('/')[-1]:
            #print ("entering")
            if i==Mphi[0]:
                    mphi50_sr1_jet1_mm.append(sr1_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet1_mm.append(sr2_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet2_mm.append(sr2_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi50_sr1_jet2_mm.append(sr1_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet3_mm.append(sr2_jet3_pT_mm.Integral()/(htotal.Integral()))



            if i==Mphi[1]:
                    mphi100_sr1_jet1_mm.append(sr1_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet1_mm.append(sr2_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet2_mm.append(sr2_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi100_sr1_jet2_mm.append(sr1_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet3_mm.append(sr2_jet3_pT_mm.Integral()/(htotal.Integral()))

            if i==Mphi[2]:
                    mphi350_sr1_jet1_mm.append(sr1_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet1_mm.append(sr2_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet2_mm.append(sr2_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi350_sr1_jet2_mm.append(sr1_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet3_mm.append(sr2_jet3_pT_mm.Integral()/(htotal.Integral()))

            if i==Mphi[3]:
                    mphi400_sr1_jet1_mm.append(sr1_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet1_mm.append(sr2_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet2_mm.append(sr2_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi400_sr1_jet2_mm.append(sr1_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet3_mm.append(sr2_jet3_pT_mm.Integral()/(htotal.Integral()))

            if i==Mphi[4]:
                    mphi500_sr1_jet1_mm.append(sr1_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet1_mm.append(sr2_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet2_mm.append(sr2_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi500_sr1_jet2_mm.append(sr1_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet3_mm.append(sr2_jet3_pT_mm.Integral()/(htotal.Integral()))


            if i==Mphi[5]:
                    mphi1000_sr1_jet1_mm.append(sr1_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet1_mm.append(sr2_jet1_pT_mm.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet2_mm.append(sr2_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi1000_sr1_jet2_mm.append(sr1_jet2_pT_mm.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet3_mm.append(sr2_jet3_pT_mm.Integral()/(htotal.Integral()))



EffMassSr1jet1_mm=[]
EffMassSr1jet2_mm=[]
EffMassSr2jet1_mm=[]
EffMassSr2jet2_mm=[]
EffMassSr2jet3_mm=[]

EffMassSr1jet1_mm.append(mphi50_sr1_jet1_mm)
EffMassSr1jet1_mm.append(mphi100_sr1_jet1_mm)
EffMassSr1jet1_mm.append(mphi350_sr1_jet1_mm)
EffMassSr1jet1_mm.append(mphi400_sr1_jet1_mm)
EffMassSr1jet1_mm.append(mphi500_sr1_jet1_mm)
EffMassSr1jet1_mm.append(mphi1000_sr1_jet1_mm)


EffMassSr1jet2_mm.append(mphi50_sr1_jet2_mm)
EffMassSr1jet2_mm.append(mphi100_sr1_jet2_mm)
EffMassSr1jet2_mm.append(mphi350_sr1_jet2_mm)
EffMassSr1jet2_mm.append(mphi400_sr1_jet2_mm)
EffMassSr1jet2_mm.append(mphi500_sr1_jet2_mm)
EffMassSr1jet2_mm.append(mphi1000_sr1_jet2_mm)


EffMassSr2jet1_mm.append(mphi50_sr2_jet1_mm)
EffMassSr2jet1_mm.append(mphi100_sr2_jet1_mm)
EffMassSr2jet1_mm.append(mphi350_sr2_jet1_mm)
EffMassSr2jet1_mm.append(mphi400_sr2_jet1_mm)
EffMassSr2jet1_mm.append(mphi500_sr2_jet1_mm)
EffMassSr2jet1_mm.append(mphi1000_sr2_jet1_mm)

EffMassSr2jet2_mm.append(mphi50_sr2_jet2_mm)
EffMassSr2jet2_mm.append(mphi100_sr2_jet2_mm)
EffMassSr2jet2_mm.append(mphi350_sr2_jet2_mm)
EffMassSr2jet2_mm.append(mphi400_sr2_jet2_mm)
EffMassSr2jet2_mm.append(mphi500_sr2_jet2_mm)
EffMassSr2jet2_mm.append(mphi1000_sr2_jet2_mm)

EffMassSr2jet3_mm.append(mphi50_sr2_jet3_mm)
EffMassSr2jet3_mm.append(mphi100_sr2_jet3_mm)
EffMassSr2jet3_mm.append(mphi350_sr2_jet3_mm)
EffMassSr2jet3_mm.append(mphi400_sr2_jet3_mm)
EffMassSr2jet3_mm.append(mphi500_sr2_jet3_mm)
EffMassSr2jet3_mm.append(mphi1000_sr2_jet3_mm)


all_srJets=[EffMassSr2jet1_mm,EffMassSr2jet2_mm,EffMassSr1jet1_mm,EffMassSr1jet2_mm,EffMassSr2jet3_mm]
all_BRjets=[sr2_jet1_mm,sr2_jet2_mm,sr1_jet1_mm,sr1_jet2_mm,sr2_jet3_mm]
label=['Sr2_jet1_mm','Sr2_jet2_mm','Sr1_jet1_mm','Sr1_jet2_mm','Sr2_jet3_mm']



y=[]
for i in range(len(EffMassSr1jet1_mm)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr1jet1_mm[i])[0])*100000/(math.sqrt((sr1_jet1_mm[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr1_jet_mm')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR1: Medium Working Point")
plt.savefig('sr1_jet1_mm.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')

y=[]
for i in range(len(EffMassSr2jet1_mm)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr2jet1_mm[i])[0])*100000/(math.sqrt((sr2_jet1_mm[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr2_jet1')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Medium Working Point")
plt.savefig('sr2_jet1_mm.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')


y=[]
for i in range(len(EffMassSr2jet2_mm)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr2jet2_mm[i])[0])*100000/(math.sqrt((sr2_jet2_mm[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr2_jet2')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Medium Working Point")
plt.savefig('sr2_jet2_mm.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')

path_sig_lm='lm/sig/*Output_pseudo_NLO_Mchi-1_Mphi*.root'
path_bkg_lm='lm/bkg/*.root'

Mphi=['50','100','350','400','500','1000']
mchi=['1']
pT_cuts=[50,55,60,65,70]    # pt cut for leading jet
pT_cuts_add=[30,35,40,45,50]  #pT cut for additional jets

bkgsr1_lm=['jet1_pT_sr1','jet2_pT_sr1']
bkgsr2_lm=['jet1_pT_sr2','jet2_pT_sr2','jet3_pT_sr2']

# Xrange=1000  # range of pt [0,1000]
# Totalbins=200
# perbin=(Xrange)/(Totalbins)
# print (perbin)
# setbins=[]   # set first bin for leading jet
# setbins_add=[]  # set first bin for additional jet
#
# for i in pT_cuts:
#     setbins.append((i)/(perbin))
#     print (i/(perbin))
#
# for i in pT_cuts_add:
#     setbins_add.append((i)/(perbin))
#     print (i/(perbin))



mphi50_sr1_jet1_lm=[]
mphi50_sr1_jet2_lm=[]
mphi50_sr2_jet1_lm=[]
mphi50_sr2_jet2_lm=[]
mphi50_sr2_jet3_lm=[]

mphi100_sr1_jet1_lm=[]
mphi100_sr1_jet2_lm=[]
mphi100_sr2_jet1_lm=[]
mphi100_sr2_jet2_lm=[]
mphi100_sr2_jet3_lm=[]

mphi350_sr1_jet1_lm=[]
mphi350_sr1_jet2_lm=[]
mphi350_sr2_jet1_lm=[]
mphi350_sr2_jet2_lm=[]
mphi350_sr2_jet3_lm=[]

mphi400_sr1_jet1_lm=[]
mphi400_sr1_jet2_lm=[]
mphi400_sr2_jet1_lm=[]
mphi400_sr2_jet2_lm=[]
mphi400_sr2_jet3_lm=[]

mphi500_sr1_jet1_lm=[]
mphi500_sr1_jet2_lm=[]
mphi500_sr2_jet1_lm=[]
mphi500_sr2_jet2_lm=[]
mphi500_sr2_jet3_lm=[]

mphi1000_sr1_jet1_lm=[]
mphi1000_sr1_jet2_lm=[]
mphi1000_sr2_jet1_lm=[]
mphi1000_sr2_jet2_lm=[]
mphi1000_sr2_jet3_lm=[]

sr1_jet1_lm=[]
sr1_jet2_lm=[]
sr2_jet1_lm=[]
sr2_jet2_lm=[]
sr2_jet3_lm=[]



files_bkg_lm = sorted(glob.glob(path_bkg_lm))
# print ("total files")
# print (files_bkg)
for file in files_bkg_lm:
    f=TFile.Open(file,'read')
    print ("selected file");f

    for i in bkgsr1_lm:
        if i in file.split('/')[-1]:
            if i==bkgsr1_lm[0]:
                # print (file)
                bkgsum=f.Get("bkgSum")
                sr1_jet1_lm.append(bkgsum.Integral())
            if i==bkgsr1_lm[1]:
                bkgsum=f.Get("bkgSum")
                sr1_jet2_lm.append(bkgsum.Integral())
    for i in bkgsr2_lm:
        if i in file.split('/')[-1]:
            if i==bkgsr2_lm[0]:
                bkgsum=f.Get("bkgSum")
                sr2_jet1_lm.append(bkgsum.Integral())
            if i==bkgsr2_lm[1]:
                bkgsum=f.Get("bkgSum")
                sr2_jet2_lm.append(bkgsum.Integral())
            if i==bkgsr2_lm[2]:
                bkgsum=f.Get("bkgSum")
                sr2_jet3_lm.append(bkgsum.Integral())





files = sorted(glob.glob(path_sig_lm))
print ("total files");files
for file in files:
    f=TFile.Open(file,'read')
    htotal=f.Get('h_total')
    print(htotal.Integral())
    print ("selected file")
    #print (f)
    sr1_jet1_pT_lm=f.Get('h_jet1_pT_sr1_')
    sr1_jet2_pT_lm=f.Get('h_jet2_pT_sr1_')
    sr2_jet1_pT_lm=f.Get('h_jet1_pT_sr2_')
    sr2_jet2_pT_lm=f.Get('h_jet2_pT_sr2_')
    sr2_jet3_pT_lm=f.Get('h_jet3_pT_sr2_')

    for i in Mphi:
        #print (file.split('/')[-1])
        if '_Mphi-'+i+'.root' in file.split('/')[-1]:
            #print ("entering")
            if i==Mphi[0]:
                    mphi50_sr1_jet1_lm.append(sr1_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet1_lm.append(sr2_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet2_lm.append(sr2_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi50_sr1_jet2_lm.append(sr1_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi50_sr2_jet3_lm.append(sr2_jet3_pT_lm.Integral()/(htotal.Integral()))



            if i==Mphi[1]:
                    mphi100_sr1_jet1_lm.append(sr1_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet1_lm.append(sr2_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet2_lm.append(sr2_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi100_sr1_jet2_lm.append(sr1_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi100_sr2_jet3_lm.append(sr2_jet3_pT_lm.Integral()/(htotal.Integral()))

            if i==Mphi[2]:
                    mphi350_sr1_jet1_lm.append(sr1_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet1_lm.append(sr2_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet2_lm.append(sr2_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi350_sr1_jet2_lm.append(sr1_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi350_sr2_jet3_lm.append(sr2_jet3_pT_lm.Integral()/(htotal.Integral()))

            if i==Mphi[3]:
                    mphi400_sr1_jet1_lm.append(sr1_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet1_lm.append(sr2_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet2_lm.append(sr2_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi400_sr1_jet2_lm.append(sr1_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi400_sr2_jet3_lm.append(sr2_jet3_pT_lm.Integral()/(htotal.Integral()))

            if i==Mphi[4]:
                    mphi500_sr1_jet1_lm.append(sr1_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet1_lm.append(sr2_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet2_lm.append(sr2_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi500_sr1_jet2_lm.append(sr1_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi500_sr2_jet3_lm.append(sr2_jet3_pT_lm.Integral()/(htotal.Integral()))


            if i==Mphi[5]:
                    mphi1000_sr1_jet1_lm.append(sr1_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet1_lm.append(sr2_jet1_pT_lm.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet2_lm.append(sr2_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi1000_sr1_jet2_lm.append(sr1_jet2_pT_lm.Integral()/(htotal.Integral()))
                    mphi1000_sr2_jet3_lm.append(sr2_jet3_pT_lm.Integral()/(htotal.Integral()))



EffMassSr1jet1_lm=[]
EffMassSr1jet2_lm=[]
EffMassSr2jet1_lm=[]
EffMassSr2jet2_lm=[]
EffMassSr2jet3_lm=[]

EffMassSr1jet1_lm.append(mphi50_sr1_jet1_lm)
EffMassSr1jet1_lm.append(mphi100_sr1_jet1_lm)
EffMassSr1jet1_lm.append(mphi350_sr1_jet1_lm)
EffMassSr1jet1_lm.append(mphi400_sr1_jet1_lm)
EffMassSr1jet1_lm.append(mphi500_sr1_jet1_lm)
EffMassSr1jet1_lm.append(mphi1000_sr1_jet1_lm)


EffMassSr1jet2_lm.append(mphi50_sr1_jet2_lm)
EffMassSr1jet2_lm.append(mphi100_sr1_jet2_lm)
EffMassSr1jet2_lm.append(mphi350_sr1_jet2_lm)
EffMassSr1jet2_lm.append(mphi400_sr1_jet2_lm)
EffMassSr1jet2_lm.append(mphi500_sr1_jet2_lm)
EffMassSr1jet2_lm.append(mphi1000_sr1_jet2_lm)


EffMassSr2jet1_lm.append(mphi50_sr2_jet1_lm)
EffMassSr2jet1_lm.append(mphi100_sr2_jet1_lm)
EffMassSr2jet1_lm.append(mphi350_sr2_jet1_lm)
EffMassSr2jet1_lm.append(mphi400_sr2_jet1_lm)
EffMassSr2jet1_lm.append(mphi500_sr2_jet1_lm)
EffMassSr2jet1_lm.append(mphi1000_sr2_jet1_lm)

EffMassSr2jet2_lm.append(mphi50_sr2_jet2_lm)
EffMassSr2jet2_lm.append(mphi100_sr2_jet2_lm)
EffMassSr2jet2_lm.append(mphi350_sr2_jet2_lm)
EffMassSr2jet2_lm.append(mphi400_sr2_jet2_lm)
EffMassSr2jet2_lm.append(mphi500_sr2_jet2_lm)
EffMassSr2jet2_lm.append(mphi1000_sr2_jet2_lm)

EffMassSr2jet3_lm.append(mphi50_sr2_jet3_lm)
EffMassSr2jet3_lm.append(mphi100_sr2_jet3_lm)
EffMassSr2jet3_lm.append(mphi350_sr2_jet3_lm)
EffMassSr2jet3_lm.append(mphi400_sr2_jet3_lm)
EffMassSr2jet3_lm.append(mphi500_sr2_jet3_lm)
EffMassSr2jet3_lm.append(mphi1000_sr2_jet3_lm)


all_srJets=[EffMassSr2jet1_lm,EffMassSr2jet2_lm,EffMassSr1jet1_lm,EffMassSr1jet2_lm,EffMassSr2jet3_lm]
all_BRjets=[sr2_jet1_lm,sr2_jet2_lm,sr1_jet1_lm,sr1_jet2_lm,sr2_jet3_lm]
label=['Sr2_jet1_lm','Sr2_jet2_lm','Sr1_jet1_lm','Sr1_jet2_lm','Sr2_jet3_lm']



y=[]
for i in range(len(EffMassSr1jet1_lm)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr1jet1_lm[i])[0])*100000/(math.sqrt((sr1_jet1_lm[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr1_jet_lm')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR1: Loose Working Point")
plt.savefig('sr1_jet1_lm.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')

y=[]
for i in range(len(EffMassSr2jet1_lm)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr2jet1_lm[i])[0])*100000/(math.sqrt((sr2_jet1_lm[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr2_jet1')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Loose Working Point")
plt.savefig('sr2_jet1_lm.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')


y=[]
for i in range(len(EffMassSr2jet2_lm)):
    #print ((sr2_jet2[pt]))
    y.append(((EffMassSr2jet2_lm[i])[0])*100000/(math.sqrt((sr2_jet2_lm[0]))))
plt.plot([50,100,350,400,500,1000],y,'o-',label='sr2_jet2')

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Loose Working Point")
plt.savefig('sr2_jet2_lm.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')

##############################################
EffMassSr2jet2=[]
EffMassSr2jet1=[]
EffMassSr1jet2=[]
EffMassSr1jet1=[]
sr2_jet2=[]
sr2_jet1=[]
sr1_jet1=[]


EffMassSr2jet2.append(EffMassSr2jet2_ll)
EffMassSr2jet2.append(EffMassSr2jet2_mm)
EffMassSr2jet2.append(EffMassSr2jet2_lm)
EffMassSr2jet1.append(EffMassSr2jet1_ll)
EffMassSr2jet1.append(EffMassSr2jet1_mm)
EffMassSr2jet1.append(EffMassSr2jet1_lm)
EffMassSr1jet1.append(EffMassSr1jet1_ll)
EffMassSr1jet1.append(EffMassSr1jet1_mm)
EffMassSr1jet1.append(EffMassSr1jet1_lm)

sr2_jet2.append(sr2_jet2_ll)
sr2_jet2.append(sr2_jet2_mm)
sr2_jet2.append(sr2_jet2_lm)
sr2_jet1.append(sr2_jet1_ll)
sr2_jet1.append(sr2_jet1_mm)
sr2_jet1.append(sr2_jet1_lm)
sr1_jet1.append(sr1_jet1_ll)
sr1_jet1.append(sr1_jet1_mm)
sr1_jet1.append(sr1_jet1_lm)

WP=['LWP','MWP','LMWP']
# for sr1 jet1
for i in range(len(EffMassSr1jet1)):
    y=[]
    for j in range(len(EffMassSr1jet1[0])):
        a=EffMassSr1jet1[i]
        b=sr1_jet1[i]
        #print (((a)[j][pt])/(b[pt]))
        y.append((((a)[j][0])*100000/(math.sqrt((b[0])))))
        #print (y[0])
    plt.plot([50,100,350,400,500,1000],y,'o-',label='jet1_$p_{T}$='+str(pT_cuts[0])+'GeV : '+(WP[i]))

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR1: LWP Vs MWP Vs MLWP(jet1 LWP) ")
plt.savefig('sr1_jet1_pT_ll_mm_lm.pdf')
plt.clf()
plt.cla()
plt.close('all')

# for sr2 jet1
for i in range(len(EffMassSr2jet1)):
    y=[]
    for j in range(len(EffMassSr2jet1[0])):
        a=EffMassSr2jet1[i]
        b=sr2_jet1[i]
        #print (((a)[j][pt])/(b[pt]))
        y.append((((a)[j][0])*100000/(math.sqrt((b[0])))))
        #print (y[0])
    plt.plot([50,100,350,400,500,1000],y,'o-',label='jet1_$p_{T}$='+str(pT_cuts[0])+'GeV : '+(WP[i]))

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: LWP Vs MWP Vs MLWP(jet1 MWP) ")
plt.savefig('sr2_jet1_pT_ll_mm_lm.pdf')
plt.clf()
plt.cla()
plt.close('all')

# for sr2 jet2
for i in range(len(EffMassSr2jet2)):
    y=[]
    for j in range(len(EffMassSr2jet2[0])):
        a=EffMassSr2jet2[i]
        b=sr2_jet2[i]
        #print (((a)[j][pt])/(b[pt]))
        y.append((((a)[j][0])*100000/(math.sqrt((b[0])))))
        #print (y[0])
    plt.plot([50,100,350,400,500,1000],y,'o-',label='jet2_$p_{T}$='+str(pT_cuts[0])+'GeV : '+(WP[i]))

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: LWP Vs MWP Vs MLWP(jet2 LWP) ")
plt.savefig('sr2_jet2_pT_ll_mm_lm.pdf')
plt.clf()
plt.cla()
plt.close('all')
