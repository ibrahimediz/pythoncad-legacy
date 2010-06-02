#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas
#
# Copyright (c) 2010 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# code for base for Fillet
#

from Kernel.GeoComposedEntity.objoint import *
from Kernel.GeoComposedEntity.bisector import Bisector
_dtr = 180.0/pi

class Fillet(ObjectJoint):
    """
        A fillet is a curved joining of two Entity Object. For a filleted
        joint to be valid, the radius must fall within some distance
        determined by the segment endpoints and segment intersection
        point, and the two Entity Object must be extendable so they can
        share a common endpoint.
    """
    def __init__(self, kw):
        """
            "OBJECTJOINT_0" obj1             :(Segment ,ACLine,Arc,CCircle)
            "OBJECTJOINT_1" obj2             :(Segment ,ACLine,Arc,CCircle)
            "OBJECTJOINT_2" pointClick1      :Clicked point from the u.i near the obj1
            "OBJECTJOINT_3" pointClick2      :Clicked point from the u.i near the obj2
            "OBJECTJOINT_4" str              :Fillet Trim Mode (FIRST,SECOND,BOTH,NO_TRIM)
            "OBJECTJOINT_5" radius           :Radius of the Fillet
        """
        argDes={"OBJECTJOINT_5":(float, int)}
        ObjectJoint.__init__(self, kw, argDes)
        self._UpdateFilletArc()

    def _calculateCenter(self):
        """
            Calculate the center point of the filler arc
            This method is private to the Fillet object.
        """
        if self.angle==0:
            raise StructuralError, "angle betwin the two line is 0 "
        if math.pi-self.angle==0:
            raise StructuralError, "angle betwin the two line is pi "
        tan=math.tan(self.angle/2.0)
        bisectorLengh=math.sqrt(self.radius**2*(1+1/tan**2))
        arg={"OBJECTJOINT_0":self.obj1,
            "OBJECTJOINT_1":self.obj2,
            "OBJECTJOINT_2":self.pointClick1, 
            "OBJECTJOINT_3":self.pointClick2, 
            "OBJECTJOINT_5":bisectorLengh}
        bisect=Bisector(arg)
        p1, p2=bisect.bisector.getEndpoints()
        if self.intersection[0].dist(p1)>self.intersection[0].dist(p2):
            self.__center=p1
        else:
            self.__center=p2
            
    def _UpdateFilletArc(self):           
        """
            Recompute the Fillet segment
        """
        self._calculateCenter()
        obj1, pc1=self._updateSegment(self.obj1, self.pointClick1 )
        obj2, pc2=self._updateSegment(self.obj2, self.pointClick2 )
        if self.trimModeKey[self.trimMode]!=self.trimModeKey["NO_TRIM"]:
            if self.trimModeKey[self.trimMode]==self.trimModeKey["FIRST"] or self.trimModeKey[self.trimMode]==self.trimModeKey["BOTH"]:
                self.obj1=obj1
            if self.trimModeKey[self.trimMode]==self.trimModeKey["SECOND"] or self.trimModeKey[self.trimMode]==self.trimModeKey["BOTH"]:
                self.obj2=obj2
        self._UpdateAngle(pc1, pc2)
        arg={"ARC_0":self.center, "ARC_1":self.radius, "ARC_2":self.startAngle, "ARC_3":self.endAngle}
        self.filletArc=Arc(arg)
    
    def _UpdateAngle(self, pc1, pc2):
        """
            update the Fillet arc angle
        """
        v1=Vector(self.intersection[0], pc1)
        v2=Vector(self.intersection[0], pc2)
        self.startAngle=v1.absAng()
        self.endAngle=v1.ang(v2)
        
        
    def _updateSegment(self,objSegment,objPoint):
        """
            Get the point used for the trim
        """
        objProjection=objSegment.getProjection(self.center)
        objInterPoint=self.intersection[0]
        _p1 , _p2 = objSegment.getEndpoints()       
        _objPoint=Point(objSegment.getProjection(objPoint))
        if not (_p1==objInterPoint or _p2==objInterPoint):
            pickIntVect=pyGeoLib.Vector(objInterPoint,_objPoint).Mag()                    
            p1IntVect=pyGeoLib.Vector(objInterPoint,_p1).Mag()            
            if(pickIntVect==p1IntVect):
                arg={"SEGMENT_0":_p1,"SEGMENT_1":objProjection}
                return Segment(arg), objProjection
            p2IntVect=pyGeoLib.Vector(objInterPoint,_p2).Mag()
            if(pickIntVect==p2IntVect):
                arg={"SEGMENT_0":objProjection,"SEGMENT_1":_p2}
                return Segment(arg), objProjection
        ldist=_objPoint.dist(_p1)
        if ldist>_objPoint.dist(_p2):
            arg={"SEGMENT_0":_p1,"SEGMENT_1":objProjection}
            return Segment(arg), objProjection
        else:
            arg={"SEGMENT_0":objProjection,"SEGMENT_1":_p2}
            return Segment(arg), objProjection  
        
    @property
    def startAngle(self):
        """
            start fillet angle
        """
        return self.__StartAngle
    @startAngle.setter
    def startAngle(self, value):
        self.__StartAngle=value
        
    @property
    def endAngle(self):
        """
            start fillet angle
        """
        return self.__EndAngle
    @startAngle.setter
    def endAngle(self, value):
        self.__EndAngle=value
    @property
    def radius(self):
        """
            Return the Fillet radius.
        """
        return self['OBJECTJOINT_5']
    @radius.setter
    def radius(self, r):
        """
            Set the Fillet radius.
            The radius should be a positive float value.
        """
        _r = get_float(r)
        if _r < 0.0:
            raise ValueError, "Invalid fillet radius: %g" % _r
        self._calculateLimits()
        _rmin, _rmax = self.getRadialLimits()
        if _r < _rmin or _r > _rmax:
            raise ValueError, "Invalid radius: %g" % _r
        _or = self.radius
        if abs(_r - _or) > 1e-10:
            self.radius = _r
            self._calculateCenter()
            self._moveSegmentPoints()

    @property
    def center(self):
        """
            Return the center location of the Fillet.
            return: Point
        """
        return self.__center
  
    def clone(self):
        return Fillet(self)
    
    def getReletedComponent(self):
        """
            get the releted componet from the fillet
            usually the entity to save
        """
        return self.obj1, self.obj2, self.filletArc
        