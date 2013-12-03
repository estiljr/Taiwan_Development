from mp2.model.db import _session, ZArea, ZLine_Pl, ZLine_PlPt_Pl, ZLine_PlPt_Pt, Boundary, Domain, NArea

geom_polygon = 'SRID=3826;POLYGON((296261 2774686,297516 2772686,299571 2775079,297601 2775883,296261 2774686))'
geom_linestring = 'SRID=3826;LINESTRING(296261 2774686,297516 2772686,299571 2775079,297601 2775883)'

def Populate_ZArea():
    _session.add_all([
            ZArea(lowest_val=1,height=5, geom= geom_polygon),
            ZArea(lowest_val=0,height=3, geom= geom_polygon),
                      ])
    _session.commit()

def Read_ZArea():
    res = _session.query(ZArea).first()
    if res is not None:
        print res.geom, res.lowest_val, res.height
        print res.geom.desc
    else:
        print 'no res found'

##===============================================

def Populate_ZLine_Pl():
    _session.add_all([
            ZLine_Pl(lowest_val=1,height=5,thick=2,geom= geom_linestring),
            ZLine_Pl(lowest_val=0,height=3,thick=2,geom= geom_linestring),
                      ])
    _session.commit()

def Read_ZLine_Pl():
    res = _session.query(ZLine_Pl).first()
    if res is not None:
        print res.geom, res.lowest_val, res.height, res.thick
        print res.geom.desc
    else:
        print 'no res found'

#=================================================

def Populate_ZLine_PlPt_Pl():
    _session.add_all([
            ZLine_PlPt_Pl(thick=1,height=5, geom= geom_linestring),
            ZLine_PlPt_Pl(thick=0,height=3, geom= geom_linestring),
                      ])
    _session.commit()

def Read_ZLine_PlPt_Pl():
    res = _session.query(ZLine_PlPt_Pl).first()
    if res is not None:
        print res.geom, res.thick, res.height
        print res.geom.desc
    else:
        print 'no res found'

#=================================================

def Populate_ZLine_PlPt_Pt():
    _session.add_all([
            ZLine_PlPt_Pt(thick=1,height=5, geom= geom_linestring),
            ZLine_PlPt_Pt(thick=0,height=3, geom= geom_linestring),
                      ])
    _session.commit()

def Read_ZLine_PlPt_Pt():
    res = _session.query(ZLine_PlPt_Pt).first()
    if res is not None:
        print res.geom, res.thick, res.height
        print res.geom.desc
    else:
        print 'no res found'

#=================================================

def Populate_NArea():
    _session.add_all([
            NArea(method="multiply",value=2, geom= geom_polygon),
            NArea(method="add",value=0.05, geom= geom_polygon),
                      ])
    _session.commit()

def Read_NArea():
    res = _session.query(NArea).first()
    if res is not None:
        print res.geom, res.method, res.value
        print res.geom.desc
    else:
        print 'no res found'


if __name__ == '__main__':
    Populate_ZArea()
    Populate_ZLine_Pl()
    Populate_ZLine_PlPt_Pl()
    Populate_ZLine_PlPt_Pt()
    Populate_NArea()