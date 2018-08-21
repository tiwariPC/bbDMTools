import elementtree.ElementTree as ET
from ROOT import TLorentzVector, TCanvas, TH1F,TLegend,gStyle,TLatex
import os
import glob

gStyle.SetFrameLineWidth(3)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)
gStyle.SetLegendBorderSize(0)
gStyle.SetFillColor(2)
gStyle.SetLineWidth(1)
gStyle.SetHistFillStyle(2)

dirpath = '/eos/user/p/ptiwari/LHE_2HDMa_2017_bbDM/LHE_FileDir/'

filelist = [f for f in os.listdir(dirpath) if os.path.isdir(os.path.join(dirpath, f))]
runs = []
for f in filelist:
    if 'MH3_600_' in f:
        runs.append(f)
print(runs)

hists=[]


for i in runs:
    genMET=[]
    h_genMET=TH1F('genMET'+i,"",100,0,1000)
    file=glob.glob(dirpath+i+'/*')
    tree=ET.parse(str(file[0]))
    root=tree.getroot()
    for child in root:
        if (child.tag=='event'):

            lines=child.text.strip().split('\n')
            event_header=lines[0].strip()
            num_part=int(event_header.split()[0].strip())
            if float (event_header.split()[2]) > 0:

                phi=[s for s in lines if s.split()[0]=='55']
                chi=[s for s in lines if s.split()[0]=='52']
                chibar=[s for s in lines if s.split()[0]=='-52']
                b=[s for s in lines if s.split()[0]=='5']
                bbar=[s for s in lines if s.split()[0]=='-5']

                if phi:
                    px=float (phi[0].split()[6])
                    py=float (phi[0].split()[7])
                    pz=float (phi[0].split()[8])
                    e=float (phi[0].split()[9])
                    p=TLorentzVector(px,py,pz,e)
                    # genMET.append(p.Pt())

                px1=float (chi[0].split()[6])
                py1=float (chi[0].split()[7])
                pz1=float (chi[0].split()[8])
                e1=float (chi[0].split()[9])

                px2=float (chibar[0].split()[6])
                py2=float (chibar[0].split()[7])
                pz2=float (chibar[0].split()[8])
                e2=float (chibar[0].split()[9])

                p1=TLorentzVector(px1,py1,pz1,e1)
                p2=TLorentzVector(px2,py2,pz2,e2)

                pi=p1+p2
                genMET.append(pi.Pt())
                if pi.Pt() < 100:
                    print (child.text)
                    print ("met",pi.Pt())

    for met in genMET:
            h_genMET.Fill(met)
    hists.append(h_genMET)
c = TCanvas()
legend=TLegend(.53,.59,.87,.89)
legend.SetTextSize(0.038)
leg_entry=['M_{a}=100 GeV','M_{a}=200 GeV','M_{a}=300 GeV','M_{a}=400 GeV','M_{A}=500 GeV']

cmsname = TLatex();
cmsname.SetTextSize(0.036)
cmsname.SetTextAlign(12)
cmsname.SetNDC(1)
cmsname.SetTextFont(61)
#print len(hists)

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
        
cmsname.DrawLatex(0.12, .94, "2HDM+a  bb+DM"+" "*15+"MA = 600")
legend.Draw()
c.SetLogy()
c.update()
c.SaveAs("Combined_mA.pdf")
