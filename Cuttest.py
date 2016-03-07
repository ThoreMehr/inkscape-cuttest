#! /usr/bin/env python
'''
Generates Inkscape SVG file containing an test patern for cuting and engraving with a laser cutter

Copyright (C) 2016 Thore Mehr thore.mehr@gmail.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
__version__ = "0.8" ### please report bugs, suggestions etc to bugs@twot.eu ###

import sys,inkex,simplestyle,gettext,math
_ = gettext.gettext

def drawS(XYstring,color):         # Draw lines from a list
  name='part'
  style = { 'stroke': color, 'fill': 'none' }
  drw = {'style':simplestyle.formatStyle(style),inkex.addNS('label','inkscape'):name,'d':XYstring}
  inkex.etree.SubElement(parent, inkex.addNS('path','svg'), drw )
  return
def groupdraw(XYstrings,colors)  :
  if len(XYstrings)==1:
    drawS(XYstrings[0],colors[0])
    return
  grp_name = 'Group'
  grp_attribs = {inkex.addNS('label','inkscape'):grp_name}
  grp = inkex.etree.SubElement(parent, 'g', grp_attribs)#the group to put everything in
  name='part'
  for i in range(len(XYstrings)):
    style = { 'stroke': colors[i], 'fill': 'none' }
    drw = {'style':simplestyle.formatStyle(style),inkex.addNS('label','inkscape'):name+str(i),'d':XYstrings[i]}
    inkex.etree.SubElement(grp, inkex.addNS('path','svg'), drw )
  return

def svg_from_points(points,offset):
  s='M'+str(points[0][0]+offset[0])+','+str(points[0][1]+offset[1])
  for i in range(1,len(points)):
    s+='L'+str(points[i][0]+offset[0])+','+str(points[i][1]+offset[1])
  s+='Z'
  return s
  
class Cuttest(inkex.Effect):
  def __init__(self):
      # Call the base class constructor.
      inkex.Effect.__init__(self)
      # Define options
      self.OptionParser.add_option('--unit',action='store',type='string',
        dest='unit',default='mm',help='Measure Units')
      
      self.OptionParser.add_option('--line_length', action='store',type='int',
        dest='line_length', default=1,help='length')
      self.OptionParser.add_option('--speed_min', action='store',type='int',
        dest='speed_min', default=1,help='speed_min')
      self.OptionParser.add_option('--speed_max', action='store',type='int',
        dest='speed_max', default=1,help='speed_max')
      self.OptionParser.add_option('--speed_step', action='store',type='int',
        dest='speed_step', default=1,help='speed_step')        
      self.OptionParser.add_option('--rows', action='store',type='int',
        dest='rows', default=1,help='rows')        
      self.OptionParser.add_option('--intensity', action='store',type='int',
        dest='intensity', default=1,help='intensity')
      self.OptionParser.add_option('--lasertag',action='store',type='string',
        dest='lasertag',default="=pass%n:%s:%i:%c=",help='color1')  
  def effect(self):
    global parent,nomTab,equalTabs,thickness,kerf,correction
    
        # Get access to main SVG document element and get its dimensions.
    svg = self.document.getroot()
    
        # Get the attibutes:
    widthDoc  = self.unittouu(svg.get('width'))
    heightDoc = self.unittouu(svg.get('height'))

        # Create a new layer.
    layer = inkex.etree.SubElement(svg, 'g')
    layer.set(inkex.addNS('label', 'inkscape'), 'newlayer')
    layer.set(inkex.addNS('groupmode', 'inkscape'), 'layer')
    
    parent=self.current_layer
    
        # Get script's option values.
    unit=self.options.unit
    length=self.unittouu(str(self.options.line_length)+unit)
    speed_min=self.options.speed_min
    
    speed_max=self.options.speed_max
    speed_step=self.options.speed_step
    rows=self.options.rows
    intensity=self.options.intensity
    lasertag=self.options.lasertag
    
    num_steps=1+ int(math.ceil(float((speed_max-speed_min))/float(speed_step)))
   
    s=[]
    colors=[]
    for j in range(num_steps):
      s+=["M"+str(((j)%rows +1)*length)+","+str(((j/rows)+1)*length)+'a'+str(length/4)+','+str(length/4)+' 0 1,0 '+str(length/2)+',0'+'a'+str(length/4)+','+str(length/4)+' 0 1,0 '+str(-length/2)+',0']
      colorstr=hex(1000*j)[2:]
      #colorstr=colorstr
      colors+=['#'+colorstr.rjust(6,"0")]
    
    s=s[0:num_steps]
    groupdraw(s,colors)
    for i in range(len(s)):
      text = inkex.etree.Element(inkex.addNS('text','svg'))
      text.text =lasertag.replace("%n",str(i+1)).replace("%s",str(max(speed_max-i*speed_step,speed_min))).replace("%i",str(intensity)).replace("%c",colors[i])
      text.set('y',str(i*-10))
      layer.append(text) 
    
# Create effect instance and apply it.
effect = Cuttest()
effect.affect()
