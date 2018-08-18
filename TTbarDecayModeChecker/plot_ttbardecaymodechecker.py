#!/usr/bin/env python
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math
from ROOT import TFile, gROOT, TCanvas
import getpass
import socket
import json

def SetCanvas():

    # CMS inputs
    # -------------
    H_ref = 1000;
    W_ref = 1000;
    W = W_ref
    H  = H_ref

    T = 0.08*H_ref
    B = 0.21*H_ref
    L = 0.12*W_ref
    R = 0.08*W_ref
    # --------------

    c1 = TCanvas("c2","c2",0,0,1500,1500)
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.SetTickx(0)
    c1.SetTicky(0)
    c1.SetGridy(0)
    c1.SetGridx(0)
    return c1

def CreateLegend(x1, y1, x2, y2, header):

    leg = ROOT.TLegend(x1, x2, y1, y2)
    leg.SetFillColor(0)
    leg.SetFillStyle(3002)
    leg.SetBorderSize(0)
    leg.SetHeader(header)
    return leg

def CustomiseHistogram(h, titleX, titleY, color, lineStyle,title):
    h.SetMarkerColor(color)
    h.SetMarkerSize(1.0)
    h.SetLineColor(color)
    h.SetLineWidth(2)
    h.SetLineStyle(lineStyle)
    h.GetXaxis().SetLabelSize(0.02)
    h.GetYaxis().SetTitle(titleY)
    h.GetXaxis().SetTitle(titleX)
    h.GetYaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetTitleOffset(1.)
    h.SetTitle(title)
    h.Scale(1/(h.Integral()));
    return

def CustomiseHistogram_(h, titleX, titleY, color, lineStyle,title):
    h.SetMarkerColor(color)
    h.SetMarkerSize(1.0)
    h.SetLineColor(color)
    h.SetLineWidth(2)
    h.SetLineStyle(lineStyle)
    h.GetXaxis().SetLabelSize(0.02)
    h.GetYaxis().SetTitle(titleY)
    h.GetXaxis().SetTitle(titleX)
    h.GetYaxis().SetTitleOffset(1.4)
    h.GetXaxis().SetTitleOffset(1.)
    h.SetTitle(title)
    h.Integral();
    return h.Integral()


def drawHisto(h,draw='hist'):
    h.Draw(draw)
    return


def AddText(txt):
    texcms = ROOT.TLatex(-20.0, 50.0, txt)
    texcms.SetNDC()
    texcms.SetTextAlign(12)
    texcms.SetX(0.15)
    texcms.SetY(0.94)
    texcms.SetTextSize(0.02)
    texcms.SetTextSizePixels(22)
    return texcms

def AddTextCat(cat):
    texCat = ROOT.TLatex(-20.0, 50.0, cat)
    texCat.SetNDC()
    texCat.SetTextAlign(12)
    texCat.SetX(0.80)
    texCat.SetY(0.94)
    texCat.SetTextFont(40)
    texCat.SetTextSize(0.02)
    texCat.SetTextSizePixels(22)
    return texCat

ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
gROOT.SetBatch(True)
myHistos=[]
myHistos_str=[]
myHistos_tmp=[]
event_fraction=open("event_fraction.txt","w")
rootFile=TFile('Output_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_new.root')
for cat in ['1l','minus1l','2l','0l']:
    for reg in ['1e1b','1e2b','1mu1b','1mu2b','1mu1e1b','1mu1e2b','2e1b','2e2b','2mu1b','2mu2b','2e2b','2e1b','2mu1b','2mu2b']:
        for metrec in ['MET','hadrecoil']:
            exec("h_reg_"+reg+"_"+metrec+"_"+cat+" = rootFile.Get('h_reg_"+reg+"_"+metrec+"_"+cat+"_')")
            exec("myHistos.append(h_reg_"+reg+"_"+metrec+"_"+cat+")")
            exec("myHistos_str.append('h_reg_"+reg+"_"+metrec+"_"+cat+"')")
    for sr in ['sr1','sr2']:
        exec("h_met_"+cat+"_"+sr+" = rootFile.Get('h_met_"+cat+"_"+sr+"_')")
        exec("myHistos.append(h_met_"+cat+"_"+sr+")")
        exec("myHistos_str.append('h_met_"+cat+"_"+sr+"')")
myHistos_tmp=myHistos
h_total=rootFile.Get('h_total')
htotal=CustomiseHistogram_(h_total, '', '# Events', ROOT.kRed, 1,'h_total')
print (htotal)
methist=[]
hadhist=[]
methist1b=[]
hadhist1b=[]
methist2b=[]
hadhist2b=[]
methist_str=[]
hadhist_str=[]
MET=False
HadRecoil=False
OnebMet=False
TwobMet=False
Onebhad=False
Twobhad=False
for hist in myHistos:
     if 'MET' in str(hist):
        MET=True
        if '1b' in str(hist):
            OnebMet=True
            methist1b.append(hist)
        if '2b' in str(hist):
            TwobMet=True
            methist2b.append(hist)
        methist.append(hist)
     if 'hadrecoil' in str(hist) or 'met' in str(hist):
        HadRecoil=True
        if '1b' in str(hist) or 'sr1' in str(hist):
            Onebhad=True
            hadhist1b.append(hist)
        if '2b' in str(hist) or 'sr2' in str(hist):
            Twobhad=True
            hadhist2b.append(hist)
        hadhist.append(hist)
