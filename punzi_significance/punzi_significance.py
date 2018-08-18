from ROOT import TGraph, TFile, TGraphAsymmErrors
from array import array
import os
import glob,math
import matplotlib.pyplot as plt

path='../test_dir/*.root'

Mphi=['50','100','350','400','500','1000']
mchi=['1']
pT_cuts=[30,50]    # pt cut for leading jet
pT_cuts_add=[30,50]  #pT cut for additional jets

bkgsr1=['jet1_pT_sr1','jet2_pT_sr1']
bkgsr2=['jet1_pT_sr2','jet2_pT_sr2','jet3_pT_sr2']

Xrange=1000  # range of pt [0,1000]
Totalbins=50
perbin=(Xrange)/(Totalbins)
print (perbin)
setbins=[]   # set first bin for leading jet
setbins_add=[]  # set first bin for additional jet

for i in pT_cuts:
    setbins.append((i)/(perbin))
    print (i/(perbin))

for i in pT_cuts_add:
    setbins_add.append((i)/(perbin))
    print (i/(perbin))



mphi50_sr1_jet1=[]
mphi50_sr1_jet2=[]
mphi50_sr2_jet1=[]
mphi50_sr2_jet2=[]
mphi50_sr2_jet3=[]

mphi100_sr1_jet1=[]
mphi100_sr1_jet2=[]
mphi100_sr2_jet1=[]
mphi100_sr2_jet2=[]
mphi100_sr2_jet3=[]

mphi350_sr1_jet1=[]
mphi350_sr1_jet2=[]
mphi350_sr2_jet1=[]
mphi350_sr2_jet2=[]
mphi350_sr2_jet3=[]

mphi400_sr1_jet1=[]
mphi400_sr1_jet2=[]
mphi400_sr2_jet1=[]
mphi400_sr2_jet2=[]
mphi400_sr2_jet3=[]

mphi500_sr1_jet1=[]
mphi500_sr1_jet2=[]
mphi500_sr2_jet1=[]
mphi500_sr2_jet2=[]
mphi500_sr2_jet3=[]

mphi1000_sr1_jet1=[]
mphi1000_sr1_jet2=[]
mphi1000_sr2_jet1=[]
mphi1000_sr2_jet2=[]
mphi1000_sr2_jet3=[]

sr1_jet1=[]
sr1_jet2=[]
sr2_jet1=[]
sr2_jet2=[]
sr2_jet3=[]



files_bkg = sorted(glob.glob(path))
# print ("total files")
# print (files_bkg)
for file in files_bkg:
    f=TFile.Open(file,'read')
    print ("selected file");f

    for i in bkgsr1:
        if i in file.split('/')[-1]:
            if i==bkgsr1[0]:
                # print (file)
                bkgsum=f.Get("bkgSum")
                # a=bkgsum.Draw()
                # print (bkgsum.Integral())
                for j in setbins:
                    # print (bkgsum.Integral(int(j+1),201))
                    sr1_jet1.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr1[1]:
                bkgsum=f.Get("bkgSum")
                # a=bkgsum.Draw()
                for j in setbins_add:
                    sr1_jet2.append(bkgsum.Integral(int(j+1),201))
    for i in bkgsr2:
        if i in file.split('/')[-1]:
            if i==bkgsr2[0]:
                bkgsum=f.Get("bkgSum")
                # a=bkgsum.Draw()
                for j in setbins:
                    sr2_jet1.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr2[1]:
                bkgsum=f.Get("bkgSum")
                for j in setbins:
                    sr2_jet2.append(bkgsum.Integral(int(j+1),201))
            if i==bkgsr2[2]:
                bkgsum=f.Get("bkgSum")
                for j in setbins_add:
                    sr2_jet3.append(bkgsum.Integral(int(j+1),201))


