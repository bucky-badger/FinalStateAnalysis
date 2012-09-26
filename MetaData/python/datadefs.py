'''

Definitions of data samples used in analyses.

Picks either data7TeV or data8TeV according to the release.

Author: Evan K. Friis, UW Madison

'''

from FinalStateAnalysis.Utilities.version import cmssw_major_version
from FinalStateAnalysis.Utilities.version import cmssw_minor_version


data_name_map = None
datadefs = None

if cmssw_major_version() == 5 and cmssw_minor_version() == 2 :
    import data8TeV
    data_name_map = data8TeV.data_name_map
    datadefs = data8TeV.datadefs
elif cmssw_major_version() == 4:
    import data7TeV
    data_name_map = data7TeV.data_name_map
    datadefs = data7TeV.datadefs
elif cmssw_major_version() == 5 and cmssw_minor_version() == 3 :
    import data8TeVNew
    data_name_map = data8TeVNew.data_name_map
    datadefs = data8TeVNew.datadefs
else:
    raise ValueError("I can't figure out which release to use!")
