/*
 * HWWAnalyzer.h
 *
 *  Created on: Dec 14, 2010
 *      Author: ale
 */

#ifndef HWWANALYZER_H_
#define HWWANALYZER_H_

#include "HWWAnalysis/CutBasedAnalyzer/interface/UserAnalyzer.h"
#include <bitset>

class HWWEvent;
class HWWNtuple;
class TTree;
class TH1F;
class TH2F;
class TParticlePDG;


class HWWAnalyzer : public UserAnalyzer {
public:
	HWWAnalyzer(int argc,char** argv);
	virtual ~HWWAnalyzer();

	virtual Bool_t Notify();
	virtual void Book();
	virtual void BeginJob();
	virtual void Process( Long64_t iEvent );
	virtual void calcNtuple();
	virtual void cutAndFill();
	virtual void EndJob();

protected:

	struct HiggsCutSet {
		int hMass;
		int ll;
		float minPtHard;
		float minPtSoft;
		float maxMll;
		float maxDphi;
		void print();
	};

	enum Lep_t {
		kEl_t,
		kMu_t
	};

	enum LL_t {
		kElEl_t = kEl_t*11,
		kElMu_t = kEl_t*10+kMu_t,
		kMuEl_t = kMu_t*10+kEl_t,
		kMuMu_t = kMu_t*11
	};

	enum HCuts_t {
		kDileptons = 1,
		kMinMet,
		kMinMll,
		kZveto,
		kProjMet,
		kJetVeto,
		kSoftMuon,
		kTopVeto,
		kHardPtMin,
		kSoftPtMin,
		kMaxMll,
		kDeltaPhi,
		kNumCuts
	};

	const static unsigned short _wordLen = 32;

	typedef std::bitset<_wordLen> higgsBitWord;

	static const double _Z0Mass;

	higgsBitWord _theMask;
	std::vector< higgsBitWord > _nthMask;

	void bookCutHistograms(std::vector<TH1F*>&, const std::string& nPrefix, const std::string& lPrefix);

	void readHiggsCutSet( const std::string& path );
	HiggsCutSet getHiggsCutSet(int mass);
//	HiggsCutSet getHiggsCutSet(int mass, int ll);
	TH2F* makeNjetsNvrtx( const std::string& name, const std::string& prefix = "");
	TH1F* makeLabelHistogram( const std::string& name, const std::string& title, std::map<int,std::string> labels);
	TH1F* glueCounters(TH1F* h);

	std::string _analysisTreeName;

	int   _higgsMass;

	float _maxD0;
	float _maxDz;
	float _minMet;
	float _minMll;
	float _zVetoWidth;

	float _minProjMetEM;
	float _minProjMetLL;

	std::vector<std::string> _histLabels;
	std::map<std::string,TH1F*> _hists;

	HiggsCutSet _theCuts;

	TH1F* _hEntries;

	TH1F* _eeCounters;
	TH1F* _emCounters;
	TH1F* _meCounters;//TODO
	TH1F* _mmCounters;

	TH1F* _llCounters;

	TH1F* _nVrtx;
	TH1F* _jetN;
	TH1F* _jetPt;
	TH1F* _jetEta;
	TH1F* _diLep_PfMet;
	TH1F* _diLep_TcMet;
	TH1F* _diLep_projPfMet;
	TH1F* _diLep_projTcMet;
	TH1F* _diLep_ptLeadLep;
	TH1F* _diLep_ptTrailLep;
	TH1F* _diLep_mll;
	TH1F* _diLep_deltaPhi;

	TH2F* _llJetNVsNvrtx;
	TH2F* _eeJetNVsNvrtx;
	TH2F* _emJetNVsNvrtx;
	TH2F* _meJetNVsNvrtx; //TODO
	TH2F* _mmJetNVsNvrtx;

	std::vector<TH1F*> _llNm1Hist;
	std::vector<TH1F*> _eeNm1Hist;
	std::vector<TH1F*> _emNm1Hist;
	std::vector<TH1F*> _meNm1Hist; //TODO
	std::vector<TH1F*> _mmNm1Hist;
	std::vector<TH1F*> _llPreCutHist;
	std::vector<TH1F*> _llPostCutHist;
	std::vector<TH1F*> _eePreCutHist;
	std::vector<TH1F*> _eePostCutHist;
	std::vector<TH1F*> _emPreCutHist;
	std::vector<TH1F*> _emPostCutHist;
	std::vector<TH1F*> _mePreCutHist;//TODO
	std::vector<TH1F*> _mePostCutHist;//TODO
	std::vector<TH1F*> _mmPreCutHist;
	std::vector<TH1F*> _mmPostCutHist;

	std::string _cutFile;

	std::vector<HiggsCutSet> _cutVector;

	TTree* _analysisTree;

	HWWEvent* _event;
	HWWNtuple* _ntuple;

};

#endif /* HWWANALYZER_H_ */
