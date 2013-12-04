from mp2.toolbox.normal_depth import normalDepth as nd

def Execute(shpXsection):
    
    nd.CalculateSlope(shpXsection)

if __name__ == '__main__':
    shpXsection = r'normal_depth\test_files\xsection3_spatialjoin.shp'
    Execute(shpXsection)