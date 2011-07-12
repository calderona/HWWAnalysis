import FWCore.ParameterSet.Config as cms

import FWCore.ParameterSet.VarParsing as VarParsing

import math

radToDeg = str(180./math.pi)

# setup 'analysis'  options
options = VarParsing.VarParsing ('analysis')

options.register ( 'monitor',
                  False,
                  VarParsing.VarParsing.multiplicity.singleton,
                  VarParsing.VarParsing.varType.bool,
                  "monitor informations for every selected event")


# setup any defaults you want
options.outputFile = 'simpleTest.root'
# options.inputFiles= 'file1.root', 'file2.root'
options.maxEvents = -1 # -1 means all events

# get and parse the command line arguments
options.parseArguments()


process = cms.PSet(
        inputFiles = cms.vstring(options.inputFiles),
        outputFile = cms.string(options.outputFile),
        maxEvents  = cms.int64(options.maxEvents),
        monitor    = cms.bool(options.monitor),
        copyObjects = cms.vstring(['entries']),
)

process.channels = cms.VPSet(
    cms.PSet(
        name = cms.string('ll'),
        selection = cms.string('1 == 1 '),
    ),
    cms.PSet(
        name = cms.string('ee'),
        selection = cms.string('is(\'elel\')'),
    ),
    cms.PSet(
        name = cms.string('em'),
        selection = cms.string('is(\'elmu\')'),
    ),
    cms.PSet(
        name = cms.string('me'),
        selection = cms.string('is(\'muel\')'),
    ),
    cms.PSet(
        name = cms.string('mm'),
        selection = cms.string('is(\'mumu\')'),
    ),
)

def cut(name, label, cut):
    return cms.PSet(
        name = cms.string(name),
        label = cms.string(label),
        cut = cms.string(cut)
        )

process.cuts = cms.VPSet(
    cut('skim',       'skim', '1 == 1'),
    cut('minMll',     'minMll','mll > 12.'),
    cut('minMet',     'min #slash{E}_{T}','met > 20'),
    cut('Zveto',      'Zveto','different() || (abs(mll - 91.18699) > 15.)'),
    cut('projMet',    'projMet','( same() &&  projMet > 35 ) || ( different() && projMet > 20 ) '),
    cut('Jet Veto',   'Jet Veto','nJets == 0'),
    cut('Soft mu',    'Soft mu','nSoftMus == 0'),
    cut('Top Veto',   'Top Veto','nBJets == 0'),
    cut('maxMll',     'maxMll','mll < 50'),
    cut('pT lead',    'pT lead','pA.pt() > 30'),
    cut('pT trail',   'pT trail','pB.pt() > 25'),
    cut('dPhi','dPhi','dPhi*'+radToDeg+' < 60'),
    )


def variable( name, title, formula,bins, min, max ):
    return cms.PSet(
        name     = cms.string(name),
        title    = cms.string(title),
        formula  = cms.string(formula),
        min      = cms.double(min),
        max      = cms.double(max),
        bins     = cms.int32(bins),
    )


