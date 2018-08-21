
# coding: utf-8

# In[1]:


import ROOT as ROOT
import os
import sys, optparse
from array import array
import math

ROOT.gSystem.Load("/Users/ptiwari/hep_software/ExROOT/ExRootAnalysis/libExRootAnalysis.so")

ROOT.gStyle.SetFrameLineWidth(3)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gStyle.SetFillColor(2)
ROOT.gStyle.SetLineWidth(1)
ROOT.gStyle.SetHistFillStyle(2)


# In[23]:


dirpath = '/eos/user/p/ptiwari/work/GridPacks_DMSimp_2017_mg26/lhe_production/CMSSW_7_1_30/src/'+sys.argv[1]+'/'

filelist = [f for f in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, f))]
runs = []
for f in filelist:
    if 'MH3_600_' in f:
        runs.append(f)
print(runs)

hists=[]


for i in runs:
    lheROOT = ROOT.TChain("LHEF")
    lheROOT.Add(glob.glob(dirpath+i+'/*.root'))
    h_genMET=ROOT.TH1F('genMET','genMET',100,0,1000)
    genMET=[]
    NEntries = lheROOT.GetEntries()
    for ievent in range(NEntries):
        if ievent%100==0: print ("Processed "+str(ievent)+" of "+str(NEntries)+" events.")
        lheROOT.GetEntry(ievent)
        ## Get all relevant branches
        event      = lheROOT.__getattr__('Event')
        num_event   = lheROOT.__getattr__('Event_size')
        num_part   = lheROOT.__getattr__('Particle_size')
        particle   = lheROOT.__getattr__('Particle')
        weight = event[0].Weight

        for ipart in range(num_part):
            if weight > 0:
                if particle[ipart].PID == 52:
                    chi    = ROOT.TLorentzVector(particle[ipart].Px,particle[ipart].Py,particle[ipart].Pz,particle[ipart].E)
                if particle[ipart].PID == -52:
                    chibar = ROOT.TLorentzVector(particle[ipart].Px,particle[ipart].Py,particle[ipart].Pz,particle[ipart].E)
        genMET.append((chi+chibar).Pt())

    for met in genMET:
        h_genMET.Fill(met)
    hists.append(h_genMET)

c = ROOT.TCanvas()
legend=ROOT.TLegend(.53,.59,.87,.89)
legend.SetTextSize(0.038)
leg_entry=['M_{a}=100 GeV','M_{a}=200 GeV','M_{a}=300 GeV','M_{a}=400 GeV','M_{A}=500 GeV']

cmsname = ROOT.TLatex();
cmsname.SetTextSize(0.036)
cmsname.SetTextAlign(12)
cmsname.SetNDC(1)
cmsname.SetTextFont(61)

for hist in range(len(hists)):
    print (hist)
    if hist==0:
        hists[hist].SetXTitle("genMET[GeV]")
        hists[hist].SetYTitle("Events")
        hists[hist].SetLineColor(hist+1)
        hists[hist].Rebin(5)
        hists[hist].SetLineWidth(3)
        hists[hist].Scale(1/hists[hist].Integral())
        hists[hist].SetMaximum(2)
        legend.AddEntry(hists[hist],leg_entry[hist],"L")
        hists[hist].Draw('HIST')

    else:
        hists[hist].SetXTitle("genMET[GeV]")
        hists[hist].SetYTitle("Events")
        hists[hist].SetLineColor(hist+1)
        hists[hist].Rebin(5)
        hists[hist].SetLineWidth(3)
        hists[hist].Scale(1/hists[hist].Integral())
        hists[hist].SetMaximum(2)
        legend.AddEntry(hists[hist],leg_entry[hist],"L")
        hists[hist].Draw('HIST same')

cmsname.DrawLatex(0.12, .94, "2HDM+a b#bar{b} + DM"+" "*13+"tan#beta = 35 sin#theta = 0.707")
legend.Draw()
c.SetLogy()
#c.update()
c.SaveAs("Combined_mA_"+sys.argv[1]+".pdf")
