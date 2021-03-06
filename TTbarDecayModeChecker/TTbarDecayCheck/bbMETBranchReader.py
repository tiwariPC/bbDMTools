#!/usr/bin/env python
from ROOT import TFile, TTree, TH1F, TH1D, TH1, TCanvas, TChain,TGraphAsymmErrors, TMath, TH2D, TLorentzVector, TF1, AddressOf
import ROOT as ROOT
import os
import random
import sys, optparse
from array import array
import math
import AllQuantList

ROOT.gROOT.SetBatch(True)
from bbMETQuantities import *
#from PileUpWeights import PUWeight
pileup2016file = TFile('pileUPinfo2016.root')
pileup2016histo=pileup2016file.Get('hpileUPhist')

#Electron Trigger reweights
eleTrigReweightFile = TFile('scalefactors/electron_Trigger_eleTrig.root')
eleTrig_hEffEtaPt = eleTrigReweightFile.Get('hEffEtaPt')

#Electron Reconstruction efficiency. Scale factors for 80X
eleRecoSFsFile = TFile('scalefactors/electron_Reco_SFs_egammaEffi_txt_EGM2D.root')
eleRecoSF_EGamma_SF2D = eleRecoSFsFile.Get('EGamma_SF2D')

#Loose electron ID SFs
eleLooseIDSFsFile = TFile('scalefactors/electron_Loose_ID_SFs_egammaEffi_txt_EGM2D.root')
eleLooseIDSF_EGamma_SF2D = eleLooseIDSFsFile.Get('EGamma_SF2D')

#Tight electron ID SFs
phoTightIDSFsFile = TFile('scalefactors/photon_Tight_ID_SFs_egammaEffi_txt_EGM2D.root')
phoTightIDSF_EGamma_SF2D = phoTightIDSFsFile.Get('EGamma_SF2D')

#Loose photon ID SFs
phoLooseIDSFsFile = TFile('scalefactors/photon_Loose_ID_SFs_egammaEffi_txt_EGM2D.root')
phoLooseIDSF_EGamma_SF2D = phoLooseIDSFsFile.Get('EGamma_SF2D')

#Tight photon ID SFs
eleTightIDSFsFile = TFile('scalefactors/electron_Tight_ID_SFs_egammaEffi_txt_EGM2D.root')
eleTightIDSF_EGamma_SF2D = eleTightIDSFsFile.Get('EGamma_SF2D')

# Veto cut-based electron ID SFs
eleVetoCutBasedIDSFsFile = TFile('scalefactors/electron_Veto_cut-based_ID_SFs_egammaEffi_txt_EGM2D.root')
eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D = eleVetoCutBasedIDSFsFile.Get('EGamma_SF2D')

#Muon Trigger SFs
#BCDEF
muonTrigSFsRunBCDEFFile = TFile('scalefactors/muon_single_lepton_trigger_EfficienciesAndSF_RunBtoF.root')
muonTrigSFs_EfficienciesAndSF_RunBtoF = muonTrigSFsRunBCDEFFile.Get('IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio')
#GH
muonTrigSFsRunGHFile = TFile('scalefactors/muon_single_lepton_trigger_EfficienciesAndSF_Period4.root')
muonTrigSFs_EfficienciesAndSF_Period4 = muonTrigSFsRunBCDEFFile.Get('IsoMu24_OR_IsoTkMu24_PtEtaBins/abseta_pt_ratio')

