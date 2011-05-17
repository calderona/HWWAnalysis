/*
 * HWWAnalyzer.h
 *
 *  Created on: Dec 14, 2010
 *      Author: ale
 */

#ifndef HWWANALYZER_H_
#define HWWANALYZER_H_

#include "HWWAnalysis/CutBasedAnalyzer/interface/UserAnalyzer.h"
#include "HWWAnalysis/DataFormats/interface/HWWEvent.h"
#include <bitset>
#include <set>

class HWWEvent;
class HWWPFJet;
class HWWNtuple;
class TTree;
class TH1D;
class TH2D;
class TParticlePDG;


class HWWAnalyzer : public UserAnalyzer {
public:
	HWWAnalyzer(int argc,char** argv);
	virtual ~HWWAnalyzer();

	virtual Bool_t Notify();
	virtual void Book();
	virtual void BeginJob();
	virtual void Process( Long64_t iEvent );
	virtual void fillNtuple();
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
		float minR;
		float maxR;
		void print();
	};

    struct HistogramSet { 
        TH1D* counters;
        TH2D* jetNVsNvrtx;
        std::vector<TH1D*> dileptons;
        std::vector<TH1D*> preCuts;
        std::vector<TH1D*> postCuts;
        std::vector<TH1D*> extra;
        std::vector<std::vector<TH1D*> > cutByCut;
    };

    // enumerators
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

    // dilepton enum
    enum allDi {
        kDiPfMet,
        kDiTcMet,
        kDiChargedMet,
        kDiProjPfMet,
        kDiProjTcMet,
        kDiProjChargedMet,
        kDiLeadPt,
        kDiTrailPt,
        kDiMll,
        kDiDeltaPhi,
        kDiGammaMRStar,
        kDiSize
    };

    //
    enum extraHist {
        kExtraDeltaPhi,
        kExtraSize
    };

    // logged variables
    enum LoggedVars_t {
        kLogNJets,
        kLogNSoftMus,
        kLogNBjets,
        kLogMet,
        kLogProjMet,
        kLogMll,
        kLogPtLead,
        kLogPtTrail,
        kLogDphi,
        kLogRazor,
        kLogSize
    };

    // yeild histogram enum
	enum HCuts_t {
		kSkimmed = 1,
		kMinMet,
		kMinMll,
		kZveto,
		kProjMet,
		kJetVeto,
		kSoftMuon,
		kTopVeto,
		kMaxMll,
		kLeadPtMin,
		kTrailPtMin,
		kDeltaPhi,
        kRazor,
		kCutsSize
	};

    // 

    // constants
	const static unsigned short _wordLen = 32;
	static const double _Z0Mass;

	typedef std::bitset<_wordLen> higgsBitWord;


	higgsBitWord _theMask;
	std::vector< higgsBitWord > _nthMask;

    // interface with cfg files
	void readHiggsCutSet( const std::string& path );
	HiggsCutSet getHiggsCutSet(int mass);

    // histogram maker helper methods
    void bookHistogramSet( HistogramSet& set, const std::string& name );
	void bookCutHistograms(std::vector<TH1D*>&, const std::string& nPrefix, const std::string& lPrefix);
	void bookDiHistograms(std::vector<TH1D*>&, const std::string& nPrefix, const std::string& lPrefix);
	void bookExtraHistograms(std::vector<TH1D*>&, const std::string& nPrefix, const std::string& lPrefix);

	TH2D* makeNjetsNvrtx( const std::string& name, const std::string& prefix = "");
    TH1D* makeVarHistogram( int code, const std::string& name, const std::string& title );

	TH1D* makeLabelHistogram( const std::string& name, const std::string& title, std::map<int,std::string> labels);
	TH1D* glueCounters(TH1D* h);

    double getWeight() { return _event->Weight; }
    

    // helper methods for the analysis
//     int countJets( double ptmin );

    void fillDiLeptons(std::vector<TH1D*>& histograms );
    void fillExtra(std::vector<TH1D*>& histograms );
    void fillVariables( HistogramSet* histograms, HCuts_t cutCode );
    
    // cuts
	int   _higgsMass;

	double _maxD0;
	double _maxDz;
	double _minMet;
	double _minMll;
	double _zVetoWidth;

	double _minProjMetEM;
	double _minProjMetLL;

    // end cuts

	std::vector<std::string> _histLabels;
	std::map<std::string,TH1D*> _hists;

	HiggsCutSet _theCuts;


    // histograms
	TH1D* _hEntries;

//     TH1D* _eeCounters;
//     TH1D* _emCounters;
//     TH1D* _meCounters;
//     TH1D* _mmCounters;

//     TH1D* _llCounters;

	TH1D* _nVrtx;
	TH1D* _jetN;
	TH1D* _jetPt;
	TH1D* _jetEta;

	TH2D* _llJetNVsNvrtx;
	TH2D* _eeJetNVsNvrtx;
	TH2D* _emJetNVsNvrtx;
	TH2D* _meJetNVsNvrtx; //TODO
	TH2D* _mmJetNVsNvrtx;

    HistogramSet    _llHistograms;
    HistogramSet    _eeHistograms;
    HistogramSet    _emHistograms;
    HistogramSet    _meHistograms;
    HistogramSet    _mmHistograms;

//     std::vector<TH1D*> _llDiHist;
//     std::vector<TH1D*> _eeDiHist;
//     std::vector<TH1D*> _emDiHist;
//     std::vector<TH1D*> _meDiHist; //TODO
//     std::vector<TH1D*> _mmDiHist;

//     std::vector<TH1D*> _llNm1Hist;
//     std::vector<TH1D*> _eeNm1Hist;
//     std::vector<TH1D*> _emNm1Hist;
//     std::vector<TH1D*> _meNm1Hist; //TODO
//     std::vector<TH1D*> _mmNm1Hist;

//     std::vector<TH1D*> _llPreCutHist;
//     std::vector<TH1D*> _llPostCutHist;
//     std::vector<TH1D*> _eePreCutHist;
//     std::vector<TH1D*> _eePostCutHist;
//     std::vector<TH1D*> _emPreCutHist;
//     std::vector<TH1D*> _emPostCutHist;
//     std::vector<TH1D*> _mePreCutHist;//TODO
//     std::vector<TH1D*> _mePostCutHist;//TODO
//     std::vector<TH1D*> _mmPreCutHist;
//     std::vector<TH1D*> _mmPostCutHist;

//     
//     std::vector<TH1D*> _llExtraHist;
//     std::vector<TH1D*> _eeExtraHist;
//     std::vector<TH1D*> _emExtraHist;
//     std::vector<TH1D*> _meExtraHist; //TODO
//     std::vector<TH1D*> _mmExtraHist;
    // end histograms


//     std::set<HWWPFJet*> _selectedJets;
//     std::set<HWWPFJet*> _btaggedJets;

	std::string _cutFile;

	std::vector<HiggsCutSet> _cutVector;

	std::string _analysisTreeName;
	TTree* _analysisTree;

	HWWEvent* _event;
	HWWNtuple* _ntuple;

};

#endif /* HWWANALYZER_H_ */