for hist in myHistos_str:
    if 'MET' in hist:
        methist_str.append(hist)
    if 'hadrecoil' in hist or 'met' in hist:
        hadhist_str.append(hist)
titlehist={}
for shist,hist in zip(myHistos_str,myHistos):
    titlehist.update({str(hist) : shist})

if MET and OnebMet:
    titleX = "E_{T}^{miss} (GeV)"
    titleY = "# Events"
    # Set Canvas
    c1 = SetCanvas()
    for hist in methist1b:
        if '1e1b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kRed
        if '1mu1b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kBlue
        if '2e1b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kCyan
        if '2e1b' in str(hist) and 'minus1l' in str(hist):
            colour=ROOT.kCyan+2
        if '2mu1b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kGray
        if '2mu1b' in str(hist) and 'minus1l' in str(hist):
            colour=ROOT.kGray+2
        if '1mu1e1b' in str(hist) and 'MET_2l' in str(hist):
            colour=ROOT.kBlack
        if '1mu1e1b' in str(hist) and 'MET_minus1l' in str(hist):
            colour=ROOT.kGreen
        if hist.GetEntries()!=0 and OnebMet:
            h_int=CustomiseHistogram_(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            val = h_int/htotal
            event_fraction.write(titlehist[str(hist)]+":           "+str(h_int)+"           "+str(val)+"  \n")
            if '0l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            if '1l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 3,titlehist[str(hist)])
            if '2l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 5,titlehist[str(hist)])

            hist.Rebin(5)
            hist.GetXaxis().SetRangeUser(50, 1000)
            if hist=='h_reg_1e1b_MET_minus1l':
                drawHisto(hist)
            else:
                drawHisto(hist,"hist same")

    leg = CreateLegend(0.6, 0.9, 0.6, 0.9, "")
    for hist in methist1b:
        if hist.GetEntries()!=0 and OnebMet:
            leg.AddEntry(hist, '' , 'l')
    leg.Draw("same")

    txt = 'DM + Heavy Flavor'

    texcms = AddText(txt)
    texCat= AddTextCat("")

    texcms.Draw("same")
    texCat.Draw("same")

    c1.SetLogy()
    c1.Update()
    c1.SaveAs('RealMET_1b.pdf')
    c1.Close()
    print ('Done for 1b and MET')

if MET and TwobMet:
    titleX = "E_{T}^{miss} (GeV)"
    titleY = "# Events"
    # Set Canvas
    c2 = SetCanvas()
    for hist in methist2b:
        if '1e2b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kRed
        if '1mu2b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kBlue
        if '2e2b' in str(hist)  and '2l' in str(hist):
            colour=ROOT.kCyan
        if '2e2b' in str(hist)  and 'minus1l' in str(hist):
            colour=ROOT.kCyan+2
        if '2mu2b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kGray
        if '2mu2b' in str(hist) and 'minus1l' in str(hist):
            colour=ROOT.kGray+2
        if ('1mu1e2b' in str(hist)) and 'MET_2l' in str(hist):
            colour=ROOT.kBlack
        if ('1mu1e2b' in str(hist)) and 'MET_minus1l' in str(hist):
            colour=ROOT.kGreen
        if hist.GetEntries()!=0 and TwobMet:
            h_int=CustomiseHistogram_(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            val = h_int/htotal
            event_fraction.write(titlehist[str(hist)]+":           "+str(h_int)+"           "+str(val)+"  \n")

            if '0l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            if '1l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 3,titlehist[str(hist)])
            if '2l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 5,titlehist[str(hist)])
            hist.Rebin(5)
            hist.GetXaxis().SetRangeUser(50, 1000)
            if hist=='h_reg_1e2b_MET_1l':
                drawHisto(hist)
            else:
                drawHisto(hist,"hist same")

    leg = CreateLegend(0.6, 0.9, 0.6, 0.9, "")
    for hist in methist2b:
        if hist.GetEntries()!=0 and TwobMet:
            leg.AddEntry(hist, '' , 'l')
    leg.Draw("same")

    txt = 'DM + Heavy Flavor'

    texcms = AddText(txt)
    texCat= AddTextCat("")

    texcms.Draw("same")
    texCat.Draw("same")

    c2.SetLogy()
    c2.Update()
    c2.SaveAs('RealMET_2b.pdf')
    c2.Close()
    print ('Done for 2b and MET')

