import os

def write_ied_boundary(fileName,tsData,type):
    '''
    @summary: write the tsData (could be for multiple sites) dictionary to IED file
    @param tsData: {tag:[(t,v),(t,v)]}
    @param type:  QTBDY,
    '''
    
    if os.path.isfile(fileName):
        os.unlink(fileName)
    fo = open(fileName, 'w')
    
    for k,v in tsData.items():
        fo.write(type + ' ' + k + '\n')
        fo.write(k + '\n')
        fo.write(format(len(v),'10d') + '     0.000     0.000     HOURS    EXTEND    LINEAR' + '\n')
        for time, value in v:
            fo.write(format(value,'10.3f')+format(time,'10.3f')+'\n')
    
    fo.close()    
    
    
if __name__ == '__main__':
    tsData = dict()
    tsData['Valea_Rece'] = [(0,1),(1,1.5),(2,0)]
    write_ied_boundary('test_files/boundary.ied',tsData,'QTBDY')