files = sorted(glob.glob(path))
print ("total files");files
for file in files:
    f=TFile.Open(file,'read')
    htotal=f.Get('h_total')
    #print ("selected file")
    #print (f)
    sr1_jet1_pT=f.Get('h_jet1_pT_sr1_')
    sr1_jet2_pT=f.Get('h_jet2_pT_sr1_')
    sr2_jet1_pT=f.Get('h_jet1_pT_sr2_')
    sr2_jet2_pT=f.Get('h_jet2_pT_sr2_')
    sr2_jet3_pT=f.Get('h_jet3_pT_sr2_')

    for i in Mphi:
        #print (file.split('/')[-1])
        if '_Mphi-'+i+'.root' in file.split('/')[-1]:
            #print ("entering")
            if i==Mphi[0]:
                #print ("entering")
                for j in setbins:
                    mphi50_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi50_sr2_jet1.append((sr2_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi50_sr2_jet2.append((sr2_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                for j in setbins_add:
                    mphi50_sr1_jet2.append((sr1_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                    mphi50_sr2_jet3.append((sr2_jet3_pT.Integral(int(j+1),201))/(htotal.Integral()))



            if i==Mphi[1]:
                #print ("entering")
                for j in setbins:
                    mphi100_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi100_sr2_jet1.append((sr2_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi100_sr2_jet2.append((sr2_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                for j in setbins_add:
                    mphi100_sr1_jet2.append((sr1_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                    mphi100_sr2_jet3.append((sr2_jet3_pT.Integral(int(j+1),201))/(htotal.Integral()))

            if i==Mphi[2]:
                #print ("entering")
                for j in setbins:
                    mphi350_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi350_sr2_jet1.append((sr2_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi350_sr2_jet2.append((sr2_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                for j in setbins_add:
                    mphi350_sr1_jet2.append((sr1_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                    mphi350_sr2_jet3.append((sr2_jet3_pT.Integral(int(j+1),201))/(htotal.Integral()))

            if i==Mphi[3]:
                #print ("entering")
                for j in setbins:
                    mphi400_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi400_sr2_jet1.append((sr2_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi400_sr2_jet2.append((sr2_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                for j in setbins_add:
                    mphi400_sr1_jet2.append((sr1_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                    mphi400_sr2_jet3.append((sr2_jet3_pT.Integral(int(j+1),201))/(htotal.Integral()))

            if i==Mphi[4]:
                #print ("entering")
                for j in setbins:
                    mphi500_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi500_sr2_jet1.append((sr2_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi500_sr2_jet2.append((sr2_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                for j in setbins_add:
                    mphi500_sr1_jet2.append((sr1_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                    mphi500_sr2_jet3.append((sr2_jet3_pT.Integral(int(j+1),201))/(htotal.Integral()))


            if i==Mphi[5]:
                #print ("entering")
                for j in setbins:
                    mphi1000_sr1_jet1.append((sr1_jet1_pT.Integral(int(j+1),201))/(htotal.Integral()))
                    mphi1000_sr2_jet1.append(sr2_jet1_pT.Integral(int(j+1),201)/(htotal.Integral()))
                    mphi1000_sr2_jet2.append((sr2_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                for j in setbins_add:
                    mphi1000_sr1_jet2.append((sr1_jet2_pT.Integral(int(j+1),201))/(htotal.Integral()))

                    mphi1000_sr2_jet3.append((sr2_jet3_pT.Integral(int(j+1),201))/(htotal.Integral()))

EffMassSr1jet1=[]
EffMassSr1jet2=[]
EffMassSr2jet1=[]
EffMassSr2jet2=[]
EffMassSr2jet3=[]

y=[]

EffMassSr1jet1.append(mphi50_sr1_jet1)
EffMassSr1jet1.append(mphi100_sr1_jet1)
EffMassSr1jet1.append(mphi350_sr1_jet1)
EffMassSr1jet1.append(mphi400_sr1_jet1)
EffMassSr1jet1.append(mphi500_sr1_jet1)
EffMassSr1jet1.append(mphi1000_sr1_jet1)


EffMassSr1jet2.append(mphi50_sr1_jet2)
EffMassSr1jet2.append(mphi100_sr1_jet2)
EffMassSr1jet2.append(mphi350_sr1_jet2)
EffMassSr1jet2.append(mphi400_sr1_jet2)
EffMassSr1jet2.append(mphi500_sr1_jet2)
EffMassSr1jet2.append(mphi1000_sr1_jet2)


EffMassSr2jet1.append(mphi50_sr2_jet1)
EffMassSr2jet1.append(mphi100_sr2_jet1)
EffMassSr2jet1.append(mphi350_sr2_jet1)
EffMassSr2jet1.append(mphi400_sr2_jet1)
EffMassSr2jet1.append(mphi500_sr2_jet1)
EffMassSr2jet1.append(mphi1000_sr2_jet1)

EffMassSr2jet2.append(mphi50_sr2_jet2)
EffMassSr2jet2.append(mphi100_sr2_jet2)
EffMassSr2jet2.append(mphi350_sr2_jet2)
EffMassSr2jet2.append(mphi400_sr2_jet2)
EffMassSr2jet2.append(mphi500_sr2_jet2)
EffMassSr2jet2.append(mphi1000_sr2_jet2)

EffMassSr2jet3.append(mphi50_sr2_jet3)
EffMassSr2jet3.append(mphi100_sr2_jet3)
EffMassSr2jet3.append(mphi350_sr2_jet3)
EffMassSr2jet3.append(mphi400_sr2_jet3)
EffMassSr2jet3.append(mphi500_sr2_jet3)
EffMassSr2jet3.append(mphi1000_sr2_jet3)

all_srJets=[EffMassSr2jet1,EffMassSr2jet2,EffMassSr1jet1,EffMassSr1jet2,EffMassSr2jet3]
all_BRjets=[sr2_jet1,sr2_jet2,sr1_jet1,sr1_jet2,sr2_jet3]
label=['Sr2_jet1','Sr2_jet2','Sr1_jet1','Sr1_jet2','Sr2_jet3']
############################################################
# print (len(EffMassSr1jet1))
# for jet in range(len(all_srJets)):
#     for pt in range(len(pT_cuts)):
#         y=[]
#         for i in range(len(all_srJets[jet])):
#             #print ((sr2_jet2[pt]))
#             y.append((((all_srJets[jet])[i])[pt])*100000/(math.sqrt(((all_BRjets[jet])[pt]))))
#             # print ('efficiency'+str(pT_cuts[pt]))
#             # print (((EffMassSr2jet1[i])[pt]))
#             # print ('background events'+str(pT_cuts[pt]))
#             # print ((sr2_jet1[pt]))
#         if jet==0 or jet==1 or jet==2:
#             plt.plot([50,100,350,400,500,1000],y,'o-',label='jet1_$p_{T}$='+str(pT_cuts[pt]))
#         elif jet==3 or jet==4:
#             plt.plot([50,100,350,400,500,1000],y,'o-',label='jet1_$p_{T}$='+str(pT_cuts_add[pt]))
#
#     #plt.rc('axes', labelsize=20)
#     plt.xlabel(r'$M_{\phi}$')
#     plt.ylabel("Significance(x$10^{-5}$)")
#     #plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
#     plt.legend()#ncol=3,title=r"tan$\beta$")
#     plt.title(r"Significance : Medium Working Point")
#     plt.savefig(''+label[jet]+'.pdf')
#     # plt.savefig(''+label[jet]+'.png')
#     plt.close('all')
############################################################

for pt in range(len(pT_cuts)):
    y=[]
    for i in range(len(EffMassSr2jet2)):
        #print ((sr2_jet2[pt]))
        y.append(((EffMassSr2jet2[i])[pt])*100000/(math.sqrt((sr2_jet2[pt]))))
        # print ('efficiency'+str(pT_cuts[pt]))
        # print (((EffMassSr2jet1[i])[pt]))
        # print ('background events'+str(pT_cuts[pt]))
        # print ((sr2_jet1[pt]))
    plt.plot([50,100,350,400,500,1000],y,'o-',label='jet2_$p_{T}$='+str(pT_cuts[pt]))

#plt.rc('axes', labelsize=20)
plt.xlabel(r'$M_{\phi}$')
plt.ylabel("Significance(x$10^{-5}$)")
#plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
plt.legend()#ncol=3,title=r"tan$\beta$")
plt.title(r"Significance for SR2: Medium Working Point")
plt.savefig('sr2_jet2.pdf')
# plt.savefig('sr2_jet2.png')
plt.close('all')
#
# #######################################################
# for pt in range(len(pT_cuts)):
#     y=[]
#     for i in range(len(EffMassSr1jet1)):
#         #print ((sr2_jet2[pt]))
#         y.append(((EffMassSr1jet1[i])[pt])*100000/(math.sqrt((sr1_jet1[pt]))))
#         # print ('efficiency'+str(pT_cuts[pt]))
#         # print (((EffMassSr2jet1[i])[pt]))
#         # print ('background events'+str(pT_cuts[pt]))
#         # print ((sr2_jet1[pt]))
#     plt.plot([50,100,350,400,500,1000],y,'o-',label='jet1_$p_{T}$='+str(pT_cuts[pt]))
#
# #plt.rc('axes', labelsize=20)
# plt.xlabel(r'$M_{\phi}$')
# plt.ylabel("Significance(x$10^{-5}$)")
# #plt.yticks([1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5])
# plt.legend()#ncol=3,title=r"tan$\beta$")
# plt.title(r"Significance for SR1: Medium Working Point")
# plt.savefig('sr1_jet1.pdf')
# plt.savefig('sr1_jet1.png')
# plt.close('all')
# ####################################
