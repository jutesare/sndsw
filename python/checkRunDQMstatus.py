import warnings

def checkRunDQMstatus(runNumber=None, systems=None, csvPath="/eos/user/j/jutesare/DQM/allRunsInfoWithLumi.csv"):
    """Check DQM status of a given data taking run.

    The status will be checked in the default lookup table, unless a different
    table is provided in the argument ``csvPath``. Per default the status will
    be returned for each subsystem, and overall, as a dict, but subsystems or
    overall can be chosen with the arguments ``systems``.

    Parameters
    ----------
    runNumber : int or str
        ...
    systems : list(str), optional
        ...
    csvPath : str, optional
        ...

    Raises
    ------
    ValueError
        If ``runNumber`` is neither an integer nor a string, or if
        the supplied run number cannot be found in the CSV mapping.
    FileNotFoundError
        If the CSV file cannot be opened.

    Notes
    -----
    ...
    """

    if not type(runNumber)==int or type(runNumber)==str:
        raise ValueError("Error: runNumber must be either an integer or a string.")    
    if type(runNumber) == int:
        runNumber = str(runNumber)
    if not type(csvPath)==str:
        raise ValueError("Error: csvPath must be a string.")
    if systems is not None:
        if type(systems)==list:
            if len(systems)==0:
                raise ValueError("Error: systems must be None or a non-empty list of strings.")
            elif len(systems)>=9:
                raise ValueError("Error: Too many items in list systems.")
            else:
                for item in systems:
                    if not type(item)==str:
                        raise ValueError("Error: systems must be None or a non-empty list of strings.")
        else:
            raise ValueError("Error: systems must be None or a non-empty list of strings.")

    with open(csvPath) as f:
        warnings.warn("Reading DQM status from " + csvPath + ".")
        lines = f.readlines()
    for line in lines[1:]:
        lineRunNumber, SciFiStatus, VSstatus, USstatus, DSstatus, overallStatus, comment, runLumi = line.strip().split(',')
        if lineRunNumber == runNumber:
            statusDict = {"overall": int(overallStatus), "VS": int(VSstatus), "SciFi": int(SciFiStatus), "US": int(USstatus), "DS": int(DSstatus), "comment": comment.strip(), "lumi": float(runLumi)}
            if systems is None:
                return statusDict
            else:
                if len(systems)==1:
                    return statusDict[systems[0]]
                else:
                    return {k: statusDict[k] for k in systems}
    else:
        raise ValueError(f"Run number {runNumber} not found in CSV file {csvPath}.")