if HadRecoil and Onebhad:

    titleX = "Hadronic Recoil (GeV)"
    titleY = "# Events"
    # Set Canvas
    c1 = SetCanvas()
    for hist in hadhist1b:
        if '1e1b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kRed
        if '1mu1b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kBlue
        if '2e1b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kCyan
        if '2e1b' in str(hist) and '1l' in str(hist):
            colour=ROOT.kCyan-6
        if '2mu1b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kGray
        if '2mu1b' in str(hist) and '1l' in str(hist):
            colour=ROOT.kYellow-8
        if '1mu1e1b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kBlack
        if '1mu1e1b' in str(hist) and '1l' in str(hist):
            colour=ROOT.kMagenta

        if 'met' in str(hist) and 'sr1'  and 'minus1l' in str(hist) :
            colour=ROOT.kGreen
        if 'met' in str(hist)  and 'sr1' in str(hist) and '0l' in str(hist) :
            colour=ROOT.kOrange
        if 'met' in str(hist)  and 'sr1' in str(hist) and '1l' in str(hist) :
            colour=ROOT.kPink+9
        if 'met' in str(hist)  and 'sr1' in str(hist) and '2l' in str(hist) :
            colour=ROOT.kAzure-9

        if hist.GetEntries()!=0:
            h_int=CustomiseHistogram_(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            val = h_int/htotal
            event_fraction.write(titlehist[str(hist)]+":           "+str(h_int)+"           "+str(val)+"  \n")

            if '0l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            if '1l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 3,titlehist[str(hist)])
            if '2l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 5,titlehist[str(hist)])

            hist.Rebin(2)
            hist.GetXaxis().SetRangeUser(200, 1000)
            if str(hist)=='h_reg_1e1b_hadrecoil_1l':
                drawHisto(hist)
            else:
                drawHisto(hist,"hist same")

    leg = CreateLegend(0.6, 0.9, 0.6, 0.9, "")
    for hist in hadhist1b:
        if hist.GetEntries()!=0:
            leg.AddEntry(hist, '' , 'l')
    leg.Draw("same")

    txt = 'DM + Heavy Flavor'

    texcms = AddText(txt)
    texCat= AddTextCat("")

    texcms.Draw("same")
    texCat.Draw("same")


    c1.SetLogy()
    c1.Update()
    c1.SaveAs('HadRecoil_1b.pdf')
    c1.Close()
    print ('Done for 1b and HadRecoil')

if HadRecoil and Twobhad:

    titleX = "Hadronic Recoil (GeV)"
    titleY = "# Events"
    # Set Canvas
    c1 = SetCanvas()
    for hist in hadhist2b:
        if '1e2b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kRed
        if '1mu2b' in str(hist) and not '1mu1e' in str(hist):
            colour=ROOT.kBlue
        if '2e2b' in str(hist)  and '2l' in str(hist):
            colour=ROOT.kCyan
        if '2e2b' in str(hist)  and 'minus1l' in str(hist):
            colour=ROOT.kCyan+2
        if '2mu2b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kGray
        if '2mu2b' in str(hist) and 'minus1l' in str(hist):
            colour=ROOT.kYellow-8
        if '1mu1e2b' in str(hist) and '2l' in str(hist):
            colour=ROOT.kBlack
        if '1mu1e2b' in str(hist) and 'minus1l' in str(hist):
            colour=ROOT.kMagenta

        if 'met' in str(hist) and 'sr2' in str(hist)  and 'minus1l' in str(hist) :
            colour=ROOT.kGreen
        if 'met' in str(hist)  and 'sr2'in str(hist)  and '0l' in str(hist) :
            colour=ROOT.kOrange
        if 'met' in str(hist)  and 'sr2' in str(hist)  and '1l' in str(hist) :
            colour=ROOT.kPink+9
        if 'met' in str(hist)  and 'sr2'in str(hist) and '2l' in str(hist) :
            colour=ROOT.kAzure-9

        if hist.GetEntries()!=0:
            h_int=CustomiseHistogram_(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            val = h_int/htotal
            event_fraction.write(titlehist[str(hist)]+":           "+str(h_int)+"           "+str(val)+"  \n")

            if '0l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 1,titlehist[str(hist)])
            if '1l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 3,titlehist[str(hist)])
            if '2l' in str(hist):
                CustomiseHistogram(hist, titleX, titleY, colour, 5,titlehist[str(hist)])

            hist.Rebin(2)
            hist.GetXaxis().SetRangeUser(200, 1000)
            if str(hist)=='h_reg_1e2b_hadrecoil_1l':
                drawHisto(hist)
            else:
                drawHisto(hist,"hist same")

    leg = CreateLegend(0.6, 0.9, 0.6, 0.9, "")
    for hist in hadhist2b:
        if hist.GetEntries()!=0:
            leg.AddEntry(hist, '' , 'l')
    leg.Draw("same")

    txt = 'DM + Heavy Flavor'

    texcms = AddText(txt)
    texCat= AddTextCat("")

    texcms.Draw("same")
    texCat.Draw("same")


    c1.SetLogy()
    c1.Update()
    c1.SaveAs('HadRecoil_2b.pdf')
    c1.Close()
    print ('Done for HadRecoil')
