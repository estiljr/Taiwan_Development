def CalculateSlope(shpXsection):
    """NB: Input shape file must be of cross section type shape file"""
    try:
        args = '-calculateslope  /i: ',shpXsection
        subprocess.call([isisMapper,args],shell=True)
    except ValueError as e: print(e)
    return csvDepthOutput