#Muon ID SFs
#BCDEF
muonIDSFsBCDEFFile = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_BCDEF.root')
muonLooseIDSFs_EfficienciesAndSF_BCDEF = muonIDSFsBCDEFFile.Get('MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
muonTightIDSFs_EfficienciesAndSF_BCDEF = muonIDSFsBCDEFFile.Get('MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
#GH
muonIDSFsGHFile = TFile('scalefactors/muon_ID_SFs_EfficienciesAndSF_GH.root')
muonLooseIDSFs_EfficienciesAndSF_GH = muonIDSFsGHFile.Get('MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')
muonTightIDSFs_EfficienciesAndSF_GH = muonIDSFsGHFile.Get('MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio')

#Muon Iso SFs
#BCDEF
muonIsoSFsBCDEFFile = TFile('scalefactors/muon_Iso_SFs_EfficienciesAndSF_BCDEF.root')
muonLooseIsoSFs_EfficienciesAndSF_BCDEF = muonIsoSFsBCDEFFile.Get('LooseISO_LooseID_pt_eta/abseta_pt_ratio')
muonTightIsoSFs_EfficienciesAndSF_BCDEF = muonIsoSFsBCDEFFile.Get('TightISO_TightID_pt_eta/abseta_pt_ratio')
#GH
muonIsoSFsGHFile = TFile('scalefactors/muon_Iso_SFs_EfficienciesAndSF_GH.root')
muonLooseIsoSFs_EfficienciesAndSF_GH = muonIsoSFsGHFile.Get('LooseISO_LooseID_pt_eta/abseta_pt_ratio')
muonTightIsoSFs_EfficienciesAndSF_GH = muonIsoSFsGHFile.Get('TightISO_TightID_pt_eta/abseta_pt_ratio')

#Muon Tracking SFs
muonTrackingSFsFile = TFile('scalefactors/muon_Tracking_SFs_Tracking_EfficienciesAndSF_BCDEFGH.root')
muonTrackingSFs_EfficienciesAndSF_BCDEFGH = muonTrackingSFsFile.Get('ratio_eff_aeta_dr030e030_corr')


#MET Trigger reweights
metTrigEff_zmmfile = TFile('scalefactors/metTriggerEfficiency_zmm_recoil_monojet_TH1F.root')
metTrig_firstmethod = metTrigEff_zmmfile.Get('hden_monojet_recoil_clone_passed')

metTrigEff_secondfile = TFile('scalefactors/metTriggerEfficiency_recoil_monojet_TH1F.root')
metTrig_secondmethod = metTrigEff_secondfile.Get('hden_monojet_recoil_clone_passed')


ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cpp+')

#ROOT.gROOT.ProcessLine('.L TheaCorrection.cpp+')

######################################
## set up running mode of the code.
######################################

#ROOT.gROOT.ProcessLine('.L PileUpWeights.h')

#print "puweight = ",PUWEIGHT(10)
usage = "usage: %prog [options] arg1 arg2"
parser = optparse.OptionParser(usage)

## data will be true if -d is passed and will be false if -m is passed
parser.add_option("-i", "--inputfile",  dest="inputfile")
parser.add_option("-o", "--outputfile", dest="outputfile")
parser.add_option("-D", "--outputdir", dest="outputdir")

parser.add_option("-a", "--analyze", action="store_true",  dest="analyze")

parser.add_option("-e", "--efficiency", action="store_true",  dest="efficiency")
parser.add_option("-F", "--farmout", action="store_true",  dest="farmout")
parser.add_option("-t", "--table", action="store_true",  dest="table")
parser.add_option("-P", "--OtherPlots", action="store_true",  dest="OtherPlots")

parser.add_option("--csv", action="store_true",  dest="CSV")
parser.add_option("--deepcsv", action="store_true",  dest="DeepCSV")

parser.add_option("--se", action="store_true",  dest="SE")
parser.add_option("--met", action="store_true",  dest="MET")
parser.add_option("--sp", action="store_true",  dest="SP")

########################################################################################################################
########################## cut values########################################################################
########################################################################################################################

parser.add_option("--dbt", action="store_true",  dest="dbt")
parser.add_option( "--dbtcut", type=float,  dest="dbtcut")

parser.add_option("--theac", action="store_true",  dest="theac")

(options, args) = parser.parse_args()

if options.farmout==None:
    isfarmout = False
else:
    isfarmout = options.farmout

if options.CSV==None:
    options.CSV = False

if options.DeepCSV==None:
    options.DeepCSV = False

if options.SE==None:
    options.SE==False

if options.MET==None:
    options.MET==False

if options.SP==None:
    options.SP==False


if options.SE: print "Using SingleElectron dataset."
if options.SP: print "Using SinglePhoton dataset."
if options.MET: print "Using MET dataset."

#if not options.SE and not options.MET and not options.SP:
    #print "Please run using --se or --met or --sp. Exiting."
    #sys.exit()

if options.CSV: print "Using CSVv2 as b-tag discriminator."
if options.DeepCSV: print "Using DeepCSV as b-tag discriminator."

if not options.CSV and not options.DeepCSV:
    print "Please run using --csv or --deepcsv. Exiting."
    sys.exit()

applydPhicut=False

#print 'options = ',[options.inputfile]
inputfilename = options.inputfile
outputdir = options.outputdir

#print inputfilename
pathlist = inputfilename.split("/")
sizeoflist = len(pathlist)
#print ('sizeoflist = ',sizeoflist)
rootfile='tmphist'
rootfile = pathlist[sizeoflist-1]
textfile = rootfile+".txt"

#outputdir='bbMETSamples/'
if outputdir!='.': os.system('mkdir -p '+outputdir)

if options.outputfile is None or options.outputfile==rootfile:
    if not isfarmout:
        outputfilename = "/Output_"+rootfile
    else:
        outputfilename = "/Output_"+rootfile.split('.')[0]+".root"
else:
    outputfilename = "/"+options.outputfile

#if isfarmout:
outfilename = outputdir + outputfilename
#else:
#    outfilename = options.outputfile

print "Input:",options.inputfile, "; Output:", outfilename

skimmedTree = TChain("outTree")


#bbMET_tree = TTree( 'bbMET_tree', 'outputTree' )
#print isfarmout



def WhichSample(filename):
    samplename = 'all'
    if filename.find('WJets')>-1:
        samplename = 'WJETS'
    elif filename.find('ZJets')>-1 or filename.find('DYJets')>-1:
        samplename = 'ZJETS'
    elif filename.find('TT')>-1:
        samplename  = 'TT'
    else:
        samplename = 'all'
#    print samplename
    return samplename

def IsoMu20isUnPrescaled(filename):
    if filename.find('2016D')>-1 or filename.find('2016E')>-1 or filename.find('2016F')>-1 or filename.find('2016G')>-1 or filename.find('2016H')>-1:
        return False
    else:
        return True

def TheaCorrection(puppipt=200.0,  puppieta=0.0):
    puppisd_corrGEN      = TF1("puppisd_corrGEN","[0]+[1]*pow(x*[2],-[3])");
    puppisd_corrGEN.SetParameters(
        1.00626,
        -1.06161,
        0.07999,
        1.20454
        )
    puppisd_corrRECO_cen =  TF1("puppisd_corrRECO_cen","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)");
    puppisd_corrRECO_cen.SetParameters(
        1.05807,
        -5.91971e-05,
        2.296e-07,
        -1.98795e-10,
        6.67382e-14,
        -7.80604e-18
        )

    puppisd_corrRECO_for = TF1("puppisd_corrRECO_for","[0]+[1]*x+[2]*pow(x,2)+[3]*pow(x,3)+[4]*pow(x,4)+[5]*pow(x,5)");
    puppisd_corrRECO_for.SetParameters(
        1.26638,
        -0.000658496,
        9.73779e-07,
        -5.93843e-10,
        1.61619e-13,
        -1.6272e-17)

    genCorr  = 1.
    recoCorr = 1.
    totalWeight = 1.

    genCorr =  puppisd_corrGEN.Eval( puppipt )
    if ( abs(puppieta)  <= 1.3 ) :
        recoCorr = puppisd_corrRECO_cen.Eval( puppipt )
    elif( abs(puppieta) > 1.3 ) :
        recoCorr = puppisd_corrRECO_for.Eval( puppipt )

    totalWeight = genCorr * recoCorr
    return totalWeight

triglist=['HLT_PFMET170_','HLT_PFMET170_NoiseCleaned','HLT_PFMET170_JetIdCleaned_v','HLT_PFMET170_HBHECleaned_v','HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v','HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v','HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v','HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v','HLT_PFMET110_PFMHT110_','HLT_IsoMu24_v','HLT_IsoTkMu24_v','HLT_Ele27_WPTight_Gsf','HLT_IsoMu20','HLT_Ele27_WPLoose_Gsf','HLT_Photon165_HE10','HLT_Photon175']

#st_quantlist = triglist + ['st_lumiSection', 'st_eventId', 'st_pfMetCorrPt', 'st_pfMetCorrPhi', 'st_THINnJet', 'st_THINjetP4', 'st_THINjetCISVV2', 'st_THINjetHadronFlavor', 'st_THINjetNHadEF', 'st_THINjetCHadEF', 'st_THINjetNPV', 'st_AK4deepCSVnJet', 'st_AK4deepCSVjetP4', 'st_AK4deepCSVjetDeepCSV_b', 'st_AK4deepCSVjetHadronFlavor', 'st_AK4deepCSVjetNHadEF', 'st_AK4deepCSVjetCHadEF', 'st_AK4deepCSVjetNPV', 'st_nPho', 'st_phoP4', 'st_phoIsPassLoose', 'st_phoIsPassMedium', 'st_phoIsPassTight', 'st_nEle', 'st_eleP4', 'st_eleIsPassLoose', 'st_eleIsPassMedium', 'st_eleIsPassTight', 'st_nMu', 'st_muP4', 'st_isLooseMuon', 'st_isMediumMuon', 'st_isTightMuon', 'st_muChHadIso', 'st_muNeHadIso', 'st_muGamIso', 'st_muPUPt', 'st_HPSTau_n', 'st_HPSTau_4Momentum', 'st_isData', 'mcweight', 'st_pu_nTrueInt', 'st_pu_nPUVert', 'st_nGenPar', 'st_genParId', 'st_genMomParId', 'st_genParSt', 'st_genParP4', 'WenuRecoil', 'Wenumass', 'WenuPhi', 'WmunuRecoil', 'Wmunumass', 'WmunuPhi', 'ZeeRecoil', 'ZeeMass', 'ZeePhi', 'ZmumuRecoil', 'ZmumuMass', 'ZmumuPhi', 'TOPRecoil', 'TOPPhi', 'GammaRecoil', 'GammaPhi']

#def fileIsCorr(rootfile):
    #try:
        #tempTree = TChain("outTree")
        #tempTree.Add(rootfile)
        #N = tempTree.GetEntries()
        #for i in range(N):
            #tempTree.GetEntry(i)
            #for quant in st_quantlist:
                #print quant
                #tempTree.__getattr__(quant)
        #return False
    #except:
        #print rootfile+" is corrupt. Skipping."
        #return True

h_t = TH1F('h_t','h_t',2,0,2)
h_t_weight = TH1F('h_t_weight','h_t_weight',2,0,2)

samplename = 'all'
if isfarmout:
    infile = open(inputfilename)
    failcount=0
    for ifile in infile:
        try:
            f_tmp = TFile.Open(ifile.rstrip(),'READ')
            if f_tmp.IsZombie():            # or fileIsCorr(ifile.rstrip()):
                failcount += 1
                continue
            skimmedTree.Add(ifile.rstrip())
            h_tmp = f_tmp.Get('h_total')
            h_tmp_weight = f_tmp.Get('h_total_mcweight')
            h_t.Add(h_tmp)
            h_t_weight.Add(h_tmp_weight)
        except:
            failcount += 1
    if failcount>0: print "Could not read %d files. Skipping them." %failcount

if not isfarmout:
    skimmedTree.Add(inputfilename)
#    samplename = WhichSample(inputfilename)
    ## for histograms
    f_tmp = TFile.Open(inputfilename,'READ')
    h_tmp = f_tmp.Get('h_total')
    h_tmp_weight = f_tmp.Get('h_total_mcweight')
    h_t.Add(h_tmp)
    h_t_weight.Add(h_tmp_weight)

debug = False

try:
    samplepath = str(f_tmp.Get('samplepath').GetTitle())
    if not isfarmout: print "Original source file: " + samplepath
except:
#    samplepath=inputfilename
    samplepath='TT'
    print "WARNING: Looks like the input was skimmed with an older version of SkimTree. Using " + samplepath + " as sample path. Gen pT Reweighting may NOT work."

samplename = WhichSample(samplepath)
print "Dataset classified as: " + samplename
UnPrescaledIsoMu20 = IsoMu20isUnPrescaled(samplepath)
#print UnPrescaledIsoMu20
#print samplename
#print

def AnalyzeDataSet():
    ## Input rootfile name

    #rootfilename = inputfilename
    #print (rootfilename,inputfilename)
    #f = TFile(rootfilename,'READ')
    #skimmedTree = f.Get('tree/treeMaker')
    NEntries = skimmedTree.GetEntries()
    print 'NEntries = '+str(NEntries)
    npass = 0


    #print [rootfilename, NEntries]
    cutStatus={'preselection':NEntries}
    cutStatusSR1={'preselection':NEntries}
    cutStatusSR2={'preselection':NEntries}

    cutflownames=['trig','MET','dPhicond','njets','nbjets','jet1','jet2/3','nlep']
    for SRname in cutflownames:
        cutStatus[SRname] = 0

    cutflownamesSR1=['trig','MET','dPhicond','njets','nbjets','jet1','jet2','nlep']
    for SRname in cutflownamesSR1:
        cutStatusSR1[SRname] = 0

    cutflownamesSR2=['trig','MET','dPhicond','njets','nbjets','jet1','jet2','jet3','nlep']
    for SRname in cutflownamesSR2:
        cutStatusSR2[SRname] = 0

    #cutStatusSR1['njet+nBjet'] = 0
    #cutStatusSR1['lep'] = 0
    #cutStatusSR1['jet1'] = 0
    #cutStatusSR1['jet2'] = 0

    #cutStatusSR2['njet+nBjet'] = 0
    #cutStatusSR2['lep'] = 0
    #cutStatusSR2['jet1'] = 0
    #cutStatusSR2['jet2'] = 0
    #cutStatusSR2['jet3'] = 0

#    CRCutFlow['njet+nBjet']=0
#    CRCutFlow['jetcond']=0
#    CRCutFlow['nlepcond']=0
#    CRCutFlow['zJet']=0
#    CRCutFlow['zLep']=0
#    CRCutFlow['zMass']=0
#    CRCutFlow['zrecoil']=0
#    CRCutFlow['ZdPhi']=0


    CRcutnames=['datatrig','trig','recoil','realMET','mass','dPhicond','njets','nbjets','jetconds','nlep/npho','lepconds']
    regionnames=['2e1b','2mu1b','2e2b','2mu2b','1e1b','1mu1b','1e2b','1mu2b','1mu1e1b','1mu1e2b','1gamma1b','1gamma2b','QCD1b','QCD2b']
    for CRreg in regionnames:
        exec("CR"+CRreg+"CutFlow={'preselection':NEntries}")
        for cutname in CRcutnames:
            exec("CR"+CRreg+"CutFlow['"+cutname+"']=0")


    CRs=['ZCRSR1','ZCRSR2','WCRSR1','WCRSR2','TopCRSR1','TopCRSR2', 'GammaCRSR1','GammaCRSR2']

    CRStatus={'total':NEntries}
    for CRname in CRs:
        CRStatus[CRname]=0

    # ---CR Summary---
    regNames=['1#mu1b','1e1b','1#mu2b','1e2b','2#mu1b','2e1b','2#mu2b','2e2b','1#mu1e1b','1#mu1e2b']
    regNamesMu=['1#mu1b','1#mu2b','2#mu1b','2#mu2b','1#mu1e1b','1#mu1e2b']
    regNamesEle=['1e1b','1e2b','2e1b','2e2b']

    CRSummary={}
    for ireg in regNames:
        CRSummary[ireg]=0.

    CRSummaryMu={}
    for ireg in regNamesMu:
        CRSummaryMu[ireg]=0.

    CRSummaryEle={}
    for ireg in regNamesEle:
        CRSummaryEle[ireg]=0.

    #print outfilename
    allquantities = MonoHbbQuantities(outfilename)
    allquantities.defineHisto()


    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
    # BTag Scale Factor Initialisation
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

    othersys = ROOT.std.vector('string')()
    othersys.push_back('down')
    othersys.push_back('up')
    ## ThinJets
    if options.CSV:
        calib1 = ROOT.BTagCalibrationStandalone('csvv2', 'CSVv2_Moriond17_B_H.csv')
    if options.DeepCSV:
        calib1 = ROOT.BTagCalibrationStandalone('deepcsv', 'DeepCSV_Moriond17_B_H.csv')

    reader1 = ROOT.BTagCalibrationStandaloneReader( 0, "central", othersys)
    reader1.load(calib1, 0,  "comb" )
    reader1.load(calib1, 1,  "comb" )
    reader1.load(calib1, 2,  "incl" )

#    h_total = TH1F('h_total','h_total',2,0,2)
#    h_total_mcweight = TH1F('h_total_mcweight','h_total_mcweight',2,0,2)

    for ievent in range(NEntries):
    #for ievent in range(501):

        ##
        sf_resolved1 = []
        sf_resolved2 = []
        sf_resolved3 = []
        #print "event number = ",ievent
        skimmedTree.GetEntry(ievent)

        ## Get all relevant branches
#        if True:
        try:
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Extract branches
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
            run                        = skimmedTree.__getattr__('st_runId')
            lumi                       = skimmedTree.__getattr__('st_lumiSection')
            event                      = skimmedTree.__getattr__('st_eventId')

            #if event != 4126: continue
            #if lumi  != 42: continue
            if ievent%100==0: print (ievent)
            #trigName                   = skimmedTree.__getattr__('st_hlt_trigName')
            #trigResult                 = skimmedTree.__getattr__('st_hlt_trigResult')
            #filterName                 = skimmedTree.__getattr__('st_hlt_filterName')
            #filterResult               = skimmedTree.__getattr__('st_hlt_filterResult')

            pfMet                      = skimmedTree.__getattr__('st_pfMetCorrPt')
            pfMetPhi                   = skimmedTree.__getattr__('st_pfMetCorrPhi')
            pfMetJetResUp              = skimmedTree.__getattr__('st_pfMetUncJetResUp')
            pfMetJetResDown            = skimmedTree.__getattr__('st_pfMetUncJetResDown')
            pfMetJetEnUp               = skimmedTree.__getattr__('st_pfMetUncJetEnUp')
            pfMetJetEnDown             = skimmedTree.__getattr__('st_pfMetUncJetEnDown')

            nTHINJets                  = skimmedTree.__getattr__('st_THINnJet')
            thinjetP4                  = skimmedTree.__getattr__('st_THINjetP4')
            thinJetCSV                 = skimmedTree.__getattr__('st_THINjetCISVV2')
            #passThinJetLooseID         = skimmedTree.__getattr__('st_THINjetPassIDLoose')
            #passThinJetPUID            = skimmedTree.__getattr__('st_THINisPUJetID')
            THINjetHadronFlavor        = skimmedTree.__getattr__('st_THINjetHadronFlavor')
            thinjetNhadEF              = skimmedTree.__getattr__('st_THINjetNHadEF')
            thinjetChadEF              = skimmedTree.__getattr__('st_THINjetCHadEF')
            thinjetNPV                 = skimmedTree.__getattr__('st_THINjetNPV')
            thinjetCorrUnc             = skimmedTree.__getattr__('st_THINjetCorrUnc')

            try:
                thinjetCEmEF               = skimmedTree.__getattr__('st_THINjetCEmEF')
                thinjetPhoEF               = skimmedTree.__getattr__('st_THINjetPhoEF')
                thinjetEleEF               = skimmedTree.__getattr__('st_THINjetEleEF')
                thinjetMuoEF               = skimmedTree.__getattr__('st_THINjetMuoEF')

            except:
                nulljet=[-1. for i in range(nTHINJets)]
                thinjetCEmEF=nulljet
                thinjetPhoEF=nulljet
                thinjetEleEF=nulljet
                thinjetMuoEF=nulljet

            nTHINdeepCSVJets           = skimmedTree.__getattr__('st_AK4deepCSVnJet')
            thindeepCSVjetP4           = skimmedTree.__getattr__('st_AK4deepCSVjetP4')
            thinJetdeepCSV             = skimmedTree.__getattr__('st_AK4deepCSVjetDeepCSV_b')
            THINdeepCSVjetHadronFlavor = skimmedTree.__getattr__('st_AK4deepCSVjetHadronFlavor')
            thindeepCSVjetNhadEF       = skimmedTree.__getattr__('st_AK4deepCSVjetNHadEF')
            thindeepCSVjetChadEF       = skimmedTree.__getattr__('st_AK4deepCSVjetCHadEF')
            thindeepCSVjetNPV          = skimmedTree.__getattr__('st_AK4deepCSVjetNPV')
            thindeepCSVjetCorrUnc      = skimmedTree.__getattr__('st_AK4deepCSVjetCorrUnc')

            try:
                thindeepCSVjetCEmEF               = skimmedTree.__getattr__('st_AK4deepCSVjetCEmEF')
                thindeepCSVjetPhoEF               = skimmedTree.__getattr__('st_AK4deepCSVjetPhoEF')
                thindeepCSVjetEleEF               = skimmedTree.__getattr__('st_AK4deepCSVjetEleEF')
                thindeepCSVjetMuoEF               = skimmedTree.__getattr__('st_AK4deepCSVjetMuoEF')

            except:
                nulljet=[-1. for i in range(nTHINdeepCSVJets)]
                thindeepCSVjetCEmEF=nulljet
                thindeepCSVjetPhoEF=nulljet
                thindeepCSVjetEleEF=nulljet
                thindeepCSVjetMuoEF=nulljet

            nPho                       = skimmedTree.__getattr__('st_nPho')
            phoP4                      = skimmedTree.__getattr__('st_phoP4')
            phoIsPassLoose             = skimmedTree.__getattr__('st_phoIsPassLoose')
            phoIsPassMedium            = skimmedTree.__getattr__('st_phoIsPassMedium')
            phoIsPassTight             = skimmedTree.__getattr__('st_phoIsPassTight')

            nEle                       = skimmedTree.__getattr__('st_nEle')
            eleP4                      = skimmedTree.__getattr__('st_eleP4')
            eleIsPassLoose             = skimmedTree.__getattr__('st_eleIsPassLoose')
            eleIsPassMedium            = skimmedTree.__getattr__('st_eleIsPassMedium')
            eleIsPassTight             = skimmedTree.__getattr__('st_eleIsPassTight')

            nMu                        = skimmedTree.__getattr__('st_nMu')
            muP4                       = skimmedTree.__getattr__('st_muP4')
            isLooseMuon                = skimmedTree.__getattr__('st_isLooseMuon')
            isMediumMuon               = skimmedTree.__getattr__('st_isMediumMuon')
            isTightMuon                = skimmedTree.__getattr__('st_isTightMuon')
            muChHadIso                 = skimmedTree.__getattr__('st_muChHadIso')
            muNeHadIso                 = skimmedTree.__getattr__('st_muNeHadIso')
            muGamIso                   = skimmedTree.__getattr__('st_muGamIso')
            muPUPt                     = skimmedTree.__getattr__('st_muPUPt')

            nTau                       = skimmedTree.__getattr__('st_HPSTau_n')
            tauP4                      = skimmedTree.__getattr__('st_HPSTau_4Momentum')
            #isDecayModeFinding         = skimmedTree.__getattr__('st_disc_decayModeFinding')
            #passLooseTauIso            = skimmedTree.__getattr__('st_disc_byLooseIsolationMVA3oldDMwLT')
            try:
                disc_againstElectronLoose  = skimmedTree.__getattr__('st_disc_againstElectronLoose')
                disc_againstElectronMedium = skimmedTree.__getattr__('st_disc_againstElectronMedium')
                disc_againstElectronTight  = skimmedTree.__getattr__('st_disc_againstElectronTight')
                disc_againstMuonLoose      = skimmedTree.__getattr__('st_disc_againstMuonLoose')
                disc_againstMuonTight      = skimmedTree.__getattr__('st_disc_againstMuonTight')
            except:
                if ievent==0: print "Tau discriminators not found. Skipping tau veto."
                disc_againstElectronLoose=None

            isData                     = skimmedTree.__getattr__('st_isData')
            mcWeight                   = skimmedTree.__getattr__('mcweight')
            pu_nTrueInt                = int(skimmedTree.__getattr__('st_pu_nTrueInt'))
            pu_nPUVert                 = int(skimmedTree.__getattr__('st_pu_nPUVert'))

            nGenPar                    = skimmedTree.__getattr__('st_nGenPar')
            genParId                   = skimmedTree.__getattr__('st_genParId')
            genMomParId                = skimmedTree.__getattr__('st_genMomParId')
            genParSt                   = skimmedTree.__getattr__('st_genParSt')
            genParP4                   = skimmedTree.__getattr__('st_genParP4')

            lepCategoryVec                = skimmedTree.__getattr__('st_LepCategory')
            lepCategory = lepCategoryVec[0]
            print lepCategory

            WenuRecoil                 = skimmedTree.__getattr__('WenuRecoil')
            Wenumass                   = skimmedTree.__getattr__('Wenumass')
            WenuPhi                    = skimmedTree.__getattr__('WenuPhi')
            WmunuRecoil                = skimmedTree.__getattr__('WmunuRecoil')
            Wmunumass                  = skimmedTree.__getattr__('Wmunumass')
            WmunuPhi                   = skimmedTree.__getattr__('WmunuPhi')

            ZeeRecoil                  = skimmedTree.__getattr__('ZeeRecoil')
            ZeeMass                    = skimmedTree.__getattr__('ZeeMass')
            ZeePhi                     = skimmedTree.__getattr__('ZeePhi')
            ZmumuRecoil                = skimmedTree.__getattr__('ZmumuRecoil')
            ZmumuMass                  = skimmedTree.__getattr__('ZmumuMass')
            ZmumuPhi                   = skimmedTree.__getattr__('ZmumuPhi')
            TOPRecoil                  = skimmedTree.__getattr__('TOPRecoil')
            TOPPhi                     = skimmedTree.__getattr__('TOPPhi')
            GammaRecoil                = skimmedTree.__getattr__('GammaRecoil')
            GammaPhi                   = skimmedTree.__getattr__('GammaPhi')

            for trig in triglist:
                exec(trig+" = skimmedTree.__getattr__('st_"+trig+"')")

        except Exception as e:
#        else:
            print e
            print "Corrupt file detected! Skipping 1 event."
            continue

        ##Define region wise triggers

        if isData:
            SRtrigstatus = HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v or HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v or HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v or HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v or HLT_PFMET170_
            MuCRtrigstatus = ((UnPrescaledIsoMu20 and HLT_IsoMu20) or HLT_IsoMu24_v or HLT_IsoTkMu24_v)
            EleCRtrigstatus = (HLT_Ele27_WPLoose_Gsf or HLT_Ele27_WPTight_Gsf)
            PhotonCRtrigstatus = (HLT_Photon165_HE10 or HLT_Photon175)

        else:
            SRtrigstatus = True
            MuCRtrigstatus = True
            EleCRtrigstatus = True
            PhotonCRtrigstatus = True


#        try:


#        HLT_IsoMu24                = skimmedTree.__getattr__('st_HLT_IsoMu20')     #Depreciated
#        HLT_Ele27_WPLoose_Gsf      = skimmedTree.__getattr__('st_HLT_Ele27_WPLoose_Gsf')


#        trig1 = CheckFilter(trigName, trigResult, 'HLT_PFMET170_') # added from  monojet
#        trig2 = CheckFilter(trigName, trigResult, 'HLT_PFMET170_NoiseCleaned')
#        trig3 = CheckFilter(trigName, trigResult, 'HLT_PFMET170_JetIdCleaned_v')
#        trig4 = CheckFilter(trigName, trigResult, 'HLT_PFMET170_HBHECleaned_v')
#        trig5 = CheckFilter(trigName, trigResult, 'HLT_PFMETNoMu90_PFMHTNoMu90_IDTight_v')
#        trig6 = CheckFilter(trigName, trigResult, 'HLT_PFMETNoMu100_PFMHTNoMu100_IDTight_v') #added from  tt+DM all hadronic analysis
#        trig7 = CheckFilter(trigName, trigResult, 'HLT_PFMETNoMu110_PFMHTNoMu110_IDTight_v')
#        trig8 = CheckFilter(trigName, trigResult, 'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v')
#        trig9 = CheckFilter(trigName, trigResult, 'HLT_PFMET110_PFMHT110_')
#        trig10 = CheckFilter(trigName, trigResult, 'HLT_IsoMu24_v') #added from tt+DM all hadronic analysis
#        trig11 = CheckFilter(trigName, trigResult, 'HLT_IsoTkMu24_v') #added from tt+DM all hadronic analysis
#        trig12 = CheckFilter(trigName, trigResult, 'HLT_Ele27_WPTight_Gsf') #added from Siew Yan slides
##        trig13 = CheckFilter(trigName, trigResult, 'HLT_IsoMu20')   #Added from AN CR
#        trig13 = CheckFilter(trigName, trigResult, 'HLT_IsoMu20')    #Added from AN CR 2015
#        trig14 = CheckFilter(trigName, trigResult, 'HLT_Ele27_WPLoose_Gsf')   #Added from AN CR

#        HLT_IsoMu24=trig10
#        HLT_IsoMu20=trig13
#        HLT_Ele27_WPLoose_Gsf=trig14

#        print MET_trig, SE_trig


#        #**************************** REMEMBER TO CHANGE DEPENDING ON THE DATASET YOU ARE USING ********************************
#        #==========================================================================
#        #
#        whichDataset = False

#        if options.MET:
#            whichDataset = MET_trig   # For signal and mu regions with MET dataset
#        if options.SE:
#            whichDataset = SE_trig  # For electron regions with SE dataset
#        if options.SP:
#            whichDataset = SP_trig  # For photon regions with SP dataset

#        #if not whichDataset: continue


#        #============================ CAUTION =====================================
#        #**************************************************************************


        jetSR1Info           = []
        jetSR2Info           = []
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # MC Weights ----------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        mcweight = 0.0
        if isData==1:   mcweight =  1.0
        if not isData :
            if mcWeight<0:  mcweight = -1.0
            if mcWeight>0:  mcweight =  1.0


               # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## PFMET Selection
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        pfmetstatus = ( pfMet > 200.0 )
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ##Calculate Muon Relative PF isolation:
        MuIso = [((muChHadIso[imu]+ max(0., muNeHadIso[imu] + muGamIso[imu] - 0.5*muPUPt[imu]))/muP4[imu].Pt()) for imu in range(nMu)]

         # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#        print (HLT_IsoMu24,HLT_Ele27_WPLoose_Gsf)

        myEles=[]
        myEleLooseID=[]
        myEleTightID=[]
        for iele in range(nEle):
            if eleP4[iele].Pt() < 10 : continue
            if abs(eleP4[iele].Eta()) >2.5: continue
            #if not bool(eleIsPassMedium[iele]): continue    ##   Temporary test

            myEles.append(eleP4[iele])
            myEleLooseID.append(eleIsPassLoose[iele])
            #myEleLooseID.append(eleIsPassMedium[iele]) ##   Temporary test
            myEleTightID.append(eleIsPassTight[iele])

        myMuos = []
        myMuLooseID=[]
        myMuTightID=[]
        myMuIso=[]
        for imu in range(nMu):
            if muP4[imu].Pt()<10 : continue
            if abs(muP4[imu].Eta()) > 2.4  : continue

            #for iele in myEles:
                #if DeltaR(iele,muP4[imu]) < 0.4: print DeltaR(iele,muP4[imu])
#            #---Fake muon cleaner----
#            isClean=True
#            for iele in myEles[:]:
#                el_mu_dR=math.sqrt(  (  iele.Eta()-muP4[imu].Eta() )**2  + (  DeltaPhi(iele.Phi(),muP4[imu].Phi()) )**2 )
#                if el_mu_dR < 0.4:
#                    isClean=False
##                    myEles.remove(iele)     #Removes correspoding electron as well
#                    break
#            if not isClean: continue
#            ##---
            myMuos.append(muP4[imu])
            myMuLooseID.append(isLooseMuon[imu])
            myMuTightID.append(isTightMuon[imu])
            myMuIso.append(MuIso[imu])


#        myTaus=[]
        nTausDRbased=0
        myTausTightElectron=[]
        myTausTightMuon=[]
        myTausTightEleMu=[]
        myTausLooseEleMu=[]
        for itau in range(nTau):
            if tauP4[itau].Pt()<18. : continue
            if abs(tauP4[itau].Eta())>2.3 : continue

            if disc_againstElectronLoose!=None: # and len(disc_againstElectronLoose)==nTau:
                if disc_againstElectronTight[itau] and disc_againstMuonLoose[itau]:
                    myTausTightElectron.append(tauP4[itau])
                if disc_againstMuonTight[itau] and disc_againstElectronLoose[itau]:
                    myTausTightMuon.append(tauP4[itau])
                if disc_againstMuonTight[itau] and disc_againstElectronTight[itau]:
                    myTausTightEleMu.append(tauP4[itau])
                if disc_againstMuonLoose[itau] and disc_againstElectronLoose[itau]:
                    myTausLooseEleMu.append(tauP4[itau])

            #---Fake tau cleaner----
            isClean=True
            for iele in myEles[:]:
                lep_tau_dR=DeltaR(iele,tauP4[itau])    # math.sqrt(  (  iele.Eta()-tauP4[itau].Eta() )**2  + (  DeltaPhi(iele.Phi(),tauP4[itau].Phi()) )**2 )
                if lep_tau_dR < 0.4:
                    isClean=False
#                    myEles.remove(iele)     #Removes correspoding electron as well
                    break
            for imu in myMuos[:]:
                lep_tau_dR=DeltaR(imu,tauP4[itau])          #math.sqrt(  (  imu.Eta()-tauP4[itau].Eta() )**2  + (  DeltaPhi(imu.Phi(),tauP4[itau].Phi()) )**2 )
                if lep_tau_dR < 0.4:
                    isClean=False
#                    myMuos.remove(imu)      #Removes correspoding muon as well
                    break
#            if not isClean: continue
            if isClean: nTausDRbased+=1
            ##---
#            myTaus.append(tauP4[itau])

        #--------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Jet Selection
        ## Also segregate CSV or DeepCSV collection of jets in this step itself

        CSVMWP=0.8484
        deepCSVMWP=0.6324

        mybjets=[]
        myJetCSV=[]
        myJetP4=[]
        myJetHadronFlavor=[]
        myJetNhadEF=[]
        myJetChadEF=[]
        myJetCorrUnc=[]
        myJetCEmEF=[]
        myJetPhoEF=[]
        myJetEleEF=[]
        myJetMuoEF=[]

        if options.CSV:

            for nb in range(nTHINJets):

            #---Fake jet cleaner, wrt electrons and muons----
                isClean=True
                for iele in myEles[:]:
                    if DeltaR(iele,thinjetP4[nb]) < 0.4:
                        isClean=False
                        break
                for imu in myMuos[:]:
                    if DeltaR(imu,thinjetP4[nb]) < 0.4:
                        isClean=False
                        break


                        #for itau in tauP4:
                            #if DeltaR(itau,iele) < 0.4:
                                #isClean=False
                                #break
                        #else:
                            #myEles.remove(iele)

                if not isClean: continue
            #---

                myJetP4.append(thinjetP4[nb])
                myJetCSV.append(thinJetCSV[nb])
                myJetHadronFlavor.append(THINjetHadronFlavor[nb])
                myJetNhadEF.append(thinjetNhadEF[nb])
                myJetChadEF.append(thinjetChadEF[nb])

                myJetCorrUnc.append(thinjetCorrUnc[nb])
                myJetCEmEF.append(thinjetCEmEF[nb])
                myJetPhoEF.append(thinjetPhoEF[nb])
                myJetEleEF.append(thinjetEleEF[nb])
                myJetMuoEF.append(thinjetMuoEF[nb])

                if thinJetCSV[nb] > CSVMWP and abs(thinjetP4[nb].Eta())<2.4:
                    mybjets.append(nb)

            myJetNPV=thinjetNPV
            nUncleanJets=nTHINJets

        if options.DeepCSV:
            for nb in range(nTHINdeepCSVJets):

            #---Fake jet cleaner, wrt electrons and muons----
                isClean=True

                for iele in myEles:
                    if DeltaR(iele,thindeepCSVjetP4[nb]) < 0.4:
                        isClean=False
                        break
                for imu in myMuos:
                    if DeltaR(imu,thindeepCSVjetP4[nb]) < 0.4:
                        isClean=False
                        break


                if not isClean: continue
            #---

                myJetP4.append(thindeepCSVjetP4[nb])
                myJetCSV.append(thinJetdeepCSV[nb])
                myJetHadronFlavor.append(THINdeepCSVjetHadronFlavor[nb])
                myJetNhadEF.append(thindeepCSVjetNhadEF[nb])
                myJetChadEF.append(thindeepCSVjetChadEF[nb])

                myJetCorrUnc.append(thindeepCSVjetCorrUnc[nb])

                if ievent==0: print "Jet Energy fractions are not saved in DeepCSV collection. Saving default -1 for these."
                myJetCEmEF.append(thindeepCSVjetCEmEF[nb])
                myJetPhoEF.append(thindeepCSVjetPhoEF[nb])
                myJetEleEF.append(thindeepCSVjetEleEF[nb])
                myJetMuoEF.append(thindeepCSVjetMuoEF[nb])

                if thinJetdeepCSV[nb] > deepCSVMWP and abs(thindeepCSVjetP4[nb].Eta())<2.4:
                    mybjets.append(nb)

            myJetNPV=thindeepCSVjetNPV
            nUncleanJets=nTHINdeepCSVJets

        myPhos=[]
        myPhoLooseID=[]
        myPhoTightID=[]
        for ipho in range(nPho):
            if phoP4[ipho].Pt() < 175 : continue
            #---Fake Pho cleaner----
            isClean=True
            for ijet in myJetP4[:]:
                pho_jet_dR=DeltaR(ijet,phoP4[ipho])    # math.sqrt(  (  ijet.Eta()-phoP4[ipho].Eta() )**2  + (  DeltaPhi(ijet.Phi(),phoP4[ipho].Phi()) )**2 )
                if pho_jet_dR < 0.4:
                    isClean=False
                    break
            for iele in myEles[:]:
                lep_pho_dR=DeltaR(iele,phoP4[ipho])
                if lep_pho_dR < 0.4:
                    isClean=False
                    break
            if not isClean: continue
            myPhos.append(phoP4[ipho])
            myPhoLooseID.append(phoIsPassLoose[ipho])
            myPhoTightID.append(phoIsPassTight[ipho])



        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

        nUncleanEle=nEle
        nUncleanMu=nMu
        nUncleanTau=nTau

        nPho=len(myPhos)
        nEle=len(myEles)
        nMu=len(myMuos)
#        nTau=len(myTaus)

        nTauTightElectron=len(myTausTightElectron)
        nTauTightMuon=len(myTausTightMuon)
        nTauTightEleMu=len(myTausTightEleMu)
        nTauLooseEleMu=len(myTausLooseEleMu)
        nTau=nTauLooseEleMu

#        print "Unclean,dR-based,Loose,ETight,MTight,EMTight:",nUncleanTau,nTausDRbased,nTauLooseEleMu,nTauTightElectron,nTauTightMuon, nTauTightEleMu

        nBjets=len(mybjets)
        nJets=len(myJetCSV)
 #----------------------------------------------------------------------------------------------------------------------------------------------------------------
 #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Sort jets

        if nJets==0: continue

        alljetPT=[jet.Pt() for jet in myJetP4]
        jetindex=[i for i in range(len(alljetPT))]

        sortedjets=[jet for pt,jet in sorted(zip(alljetPT,myJetP4), reverse=True)]      # This gives a list of jets with their pTs in descending order
        sortedindex=[jetindex for pt,jetindex in sorted(zip(alljetPT,jetindex), reverse=True)]     # Indices of jets in myJetP4 in decscending order of jetPT

        j1=sortedjets[0]
        if nJets>1: j2=sortedjets[1]
        if nJets>2: j3=sortedjets[2]

        ifirstjet=sortedindex[0]
        if nJets>1: isecondjet=sortedindex[1]
        if nJets>2: ithirdjet=sortedindex[2]

        min_dPhi_jet_MET = min(   [  DeltaPhi(jt.Phi(),pfMetPhi) for jt in myJetP4]   )
#        print alljetPT
#        print [jet.Pt() for jet in sortedjets]
#        print sortedindex
#        print

        ##
# --------------------------------------------------------------------------------------------------------------------------------------------------------

        allquantlist=AllQuantList.getAll()

        for quant in allquantlist:
            exec("allquantities."+quant+" = None")
# --------------------------------------------------------------------------------------------------------------------------------------------------------


        # SR start

        ###
        #********
        #Part of data is blinded
        #********
        if isData:
            if ievent%20==0:
                keepevent=True
            else:
                keepevent=False
        else:
            keepevent=True
        #********************              REMEMBER TO UNBLIND AT SOME POINT!

        writeSR1=False
        writeSR2=False
        isZeeCR1=False
        isZeeCR2=False
        isZmumuCR1=False
        isZmumuCR2=False
        isWenuCR1=False
        isWenuCR2=False
        isWmunuCR1=False
        isWmunuCR2=False
        isTopCR1=False
        isTopCR2=False
        isGammaCR1=False
        isGammaCR2=False



        SR1njetcond=False
        SR2njetcond=False
        SR1jetcond=False
        SR2jetcond=False


        if nEle+nMu+nTauLooseEleMu==0:
            SRlepcond=True
        else:
            SRlepcond=False

        ## for SR1
         # 1 or 2 jets and 1 btagged

        Histos2D=AllQuantList.getHistos2D()
        for quant in Histos2D:
            exec("allquantities."+quant+" = None")

        if (nJets == 1 or nJets == 2) and pfmetstatus and SRlepcond and SRtrigstatus:
            #===CSVs before any selection===
            preselquantlist=AllQuantList.getPresel()
            for quant in preselquantlist:
                exec("allquantities."+quant+" = None")

            if options.CSV:
                allquantities.presel_jet1_csv_sr1=myJetCSV[ifirstjet]
                if nJets>1: allquantities.presel_jet2_csv_sr1=myJetCSV[isecondjet]
            if options.DeepCSV:
                allquantities.presel_jet1_deepcsv_sr1=myJetCSV[ifirstjet]
                if nJets>1: allquantities.presel_jet2_deepcsv_sr1=myJetCSV[isecondjet]

            allquantities.presel_jet1_chf_sr1=myJetChadEF[ifirstjet]
            allquantities.presel_jet1_nhf_sr1=myJetNhadEF[ifirstjet]
            allquantities.FillPreSel()



            if options.CSV:
                allquantities.csv_vs_dPhi_sr1 = [min_dPhi_jet_MET,myJetCSV[ifirstjet]]
            if options.DeepCSV:
                allquantities.deepcsv_vs_dPhi_sr1 = [min_dPhi_jet_MET,myJetCSV[ifirstjet]]
            #===
        if (nJets == 1 or nJets == 2):
            SR1jetcond=True
        if (nJets == 1 or nJets == 2) and nBjets==1:
            SR1njetcond=True

        SR1_Cut1_nJets          =   nJets == 1 or nJets == 2
        SR1_Cut2_nBjets         =   nBjets==1
        SR1_Cut3_trigstatus     =   SRtrigstatus
        SR1_Cut4_jet1           =   j1.Pt() > 50.0 and myJetNhadEF[ifirstjet] < 0.8 and myJetChadEF[ifirstjet] > 0.1
        if nJets>1:
            SR1_Cut5_jet2       =   j2.Pt() > 30.0
        else:
            SR1_Cut5_jet2       =   True
        SR1_Cut6_dPhi_jet_MET   =   min_dPhi_jet_MET > 0.5
        SR1_Cut7_nLep           =   nEle+nMu+nTauLooseEleMu == 0
        SR1_Cut8_pfMET          =   pfmetstatus

        if SR1_Cut1_nJets and SR1_Cut2_nBjets and SR1_Cut3_trigstatus and SR1_Cut4_jet1 and SR1_Cut5_jet2 and SR1_Cut7_nLep and SR1_Cut8_pfMET and keepevent:
            allquantities.dPhi_leadJET_sr1=DeltaPhi(j1.Phi(),pfMetPhi)
            if nJets>1:
                allquantities.dPhi_lastJet_sr1=DeltaPhi(j2.Phi(),pfMetPhi)

        if SR1_Cut1_nJets and SR1_Cut2_nBjets and SR1_Cut3_trigstatus and SR1_Cut4_jet1 and SR1_Cut5_jet2 and SR1_Cut6_dPhi_jet_MET and SR1_Cut7_nLep and SR1_Cut8_pfMET and keepevent:
            allquantities.jet1_pT_sr1     = j1.Pt()
            allquantities.jet1_eta_sr1    = j1.Eta()
            allquantities.jet1_phi_sr1    = j1.Phi()
            if options.CSV:
               allquantities.jet1_csv_sr1       = myJetCSV[ifirstjet]
            if options.DeepCSV:
               allquantities.jet1_deepcsv_sr1   = myJetCSV[ifirstjet]

            if nJets>1:
                allquantities.jet2_pT_sr1     = j2.Pt()
                allquantities.jet2_eta_sr1    = j2.Eta()
                allquantities.jet2_phi_sr1    = j2.Phi()
                if options.CSV:
                    allquantities.jet2_csv_sr1      = myJetCSV[isecondjet]
                if options.DeepCSV:
                    allquantities.jet2_deepcsv_sr1  = myJetCSV[isecondjet]

            allquantities.min_dPhi_sr1    = min_dPhi_jet_MET
            allquantities.met_sr1         = pfMet
            allquantities.jet1_nhf_sr1    = myJetNhadEF[ifirstjet]
            allquantities.jet1_chf_sr1    = myJetChadEF[ifirstjet]
            allquantities.lep_syst_sr1_up = pfMet
            allquantities.lep_syst_sr1_down = pfMet
            allquantities.btag_syst_sr1_up = pfMet
            allquantities.btag_syst_sr1_down = pfMet
            allquantities.metTrig_syst_sr1_up = pfMet
            allquantities.metTrig_syst_sr1_down = pfMet
            allquantities.ewkZ_syst_sr1_up = pfMet
            allquantities.ewkZ_syst_sr1_down = pfMet
            allquantities.ewkW_syst_sr1_up = pfMet
            allquantities.ewkW_syst_sr1_down = pfMet
            allquantities.ewkTop_syst_sr1_up = pfMet
            allquantities.ewkTop_syst_sr1_down = pfMet
            allquantities.pho_syst_sr1_up = pfMet
            allquantities.pho_syst_sr1_down = pfMet
            allquantities.jec_syst_sr1_up = pfMetJetResUp[0]
            allquantities.jec_syst_sr1_down = pfMetJetResDown[0]
            allquantities.jer_syst_sr1_up = pfMetJetEnUp[0]
            allquantities.jer_syst_sr1_down = pfMetJetEnDown[0]
            if lepCategory==0:
                allquantities.met_0l_sr1=pfMet
            if lepCategory==1:
                allquantities.met_1l_sr1=pfMet
            if lepCategory==2:
                allquantities.met_2l_sr1=pfMet
            if lepCategory==-1:
                allquantities.met_minus1l_sr1=pfMet
            writeSR1=True

     ## for SR2
        # 3 jets and 2 btagged

        if (nJets == 2 or nJets == 3) and pfmetstatus and SRlepcond and SRtrigstatus:
            #===CSVs before any selection===
            preselquantlist=AllQuantList.getPresel()
            for quant in preselquantlist:
                exec("allquantities."+quant+" = None")

            if options.CSV:
                allquantities.presel_jet1_csv_sr2=myJetCSV[ifirstjet]
                allquantities.presel_jet2_csv_sr2=myJetCSV[isecondjet]
                if nJets>2: allquantities.presel_jet3_csv_sr2=myJetCSV[ithirdjet]

            if options.DeepCSV:
                allquantities.presel_jet1_deepcsv_sr2=myJetCSV[ifirstjet]
                allquantities.presel_jet2_deepcsv_sr2=myJetCSV[isecondjet]
                if nJets>2: allquantities.presel_jet3_deepcsv_sr2=myJetCSV[ithirdjet]

            allquantities.presel_jet1_chf_sr2=myJetChadEF[ifirstjet]
            allquantities.presel_jet1_nhf_sr2=myJetNhadEF[ifirstjet]
            allquantities.FillPreSel()


            #===
            if options.CSV:
                csv_ = min(myJetCSV[ifirstjet],myJetCSV[isecondjet])
                allquantities.csv_vs_dPhi_sr2 = [min_dPhi_jet_MET,csv_]

            if options.DeepCSV:
                deepcsv_ = min(myJetCSV[ifirstjet],myJetCSV[isecondjet])
                allquantities.deepcsv_vs_dPhi_sr2 = [min_dPhi_jet_MET,deepcsv_]

        if (nJets == 2 or nJets == 3):
            SR2jetcond=True

        if (nJets == 2 or nJets == 3) and nBjets==2:
            SR2njetcond=True

        SR2_Cut1_nJets          =   nJets == 2 or nJets == 3
        SR2_Cut2_nBjets         =   nBjets==2
        SR2_Cut3_trigstatus     =   SRtrigstatus
        SR2_Cut4_jet1           =   j1.Pt() > 50.0 and myJetNhadEF[ifirstjet] < 0.8 and myJetChadEF[ifirstjet] > 0.1
        if nJets>1:
            SR2_Cut5_jet2           =   j2.Pt() > 50.0
        else:
            SR2_Cut5_jet2           =   False
        if nJets>2:
            SR2_Cut6_jet3       =   j3.Pt() > 30.0
        else:
            SR2_Cut6_jet3       =   True
        SR2_Cut7_dPhi_jet_MET   =   min_dPhi_jet_MET > 0.5
        SR2_Cut8_nLep           =   nEle+nMu+nTauLooseEleMu == 0
        SR2_Cut9_pfMET          =   pfmetstatus

        if SR2_Cut1_nJets and SR2_Cut2_nBjets and SR2_Cut3_trigstatus and SR2_Cut4_jet1 and SR2_Cut5_jet2 and SR2_Cut6_jet3 and SR2_Cut8_nLep and SR2_Cut9_pfMET and keepevent:
            allquantities.dPhi_leadJET_sr2=DeltaPhi(j1.Phi(),pfMetPhi)
            if nJets>2:
                allquantities.dPhi_lastJet_sr2=DeltaPhi(j3.Phi(),pfMetPhi)
            else:
                allquantities.dPhi_lastJet_sr2=DeltaPhi(j2.Phi(),pfMetPhi)

        if SR2_Cut1_nJets and SR2_Cut2_nBjets and SR2_Cut3_trigstatus and SR2_Cut4_jet1 and SR2_Cut5_jet2 and SR2_Cut6_jet3 and SR2_Cut7_dPhi_jet_MET and SR2_Cut8_nLep and SR2_Cut9_pfMET and keepevent:
            allquantities.jet1_pT_sr2     = j1.Pt()
            allquantities.jet1_eta_sr2    = j1.Eta()
            allquantities.jet1_phi_sr2    = j1.Phi()
            if options.CSV:
               allquantities.jet1_csv_sr2       = myJetCSV[ifirstjet]
            if options.DeepCSV:
               allquantities.jet1_deepcsv_sr2   = myJetCSV[ifirstjet]


            allquantities.jet2_pT_sr2     = j2.Pt()
            allquantities.jet2_eta_sr2    = j2.Eta()
            allquantities.jet2_phi_sr2    = j2.Phi()
            if options.CSV:
                allquantities.jet2_csv_sr2      = myJetCSV[isecondjet]
            if options.DeepCSV:
                allquantities.jet2_deepcsv_sr2  = myJetCSV[isecondjet]

            if nJets>2:
                allquantities.jet3_pT_sr2     = j3.Pt()
                allquantities.jet3_eta_sr2    = j3.Eta()
                allquantities.jet3_phi_sr2    = j3.Phi()
                if options.CSV:
                    allquantities.jet3_csv_sr2       = myJetCSV[ithirdjet]
                if options.DeepCSV:
                    allquantities.jet3_deepcsv_sr2   = myJetCSV[ithirdjet]

            allquantities.min_dPhi_sr2    = min_dPhi_jet_MET
            allquantities.met_sr2         = pfMet
            allquantities.jet1_nhf_sr2    = myJetNhadEF[ifirstjet]
            allquantities.jet1_chf_sr2    = myJetChadEF[ifirstjet]
            allquantities.lep_syst_sr2_up = pfMet
            allquantities.lep_syst_sr2_down = pfMet
            allquantities.btag_syst_sr2_up = pfMet
            allquantities.btag_syst_sr2_down = pfMet
            allquantities.metTrig_syst_sr2_up = pfMet
            allquantities.metTrig_syst_sr2_down = pfMet
            allquantities.ewkZ_syst_sr2_up = pfMet
            allquantities.ewkZ_syst_sr2_down = pfMet
            allquantities.ewkW_syst_sr2_up = pfMet
            allquantities.ewkW_syst_sr2_down = pfMet
            allquantities.ewkTop_syst_sr2_up = pfMet
            allquantities.ewkTop_syst_sr2_down = pfMet
            allquantities.pho_syst_sr2_up = pfMet
            allquantities.pho_syst_sr2_down = pfMet
            allquantities.jec_syst_sr2_up = pfMetJetResUp[0]
            allquantities.jec_syst_sr2_down = pfMetJetResDown[0]
            allquantities.jer_syst_sr2_up = pfMetJetEnUp[0]
            allquantities.jer_syst_sr2_down = pfMetJetEnDown[0]
            if lepCategory==0:
                allquantities.met_0l_sr2=pfMet
            if lepCategory==1:
                allquantities.met_1l_sr2=pfMet
            if lepCategory==2:
                allquantities.met_2l_sr2=pfMet
            if lepCategory==-1:
                allquantities.met_minus1l_sr2=pfMet
            writeSR2=True

# --------------------------------------------------------------------------------------------------------------------------------------------------------

        #Control Regions

# --------------------------------------------------------------------------------------------------------------------------------------------------------

        preselquantlist=AllQuantList.getPresel()

        for quant in preselquantlist:
            exec("allquantities."+quant+" = None")


        regquants=AllQuantList.getRegionQuants()

        for quant in regquants:
            exec("allquantities."+quant+" = None")

        # Histos2D=AllQuantList.getHistos2D()
        # for quant in Histos2D:
        #     exec("allquantities."+quant+" = None")



        ####new conds
        jetcond=True
        SR2jet2=True

        if j1.Pt() < 50.0: jetcond=False

        if myJetNhadEF[ifirstjet] > 0.8 : jetcond=False
        if myJetChadEF[ifirstjet]< 0.1: jetcond=False

        if nJets>=2:
            if j2.Pt() < 30.0: jetcond=False

            if j2.Pt() > 50.0:
                SR2jet2=True
            else:
                SR2jet2=False

            if nJets>=3:
                if j3.Pt() < 30.0: jetcond=False

# -------------------------------------------
# Z CR
# -------------------------------------------

        #Z CR specific bools

        ZdPhicond=True

        if applydPhicut:
            if ZeePhi>-10.:
                if min( [DeltaPhi(ZeePhi,myJetP4[nb].Phi()) for nb in range(nJets)] ) < 0.5: ZdPhicond=False
            if ZmumuPhi>-10.:
                if min( [DeltaPhi(ZmumuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] ) < 0.5: ZdPhicond=False

            #if ZeePhi>-10.:
                #if DeltaPhi(j1.Phi(),Phi_mpi_pi(math.pi+ZeePhi)) < 0.5: ZdPhicond = False      #Added +pi to ZPhi to reverse an error in SkimTree which will be fixed in next iteration.
                #if nJets>=2:
                    #if DeltaPhi(j2.Phi(),Phi_mpi_pi(math.pi+ZeePhi)) < 0.5: ZdPhicond=False
                #if nJets>=3:
                    #if DeltaPhi(j3.Phi(),Phi_mpi_pi(math.pi+ZeePhi)) < 0.5: ZdPhicond=False

            #if ZmumuPhi>-10.:
                #if DeltaPhi(j1.Phi(),Phi_mpi_pi(math.pi+ZmumuPhi)) < 0.5: ZdPhicond = False
                #if nJets>=2:
                    #if DeltaPhi(j2.Phi(),Phi_mpi_pi(math.pi+ZmumuPhi)) < 0.5: ZdPhicond=False
                #if nJets>=3:
                    #if DeltaPhi(j3.Phi(),Phi_mpi_pi(math.pi+ZmumuPhi)) < 0.5: ZdPhicond=False


         #2e, 1 b-tagged

        if nEle==2 and nMu==0 and nTauTightElectron==0 and EleCRtrigstatus and ZeeMass>70. and ZeeMass<110. and ZeeRecoil>200. and jetcond and pfMet > 0.:
#            CRCutFlow['nlepcond']+=1
            alllepPT=[lep.Pt() for lep in myEles]
            lepindex=[i for i in range(len(myEles))]

            sortedleps=[lep for pt,lep in sorted(zip(alllepPT,myEles), reverse=True)]      # This gives a list of leps with their pTs in descending order
            sortedindex=[lepind for pt,lepind in sorted(zip(alllepPT,lepindex), reverse=True)]     # Indices of leps in myJetP4 in decscending order of jetPT

            iLeadLep=sortedindex[0]
            iSecondLep=sortedindex[1]

            if myEles[iLeadLep].Pt() > 30. and myEleTightID[iLeadLep] and myEles[iSecondLep].Pt() > 10. and myEleLooseID[iSecondLep]:

                ZpT = math.sqrt( (myEles[iLeadLep].Px()+myEles[iSecondLep].Px())*(myEles[iLeadLep].Px()+myEles[iSecondLep].Px()) + (myEles[iLeadLep].Py()+myEles[iSecondLep].Py())*(myEles[iLeadLep].Py()+myEles[iSecondLep].Py()) )
                if nBjets==1 and SR1njetcond:
                    allquantities.reg_2e1b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(ZeePhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==1 and ZdPhicond and (nJets-nBjets)==0:
                    allquantities.reg_2e1b_Zmass = ZeeMass
                    allquantities.reg_2e1b_ZpT=ZpT

                    allquantities.reg_2e1b_hadrecoil = ZeeRecoil
                    allquantities.reg_2e1b_MET = pfMet

                    allquantities.reg_2e1b_lep1_pT=myEles[iLeadLep].Pt()
                    allquantities.reg_2e1b_lep2_pT=myEles[iSecondLep].Pt()

                    allquantities.reg_2e1b_jet1_pT=j1.Pt()
                    if nJets>1: allquantities.reg_2e1b_jet2_pT=j2.Pt()

                    allquantities.reg_2e1b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_2e1b_jet2_eta=j2.Eta()

                    allquantities.reg_2e1b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_2e1b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_2e1b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_2e1b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_2e1b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_2e1b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_2e1b_njet = nJets

                    if options.CSV:
                        allquantities.reg_2e1b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2e1b_jet2_csv = myJetCSV[isecondjet]
                    if options.DeepCSV:
                        allquantities.reg_2e1b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2e1b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_2e1b_min_dPhi_jet_Recoil = min( [DeltaPhi(ZeePhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_2e1b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_2e1b_ntau = nTauTightElectron
                    allquantities.reg_2e1b_nele = nEle
                    allquantities.reg_2e1b_nmu = nMu

                    allquantities.reg_2e1b_nUncleanTau = nUncleanTau
                    allquantities.reg_2e1b_nUncleanEle = nUncleanEle
                    allquantities.reg_2e1b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_2e1b_up = ZeeRecoil
                    allquantities.lep_syst_2e1b_down = ZeeRecoil
                    allquantities.btag_syst_2e1b_up = ZeeRecoil
                    allquantities.btag_syst_2e1b_down = ZeeRecoil
                    allquantities.metTrig_syst_2e1b_up = ZeeRecoil
                    allquantities.metTrig_syst_2e1b_down = ZeeRecoil
                    allquantities.ewkZ_syst_2e1b_up = ZeeRecoil
                    allquantities.ewkZ_syst_2e1b_down = ZeeRecoil
                    allquantities.ewkW_syst_2e1b_up = ZeeRecoil
                    allquantities.ewkW_syst_2e1b_down = ZeeRecoil
                    allquantities.ewkTop_syst_2e1b_up = ZeeRecoil
                    allquantities.ewkTop_syst_2e1b_down = ZeeRecoil
                    allquantities.pho_syst_2e1b_up = ZeeRecoil
                    allquantities.pho_syst_2e1b_down = ZeeRecoil
                    allquantities.jec_syst_2e1b_up = ZeeRecoil
                    allquantities.jec_syst_2e1b_down = ZeeRecoil
                    allquantities.jer_syst_2e1b_up = ZeeRecoil
                    allquantities.jer_syst_2e1b_down = ZeeRecoil
                    if lepCategory==2:
                        allquantities.reg_2e1b_MET_2l=pfMet
                        allquantities.reg_2e1b_hadrecoil_2l=ZeeRecoil
                    if lepCategory==-1:
                        allquantities.reg_2e1b_MET_minus1l=pfMet
                        allquantities.reg_2e1b_hadrecoil_minus1l=ZeeRecoil
                    isZeeCR1 = True

            #2e, 2 b-tagged
                if nBjets==2 and SR2jet2 and SR2njetcond:
                    allquantities.reg_2e2b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(ZeePhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==2 and SR2jet2 and SR2njetcond and ZdPhicond:
                    allquantities.reg_2e2b_Zmass = ZeeMass
                    allquantities.reg_2e2b_ZpT=ZpT

                    allquantities.reg_2e2b_hadrecoil = ZeeRecoil
                    allquantities.reg_2e2b_MET = pfMet

                    allquantities.reg_2e2b_lep1_pT=myEles[iLeadLep].Pt()
                    allquantities.reg_2e2b_lep2_pT=myEles[iSecondLep].Pt()


                    allquantities.reg_2e2b_jet1_pT=j1.Pt()
                    if nJets>1: allquantities.reg_2e2b_jet2_pT=j2.Pt()

                    allquantities.reg_2e2b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_2e2b_jet2_eta=j2.Eta()

                    allquantities.reg_2e2b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_2e2b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_2e2b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_2e2b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_2e2b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_2e2b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_2e2b_njet = nJets

                    if options.CSV:
                        allquantities.reg_2e2b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2e2b_jet2_csv = myJetCSV[isecondjet]
                    if options.DeepCSV:
                        allquantities.reg_2e2b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2e2b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_2e2b_min_dPhi_jet_Recoil = min( [DeltaPhi(ZeePhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_2e2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_2e2b_ntau = nTauTightElectron
                    allquantities.reg_2e2b_nele = nEle
                    allquantities.reg_2e2b_nmu = nMu
                    allquantities.reg_2e2b_nUncleanTau = nUncleanTau
                    allquantities.reg_2e2b_nUncleanEle = nUncleanEle
                    allquantities.reg_2e2b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_2e2b_up = ZeeRecoil
                    allquantities.lep_syst_2e2b_down = ZeeRecoil
                    allquantities.btag_syst_2e2b_up = ZeeRecoil
                    allquantities.btag_syst_2e2b_down = ZeeRecoil
                    allquantities.metTrig_syst_2e2b_up = ZeeRecoil
                    allquantities.metTrig_syst_2e2b_down = ZeeRecoil
                    allquantities.ewkZ_syst_2e2b_up = ZeeRecoil
                    allquantities.ewkZ_syst_2e2b_down = ZeeRecoil
                    allquantities.ewkW_syst_2e2b_up = ZeeRecoil
                    allquantities.ewkW_syst_2e2b_down = ZeeRecoil
                    allquantities.ewkTop_syst_2e2b_up = ZeeRecoil
                    allquantities.ewkTop_syst_2e2b_down = ZeeRecoil
                    allquantities.pho_syst_2e2b_up = ZeeRecoil
                    allquantities.pho_syst_2e2b_down = ZeeRecoil
                    allquantities.jec_syst_2e2b_up = ZeeRecoil
                    allquantities.jec_syst_2e2b_down = ZeeRecoil
                    allquantities.jer_syst_2e2b_up = ZeeRecoil
                    allquantities.jer_syst_2e2b_down = ZeeRecoil
                    if lepCategory==2:
                        allquantities.reg_2e2b_MET_2l=pfMet
                        allquantities.reg_2e2b_hadrecoil_2l=ZeeRecoil
                    if lepCategory==-1:
                        allquantities.reg_2e2b_MET_minus1l=pfMet
                        allquantities.reg_2e2b_hadrecoil_minus1l=ZeeRecoil
                    isZeeCR2 = True


        #2mu, 1 b-tagged
        if nMu==2 and nEle==0 and nTauTightMuon==0 and MuCRtrigstatus and ZmumuMass>70. and ZmumuMass<110. and ZmumuRecoil>200. and jetcond and pfMet > 0.:

#            CRCutFlow['nlepcond']+=1
            alllepPT=[lep.Pt() for lep in myMuos]
            lepindex=[i for i in range(len(myMuos))]

            sortedleps=[lep for pt,lep in sorted(zip(alllepPT,myMuos), reverse=True)]      # This gives a list of leps with their pTs in descending order
            sortedindex=[lepind for pt,lepind in sorted(zip(alllepPT,lepindex), reverse=True)]     # Indices of leps in myJetP4 in decscending order of jetPT

            iLeadLep=sortedindex[0]
            iSecondLep=sortedindex[1]

            if myMuos[iLeadLep].Pt() > 30. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15 and myMuos[iSecondLep].Pt() > 10. and myMuLooseID[iSecondLep] and myMuIso[iSecondLep]<0.25:

                ZpT = math.sqrt( (myMuos[iLeadLep].Px()+myMuos[iSecondLep].Px())*(myMuos[iLeadLep].Px()+myMuos[iSecondLep].Px()) + (myMuos[iLeadLep].Py()+myMuos[iSecondLep].Py())*(myMuos[iLeadLep].Py()+myMuos[iSecondLep].Py()) )
                if  nBjets==1 and SR1njetcond:
                    allquantities.reg_2mu1b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(ZmumuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if  nBjets==1 and SR1njetcond and ZdPhicond:
                    allquantities.reg_2mu1b_Zmass = ZmumuMass
                    allquantities.reg_2mu1b_ZpT=ZpT

                    allquantities.reg_2mu1b_hadrecoil = ZmumuRecoil
                    allquantities.reg_2mu1b_MET = pfMet

                    allquantities.reg_2mu1b_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_2mu1b_lep2_pT=myMuos[iSecondLep].Pt()

                    allquantities.reg_2mu1b_lep1_iso=myMuIso[iLeadLep]
                    allquantities.reg_2mu1b_lep2_iso=myMuIso[iSecondLep]

                    allquantities.reg_2mu1b_jet1_pT=j1.Pt()
                    if nJets>1: allquantities.reg_2mu1b_jet2_pT=j2.Pt()

                    allquantities.reg_2mu1b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_2mu1b_jet2_eta=j2.Eta()

                    allquantities.reg_2mu1b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_2mu1b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_2mu1b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_2mu1b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_2mu1b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_2mu1b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_2mu1b_njet = nJets

                    if options.CSV:
                        allquantities.reg_2mu1b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2mu1b_jet2_csv = myJetCSV[isecondjet]
                    if options.DeepCSV:
                        allquantities.reg_2mu1b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2mu1b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_2mu1b_min_dPhi_jet_Recoil = min( [DeltaPhi(ZmumuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_2mu1b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_2mu1b_ntau = nTauTightMuon
                    allquantities.reg_2mu1b_nele = nEle
                    allquantities.reg_2mu1b_nmu = nMu
                    allquantities.reg_2mu1b_nUncleanTau = nUncleanTau
                    allquantities.reg_2mu1b_nUncleanEle = nUncleanEle
                    allquantities.reg_2mu1b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_2mu1b_up = ZmumuRecoil
                    allquantities.lep_syst_2mu1b_down = ZmumuRecoil
                    allquantities.btag_syst_2mu1b_up = ZmumuRecoil
                    allquantities.btag_syst_2mu1b_down = ZmumuRecoil
                    allquantities.metTrig_syst_2mu1b_up = ZmumuRecoil
                    allquantities.metTrig_syst_2mu1b_down = ZmumuRecoil
                    allquantities.ewkZ_syst_2mu1b_up = ZmumuRecoil
                    allquantities.ewkZ_syst_2mu1b_down = ZmumuRecoil
                    allquantities.ewkW_syst_2mu1b_up = ZmumuRecoil
                    allquantities.ewkW_syst_2mu1b_down = ZmumuRecoil
                    allquantities.ewkTop_syst_2mu1b_up = ZmumuRecoil
                    allquantities.ewkTop_syst_2mu1b_down = ZmumuRecoil
                    allquantities.pho_syst_2mu1b_up = ZmumuRecoil
                    allquantities.pho_syst_2mu1b_down = ZmumuRecoil
                    allquantities.jec_syst_2mu1b_up = ZmumuRecoil
                    allquantities.jec_syst_2mu1b_down = ZmumuRecoil
                    allquantities.jer_syst_2mu1b_up = ZmumuRecoil
                    allquantities.jer_syst_2mu1b_down = ZmumuRecoil
                    if lepCategory==2:
                        allquantities.reg_2mu1b_MET_2l=pfMet
                        allquantities.reg_2mu1b_hadrecoil_2l=ZmumuRecoil
                    if lepCategory==-1:
                        allquantities.reg_2mu1b_MET_minus1l=pfMet
                        allquantities.reg_2mu1b_hadrecoil_minus1l=ZmumuRecoil

                    allquantities.ZpT_MET = [ZpT,pfMet]
                    allquantities.MET_Recoil = [pfMet,ZmumuRecoil]
                    allquantities.ZpT_Recoil_MET0 = [ZpT,ZmumuRecoil]
                    if pfMet > 50.  : allquantities.ZpT_Recoil_MET50  = [ZpT,ZmumuRecoil]
                    if pfMet > 100. : allquantities.ZpT_Recoil_MET100 = [ZpT,ZmumuRecoil]
                    if pfMet > 150. : allquantities.ZpT_Recoil_MET150 = [ZpT,ZmumuRecoil]
                    if pfMet > 200. : allquantities.ZpT_Recoil_MET200 = [ZpT,ZmumuRecoil]
                    isZmumuCR1 = True

            #2mu, 2 b-tagged
                if  nBjets==2 and SR2jet2 and SR2njetcond:
                    allquantities.reg_2mu2b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(ZmumuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if  nBjets==2 and SR2jet2 and SR2njetcond and ZdPhicond:
                    allquantities.reg_2mu2b_Zmass = ZmumuMass
                    allquantities.reg_2mu2b_ZpT=ZpT

                    allquantities.reg_2mu2b_hadrecoil = ZmumuRecoil
                    allquantities.reg_2mu2b_MET = pfMet

                    allquantities.reg_2mu2b_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_2mu2b_lep2_pT=myMuos[iSecondLep].Pt()

                    allquantities.reg_2mu2b_lep1_iso=myMuIso[iLeadLep]
                    allquantities.reg_2mu2b_lep2_iso=myMuIso[iSecondLep]


                    allquantities.reg_2mu2b_jet1_pT=j1.Pt()
                    if nJets>1: allquantities.reg_2mu2b_jet2_pT=j2.Pt()

                    allquantities.reg_2mu2b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_2mu2b_jet2_eta=j2.Eta()

                    allquantities.reg_2mu2b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_2mu2b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_2mu2b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_2mu2b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_2mu2b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_2mu2b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_2mu2b_njet = nJets

                    if options.CSV:
                        allquantities.reg_2mu2b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2mu2b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_2mu2b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_2mu2b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_2mu2b_min_dPhi_jet_Recoil = min( [DeltaPhi(ZmumuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_2mu2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_2mu2b_ntau = nTauTightMuon
                    allquantities.reg_2mu2b_nele = nEle
                    allquantities.reg_2mu2b_nmu = nMu
                    allquantities.reg_2mu2b_nUncleanTau = nUncleanTau
                    allquantities.reg_2mu2b_nUncleanEle = nUncleanEle
                    allquantities.reg_2mu2b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_2mu2b_up = ZmumuRecoil
                    allquantities.lep_syst_2mu2b_down = ZmumuRecoil
                    allquantities.btag_syst_2mu2b_up = ZmumuRecoil
                    allquantities.btag_syst_2mu2b_down = ZmumuRecoil
                    allquantities.metTrig_syst_2mu2b_up = ZmumuRecoil
                    allquantities.metTrig_syst_2mu2b_down = ZmumuRecoil
                    allquantities.ewkZ_syst_2mu2b_up = ZmumuRecoil
                    allquantities.ewkZ_syst_2mu2b_down = ZmumuRecoil
                    allquantities.ewkW_syst_2mu2b_up = ZmumuRecoil
                    allquantities.ewkW_syst_2mu2b_down = ZmumuRecoil
                    allquantities.ewkTop_syst_2mu2b_up = ZmumuRecoil
                    allquantities.ewkTop_syst_2mu2b_down = ZmumuRecoil
                    allquantities.pho_syst_2mu2b_up = ZmumuRecoil
                    allquantities.pho_syst_2mu2b_down = ZmumuRecoil
                    allquantities.jec_syst_2mu2b_up = ZmumuRecoil
                    allquantities.jec_syst_2mu2b_down = ZmumuRecoil
                    allquantities.jer_syst_2mu2b_up = ZmumuRecoil
                    allquantities.jer_syst_2mu2b_down = ZmumuRecoil
                    if lepCategory==2:
                        allquantities.reg_2mu2b_MET_2l=pfMet
                        allquantities.reg_2mu2b_hadrecoil_2l=ZmumuRecoil
                    if lepCategory==-1:
                        allquantities.reg_2mu2b_MET_minus1l=pfMet
                        allquantities.reg_2mu2b_hadrecoil_minus1l=ZmumuRecoil
                    isZmunuCR2 = True

# -------------------------------------------
# W CR
# -------------------------------------------

        #W CR specific bools

        WdPhicond=True

        if applydPhicut:
            if WenuPhi>-10.:
                if min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] ) < 0.5: WdPhicond=False
            if WmunuPhi>-10.:
                if min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] ) < 0.5: WdPhicond=False
            #if WenuPhi>-10.:
                #if DeltaPhi(j1.Phi(),Phi_mpi_pi(math.pi+WenuPhi)) < 0.5: WdPhicond = False      #Added +pi to ZPhi to reverse an error in SkimTree which will be fixed in next iteration.
                #if nJets>=2:
                    #if DeltaPhi(j2.Phi(),Phi_mpi_pi(math.pi+WenuPhi)) < 0.5: WdPhicond=False
                #if nJets>=3:
                    #if DeltaPhi(j3.Phi(),Phi_mpi_pi(math.pi+WenuPhi)) < 0.5: WdPhicond=False

            #if WmunuPhi>-10.:
                #if DeltaPhi(j1.Phi(),Phi_mpi_pi(math.pi+WmunuPhi)) < 0.5: WdPhicond = False
                #if nJets>=2:
                    #if DeltaPhi(j2.Phi(),Phi_mpi_pi(math.pi+WmunuPhi)) < 0.5: WdPhicond=False
                #if nJets>=3:
                    #if DeltaPhi(j3.Phi(),Phi_mpi_pi(math.pi+WmunuPhi)) < 0.5: WdPhicond=False


        #1e, 1 b-tagged
        if nEle==1 and nMu==0 and nTauTightElectron==0 and EleCRtrigstatus and WenuRecoil>200. and jetcond and Wenumass>50. and Wenumass<160. and pfMet > 50.:

            iLeadLep=0

            if myEles[iLeadLep].Pt() > 30. and myEleTightID[iLeadLep]:

                WpT = math.sqrt( ( pfMet*math.cos(pfMetPhi) + myEles[iLeadLep].Px())**2 + ( pfMet*math.sin(pfMetPhi) + myEles[iLeadLep].Py())**2)

                if nBjets==1 and WdPhicond:
                    allquantities.reg_1e1b_njet_n_minus_1=nJets
                    allquantities.reg_1e1b_unclean_njet_n_minus_1=nUncleanJets

                if nBjets==1 and SR1njetcond:
                    allquantities.reg_1e1b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==1 and WdPhicond and (nJets-nBjets)==0:
                    allquantities.reg_1e1b_Wmass = Wenumass
                    allquantities.reg_1e1b_WpT=WpT

                    allquantities.reg_1e1b_hadrecoil = WenuRecoil
                    allquantities.reg_1e1b_MET = pfMet

                    allquantities.reg_1e1b_lep1_pT=myEles[iLeadLep].Pt()

                    allquantities.reg_1e1b_jet1_pT=j1.Pt()


                    if nJets>1: allquantities.reg_1e1b_jet2_pT=j2.Pt()

                    allquantities.reg_1e1b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1e1b_jet2_eta=j2.Eta()

                    allquantities.reg_1e1b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1e1b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1e1b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1e1b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1e1b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1e1b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1e1b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1e1b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1e1b_jet2_csv = myJetCSV[isecondjet]

                        allquantities.reg_1e1b_min_dR_jet_ele_preclean = min( [DeltaR(myEles[iLeadLep],thinjetP4[nb]) for nb in range(nTHINJets)] )          #For diagnosis

                    if options.DeepCSV:
                        allquantities.reg_1e1b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1e1b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1e1b_min_dR_jet_ele_postclean = min( [DeltaR(myEles[iLeadLep],myJetP4[nb]) for nb in range(nJets)] )

                    allquantities.reg_1e1b_min_dPhi_jet_Recoil = min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1e1b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1e1b_ntau = nTauTightElectron
                    allquantities.reg_1e1b_nele = nEle
                    allquantities.reg_1e1b_nmu = nMu
                    allquantities.reg_1e1b_nUncleanTau = nUncleanTau
                    allquantities.reg_1e1b_nUncleanEle = nUncleanEle
                    allquantities.reg_1e1b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1e1b_up = WenuRecoil
                    allquantities.lep_syst_1e1b_down = WenuRecoil
                    allquantities.btag_syst_1e1b_up = WenuRecoil
                    allquantities.btag_syst_1e1b_down = WenuRecoil
                    allquantities.metTrig_syst_1e1b_up =WenuRecoil
                    allquantities.metTrig_syst_1e1b_down =WenuRecoil
                    allquantities.ewkZ_syst_1e1b_up = WenuRecoil
                    allquantities.ewkZ_syst_1e1b_down = WenuRecoil
                    allquantities.ewkW_syst_1e1b_up = WenuRecoil
                    allquantities.ewkW_syst_1e1b_down = WenuRecoil
                    allquantities.ewkTop_syst_1e1b_up = WenuRecoil
                    allquantities.ewkTop_syst_1e1b_down = WenuRecoil
                    allquantities.pho_syst_1e1b_up = WenuRecoil
                    allquantities.pho_syst_1e1b_down = WenuRecoil
                    allquantities.jec_syst_1e1b_up = WenuRecoil
                    allquantities.jec_syst_1e1b_down = WenuRecoil
                    allquantities.jer_syst_1e1b_up = WenuRecoil
                    allquantities.jer_syst_1e1b_down = WenuRecoil
                    if lepCategory==0:
                        allquantities.reg_1e1b_MET_0l=pfMet
                        allquantities.reg_1e1b_hadrecoil_0l=WenuRecoil
                    if lepCategory==1:
                        allquantities.reg_1e1b_MET_1l=pfMet
                        allquantities.reg_1e1b_hadrecoil_1l=WenuRecoil
                    if lepCategory==2:
                        allquantities.reg_1e1b_MET_2l=pfMet
                        allquantities.reg_1e1b_hadrecoil_2l=WenuRecoil
                    if lepCategory==-1:
                        allquantities.reg_1e1b_MET_minus1l=pfMet
                        allquantities.reg_1e1b_hadrecoil_minus1l=WenuRecoil
                    isWenuCR1 = True


            #1e, 2 b-tagged
                if nBjets==2 and SR2jet2 and SR2njetcond:
                    allquantities.reg_1e2b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==2 and SR2jet2 and WdPhicond and (nJets-nBjets)==0:
                    allquantities.reg_1e2b_Wmass = Wenumass
                    allquantities.reg_1e2b_WpT=WpT

                    allquantities.reg_1e2b_hadrecoil = WenuRecoil
                    allquantities.reg_1e2b_MET = pfMet

                    allquantities.reg_1e2b_lep1_pT=myEles[iLeadLep].Pt()

                    allquantities.reg_1e2b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1e2b_jet2_pT=j2.Pt()

                    allquantities.reg_1e2b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1e2b_jet2_eta=j2.Eta()

                    allquantities.reg_1e2b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1e2b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1e2b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1e2b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1e2b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1e2b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1e2b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1e2b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1e2b_jet2_csv = myJetCSV[isecondjet]

                        allquantities.reg_1e2b_min_dR_jet_ele_preclean = min( [DeltaR(myEles[iLeadLep],thinjetP4[nb]) for nb in range(nTHINJets)] )          #For diagnosis

                    if options.DeepCSV:
                        allquantities.reg_1e2b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1e2b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1e2b_min_dR_jet_ele_postclean = min( [DeltaR(myEles[iLeadLep],myJetP4[nb]) for nb in range(nJets)] )

                    allquantities.reg_1e2b_min_dPhi_jet_Recoil = min( [DeltaPhi(WenuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1e2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1e2b_ntau = nTauTightElectron
                    allquantities.reg_1e2b_nele = nEle
                    allquantities.reg_1e2b_nmu = nMu
                    allquantities.reg_1e2b_nUncleanTau = nUncleanTau
                    allquantities.reg_1e2b_nUncleanEle = nUncleanEle
                    allquantities.reg_1e2b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1e2b_up = WenuRecoil
                    allquantities.lep_syst_1e2b_down = WenuRecoil
                    allquantities.btag_syst_1e2b_up = WenuRecoil
                    allquantities.btag_syst_1e2b_down = WenuRecoil
                    allquantities.metTrig_syst_1e2b_up = WenuRecoil
                    allquantities.metTrig_syst_1e2b_down = WenuRecoil
                    allquantities.ewkZ_syst_1e2b_up = WenuRecoil
                    allquantities.ewkZ_syst_1e2b_down = WenuRecoil
                    allquantities.ewkW_syst_1e2b_up = WenuRecoil
                    allquantities.ewkW_syst_1e2b_down = WenuRecoil
                    allquantities.ewkTop_syst_1e2b_up = WenuRecoil
                    allquantities.ewkTop_syst_1e2b_down = WenuRecoil
                    allquantities.pho_syst_1e2b_up = WenuRecoil
                    allquantities.pho_syst_1e2b_down = WenuRecoil
                    allquantities.jec_syst_1e2b_up = WenuRecoil
                    allquantities.jec_syst_1e2b_down = WenuRecoil
                    allquantities.jer_syst_1e2b_up = WenuRecoil
                    allquantities.jer_syst_1e2b_down = WenuRecoil
                    if lepCategory==0:
                        allquantities.reg_1e2b_MET_0l=pfMet
                        allquantities.reg_1e2b_hadrecoil_0l=WenuRecoil
                    if lepCategory==1:
                        allquantities.reg_1e2b_MET_1l=pfMet
                        allquantities.reg_1e2b_hadrecoil_1l=WenuRecoil
                    if lepCategory==2:
                        allquantities.reg_1e2b_MET_2l=pfMet
                        allquantities.reg_1e2b_hadrecoil_2l=WenuRecoil
                    if lepCategory==-1:
                        allquantities.reg_1e2b_MET_minus1l=pfMet
                        allquantities.reg_1e2b_hadrecoil_minus1l=WenuRecoil
                    isWenuCR2 = True

        #1mu, 1 b-tagged
        if nMu==1 and nEle==0 and nTauTightMuon==0 and MuCRtrigstatus and WmunuRecoil>200. and jetcond and Wmunumass>50. and Wmunumass<160. and pfMet > 50.:
            iLeadLep=0

            if myMuos[iLeadLep].Pt() > 30. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15:

                WpT = math.sqrt( ( pfMet*math.cos(pfMetPhi) + myMuos[iLeadLep].Px())**2 + ( pfMet*math.sin(pfMetPhi) + myMuos[iLeadLep].Py())**2)

                if nBjets==1 and WdPhicond:
                    allquantities.reg_1mu1b_njet_n_minus_1=nJets
                    allquantities.reg_1mu1b_unclean_njet_n_minus_1=nUncleanJets

                if  nBjets==1 and SR1njetcond:
                    allquantities.reg_1mu1b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if  nBjets==1 and WdPhicond and (nJets-nBjets)==0:
                    allquantities.reg_1mu1b_Wmass = Wmunumass
                    allquantities.reg_1mu1b_WpT=WpT

                    allquantities.reg_1mu1b_hadrecoil = WmunuRecoil
                    allquantities.reg_1mu1b_MET = pfMet

                    allquantities.reg_1mu1b_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_1mu1b_lep1_iso=myMuIso[iLeadLep]

                    allquantities.reg_1mu1b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1mu1b_jet2_pT=j2.Pt()

                    allquantities.reg_1mu1b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1mu1b_jet2_eta=j2.Eta()

                    allquantities.reg_1mu1b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1mu1b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1mu1b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1mu1b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1mu1b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1mu1b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1mu1b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1mu1b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu1b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_1mu1b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu1b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1mu1b_min_dPhi_jet_Recoil = min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1mu1b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1mu1b_ntau = nTauTightMuon
                    allquantities.reg_1mu1b_nele = nEle
                    allquantities.reg_1mu1b_nmu = nMu
                    allquantities.reg_1mu1b_nUncleanTau = nUncleanTau
                    allquantities.reg_1mu1b_nUncleanEle = nUncleanEle
                    allquantities.reg_1mu1b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1mu1b_up = WmunuRecoil
                    allquantities.lep_syst_1mu1b_down = WmunuRecoil
                    allquantities.btag_syst_1mu1b_up = WmunuRecoil
                    allquantities.btag_syst_1mu1b_down = WmunuRecoil
                    allquantities.metTrig_syst_1mu1b_up = WmunuRecoil
                    allquantities.metTrig_syst_1mu1b_down = WmunuRecoil
                    allquantities.ewkZ_syst_1mu1b_up = WmunuRecoil
                    allquantities.ewkZ_syst_1mu1b_down = WmunuRecoil
                    allquantities.ewkW_syst_1mu1b_up = WmunuRecoil
                    allquantities.ewkW_syst_1mu1b_down = WmunuRecoil
                    allquantities.ewkTop_syst_1mu1b_up = WmunuRecoil
                    allquantities.ewkTop_syst_1mu1b_down = WmunuRecoil
                    allquantities.pho_syst_1mu1b_up = WmunuRecoil
                    allquantities.pho_syst_1mu1b_down = WmunuRecoil
                    allquantities.jec_syst_1mu1b_up = WmunuRecoil
                    allquantities.jec_syst_1mu1b_down = WmunuRecoil
                    allquantities.jer_syst_1mu1b_up = WmunuRecoil
                    allquantities.jer_syst_1mu1b_down = WmunuRecoil
                    if lepCategory==0:
                        allquantities.reg_1mu1b_MET_0l=pfMet
                        allquantities.reg_1mu1b_hadrecoil_0l=WmunuRecoil
                    if lepCategory==1:
                        allquantities.reg_1mu1b_MET_1l=pfMet
                        allquantities.reg_1mu1b_hadrecoil_1l=WmunuRecoil
                    if lepCategory==2:
                        allquantities.reg_1mu1b_MET_2l=pfMet
                        allquantities.reg_1mu1b_hadrecoil_2l=WmunuRecoil
                    if lepCategory==-1:
                        allquantities.reg_1mu1b_MET_minus1l=pfMet
                        allquantities.reg_1mu1b_hadrecoil_minus1l=WmunuRecoil
                    isWmunuCR1 = True


            #1mu, 2 b-tagged
                if  nBjets==2 and SR2jet2 and SR2njetcond:
                    allquantities.reg_1mu2b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if  nBjets==2 and SR2jet2 and WdPhicond and (nJets-nBjets)==0:
                    allquantities.reg_1mu2b_Wmass = Wmunumass
                    allquantities.reg_1mu2b_WpT=WpT

                    allquantities.reg_1mu2b_hadrecoil = WmunuRecoil
                    allquantities.reg_1mu2b_MET = pfMet

                    allquantities.reg_1mu2b_lep1_pT=myMuos[iLeadLep].Pt()
                    allquantities.reg_1mu2b_lep1_iso=myMuIso[iLeadLep]

                    allquantities.reg_1mu2b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1mu2b_jet2_pT=j2.Pt()

                    allquantities.reg_1mu2b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1mu2b_jet2_eta=j2.Eta()

                    allquantities.reg_1mu2b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1mu2b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1mu2b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1mu2b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1mu2b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1mu2b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1mu2b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1mu2b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu2b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_1mu2b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu2b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1mu2b_min_dPhi_jet_Recoil = min( [DeltaPhi(WmunuPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1mu2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1mu2b_ntau = nTauTightMuon
                    allquantities.reg_1mu2b_nele = nEle
                    allquantities.reg_1mu2b_nmu = nMu
                    allquantities.reg_1mu2b_nUncleanTau = nUncleanTau
                    allquantities.reg_1mu2b_nUncleanEle = nUncleanEle
                    allquantities.reg_1mu2b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1mu2b_up = WmunuRecoil
                    allquantities.lep_syst_1mu2b_down = WmunuRecoil
                    allquantities.btag_syst_1mu2b_up = WmunuRecoil
                    allquantities.btag_syst_1mu2b_down = WmunuRecoil
                    allquantities.metTrig_syst_1mu2b_up = WmunuRecoil
                    allquantities.metTrig_syst_1mu2b_down = WmunuRecoil
                    allquantities.ewkZ_syst_1mu2b_up = WmunuRecoil
                    allquantities.ewkZ_syst_1mu2b_down = WmunuRecoil
                    allquantities.ewkW_syst_1mu2b_up = WmunuRecoil
                    allquantities.ewkW_syst_1mu2b_down = WmunuRecoil
                    allquantities.ewkTop_syst_1mu2b_up = WmunuRecoil
                    allquantities.ewkTop_syst_1mu2b_down = WmunuRecoil
                    allquantities.pho_syst_1mu2b_up = WmunuRecoil
                    allquantities.pho_syst_1mu2b_down = WmunuRecoil
                    allquantities.jec_syst_1mu2b_up = WmunuRecoil
                    allquantities.jec_syst_1mu2b_down = WmunuRecoil
                    allquantities.jer_syst_1mu2b_up = WmunuRecoil
                    allquantities.jer_syst_1mu2b_down = WmunuRecoil
                    if lepCategory==0:
                        allquantities.reg_1mu2b_MET_0l=pfMet
                        allquantities.reg_1mu2b_hadrecoil_1l=WmunuRecoil
                    if lepCategory==1:
                        allquantities.reg_1mu2b_MET_1l=pfMet
                        allquantities.reg_1mu2b_hadrecoil_1l=WmunuRecoil
                    if lepCategory==2:
                        allquantities.reg_1mu2b_MET_2l=pfMet
                        allquantities.reg_1mu2b_hadrecoil_1l=WmunuRecoil
                    if lepCategory==-1:
                        allquantities.reg_1mu2b_MET_minus1l=pfMet
                        allquantities.reg_1mu2b_hadrecoil_minus1l=WmunuRecoil
                    isWmunuCR2 = True




# -------------------------------------------
# Top CR
# -------------------------------------------
        #Top CR specific bools

        TopdPhicond=True

        if applydPhicut:
            if TOPPhi>-10.:
                if min( [DeltaPhi(TOPPhi,myJetP4[nb].Phi()) for nb in range(nJets)] ) < 0.5: TopdPhicond=False
            #if TOPPhi>-10.:
                #if DeltaPhi(j1.Phi(),Phi_mpi_pi(math.pi+TOPPhi)) < 0.5: TopdPhicond = False      #Added +pi to ZPhi to reverse an error in SkimTree which will be fixed in next iteration.
                #if nJets>=2:
                    #if DeltaPhi(j2.Phi(),Phi_mpi_pi(math.pi+TOPPhi)) < 0.5: TopdPhicond=False
                #if nJets>=3:
                    #if DeltaPhi(j3.Phi(),Phi_mpi_pi(math.pi+TOPPhi)) < 0.5: TopdPhicond=False

        #1mu, 1e, 1 b-tagged
        if nEle==1 and nMu==1 and nTauTightEleMu==0 and MuCRtrigstatus and TOPRecoil>200. and jetcond and pfMet > 50.:

            if myEles[0].Pt() > 30. and myEleTightID[0] and myMuos[0].Pt() > 30. and myMuTightID[0] and myMuIso[0]<0.15:

                if myEles[0].Pt() > myMuos[0].Pt():
                    EleLead=True
                else:
                    EleLead=False

                if nBjets==1 and SR1njetcond:
                    allquantities.reg_1mu1e1b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(TOPPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==1 and SR1njetcond and TopdPhicond:

                    allquantities.reg_1mu1e1b_hadrecoil = TOPRecoil
                    allquantities.reg_1mu1e1b_MET = pfMet

                    if EleLead:
                        allquantities.reg_1mu1e1b_lep1_pT=myEles[0].Pt()
                        allquantities.reg_1mu1e1b_lep2_pT=myMuos[0].Pt()
                        allquantities.reg_1mu1e1b_lep2_iso=myMuIso[0]
                    else:
                        allquantities.reg_1mu1e1b_lep2_pT=myEles[0].Pt()
                        allquantities.reg_1mu1e1b_lep1_pT=myMuos[0].Pt()
                        allquantities.reg_1mu1e1b_lep1_iso=myMuIso[0]

                    allquantities.reg_1mu1e1b_e_pT=myEles[0].Pt()
                    allquantities.reg_1mu1e1b_mu_pT=myMuos[0].Pt()
                    allquantities.reg_1mu1e1b_mu_iso=myMuIso[0]

                    allquantities.reg_1mu1e1b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1mu1e1b_jet2_pT=j2.Pt()

                    allquantities.reg_1mu1e1b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1mu1e1b_jet2_eta=j2.Eta()

                    allquantities.reg_1mu1e1b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1mu1e1b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1mu1e1b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1mu1e1b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1mu1e1b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1mu1e1b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1mu1e1b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1mu1e1b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu1e1b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_1mu1e1b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu1e1b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1mu1e1b_min_dPhi_jet_Recoil = min( [DeltaPhi(TOPPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1mu1e1b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1mu1e1b_ntau = nTauTightEleMu
                    allquantities.reg_1mu1e1b_nele = nEle
                    allquantities.reg_1mu1e1b_nmu = nMu
                    allquantities.reg_1mu1e1b_nUncleanTau = nUncleanTau
                    allquantities.reg_1mu1e1b_nUncleanEle = nUncleanEle
                    allquantities.reg_1mu1e1b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1mu1e1b_up = TOPRecoil
                    allquantities.lep_syst_1mu1e1b_down = TOPRecoil
                    allquantities.btag_syst_1mu1e1b_up = TOPRecoil
                    allquantities.btag_syst_1mu1e1b_down = TOPRecoil
                    allquantities.metTrig_syst_1mu1e1b_up = TOPRecoil
                    allquantities.metTrig_syst_1mu1e1b_down = TOPRecoil
                    allquantities.ewkZ_syst_1mu1e1b_up = TOPRecoil
                    allquantities.ewkZ_syst_1mu1e1b_down = TOPRecoil
                    allquantities.ewkW_syst_1mu1e1b_up = TOPRecoil
                    allquantities.ewkW_syst_1mu1e1b_down = TOPRecoil
                    allquantities.ewkTop_syst_1mu1e1b_up = TOPRecoil
                    allquantities.ewkTop_syst_1mu1e1b_down = TOPRecoil
                    allquantities.pho_syst_1mu1e1b_up = TOPRecoil
                    allquantities.pho_syst_1mu1e1b_down = TOPRecoil
                    allquantities.jec_syst_1mu1e1b_up = TOPRecoil
                    allquantities.jec_syst_1mu1e1b_down = TOPRecoil
                    allquantities.jer_syst_1mu1e1b_up = TOPRecoil
                    allquantities.jer_syst_1mu1e1b_down = TOPRecoil
                    if lepCategory==0:
                        allquantities.reg_1mu1e1b_MET_0l=pfMet
                        allquantities.reg_1mu1e1b_hadrecoil_0l=TOPRecoil
                    if lepCategory==1:
                        allquantities.reg_1mu1e1b_MET_1l=pfMet
                        allquantities.reg_1mu1e1b_hadrecoil_1l=TOPRecoil
                    if lepCategory==2:
                        allquantities.reg_1mu1e1b_MET_2l=pfMet
                        allquantities.reg_1mu1e1b_hadrecoil_2l=TOPRecoil
                    if lepCategory==-1:
                        allquantities.reg_1mu1e1b_MET_minus1l=pfMet
                        allquantities.reg_1mu1e1b_hadrecoil_minus1l=TOPRecoil
                    isTopCR1 = True

            #1mu, 1e, 2 b-tagged
                if nBjets==2 and SR2jet2 and SR2njetcond:
                    allquantities.reg_1mu1e2b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(TOPPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==2 and SR2jet2 and SR2njetcond and TopdPhicond:

                    allquantities.reg_1mu1e2b_hadrecoil = TOPRecoil
                    allquantities.reg_1mu1e2b_MET = pfMet

                    if EleLead:
                        allquantities.reg_1mu1e2b_lep1_pT=myEles[0].Pt()
                        allquantities.reg_1mu1e2b_lep2_pT=myMuos[0].Pt()
                        allquantities.reg_1mu1e2b_lep2_iso=myMuIso[0]
                    else:
                        allquantities.reg_1mu1e2b_lep2_pT=myEles[0].Pt()
                        allquantities.reg_1mu1e2b_lep1_pT=myMuos[0].Pt()
                        allquantities.reg_1mu1e2b_lep1_iso=myMuIso[0]

                    allquantities.reg_1mu1e2b_e_pT=myEles[0].Pt()
                    allquantities.reg_1mu1e2b_mu_pT=myMuos[0].Pt()
                    allquantities.reg_1mu1e2b_mu_iso=myMuIso[0]

                    allquantities.reg_1mu1e2b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1mu1e2b_jet2_pT=j2.Pt()

                    allquantities.reg_1mu1e2b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1mu1e2b_jet2_eta=j2.Eta()

                    allquantities.reg_1mu1e2b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1mu1e2b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1mu1e2b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1mu1e2b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1mu1e2b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1mu1e2b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1mu1e2b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1mu1e2b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu1e2b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_1mu1e2b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1mu1e2b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1mu1e2b_min_dPhi_jet_Recoil = min( [DeltaPhi(TOPPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1mu1e2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1mu1e2b_ntau = nTauTightEleMu
                    allquantities.reg_1mu1e2b_nele = nEle
                    allquantities.reg_1mu1e2b_nmu = nMu
                    allquantities.reg_1mu1e2b_nUncleanTau = nUncleanTau
                    allquantities.reg_1mu1e2b_nUncleanEle = nUncleanEle
                    allquantities.reg_1mu1e2b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1mu1e2b_up = TOPRecoil
                    allquantities.lep_syst_1mu1e2b_down = TOPRecoil
                    allquantities.btag_syst_1mu1e2b_up = TOPRecoil
                    allquantities.btag_syst_1mu1e2b_down = TOPRecoil
                    allquantities.metTrig_syst_1mu1e2b_up = TOPRecoil
                    allquantities.metTrig_syst_1mu1e2b_down = TOPRecoil
                    allquantities.ewkZ_syst_1mu1e2b_up = TOPRecoil
                    allquantities.ewkZ_syst_1mu1e2b_down = TOPRecoil
                    allquantities.ewkW_syst_1mu1e2b_up = TOPRecoil
                    allquantities.ewkW_syst_1mu1e2b_down = TOPRecoil
                    allquantities.ewkTop_syst_1mu1e2b_up = TOPRecoil
                    allquantities.ewkTop_syst_1mu1e2b_down = TOPRecoil
                    allquantities.pho_syst_1mu1e2b_up = TOPRecoil
                    allquantities.pho_syst_1mu1e2b_down = TOPRecoil
                    allquantities.jec_syst_1mu1e2b_up = TOPRecoil
                    allquantities.jec_syst_1mu1e2b_down = TOPRecoil
                    allquantities.jer_syst_1mu1e2b_up = TOPRecoil
                    allquantities.jer_syst_1mu1e2b_down = TOPRecoil
                    if lepCategory==0:
                        allquantities.reg_1mu1e2b_MET_0l=pfMet
                        allquantities.reg_1mu1e2b_hadrecoil_0l=TOPRecoil
                    if lepCategory==1:
                        allquantities.reg_1mu1e2b_MET_1l=pfMet
                        allquantities.reg_1mu1e2b_hadrecoil_1l=TOPRecoil
                    if lepCategory==2:
                        allquantities.reg_1mu1e2b_MET_2l=pfMet
                        allquantities.reg_1mu1e2b_hadrecoil_2l=TOPRecoil
                    if lepCategory==-1:
                        allquantities.reg_1mu1e2b_MET_minus1l=pfMet
                        allquantities.reg_1mu1e2b_hadrecoil_minus1l=TOPRecoil
                    isTopCR2 = True
# -------------------------------------------
# Gamma CR
# -------------------------------------------

        #Gamma CR specific bools

        GammaPhicond=True

        if applydPhicut:
            if GammaPhi>-10.:
                if min( [DeltaPhi(GammaPhi,myJetP4[nb].Phi()) for nb in range(nJets)] ) < 0.5: GammaPhicond=False

            #if GammaPhi>-10.:
                #if DeltaPhi(j1.Phi(),Phi_mpi_pi(math.pi+GammaPhi)) < 0.5: GammaPhicond = False      #Added +pi to ZPhi to reverse an error in SkimTree which will be fixed in next iteration.
                #if nJets>=2:
                    #if DeltaPhi(j2.Phi(),Phi_mpi_pi(math.pi+GammaPhi)) < 0.5: GammaPhicond=False
                #if nJets>=3:
                    #if DeltaPhi(j3.Phi(),Phi_mpi_pi(math.pi+GammaPhi)) < 0.5: GammaPhicond=False

        #1 pho , 1 b-tagged
        if nPho==1 and nEle==0 and nMu==0 and nTauLooseEleMu==0 and PhotonCRtrigstatus and GammaRecoil>200. and jetcond and pfMet > 0.:

            if myPhos[0].Pt() > 175. and myPhoTightID[0] and myPhoLooseID[0]:

                if nBjets==1 and SR1njetcond:
                    allquantities.reg_1gamma1b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(GammaPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==0 and SR1jetcond and GammaPhicond:
#                if SR1njetcond and GammaPhicond:

                    allquantities.reg_1gamma1b_hadrecoil = GammaRecoil
                    allquantities.reg_1gamma1b_MET = pfMet

                    allquantities.reg_1gamma1b_pho_pT=myPhos[0].Pt()
                    #allquantities.reg_1mu1e1b_lep2_pT=myPhos[0].Pt()
                    #allquantities.reg_1mu1e1b_lep2_iso=myMuIso[0]

                    allquantities.reg_1gamma1b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1gamma1b_jet2_pT=j2.Pt()

                    allquantities.reg_1gamma1b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1gamma1b_jet2_eta=j2.Eta()

                    allquantities.reg_1gamma1b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1gamma1b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1gamma1b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1gamma1b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1gamma1b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1gamma1b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1gamma1b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1gamma1b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1gamma1b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_1gamma1b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1gamma1b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1gamma1b_min_dPhi_jet_Recoil = min( [DeltaPhi(GammaPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1gamma1b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1gamma1b_ntau = nTauLooseEleMu
                    allquantities.reg_1gamma1b_nele = nEle
                    allquantities.reg_1gamma1b_nmu = nMu
                    allquantities.reg_1gamma1b_nPho = nPho
                    allquantities.reg_1gamma1b_nUncleanTau = nUncleanTau
                    allquantities.reg_1gamma1b_nUncleanEle = nUncleanEle
                    allquantities.reg_1gamma1b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1gamma1b_up = GammaRecoil
                    allquantities.lep_syst_1gamma1b_down = GammaRecoil
                    allquantities.btag_syst_1gamma1b_up = GammaRecoil
                    allquantities.btag_syst_1gamma1b_down = GammaRecoil
                    allquantities.metTrig_syst_1gamma1b_up = GammaRecoil
                    allquantities.metTrig_syst_1gamma1b_down = GammaRecoil
                    allquantities.ewkZ_syst_1gamma1b_up = GammaRecoil
                    allquantities.ewkZ_syst_1gamma1b_down = GammaRecoil
                    allquantities.ewkW_syst_1gamma1b_up = GammaRecoil
                    allquantities.ewkW_syst_1gamma1b_down = GammaRecoil
                    allquantities.ewkTop_syst_1gamma1b_up = GammaRecoil
                    allquantities.ewkTop_syst_1gamma1b_down = GammaRecoil
                    allquantities.pho_syst_1gamma1b_up = GammaRecoil
                    allquantities.pho_syst_1gamma1b_down = GammaRecoil
                    allquantities.jec_syst_1gamma1b_up = GammaRecoil
                    allquantities.jec_syst_1gamma1b_down = GammaRecoil
                    allquantities.jer_syst_1gamma1b_up = GammaRecoil
                    allquantities.jer_syst_1gamma1b_down = GammaRecoil
                    isGammaCR1 = True

   #1 photon, 2 b-tagged
                if nBjets==2 and SR2jet2 and SR2njetcond:
                    allquantities.reg_1gamma2b_min_dPhi_jet_Recoil_n_minus_1 = min( [DeltaPhi(GammaPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                if nBjets==0 and SR2jet2 and SR2jetcond and GammaPhicond:
#		if SR2jet2 and SR2njetcond and GammaPhicond:

                    allquantities.reg_1gamma2b_hadrecoil = GammaRecoil
                    allquantities.reg_1gamma2b_MET = pfMet

                    allquantities.reg_1gamma2b_pho_pT=myPhos[0].Pt()
                    #allquantities.reg_1gamma2b_lep2_pT=myMuos[0].Pt()
                    #allquantities.reg_1gamma2b_lep2_iso=myMuIso[0]

                    allquantities.reg_1gamma2b_jet1_pT=j1.Pt()

                    if nJets>1: allquantities.reg_1gamma2b_jet2_pT=j2.Pt()

                    allquantities.reg_1gamma2b_jet1_eta=j1.Eta()
                    if nJets>1: allquantities.reg_1gamma2b_jet2_eta=j2.Eta()

                    allquantities.reg_1gamma2b_jet1_NHadEF=myJetNhadEF[ifirstjet]
                    allquantities.reg_1gamma2b_jet1_CHadEF=myJetChadEF[ifirstjet]
                    allquantities.reg_1gamma2b_jet1_CEmEF=myJetCEmEF[ifirstjet]
                    allquantities.reg_1gamma2b_jet1_PhoEF=myJetPhoEF[ifirstjet]
                    allquantities.reg_1gamma2b_jet1_EleEF=myJetEleEF[ifirstjet]
                    allquantities.reg_1gamma2b_jet1_MuoEF=myJetMuoEF[ifirstjet]

                    allquantities.reg_1gamma2b_njet = nJets

                    if options.CSV:
                        allquantities.reg_1gamma2b_jet1_csv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1gamma2b_jet2_csv = myJetCSV[isecondjet]

                    if options.DeepCSV:
                        allquantities.reg_1gamma2b_jet1_deepcsv = myJetCSV[ifirstjet]
                        if nJets>1: allquantities.reg_1gamma2b_jet2_deepcsv = myJetCSV[isecondjet]

                    allquantities.reg_1gamma2b_min_dPhi_jet_Recoil = min( [DeltaPhi(GammaPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )
                    allquantities.reg_1gamma2b_min_dPhi_jet_MET = min( [DeltaPhi(pfMetPhi,myJetP4[nb].Phi()) for nb in range(nJets)] )

                    allquantities.reg_1gamma2b_ntau = nTauLooseEleMu
                    allquantities.reg_1gamma2b_nele = nEle
                    allquantities.reg_1gamma2b_nmu = nMu
                    allquantities.reg_1gamma2b_nPho = nPho
                    allquantities.reg_1gamma2b_nUncleanTau = nUncleanTau
                    allquantities.reg_1gamma2b_nUncleanEle = nUncleanEle
                    allquantities.reg_1gamma2b_nUncleanMu = nUncleanMu
                    allquantities.lep_syst_1gamma2b_up = GammaRecoil
                    allquantities.lep_syst_1gamma2b_down = GammaRecoil
                    allquantities.btag_syst_1gamma2b_up = GammaRecoil
                    allquantities.btag_syst_1gamma2b_down = GammaRecoil
                    allquantities.metTrig_syst_1gamma2b_up = GammaRecoil
                    allquantities.metTrig_syst_1gamma2b_down = GammaRecoil
                    allquantities.ewkZ_syst_1gamma2b_up = GammaRecoil
                    allquantities.ewkZ_syst_1gamma2b_down = GammaRecoil
                    allquantities.ewkW_syst_1gamma2b_up = GammaRecoil
                    allquantities.ewkW_syst_1gamma2b_down = GammaRecoil
                    allquantities.ewkTop_syst_1gamma2b_up = GammaRecoil
                    allquantities.ewkTop_syst_1gamma2b_down = GammaRecoil
                    allquantities.pho_syst_1gamma2b_up = GammaRecoil
                    allquantities.pho_syst_1gamma2b_down = GammaRecoil
                    allquantities.jec_syst_1gamma2b_up = GammaRecoil
                    allquantities.jec_syst_1gamma2b_down = GammaRecoil
                    allquantities.jer_syst_1gamma2b_up = GammaRecoil
                    allquantities.jer_syst_1gamma2b_down = GammaRecoil
                    isGammaCR2 = True


        # QCD CR

        # 1b

        QCD1b_Cut1_nJets        =   SR1_Cut1_nJets
        QCD1b_Cut2_nBjets       =   SR1_Cut2_nBjets
        QCD1b_Cut3_trigstatus   =   SR1_Cut3_trigstatus
        QCD1b_Cut4_jet1         =   SR1_Cut4_jet1

        QCD1b_Cut5_jet2         =   SR1_Cut5_jet2
        QCD1b_Cut6_dPhi_jet_MET =   not SR1_Cut6_dPhi_jet_MET
        QCD1b_Cut7_nLep         =   SR1_Cut7_nLep
        QCD1b_Cut8_pfMET        =   SR1_Cut8_pfMET

        if QCD1b_Cut1_nJets and QCD1b_Cut3_trigstatus and QCD1b_Cut7_nLep and QCD1b_Cut8_pfMET:
            allquantities.reg_QCD1b_dPhi_leadJet=DeltaPhi(j1.Phi(),pfMetPhi)
            if nJets>1:
                allquantities.reg_QCD2b_dPhi_lastJet=DeltaPhi(j2.Phi(),pfMetPhi)


        if QCD1b_Cut1_nJets and QCD1b_Cut2_nBjets and QCD1b_Cut3_trigstatus and QCD1b_Cut4_jet1 and QCD1b_Cut5_jet2 and QCD1b_Cut6_dPhi_jet_MET and QCD1b_Cut7_nLep and QCD1b_Cut8_pfMET:

            allquantities.reg_QCD1b_MET         =   pfMet
            allquantities.reg_QCD1b_jet1_pT     =   j1.Pt()
            if nJets>1: allquantities.reg_QCD1b_jet2_pT     =   j2.Pt()
            allquantities.reg_QCD1b_jet1_eta        =   j1.Eta()
            if nJets>1: allquantities.reg_QCD1b_jet2_eta    =   j2.Eta()

            if options.CSV:
                allquantities.reg_QCD1b_jet1_csv    =   myJetCSV[ifirstjet]
                if nJets>1: allquantities.reg_QCD1b_jet2_csv    = myJetCSV[isecondjet]
            if options.DeepCSV:
                allquantities.reg_QCD1b_jet1_deepcsv    =   myJetCSV[ifirstjet]
                if nJets>1: allquantities.reg_QCD1b_jet2_deepcsv    = myJetCSV[isecondjet]

            allquantities.reg_QCD1b_njet    =   nJets
            allquantities.reg_QCD1b_ntau    =   nTauLooseEleMu
            allquantities.reg_QCD1b_nele    =   nEle
            allquantities.reg_QCD1b_nmu     =   nMu
            allquantities.reg_QCD1b_nUncleanEle =   nUncleanEle
            allquantities.reg_QCD1b_nUncleanMu  =   nUncleanMu
            allquantities.reg_QCD1b_nUncleanTau =   nUncleanTau
            allquantities.reg_QCD1b_min_dPhi_jet_MET    =   min_dPhi_jet_MET



        #2b

        QCD2b_Cut1_nJets        =   SR2_Cut1_nJets
        QCD2b_Cut2_nBjets       =   SR2_Cut2_nBjets
        QCD2b_Cut3_trigstatus   =   SR2_Cut3_trigstatus
        QCD2b_Cut4_jet1         =   SR2_Cut4_jet1
        QCD2b_Cut5_jet2         =   SR2_Cut5_jet2

        QCD2b_Cut6_jet3         =   SR2_Cut6_jet3
        QCD2b_Cut7_dPhi_jet_MET =   not SR2_Cut7_dPhi_jet_MET
        QCD2b_Cut8_nLep         =   SR2_Cut8_nLep
        QCD2b_Cut9_pfMET        =   SR2_Cut9_pfMET

        if QCD2b_Cut1_nJets and QCD2b_Cut3_trigstatus and QCD2b_Cut8_nLep and QCD2b_Cut9_pfMET:
            allquantities.reg_QCD2b_dPhi_leadJet=DeltaPhi(j1.Phi(),pfMetPhi)
            if nJets>2:
                allquantities.reg_QCD2b_dPhi_lastJet=DeltaPhi(j3.Phi(),pfMetPhi)
            else:
                allquantities.reg_QCD2b_dPhi_lastJet=DeltaPhi(j2.Phi(),pfMetPhi)

        if QCD2b_Cut1_nJets and QCD2b_Cut2_nBjets and QCD2b_Cut3_trigstatus and QCD2b_Cut4_jet1 and QCD2b_Cut5_jet2 and QCD2b_Cut6_jet3 and QCD2b_Cut7_dPhi_jet_MET and QCD2b_Cut8_nLep and QCD2b_Cut9_pfMET:

            allquantities.reg_QCD2b_MET         =   pfMet
            allquantities.reg_QCD2b_jet1_pT     =   j1.Pt()
            allquantities.reg_QCD2b_jet2_pT     =   j2.Pt()
            allquantities.reg_QCD2b_jet1_eta        =   j1.Eta()
            allquantities.reg_QCD2b_jet2_eta    =   j2.Eta()

            if options.CSV:
                allquantities.reg_QCD2b_jet1_csv    =   myJetCSV[ifirstjet]
                allquantities.reg_QCD2b_jet2_csv    = myJetCSV[isecondjet]
            if options.DeepCSV:
                allquantities.reg_QCD2b_jet1_deepcsv    =   myJetCSV[ifirstjet]
                allquantities.reg_QCD2b_jet2_deepcsv    = myJetCSV[isecondjet]

            allquantities.reg_QCD2b_njet    =   nJets
            allquantities.reg_QCD2b_ntau    =   nTauLooseEleMu
            allquantities.reg_QCD2b_nele    =   nEle
            allquantities.reg_QCD2b_nmu     =   nMu
            allquantities.reg_QCD2b_nUncleanEle =   nUncleanEle
            allquantities.reg_QCD2b_nUncleanMu  =   nUncleanMu
            allquantities.reg_QCD2b_nUncleanTau =   nUncleanTau
            allquantities.reg_QCD2b_min_dPhi_jet_MET    =   min_dPhi_jet_MET
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## min DPhi
        ## nT<hinJets
        ## b-jet Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Lepton Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#        nleptons_ = (len(myTaus) + len(myMuos) + len(myEles))

        #if not (nleptons_ >= nlepton) : continue
        #if not (nleptons_ < nLepton) : continue

        #regime = False
        #if isboosted: regime = True
        #if isresolved: regime = False


        #if regime:
         #   mt_ = MT(fatjetP4[HIndex].Pt(), pfMet, Phi_mpi_pi(pfMetPhi-fatjetP4[HIndex].Phi()) )
        #if not regime:
         #   mt_ = MT(HiggsInfo[0][3], pfMet, Phi_mpi_pi(pfMetPhi-HiggsInfo[0][4]) )

        #if mt_ < 450.0: continue

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Photon Veto
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----to be added in future---------------------------------------------------------------------------------------------------------------------------------------


        if pfmetstatus and SRlepcond and (SR1jetcond or SR2jetcond): npass = npass + 1

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#       ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        genpTReweighting = 1.0
        if isData==1:   genpTReweighting  =  1.0
        if not isData :  genpTReweighting = GenWeightProducer(samplename, nGenPar, genParId, genMomParId, genParSt,genParP4)
#        print genpTReweighting
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## MET reweights
        #----------------------------------------------------------------------------------------------------------------------------------------------------------------
        metTrig_firstmethodReweight=1.0
        metTrig_secondmethodReweight=1.0
        metTrig_firstmethodReweight_up=1.0
        metTrig_firstmethodReweight_down=1.0
        if writeSR1:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(pfMet)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(pfMet)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        if writeSR2:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(pfMet)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(pfMet)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        if ZmumuRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(ZmumuRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(ZmumuRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif ZeeRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(ZeeRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(ZeeRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif WmunuRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(WmunuRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(WmunuRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif WenuRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(WenuRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(WenuRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif TOPRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(TOPRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(TOPRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
        elif GammaRecoil > 200:
            xbin1 = metTrig_firstmethod.GetXaxis().FindBin(GammaRecoil)
            xbin2 = metTrig_secondmethod.GetXaxis().FindBin(GammaRecoil)
            metTrig_firstmethodReweight = metTrig_firstmethod.GetBinContent(xbin1)
            metTrig_secondmethodReweight = metTrig_secondmethod.GetBinContent(xbin2)
            metTrig_firstmethodReweight_up = metTrig_firstmethodReweight + (metTrig_firstmethodReweight-metTrig_secondmethodReweight)
            metTrig_firstmethodReweight_down = metTrig_firstmethodReweight - (metTrig_firstmethodReweight-metTrig_secondmethodReweight)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Muon reweight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        #
        uni = random.uniform(0., 1.)
        muonTrig_SF = 1.0
        muonTrig_SF_systUP=1.0
        muonTrig_SF_systDOWN=1.0
        if nMu == 1:
            mupt = muP4[0].Pt()
            abeta = abs(muP4[0].Eta())
        if nMu == 2:
            if muP4[0].Pt() > muP4[1].Pt():
                leadmu=0
            else:
                leadmu=1
            mupt = muP4[leadmu].Pt()
            abeta = abs(muP4[leadmu].Eta())
        if nMu==1 or nMu==2:
            if uni < 0.54:
                xbin = muonTrigSFs_EfficienciesAndSF_RunBtoF.GetXaxis().FindBin(abeta)
                ybin = muonTrigSFs_EfficienciesAndSF_RunBtoF.GetYaxis().FindBin(mupt)
                muonTrig_SF *= muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinContent(xbin,ybin)
                muonTrig_SF_systUP *= muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinContent(xbin,ybin) + muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinErrorUp(xbin,ybin)
                muonTrig_SF_systDOWN *= muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinContent(xbin,ybin) - muonTrigSFs_EfficienciesAndSF_RunBtoF.GetBinErrorLow(xbin,ybin)
            elif uni > 0.54:
                xbin = muonTrigSFs_EfficienciesAndSF_Period4.GetXaxis().FindBin(abeta)
                ybin = muonTrigSFs_EfficienciesAndSF_Period4.GetYaxis().FindBin(mupt)
                muonTrig_SF *= muonTrigSFs_EfficienciesAndSF_Period4.GetBinContent(xbin,ybin)
                muonTrig_SF_systUP *= muonTrigSFs_EfficienciesAndSF_Period4.GetBinContent(xbin,ybin) + muonTrigSFs_EfficienciesAndSF_Period4.GetBinErrorUp(xbin,ybin)
                muonTrig_SF_systDOWN *= muonTrigSFs_EfficienciesAndSF_Period4.GetBinContent(xbin,ybin) - muonTrigSFs_EfficienciesAndSF_Period4.GetBinErrorLow(xbin,ybin)
        muIDSF_loose = 1.0
        muIDSF_loose_systUP=1.0
        muIDSF_loose_systDOWN=1.0
        muIDSF_tight = 1.0
        muIDSF_tight_systUP=1.0
        muIDSF_tight_systDOWN=1.0
        for imu in range(nMu):
            mupt = muP4[imu].Pt()
            abeta = abs(muP4[imu].Eta())
            if uni < 0.54:
                if mupt > 30:
                    xbin = muonTightIDSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonTightIDSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIDSF_tight *= muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIDSF_tight_systUP *= (muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIDSF_tight_systDOWN *= (muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonTightIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
                else:
                    xbin = muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIDSF_loose *= muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIDSF_loose_systUP *= (muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIDSF_loose_systDOWN *= (muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonLooseIDSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
            if uni > 0.54:
                if mupt > 30:
                    xbin = muonTightIDSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonTightIDSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIDSF_tight *= muonTightIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIDSF_tight_systUP *= (muonTightIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonTightIDSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIDSF_tight_systDOWN *= (muonTightIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonTightIDSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))
                else:
                    xbin = muonLooseIDSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIDSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIDSF_loose *= muonLooseIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIDSF_loose_systUP *= (muonLooseIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonLooseIDSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIDSF_loose_systDOWN *= (muonLooseIDSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonLooseIDSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))

        muIsoSF_loose = 1.0
        muIsoSF_loose_systUP=1.0
        muIsoSF_loose_systDOWN=1.0
        muIsoSF_tight = 1.0
        muIsoSF_tight_systUP=1.0
        muIsoSF_tight_systDOWN=1.0
        for imu in range(nMu):
            mupt = muP4[imu].Pt()
            abeta = abs(muP4[imu].Eta())
            muiso = MuIso[imu]
            if uni < 0.54:
                if muiso < 0.15:
                    xbin = muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIsoSF_tight *= muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIsoSF_tight_systUP *= (muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIsoSF_tight_systDOWN *= (muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonTightIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
                elif muiso < 0.25:
                    xbin = muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetYaxis().FindBin(mupt)
                    muIsoSF_loose *= muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin)
                    muIsoSF_loose_systUP *= (muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) + muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorUp(xbin,ybin))
                    muIsoSF_loose_systDOWN *= (muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinContent(xbin,ybin) - muonLooseIsoSFs_EfficienciesAndSF_BCDEF.GetBinErrorLow(xbin,ybin))
            if uni > 0.54:
                if muiso < 0.15:
                    xbin = muonTightIsoSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonTightIsoSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIsoSF_tight *= muonTightIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIsoSF_tight_systUP *= (muonTightIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonTightIsoSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIsoSF_tight_systDOWN *= (muonTightIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonTightIsoSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))
                elif muiso < 0.25:
                    xbin = muonLooseIsoSFs_EfficienciesAndSF_GH.GetXaxis().FindBin(abeta)
                    ybin = muonLooseIsoSFs_EfficienciesAndSF_GH.GetYaxis().FindBin(mupt)
                    muIsoSF_loose *= muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin)
                    muIsoSF_loose_systUP *= (muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) + muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinErrorUp(xbin,ybin))
                    muIsoSF_loose_systDOWN *= (muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinContent(xbin,ybin) - muonLooseIsoSFs_EfficienciesAndSF_GH.GetBinErrorLow(xbin,ybin))

        muTracking_SF = 1.0
        muTracking_SF_systUP=1.0
        muTracking_SF_systDOWN=1.0
        for imu in range(nMu):
            abeta = abs(muP4[imu].Eta())
            muTracking_SF *= muonTrackingSFs_EfficienciesAndSF_BCDEFGH.Eval(abeta)
            ybin = muonTrackingSFs_EfficienciesAndSF_BCDEFGH.GetYaxis().FindBin(abeta)
            muTracking_SF_systUP *= (muonTrackingSFs_EfficienciesAndSF_BCDEFGH.Eval(abeta) + muonTrackingSFs_EfficienciesAndSF_BCDEFGH.GetErrorYhigh(ybin))
            muTracking_SF_systDOWN *= (muonTrackingSFs_EfficienciesAndSF_BCDEFGH.Eval(abeta) - muonTrackingSFs_EfficienciesAndSF_BCDEFGH.GetErrorYlow(ybin))


        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Electron reweight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        eleTrig_reweight = 1.0
        eleTrig_reweight_systUP = 1.0
        eleTrig_reweight_systDOWN = 1.0
        if nEle == 1:
            elept = eleP4[0].Pt()
            eleeta = eleP4[0].Eta()
        if nEle == 2:
            if eleP4[0].Pt() > eleP4[1].Pt():
                leadele=0
            else:
                leadele=1
            elept = eleP4[leadele].Pt()
            eleeta = eleP4[leadele].Eta()
        if nEle==1 or nEle==2:
            xbin = eleTrig_hEffEtaPt.GetXaxis().FindBin(eleeta)
            ybin = eleTrig_hEffEtaPt.GetYaxis().FindBin(elept)
            eleTrig_reweight *= eleTrig_hEffEtaPt.GetBinContent(xbin,ybin)
            eleTrig_reweight_systUP *= (eleTrig_hEffEtaPt.GetBinContent(xbin,ybin) + eleTrig_hEffEtaPt.GetBinErrorUp(xbin,ybin))
            eleTrig_reweight_systDOWN *= (eleTrig_hEffEtaPt.GetBinContent(xbin,ybin) - eleTrig_hEffEtaPt.GetBinErrorLow(xbin,ybin))
#            print 'eleTrig_reweight_systUP, eleTrig_reweight, eleTrig_reweight_systDOWN', eleTrig_reweight_systUP, eleTrig_reweight, eleTrig_reweight_systDOWN


        eleRecoSF = 1.0
        eleRecoSF_systUP = 1.0
        eleRecoSF_systDOWN = 1.0
        for iele in range(nEle):
            elept = eleP4[iele].Pt()
            eleeta = eleP4[iele].Eta()
            xbin = eleRecoSF_EGamma_SF2D.GetXaxis().FindBin(eleeta)
            ybin = eleRecoSF_EGamma_SF2D.GetYaxis().FindBin(elept)
            eleRecoSF *= eleRecoSF_EGamma_SF2D.GetBinContent(xbin,ybin)
            eleRecoSF_systUP *= (eleRecoSF_EGamma_SF2D.GetBinContent(xbin,ybin) + eleRecoSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
            eleRecoSF_systDOWN *= (eleRecoSF_EGamma_SF2D.GetBinContent(xbin,ybin) - eleRecoSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))
#            print 'eleRecoSF_systUP, eleRecoSF, eleRecoSF_systDOWN', eleRecoSF_systUP, eleRecoSF, eleRecoSF_systDOWN


        eleIDSF_loose = 1.0
        eleIDSF_loose_systUP = 1.0
        eleIDSF_loose_systDOWN = 1.0
        eleIDSF_tight = 1.0
        eleIDSF_tight_systUP = 1.0
        eleIDSF_tight_systDOWN = 1.0
        for iele in range(nEle):
            elept = eleP4[iele].Pt()
            eleeta = eleP4[iele].Eta()
            if elept > 30:
                xbin = eleTightIDSF_EGamma_SF2D.GetXaxis().FindBin(eleeta)
                ybin = eleTightIDSF_EGamma_SF2D.GetYaxis().FindBin(elept)
                eleIDSF_tight *= eleTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin)
                eleIDSF_tight_systUP *= (eleTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) + eleTightIDSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
                eleIDSF_tight_systDOWN *= (eleTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) - eleTightIDSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))
            else:
                xbin = eleLooseIDSF_EGamma_SF2D.GetXaxis().FindBin(eleeta)
                ybin = eleLooseIDSF_EGamma_SF2D.GetYaxis().FindBin(elept)
                eleIDSF_loose *= eleLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin)
                eleIDSF_loose_systUP *= (eleLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) + eleLooseIDSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
                eleIDSF_loose_systDOWN *= (eleLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) - eleLooseIDSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))

        #eleVetoCutBasedIDSF = 1.0
        #for iele in range(nEle):
        #    elept = eleP4[iele].Pt()
        #    eleeta = eleP4[iele].Eta()
        #    xbin = eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D.GetXaxis().FindBin(eleeta)
        #    ybin = eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D.GetYaxis().FindBin(elept)
        #    eleVetoCutBasedIDSF *= eleVetoCutBasedIDSF_egammaEffi_txt_EGM2D.GetBinContent(xbin,ybin)

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Photon reweight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        phoIDSF_loose = 1.0
        phoIDSF_loose_systUP = 1.0
        phoIDSF_loose_systDOWN = 1.0
        phoIDSF_tight = 1.0
        phoIDSF_tight_systUP = 1.0
        phoIDSF_tight_systDOWN = 1.0
        for pho in range(nPho):
            phopt = phoP4[ipho].Pt()
            phoeta = phoP4[ipho].Eta()
            if phopt > 175:
                xbin = phoTightIDSF_EGamma_SF2D.GetXaxis().FindBin(phoeta)
                ybin = phoTightIDSF_EGamma_SF2D.GetYaxis().FindBin(phopt)
                phoIDSF_tight *= phoTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin)
                phoIDSF_tight_systUP *= (phoTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) + phoTightIDSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
                phoIDSF_tight_systDOWN *= (phoTightIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) - phoTightIDSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))
            else:
                xbin = phoLooseIDSF_EGamma_SF2D.GetXaxis().FindBin(phoeta)
                ybin = phoLooseIDSF_EGamma_SF2D.GetYaxis().FindBin(phopt)
                phoIDSF_loose *= phoLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin)
                phoIDSF_loose_systUP *= (phoLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) + phoLooseIDSF_EGamma_SF2D.GetBinErrorUp(xbin,ybin))
                phoIDSF_loose_systDOWN *= (phoLooseIDSF_EGamma_SF2D.GetBinContent(xbin,ybin) - phoLooseIDSF_EGamma_SF2D.GetBinErrorLow(xbin,ybin))

        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## JEC uncertainity
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        #print ('\n')
        jecUncUP = 1.0
        jecUncDOWN = 1.0
        jecUnc = 1.0
        for jet in range(nJets):
            jecUnc *= myJetCorrUnc[jet]
        jecUncUP = 1+jecUnc
        jecUncDOWN = 1-jecUnc
        #print jecUncUP,jecUncDOWN
        #print ('\n')
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Pileup weight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
#        allpuweights = PUWeight()
#        len_puweight = len(allpuweights)
        puweight = 0.0
        if isData: puweight = 1.0
        if not isData:
#            if pu_nTrueInt  <= len_puweight: puweight = allpuweights[pu_nTrueInt-1]
#            if pu_nTrueInt  > len_puweight : puweight = 0.0
            if pu_nTrueInt < 100:
                puweight = pileup2016histo.GetBinContent(pu_nTrueInt)
            else:
                puweight = 1.


#            print pu_nTrueInt

        #print (len_puweight, pu_nTrueInt, puweight)
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Total weight
        # ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        if puweight == 0.0:
#            print 'Warning:: puweight is 0, setting it to 1'
            puweight = 1.0

        if genpTReweighting == 0.0:
#            print 'Warning:: genpTReweighting is 0, setting it to 1'
            genpTReweighting = 1.0

        if metTrig_firstmethodReweight == 0.0:
#            print 'Warning:: metTrig_Reweight is 0, setting it to 1'
            metTrig_firstmethodReweight = 1.0

        if metTrig_firstmethodReweight_up == 0.0:
#            print 'Warning:: metTrig_Reweight is 0, setting it to 1'
            metTrig_firstmethodReweight_up = 1.0

        if metTrig_firstmethodReweight_down == 0.0:
#            print 'Warning:: metTrig_Reweight is 0, setting it to 1'
            metTrig_firstmethodReweight_down = 1.0

        muweights = muonTrig_SF * muIDSF_loose * muIDSF_tight * muIsoSF_loose * muIsoSF_tight * muTracking_SF
        if muweights == 0.0:
#            print 'Warning:: muon weight is 0, setting it to 1'
            muweights = 1.0

        #eleweights = eleTrig_reweight * eleRecoSF * eleIDSF_loose * eleIDSF_tight * eleVetoCutBasedIDSF
        eleweights = eleTrig_reweight * eleRecoSF * eleIDSF_loose * eleIDSF_tight
        if eleweights == 0.0:
#            print 'Warning:: electron weight is 0, setting it to 1'
            eleweights = 1.0

        phoweights = phoIDSF_loose * phoIDSF_tight
        if phoweights == 0.0:
#            print 'Warning:: photon weight is 0, setting it to 1'
            phoweights = 1.0

        allweights = puweight * mcweight * genpTReweighting * eleweights * metTrig_firstmethodReweight * muweights*phoweights

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
        temp_weight_withOutBtag = allweights
        ## BTag Scale Factor
        if SR1njetcond:
            ij = ifirstjet
            if nJets>1: jj = isecondjet

            flav1 = jetflav(myJetHadronFlavor[ij])
            if nJets>1: flav2 = jetflav(myJetHadronFlavor[jj])

#            print ("ij, flav, pt, eta, ",ij, flav1, myJetP4[ij].Pt(), myJetP4[ij].Eta())
            reader1.eval_auto_bounds('central', 0, 1.2, 50.)
            sf_resolved1 = weightbtag(reader1, flav1, myJetP4[ij].Pt(), myJetP4[ij].Eta())
            if nJets>1: sf_resolved2 = weightbtag(reader1, flav2, myJetP4[jj].Pt(), myJetP4[jj].Eta())

#            print (sf_resolved1, sf_resolved2)
        elif SR2njetcond:
            ij = ifirstjet
            jj = isecondjet
            if nJets>2: jk = ithirdjet

            flav1 = jetflav(myJetHadronFlavor[ij])
            flav2 = jetflav(myJetHadronFlavor[jj])
            if nJets>2: flav3 = jetflav(myJetHadronFlavor[jj])

#            print ("ij, flav, pt, eta, ",ij, flav1, myJetP4[ij].Pt(), myJetP4[ij].Eta())
            reader1.eval_auto_bounds('central', 0, 1.2, 50.)
            sf_resolved1 = weightbtag(reader1, flav1, myJetP4[ij].Pt(), myJetP4[ij].Eta())
            sf_resolved2 = weightbtag(reader1, flav2, myJetP4[jj].Pt(), myJetP4[jj].Eta())
            if nJets>2: sf_resolved3 = weightbtag(reader1, flav3, myJetP4[jk].Pt(), myJetP4[jk].Eta())


        if SR1njetcond:
            if sf_resolved1[0]==0.0:
                sf_resolved1[0]=1.0
            allweights = allweights * sf_resolved1[0]
            if nJets>1:
                if sf_resolved2[0]==0.0:
                    sf_resolved2[0]=1.0
                allweights = allweights * sf_resolved2[0]

        if SR2njetcond:
            if sf_resolved1[0]==0.0:
                sf_resolved1[0]=1.0
            if sf_resolved2[0]==0.0:
                sf_resolved2[0]=1.0
            allweights = allweights * sf_resolved1[0] * sf_resolved2[0]
            if nJets>2:
                if sf_resolved3[0]==0.0:
                    sf_resolved3[0]=1.0
                allweights = allweights * sf_resolved3[0]

        temp_original_weight  = allweights
        allweights_jec_up = temp_original_weight*jecUncUP
        allquantities.weight_jec_up = allweights_jec_up
        allweights_jec_down= temp_original_weight*jecUncDOWN
        allquantities.weight_jec_down = allweights_jec_down
        allweights_ewkW_down = temp_original_weight
        allweights_ewkW_up = temp_original_weight
        allweights_ewkZ_down = temp_original_weight
        allweights_ewkZ_up = temp_original_weight
        allweights_ewkTop_down = temp_original_weight
        allweights_ewkTop_up = temp_original_weight
        allweights_metTrig_up = temp_original_weight
        allweights_metTrig_down = temp_original_weight

        allweights_metTrig_up = (allweights/metTrig_firstmethodReweight)*metTrig_firstmethodReweight_up
        allweights_metTrig_down = (allweights/metTrig_firstmethodReweight)*metTrig_firstmethodReweight_down
        temp_weight_withBtag = allweights/(eleweights*muweights)
        temp_weight_withBtag_noPhoSF = allweights/phoweights

        if isData: allweights = 1.0
        allweights_noPU = allweights/puweight


#----------------------------------------------------------------------------------------------------------------------------------------------------------------

        if samplename=="WJETS":
            allweights_ewkW_down = temp_original_weight/genpTReweighting
            allweights_ewkW_up = temp_original_weight*genpTReweighting
            allquantities.weight_ewkW_up  = allweights_ewkW_up
            allquantities.weight_ewkW_down  =  allweights_ewkW_down

        if samplename == "ZJETS":
            allweights_ewkZ_down = temp_original_weight/genpTReweighting
            allweights_ewkZ_up = temp_original_weight*genpTReweighting
            allquantities.weight_ewkZ_up  = allweights_ewkZ_up
            allquantities.weight_ewkZ_down  =  allweights_ewkZ_down
        if samplename == "TT":
            allweights_ewkTop_down = temp_original_weight/genpTReweighting
            allweights_ewkTop_up = temp_original_weight*genpTReweighting
            allquantities.weight_ewkTop_up  = allweights_ewkTop_up
            allquantities.weight_ewkTop_down  =  allweights_ewkTop_down
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

        #SR 1 Cutflow

        if keepevent:
            if SR1_Cut3_trigstatus:
                cutStatus['trig']+=allweights
                cutStatusSR1['trig']+=allweights

                if SR1_Cut8_pfMET:
                    cutStatus['MET']+=allweights
                    cutStatusSR1['MET']+=allweights

                    if SR1_Cut6_dPhi_jet_MET:
                        cutStatus['dPhicond']+=allweights
                        cutStatusSR1['dPhicond']+=allweights

                        if SR1_Cut1_nJets:
                            cutStatus['njets']+=allweights
                            cutStatusSR1['njets']+=allweights

                            if SR1_Cut2_nBjets:
                                cutStatus['nbjets']+=allweights
                                cutStatusSR1['nbjets']+=allweights

                                if SR1_Cut4_jet1:
                                    cutStatus['jet1']+=allweights
                                    cutStatusSR1['jet1']+=allweights

                                    if SR1_Cut5_jet2:
                                        cutStatus['jet2/3']+=allweights
                                        cutStatusSR1['jet2']+=allweights

                                        if SR1_Cut7_nLep:
                                            cutStatus['nlep']+=allweights
                                            cutStatusSR1['nlep']+=allweights

        #SR2 Cutflow

            if SR2_Cut3_trigstatus:
                cutStatus['trig']+=allweights
                cutStatusSR2['trig']+=allweights

                if SR2_Cut9_pfMET:
                    cutStatus['MET']+=allweights
                    cutStatusSR2['MET']+=allweights

                    if SR2_Cut7_dPhi_jet_MET:
                        cutStatus['dPhicond']+=allweights
                        cutStatusSR2['dPhicond']+=allweights

                        if SR2_Cut1_nJets:
                            cutStatus['njets']+=allweights
                            cutStatusSR2['njets']+=allweights

                            if SR2_Cut2_nBjets:
                                cutStatus['nbjets']+=allweights
                                cutStatusSR2['nbjets']+=allweights

                                if SR2_Cut4_jet1:
                                    cutStatus['jet1']+=allweights
                                    cutStatusSR2['jet1']+=allweights

                                    if SR2_Cut5_jet2:
                                        cutStatusSR2['jet2']+=allweights

                                        if SR2_Cut6_jet3:
                                            cutStatus['jet2/3']+=allweights
                                            cutStatusSR2['jet3']+=allweights

                                            if SR2_Cut8_nLep:
                                                cutStatus['nlep']+=allweights
                                                cutStatusSR2['nlep']+=allweights


        # 2e cutflow

        for CRreg in regionnames:
            exec("CR"+CRreg+"CutFlow['datatrig']+=allweights")


        if EleCRtrigstatus:
            CR2e1bCutFlow['trig']+=allweights
            CR2e2bCutFlow['trig']+=allweights

            if ZeeRecoil>200.:
                CR2e1bCutFlow['recoil']+=allweights
                CR2e2bCutFlow['recoil']+=allweights

                if pfMet > 0.:
                    CR2e1bCutFlow['realMET']+=allweights
                    CR2e2bCutFlow['realMET']+=allweights

                    if ZeeMass>70. and ZeeMass<110.:
                        CR2e1bCutFlow['mass']+=allweights
                        CR2e2bCutFlow['mass']+=allweights

                        if ZdPhicond:
                            CR2e1bCutFlow['dPhicond']+=allweights
                            CR2e2bCutFlow['dPhicond']+=allweights

                            if nJets==1 or nJets==2:
                                CR2e1bCutFlow['njets']+=allweights

                                if nBjets==1:
                                    CR2e1bCutFlow['nbjets']+=allweights

                                    if jetcond:
                                        CR2e1bCutFlow['jetconds']+=allweights

                                        if nEle==2 and nMu==0:
                                            CR2e1bCutFlow['nlep/npho']+=allweights
                                            if myEles[0].Pt()>myEles[1].Pt():
                                                iLeadLep=0
                                                iSecondLep=1
                                            else:
                                                iLeadLep=1
                                                iSecondLep=0

                                            if myEles[iLeadLep].Pt() > 30. and myEleTightID[iLeadLep] and myEles[iSecondLep].Pt() > 10. and myEleLooseID[iSecondLep]:
                                                CR2e1bCutFlow['lepconds']+=allweights

                            if nJets==2 or nJets==3:
                                CR2e2bCutFlow['njets']+=allweights

                                if nBjets==2:
                                    CR2e2bCutFlow['nbjets']+=allweights

                                    if jetcond and SR2jet2:
                                        CR2e2bCutFlow['jetconds']+=allweights

                                        if nEle==2 and nMu==0:
                                            CR2e2bCutFlow['nlep/npho']+=allweights
                                            if myEles[0].Pt()>myEles[1].Pt():
                                                iLeadLep=0
                                                iSecondLep=1
                                            else:
                                                iLeadLep=1
                                                iSecondLep=0

                                            if myEles[iLeadLep].Pt() > 30. and myEleTightID[iLeadLep] and myEles[iSecondLep].Pt() > 10. and myEleLooseID[iSecondLep]:
                                                CR2e2bCutFlow['lepconds']+=allweights



        if MuCRtrigstatus:
            CR2mu1bCutFlow['trig']+=allweights
            CR2mu2bCutFlow['trig']+=allweights

            if ZmumuRecoil>200.:
                CR2mu1bCutFlow['recoil']+=allweights
                CR2mu2bCutFlow['recoil']+=allweights

                if pfMet > 0.:
                    CR2mu1bCutFlow['realMET']+=allweights
                    CR2mu2bCutFlow['realMET']+=allweights

                    if ZmumuMass>70. and ZmumuMass<110.:
                        CR2mu1bCutFlow['mass']+=allweights
                        CR2mu2bCutFlow['mass']+=allweights

                        if ZdPhicond:
                            CR2mu1bCutFlow['dPhicond']+=allweights
                            CR2mu2bCutFlow['dPhicond']+=allweights

                            if nJets==1 or nJets==2:
                                CR2mu1bCutFlow['njets']+=allweights

                                if nBjets==1:
                                    CR2mu1bCutFlow['nbjets']+=allweights

                                    if jetcond:
                                        CR2mu1bCutFlow['jetconds']+=allweights

                                        if nMu==2 and nEle==0:
                                            CR2mu1bCutFlow['nlep/npho']+=allweights
                                            if myMuos[0].Pt()>myMuos[1].Pt():
                                                iLeadLep=0
                                                iSecondLep=1
                                            else:
                                                iLeadLep=1
                                                iSecondLep=0

                                            if myMuos[iLeadLep].Pt() > 30. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15 and myMuos[iSecondLep].Pt() > 10. and myMuLooseID[iSecondLep] and myMuIso[iSecondLep]<0.25:
                                                CR2mu1bCutFlow['lepconds']+=allweights

                            if nJets==2 or nJets==3:
                                CR2mu2bCutFlow['njets']+=allweights

                                if nBjets==2:
                                    CR2mu2bCutFlow['nbjets']+=allweights

                                    if jetcond and SR2jet2:
                                        CR2mu2bCutFlow['jetconds']+=allweights

                                        if nMu==2 and nEle==0:
                                            CR2mu2bCutFlow['nlep/npho']+=allweights
                                            if myMuos[0].Pt()>myMuos[1].Pt():
                                                iLeadLep=0
                                                iSecondLep=1
                                            else:
                                                iLeadLep=1
                                                iSecondLep=0

                                            if myMuos[iLeadLep].Pt() > 30. and myMuTightID[iLeadLep] and myMuIso[iLeadLep]<0.15 and myMuos[iSecondLep].Pt() > 10. and myMuLooseID[iSecondLep] and myMuIso[iSecondLep]<0.25:
                                                CR2mu2bCutFlow['lepconds']+=allweights


        if EleCRtrigstatus:
            CR1e1bCutFlow['trig']+=allweights
            CR1e2bCutFlow['trig']+=allweights

            if WenuRecoil>200.:
                CR1e1bCutFlow['recoil']+=allweights
                CR1e2bCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1e1bCutFlow['realMET']+=allweights
                    CR1e2bCutFlow['realMET']+=allweights

                    if Wenumass>50. and  Wenumass<160.:

                    #if True:
                        CR1e1bCutFlow['mass']+=allweights
                        CR1e2bCutFlow['mass']+=allweights

                        if WdPhicond:
                            CR1e1bCutFlow['dPhicond']+=allweights
                            CR1e2bCutFlow['dPhicond']+=allweights

                            if nJets==1 or nJets==2:
                                CR1e1bCutFlow['njets']+=allweights

                                if nBjets==1:
                                    CR1e1bCutFlow['nbjets']+=allweights

                                    if jetcond:
                                        CR1e1bCutFlow['jetconds']+=allweights

                                        if nEle==1 and nMu==0:
                                            CR1e1bCutFlow['nlep/npho']+=allweights

                                            if myEles[0].Pt() > 30. and myEleTightID[0]:
                                                CR1e1bCutFlow['lepconds']+=allweights

                            if nJets==2 or nJets==3:
                                CR1e2bCutFlow['njets']+=allweights

                                if nBjets==2:
                                    CR1e2bCutFlow['nbjets']+=allweights

                                    if jetcond and SR2jet2:
                                        CR1e2bCutFlow['jetconds']+=allweights

                                        if nEle==1 and nMu==0:
                                            CR1e2bCutFlow['nlep/npho']+=allweights

                                            if myEles[0].Pt() > 30. and myEleTightID[0]:
                                                CR1e2bCutFlow['lepconds']+=allweights



  #Cutflow
        if MuCRtrigstatus:
            CR1mu1bCutFlow['trig']+=allweights
            CR1mu2bCutFlow['trig']+=allweights

            if WmunuRecoil>200.:
                CR1mu1bCutFlow['recoil']+=allweights
                CR1mu2bCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1mu1bCutFlow['realMET']+=allweights
                    CR1mu2bCutFlow['realMET']+=allweights

                    if Wmunumass>50. and Wmunumass<160.:
                    #if True:
                        CR1mu1bCutFlow['mass']+=allweights
                        CR1mu2bCutFlow['mass']+=allweights

                        if WdPhicond:
                            CR1mu1bCutFlow['dPhicond']+=allweights
                            CR1mu2bCutFlow['dPhicond']+=allweights

                            if nJets==1 or nJets==2:
                                CR1mu1bCutFlow['njets']+=allweights

                                if nBjets==1:
                                    CR1mu1bCutFlow['nbjets']+=allweights

                                    if jetcond:
                                        CR1mu1bCutFlow['jetconds']+=allweights

                                        if nEle==0 and nMu==1:
                                            CR1mu1bCutFlow['nlep/npho']+=allweights

                                            if myMuos[0].Pt() > 30. and myMuTightID[0]:
                                                CR1mu1bCutFlow['lepconds']+=allweights

                            if nJets==2 or nJets==3:
                                CR1mu2bCutFlow['njets']+=allweights

                                if nBjets==2:
                                    CR1mu2bCutFlow['nbjets']+=allweights

                                    if jetcond and SR2jet2:
                                        CR1mu2bCutFlow['jetconds']+=allweights

                                        if nEle==0 and nMu==1:
                                            CR1mu2bCutFlow['nlep/npho']+=allweights

                                            if myMuos[0].Pt() > 30. and myMuTightID[0]:
                                                CR1mu2bCutFlow['lepconds']+=allweights



 #Cutflow
        if MuCRtrigstatus:
            CR1mu1e1bCutFlow['trig']+=allweights
            CR1mu1e2bCutFlow['trig']+=allweights

            if TOPRecoil>200.:
                CR1mu1e1bCutFlow['recoil']+=allweights
                CR1mu1e2bCutFlow['recoil']+=allweights

                if pfMet > 50.:
                    CR1mu1e1bCutFlow['realMET']+=allweights
                    CR1mu1e2bCutFlow['realMET']+=allweights
                    CR1mu1e1bCutFlow['mass']+=allweights
                    CR1mu1e2bCutFlow['mass']+=allweights

                    if TopdPhicond:
                        CR1mu1e1bCutFlow['dPhicond']+=allweights
                        CR1mu1e2bCutFlow['dPhicond']+=allweights

                        if nJets==1 or nJets==2:
                            CR1mu1e1bCutFlow['njets']+=allweights

                            if nBjets==1:
                                CR1mu1e1bCutFlow['nbjets']+=allweights

                                if jetcond:
                                    CR1mu1e1bCutFlow['jetconds']+=allweights

                                    if nEle==1 and nMu==1:
                                        CR1mu1e1bCutFlow['nlep/npho']+=allweights

                                        if myEles[0].Pt() > 30. and myEleTightID[0] and myMuos[0].Pt() > 30. and myMuTightID[0] and myMuIso[0]<0.15:
                                            CR1mu1e1bCutFlow['lepconds']+=allweights

                        if nJets==2 or nJets==3:
                            CR1mu1e2bCutFlow['njets']+=allweights

                            if nBjets==2:
                                CR1mu1e2bCutFlow['nbjets']+=allweights

                                if jetcond and SR2jet2:
                                    CR1mu1e2bCutFlow['jetconds']+=allweights

                                    if nEle==1 and nMu==1:
                                        CR1mu1e2bCutFlow['nlep/npho']+=allweights

                                        if myEles[0].Pt() > 30. and myEleTightID[0] and myMuos[0].Pt() > 30. and myMuTightID[0] and myMuIso[0]<0.15:
                                            CR1mu1e2bCutFlow['lepconds']+=allweights


 #Cutflow
        if PhotonCRtrigstatus:
            CR1gamma1bCutFlow['trig']+=allweights
            CR1gamma2bCutFlow['trig']+=allweights


            if GammaRecoil>200.:
                CR1gamma1bCutFlow['recoil']+=allweights
                CR1gamma2bCutFlow['recoil']+=allweights


                if pfMet > 0.:
                    CR1gamma1bCutFlow['realMET']+=allweights
                    CR1gamma2bCutFlow['realMET']+=allweights
                    CR1gamma1bCutFlow['mass']+=allweights
                    CR1gamma2bCutFlow['mass']+=allweights

                    if GammaPhicond:
                        CR1gamma1bCutFlow['dPhicond']+=allweights
                        CR1gamma2bCutFlow['dPhicond']+=allweights

                        if nJets==1 or nJets==2:
                            CR1gamma1bCutFlow['njets']+=allweights

                            if nBjets==1:
                                CR1gamma1bCutFlow['nbjets']+=allweights

                                if jetcond:
                                    CR1gamma1bCutFlow['jetconds']+=allweights

                                    if nPho==1 and nEle==0 and nMu==0:
                                        CR1gamma1bCutFlow['nlep/npho']+=allweights

                                        if myPhos[0].Pt() > 175. and myPhoTightID[0] and myPhoLooseID[0]:
                                            CR1gamma1bCutFlow['lepconds']+=allweights

                        if nJets==2 or nJets==3:
                            CR1gamma2bCutFlow['njets']+=allweights

                            if nBjets==2:
                                CR1gamma2bCutFlow['nbjets']+=allweights

                                if jetcond and SR2jet2:
                                    CR1gamma2bCutFlow['jetconds']+=allweights

                                    if nPho==1 and nEle==0 and nMu==0:
                                        CR1gamma2bCutFlow['nlep/npho']+=allweights

                                        if myPhos[0].Pt() > 175. and myPhoTightID[0] and myPhoLooseID[0]:
                                            CR1gamma2bCutFlow['lepconds']+=allweights


        # QCD cutflow

        if QCD1b_Cut3_trigstatus:
            CRQCD1bCutFlow['trig']+=allweights

            if QCD1b_Cut8_pfMET:
                CRQCD1bCutFlow['recoil']+=allweights

                if QCD1b_Cut6_dPhi_jet_MET:
                    CRQCD1bCutFlow['dPhicond']+=allweights

                    if QCD1b_Cut1_nJets:
                        CRQCD1bCutFlow['njets']+=allweights

                        if QCD1b_Cut2_nBjets:
                            CRQCD1bCutFlow['nbjets']+=allweights

                            if QCD1b_Cut4_jet1:
                                if QCD1b_Cut5_jet2:
                                    CRQCD1bCutFlow['jetconds']+=allweights

                                    if QCD1b_Cut7_nLep:
                                        CRQCD1bCutFlow['nlep/npho']+=allweights
                                        CRQCD1bCutFlow['lepconds']+=allweights

        if QCD2b_Cut3_trigstatus:
            CRQCD2bCutFlow['trig']+=allweights

            if QCD2b_Cut9_pfMET:
                CRQCD2bCutFlow['recoil']+=allweights

                if QCD2b_Cut7_dPhi_jet_MET:
                    CRQCD2bCutFlow['dPhicond']+=allweights

                    if QCD2b_Cut1_nJets:
                        CRQCD2bCutFlow['njets']+=allweights

                        if QCD2b_Cut2_nBjets:
                            CRQCD2bCutFlow['nbjets']+=allweights

                            if QCD2b_Cut4_jet1:
                                if QCD2b_Cut5_jet2:
                                    if QCD2b_Cut6_jet3:
                                        CRQCD2bCutFlow['jetconds']+=allweights

                                        if QCD2b_Cut8_nLep:
                                            CRQCD2bCutFlow['nlep/npho']+=allweights
                                            CRQCD2bCutFlow['lepconds']+=allweights
 # ---
        #CR Summary
        if isZeeCR1:
            CRSummary['2e1b']+=allweights
            CRSummaryEle['2e1b']+=allweights
        if isZeeCR2:
            CRSummary['2e2b']+=allweights
            CRSummaryEle['2e2b']+=allweights
        if isZmumuCR1:
            CRSummary['2#mu1b']+=allweights
            CRSummaryMu['2#mu1b']+=allweights
        if isZmumuCR2:
            CRSummary['2#mu2b']+=allweights
            CRSummaryMu['2#mu2b']+=allweights

        if isWenuCR1:
            CRSummary['1e1b']+=allweights
            CRSummaryEle['1e1b']+=allweights
        if isWenuCR2:
            CRSummary['1e2b']+=allweights
            CRSummaryEle['1e2b']+=allweights
        if isWmunuCR1:
            CRSummary['1#mu1b']+=allweights
            CRSummaryMu['1#mu1b']+=allweights
        if isWmunuCR2:
            CRSummary['1#mu2b']+=allweights
            CRSummaryMu['1#mu2b']+=allweights

        if isTopCR1:
            CRSummary['1#mu1e1b']+=allweights
            CRSummaryMu['1#mu1e1b']+=allweights
        if isTopCR2:
            CRSummary['1#mu1e2b']+=allweights
            CRSummaryMu['1#mu1e2b']+=allweights


 #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
        allquantities.met             = pfMet
        allquantities.N_e             = nEle
        allquantities.N_mu            = nMu
        allquantities.N_tau           = nTauLooseEleMu
        allquantities.N_Pho           = nPho
        allquantities.N_b             = nBjets
        allquantities.N_j             = nJets
        allquantities.weight          = allweights
        allquantities.weight_NoPU     = allweights_noPU
        allquantities.weight_met_up   = allweights_metTrig_up
        allquantities.weight_met_down = allweights_metTrig_down
        allquantities.totalevents     = 1

        btag_sysnum=0
        for btag_sysnum in[1,2]:
            allweights = temp_weight_withOutBtag
            if SR1njetcond:
                if sf_resolved1[btag_sysnum]==0.0: sf_resolved1[btag_sysnum]=1.0
                allweights = allweights*sf_resolved1[btag_sysnum]
                if nJets>1:
                    if sf_resolved2[btag_sysnum]==0.0: sf_resolved2[btag_sysnum]=1.0
                    allweights = allweights *sf_resolved2[btag_sysnum]
            if SR2njetcond:
                if sf_resolved1[btag_sysnum]==0.0: sf_resolved1[btag_sysnum]=1.0
                if sf_resolved2[btag_sysnum]==0.0: sf_resolved2[btag_sysnum]=1.0
                allweights = allweights * sf_resolved1[btag_sysnum] * sf_resolved2[btag_sysnum]
                if nJets>2:
                    if sf_resolved3[btag_sysnum]==0.0: sf_resolved3[btag_sysnum]=1.0
                    allweights = allweights * sf_resolved3[btag_sysnum]
#                print 'btag central weight', temp_original_weight
                if btag_sysnum==2:
                    allquantities.weight_btag_up = allweights
#                    print 'btag up weight', allweights
                if btag_sysnum==1:
                    allquantities.weight_btag_down = allweights
#                    print 'btag down weight', allweights
        allweights = temp_weight_withBtag
        muweights_systUP = muonTrig_SF_systUP * muIDSF_loose_systUP * muIDSF_tight_systUP * muIsoSF_loose_systUP * muIsoSF_tight_systUP * muTracking_SF_systUP
        muweights_systDOWN = muonTrig_SF_systDOWN * muIDSF_loose_systDOWN * muIDSF_tight_systDOWN * muIsoSF_loose_systDOWN * muIsoSF_tight_systDOWN * muTracking_SF_systDOWN
        eleweights_systUP = eleTrig_reweight_systUP * eleRecoSF_systUP * eleIDSF_loose_systUP * eleIDSF_tight_systUP
        eleweights_systDOWN = eleTrig_reweight_systDOWN * eleRecoSF_systDOWN * eleIDSF_loose_systDOWN * eleIDSF_tight_systDOWN
        if muweights_systUP == 0.0:
            muweights_systUP = 1.0
        if muweights_systDOWN == 0.0:
            muweights_systDOWN = 1.0
        if eleweights_systUP == 0.0:
            eleweights_systUP = 1.0
        if eleweights_systDOWN == 0.0:
            eleweights_systDOWN = 1.0
#                print 'muweights_systUP, eleweights_systUP',muweights_systUP ,eleweights_systUP
#                print 'muweights_systDOWN, eleweights_systDOWN',muweights_systDOWN,eleweights_systDOWN
        allweights = allweights * muweights_systUP * eleweights_systUP
        allquantities.weight_lep_up = allweights
#        if abs(allweights-temp_weight_withBtag) > 0.001:
#            print 'lep up value', allweights
        allweights = temp_weight_withBtag
#        if abs(allweights-temp_weight_withBtag) > 0.001:
#            print 'lep central weight', allweights
        allweights = allweights * muweights_systDOWN * eleweights_systDOWN
        allquantities.weight_lep_down = allweights
#        if abs(allweights-temp_weight_withBtag) > 0.001:
#            print 'lep down value', allweights
        allweights = temp_weight_withBtag_noPhoSF
        phoweights_systUP = phoIDSF_loose_systUP * phoIDSF_tight_systUP
        allquantities.weight_pho_up = allweights*phoweights_systUP
        phoweights_systDOWN = phoIDSF_loose_systDOWN * phoIDSF_tight_systDOWN
        allquantities.weight_pho_down = allweights*phoweights_systDOWN
        nPV = myJetNPV

        allquantities.PuReweightPV = nPV
        allquantities.noPuReweightPV = nPV

        if nMu==2 and nEle==0 and MuCRtrigstatus:
            allquantities.mu_PuReweightPV = nPV
            allquantities.mu_noPuReweightPV = nPV

        if nEle==2 and nMu==0 and EleCRtrigstatus:
            allquantities.ele_PuReweightPV = nPV
            allquantities.ele_noPuReweightPV = nPV

        if nPho==1 and nEle==0 and nMu==0 and PhotonCRtrigstatus:
            allquantities.pho_PuReweightPV = nPV
            allquantities.pho_noPuReweightPV = nPV

        #print (allquantities.regime, allquantities.met,allquantities.mass )
        allquantities.FillRegionHisto()
        allquantities.FillHisto()

    #print cutStatus
    NEntries_Weight = h_t_weight.Integral()
    NEntries_total  = h_t.Integral()
    cutStatus['total'] = int(NEntries_total)
    cutStatusSR1['total'] = int(NEntries_total)
    cutStatusSR2['total'] = int(NEntries_total)

    for CRreg in regionnames:
        exec("CR"+CRreg+"CutFlow['total']=int(NEntries_total)")


    #cutStatusSR1['pfmet'] = cutStatus['pfmet']
    #cutStatusSR2['pfmet'] = cutStatus['pfmet']
    print "Total events =", int(NEntries_total)
    print "Preselected events=", cutStatus['preselection']
    print "Selected events =", npass

    # Cutflow
    cutflowTable=""
    cutflowHeader=""
    cutflowvalues=[]
    #cutflownames=['total','preselection','pfmet','njet+nBjet','jet1','jet2/3','lep']
    for cutflowname in cutflownames:
        cutflowvalues.append(cutStatus[cutflowname])
        cutflowTable += str(cutStatus[cutflowname])+" "
        cutflowHeader += cutflowname+" "

    cutflowvaluesSR1=[]
    #cutflownamesSR1=['total','preselection','pfmet','njet+nBjet','jet1','jet2','lep']
    for cutflowname in cutflownamesSR1:
        cutflowvaluesSR1.append(cutStatusSR1[cutflowname])

    cutflowvaluesSR2=[]
    #cutflownamesSR2=['total','preselection','pfmet','njet+nBjet','jet1','jet2','jet3','lep']
    for cutflowname in cutflownamesSR2:
        cutflowvaluesSR2.append(cutStatusSR2[cutflowname])

    # CR counts
    CRTable=""
    CRHeader=""
    CRvalues=[]
    for CRname in CRs:
        CRvalues.append(CRStatus[CRname])
        CRTable += str(CRStatus[CRname])+" "
        CRHeader += CRname+" "

    #Cutflows for SR1 and SR2
    print "\nCutflow:"
    print cutStatus
    print
    print "SR1:"
    print cutStatusSR1
    print
    print "SR2:"
    print cutStatusSR2
    #print
    #print "CRs:"
    #print CRStatus
#    print
#    print "CR Cutflow:"
#    print CRCutFlow
    print

    CRcutflowvaluesSet=[]
    CRcutnames=['total','preselection']+CRcutnames
    for CRreg in regionnames:
        CFvalues=[]
        for cutname in CRcutnames:
            exec("CFvalues.append(CR"+CRreg+"CutFlow['"+cutname+"'])")
        CRcutflowvaluesSet.append(CFvalues)

    print CRSummary

    allquantities.WriteHisto((NEntries_total,NEntries_Weight,npass,cutflowvalues,cutflownames,cutflowvaluesSR1,cutflownamesSR1, cutflowvaluesSR2,cutflownamesSR2,CRvalues,CRs,regionnames,CRcutnames,CRcutflowvaluesSet, CRSummary,regNames, CRSummaryMu,regNamesMu, CRSummaryEle,regNamesEle))

    if NEntries > 0:
        eff=round(float(npass/float(NEntries_total)),5)
    else:
        eff = "NA"
    print "efficiency =", eff

#    os.system("mkdir -p "+outputdir+'/efficiencyfiles/')

#    f = open(outputdir+'/efficiencyfiles/'+textfile, 'w')
#    f.write(str(eff)+"\n\n#Cutflow Table:\n"+cutflowHeader[:-1]+"\n"+cutflowTable[:-1]+"\n\n#CR Table:\n"+CRHeader[:-1]+"\n"+CRTable[:-1])
    print "ROOT file written to", outfilename
#    print "Log written to "+outputdir+'/efficiencyfiles/'+textfile
#    f.close()
    print "Completed."




def CheckFilter(filterName, filterResult,filtercompare):
    ifilter_=0
    filter1 = False
    for ifilter in filterName:
        filter1 = (ifilter.find(filtercompare) != -1)  & (bool(filterResult[ifilter_]) == True)
        if filter1: break
        ifilter_ = ifilter_ + 1
    return filter1





######################################
######################################
######################################
def MakeTable():
    print "called MakeTable"
    files= [inputfilename]
    legend=legendTemplate
    prefix="V_met_"
    effnamelist = [prefix + ihisto  for ihisto in namelist]
    inputfile={}
    histList=[]
    for ifile_ in range(len(files)):
        print ("opening file  "+files[ifile_])
        inputfile[ifile_] = TFile( files[ifile_] )
        print "fetching histograms"
        for ihisto_ in range(len(effnamelist)):
            histo = inputfile[ifile_].Get(effnamelist[ihisto_])
            histList.append(histo)

    for ih in range(len(histList)):
        eff = ("%0.4f" % float(histList[ih].Integral()/histList[0].Integral()))
        toprint =  legendTemplate[ih] + " & " + str(eff) + " \\\\"
        print toprint


def DeltaR(p4_1, p4_2):
    eta1 = p4_1.Eta()
    eta2 = p4_2.Eta()
    eta = eta1 - eta2
    eta_2 = eta * eta

    phi1 = p4_1.Phi()
    phi2 = p4_2.Phi()
    phi = Phi_mpi_pi(phi1-phi2)
    phi_2 = phi * phi

    return math.sqrt(eta_2 + phi_2)

def DeltaPhi(phi1,phi2):
   phi = Phi_mpi_pi(phi1-phi2)

   return abs(phi)

def DeltaR(P4_1,P4_2):
    return math.sqrt(  (  P4_1.Eta()-P4_2.Eta() )**2  + (  DeltaPhi(P4_1.Phi(),P4_2.Phi()) )**2 )


def Phi_mpi_pi(x):
    kPI = 3.14159265358979323846
    kTWOPI = 2 * kPI

    while (x >= kPI): x = x - kTWOPI;
    while (x < -kPI): x = x + kTWOPI;
    return x;

def weightbtag(reader, flav, pt, eta):
    sf_c = reader.eval_auto_bounds('central', flav, eta, pt)
    sf_low = reader.eval_auto_bounds('down', flav, eta, pt)
    sf_up  = reader.eval_auto_bounds('up', flav, eta, pt)
    btagsf = [sf_c, sf_low, sf_up]
    return btagsf

def jetflav(flav):
    if flav == 5:
        flavor = 0
    elif flav == 4:
        flavor = 1
    else:
        flavor = 2
    return flavor




def GenWeightProducer(sample,nGenPar, genParId, genMomParId, genParSt,genParP4):
    pt__=0;
    #print " inside gen weight "
    k2=1.0
    #################
    # WJets
    #################
    if sample=="WJETS":
        goodLepID = []
        for ig in range(nGenPar):
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]
            if ( (abs(PID) != 11) & (abs(PID) != 12) &  (abs(PID) != 13) & (abs(PID) != 14) &  (abs(PID) != 15) &  (abs(PID) != 16) ): continue
            if ( ( (status != 1) & (abs(PID) != 15)) | ( (status != 2) & (abs(PID) == 15)) ): continue
            if ( (abs(momPID) != 24) & (momPID != PID) ): continue
            goodLepID.append(ig)

        if len(goodLepID) == 2 :
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            l4_z = l4_thisLep + l4_thatLep

            pt = l4_z.Pt()
            pt__ = pt

            k2 = -0.830041 + 7.93714 *TMath.Power( pt - (-877.978) ,(-0.213831) ) ;

    #################
    #ZJets
    #################
    if sample == "ZJETS":
        goodLepID = []
        for ig in range(nGenPar):
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]


            if ( (abs(PID) != 12) &  (abs(PID) != 14) &  (abs(PID) != 16) ) : continue
            if ( status != 1 ) : continue
            if ( (momPID != 23) & (momPID != PID) ) : continue
            goodLepID.append(ig)

        if len(goodLepID) == 2 :
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            l4_z = l4_thisLep + l4_thatLep
            pt = l4_z.Pt()
            k2 = -0.180805 + 6.04146 *TMath.Power( pt - (-759.098) ,(-0.242556) ) ;

    #################
    #TTBar
    #################
    if (sample=="TT"):
        goodLepID = []
        for ig in range(nGenPar):
            PID    = genParId[ig]
            momPID = genMomParId[ig]
            status = genParSt[ig]
            if ( abs(PID) == 6) :
                goodLepID.append(ig)
        if(len(goodLepID)==2):
            l4_thisLep = genParP4[goodLepID[0]]
            l4_thatLep = genParP4[goodLepID[1]]
            pt1 = TMath.Min(400.0, l4_thisLep.Pt())
            pt2 = TMath.Min(400.0, l4_thatLep.Pt())

            w1 = TMath.Exp(0.156 - 0.00137*pt1);
            w2 = TMath.Exp(0.156 - 0.00137*pt2);
            k2 =  1.001*TMath.Sqrt(w1*w2);

    if(sample=="all"):
        k2 = 1.0

    return k2


def MT(Pt, met, dphi):
    return ROOT.TMath.Sqrt( 2 * Pt * met * (1.0 - ROOT.TMath.Cos(dphi)) )

if __name__ == "__main__":
    ## analyze the tree and make histograms and all the 2D plots and Efficiency plots.
    if options.analyze:
        print "now calling analyzedataset"
        AnalyzeDataSet()
