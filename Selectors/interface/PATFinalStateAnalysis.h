/*
 * Wrapper about PATFinalStateSelection which handles the getting objects from
 * the event.
 */

#ifndef PATFINALSTATEANALYSIS_FRM3UCVB
#define PATFINALSTATEANALYSIS_FRM3UCVB

#include <vector>
#include <map>
#include <boost/shared_ptr.hpp>

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/Provenance/interface/RunID.h"

#include "FinalStateAnalysis/DataFormats/interface/PATFinalStateEventFwd.h"
#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "PhysicsTools/UtilAlgos/interface/BasicAnalyzer.h"

class TH1;
class PATFinalStateSelection;
class TFileDirectory;
namespace edm {
  class LuminosityBlockBase;
}

class PATFinalStateAnalysis : public edm::BasicAnalyzer {
  public:
    PATFinalStateAnalysis(const edm::ParameterSet& pset, TFileDirectory& fs);
    virtual ~PATFinalStateAnalysis();
    void beginJob() {}
    void endJob();
    // Alias for filter with no return value
    void analyze(const edm::EventBase& evt);
    bool filter(const edm::EventBase& evt);
    void beginLuminosityBlock(const edm::LuminosityBlockBase& ls);

  private:
    edm::InputTag src_;
    std::string name_;
    TFileDirectory& fs_;
    edm::ParameterSet analysisCfg_;
    boost::shared_ptr<PATFinalStateSelection> analysis_;

    // Tools for applying event weights
    typedef StringObjectFunction<PATFinalStateEvent> EventFunction;
    edm::InputTag evtSrc_;
    std::vector<EventFunction> evtWeights_;

    // Tool for examining individual runs
    bool splitRuns_;
    std::auto_ptr<TFileDirectory> runDir_;
    typedef std::map<edm::RunNumber_t, boost::shared_ptr<PATFinalStateSelection> > RunMap;
    RunMap runAnalysis_;

    // For counting events
    TH1* eventCounter_;
    TH1* eventCounterWeighted_;
    TH1* eventWeights_;
    // For keeping track of the skimming
    edm::InputTag skimCounter_;
    TH1* skimEventCounter_;
    // For counting the luminosity
    edm::InputTag lumiProducer_;
    TH1* integratedLumi_;

    bool filter_;
};

#endif /* end of include guard: PATFINALSTATEANALYSIS_FRM3UCVB */