process.variables = cms.VPSet(
    variable('mll',     'm_{ll};GeV',               'mll',50,0.,200.),
     variable('met',     '#slash{E}_{T};GeV',        'met',50,0.,100.),
     variable('projMet', 'proj#slash{E}_{T};GeV',    'projMet',50,0.,100.),
     variable('nJets',   'N_{jets}',                 'nJets',10,0.,10.),
     variable('dPhillj', '#Delta#Phi_{ll,j};deg',    'dPhillj*'+radToDeg,36,0.,180.),
     variable('dPhi',    '#Delta#phi',               'dPhi*'+radToDeg,36,0.,180.),
     variable('ptLead',  'p_{T}^{lead}',             'pA.pt()',50,0,200.),
     variable('ptTrail', 'p_{T}^{trail}',            'pB.pt()',50,0,200.),
    
    ## variables from Maiko's shopping list

     variable('etaLead', '#eta^{lead};#eta^{lead}',                  'pA.eta()',30,-3.,3.),
     variable('etaTrail','#eta^{trail};#eta^{trail};deg',            'pB.eta()',30,-3.,3.),
     variable('phiLead', '#phi^{lead};#phi^{lead};deg',              'pA.phi()',30,-3.14159,3.14159),
     variable('phiTrail','#phi^{trail};#phi^{trail}',                'pB.phi()',30,-3.14159,3.14159),
     variable('dEta',    '#Delta#eta_{ll};#Delta#eta_{ll}',          'pA.eta()-pB.eta()',120,-6.,6.),
     variable('dPt',     '#Delta p_{T, ll};GeV',                     'pA.pt()-pB.pt()',200,0.,200.),
     variable('dRll',    '#DeltaR{ll}:#DeltaR{ll}',                  'deltaRll',100,0.,5.),
     variable('dileptonPt', 'p_{T, ll};GeV',                         'dileptonPt',50,0,50.),

     variable('PfMetPhi', '#phi_{#slash{E}_{T}};',                   'pfMetPhi',30,-3.14159,3.14159),
    
     variable('sumPtJetsScalar', '#Sigma p_{T}^{j};scalar #Sigma p_{T}^{j} [GeV]',                 'sumPtJetsScalar',50,0,200),
     variable('sumPtCentralJetsScalar', '#Sigma p_{T}^{cj};scalar #Sigma p_{T}^{cj} [GeV]',        'sumPtCentralJetsScalar',50,0,200),
     variable('sumPtCentralJets40Scalar', '#Sigma p_{T}^{cj};scalar #Sigma p_{T}^{cj40} [GeV]',    'sumPtCentralJets40Scalar',50,0,200),
     variable('sumPtJetsVectorial', '#Sigma p_{T}^{j};vectorial #Sigma p_{T}^{j} [GeV]',                 'sumPtJetsVectorial',50,0,200),
     variable('sumPtCentralJetsVectorial', '#Sigma p_{T}^{cj};vectorial #Sigma p_{T}^{cj} [GeV]',        'sumPtCentralJetsVectorial',50,0,200),
     variable('sumPtCentralJets40Vectorial', '#Sigma p_{T}^{cj};vectorial #Sigma p_{T}^{cj40} [GeV]',    'sumPtCentralJets40Vectorial',50,0,200),

     variable('mtLead',  'm_{T}^{lead}',             'mtA',50,0,200.),
     variable('mtTrail', 'm_{T}^{trail}',            'mtB',50,0,200.),
     variable('mt2', 'm_{T2}',                       'mt2',50,0,200.),

     variable('centralityJetsScalar', '#Sigma p_{T}^{j}/#Sigma E^{j}',            'centralityJetsScalar',50,0,1.),
     variable('centralityJetsVectorial', '#Sigma p_{T}^{j}/#Sigma E^{j}',         'centralityJetsVectorial',50,0,1.),

     variable('jet1pt', 'leading jet p_{T};GeV',         'jet1pt',100,0,200),
     variable('jet2pt', 'second jet p_{T};GeV',          'jet2pt',100,0,200),
     variable('jet1phi', 'leading jet #phi;#phi',        'jet1phi',30,-3.14159,3.14159),
     variable('jet2phi', 'second jet #phi;#phi',         'jet2phi',30,-3.14159,3.14159),
     variable('jet1eta', 'leading jet #eta;#eta',        'jet1eta',60,-6.,6.),
     variable('jet2eta', 'second jet #eta;#eta',         'jet2eta',60,-6.,6.),
 ##     variable('jetPt', 'inclusive jet p_{T};GeV',        'jetPt',200,0,400),
 ##     variable('jetPhi', 'inclusive jet #phi;#phi',       'jetPhi',30,-3.14159,3.14159),
 ##     variable('jetEta', 'inclusive jet #eta;#eta',       'jetPhi',60,-6.,6),
     variable('jet1bTagProb', 'leading jet b-tag prob;b-tag prob.',       'jet1bTagProb',100,-5.,15),
     variable('jet2bTagProb', 'second jet b-tag prob;b-tag prob.',        'jet2bTagProb',100,-5.,15),
     variable('sumJet12bTagProb', 'sum jet (1&2) b-tag prob;b-tag prob.', 'sumJet12bTagProb',100,-5.,15),
     variable('maxbTagProb', 'max b-tag prob (all jets);b-tag prob.',     'maxbtagProb',100,-5.,15),


)

process.monitored = cms.vstring([]) 

process.xxx = cms.PSet(
        a = cms.string('a'),
        b = cms.int32(10),
        c = cms.double(1E-3),
        )
