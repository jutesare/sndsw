import json
import ROOT

def loadConstants(constantsJSONpath="averageMIPpeakPos2025.json"):
    ROOT.gInterpreter.Declare(r"""
    #include <map>
    extern std::map<int, double> SiPM_qdc_calibration_constants;
    """)

    with open(constantsJSONpath) as f:
        data = json.load(f)

    for k, v in data.items():
        ROOT.SiPM_qdc_calibration_constants[int(k)] = float(v)