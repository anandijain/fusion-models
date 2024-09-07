# houses some fusion models 


wired connection serial phone to Pico 
bearing redesign 
rust embassy Pico w 
protoboard or PCB 
flywheel motor ball shooter 
bldc 
3d printable latching assemblies 
switch to pose detection, basically max out frame rate and latency. also slim tf down out of the app to just what I need. also maybe look into model quantization - fun ml thing I've never done
"guitar hero but every time you mess up you get shot" 

9/6/24 todo
  * design an adjustable width flywheel projectile shooter
  * wired connection serial phone to Pico 
  * model/experimentally determine the compression of the nerf rival round 

done: 
  * get a motor working (with pwd speed control)
  * get a kilawatt for the ps 
    - at full speed current draw is only 1/3 A 
  * get 4 pin male male headers for plugging in motors 
  * solder headers onto the pico 
  * design the flywheel and mounting stuff for the dc motors   
  * get the face tracker working again 
  * 
for stepper_with_joints:
the m5x2x10s mount the phone holder
the 16s are the set screws

todo
  - control pico from android wired to see if its faster 
  - mount pico and driver to bottom plate 
  - [ ] the pitch holder should be screwed together with the coupler instead of just awkwardly joined to it
  - use a belt to couple the stepper and pitch holder to save footprint
  - commit to this repo the ISOMetricprofile.xml file with a huge matrix of differently pitched threads 
  - BOM 
  - at some point probably find a power supply to 3A to power both steppers
  - protoboard so wires dont keep falling out
  - custom pcb to see how small i can get things 
  - make delay a query parameer
  - redo assembly animation with rest of fasteners 

completed
  - create a level shifter with a transistor to give 5v logic to driver from pico 
      - resolved by using a motor driver (a4988) that cnan handle 3.3v logic
  - probably need to redesign shaft collar to use real metal screws as set screws
  - add a way for the coupler to slot into the bottom plate and be aligned with the mounting screws
    - made irrelevant by gears
  - add bolt to prevent horizontal movement of the top plate in cad 
  - fix pitch bearing holder holes to be 1) m5 2) the mirror of the holes for the stepper holder to make it easier to assemble (dont have to put on the holder before screwing in the big yaw gear)
  - single cable power-use a 5v regulator to power the pico from the 19v supply
  

https://grabcad.com/library/mg995-servo-3
https://grabcad.com/library/mg-996r-servo-motor-1


note for the m8 model you will likely have to paste in the following to the following path. this video explains how to add custom thread types to fusion https://www.youtube.com/watch?v=VPDngPAvFnQ

for laptop 
C:\Users\anand\AppData\Local\Autodesk\webdeploy\production\4826aec956713f599d57385857ff62484fd50dd3\Fusion\Server\Fusion\Configuration\ThreadData\ISOMetricprofile.xml

for desktop 
C:\Users\anand\AppData\Local\Autodesk\webdeploy\production\35f4ba95ffc4701e35102fa6485053ed4c1923cf\Fusion\Server\Fusion\Configuration\ThreadData\ISOMetricprofile.xml

```xml
<ThreadSize>
    <Size>8.0</Size>
    <Designation>
      <ThreadDesignation>M8x2</ThreadDesignation>
      <CTD>M8x2</CTD>
      <Pitch>2</Pitch>
      <Thread>
        <Gender>external</Gender>
        <Class>6g</Class>
        <MajorDia>7.866</MajorDia>
        <PitchDia>7.101</PitchDia>
        <MinorDia>6.4455</MinorDia>
      </Thread>
      <Thread>
        <Gender>internal</Gender>
        <Class>6H</Class>
        <MajorDia>8.17</MajorDia>
        <PitchDia>7.268</PitchDia>
        <MinorDia>6.7795</MinorDia>
        <TapDrill>6.75</TapDrill>
      </Thread>
      <Thread>
        <Gender>external</Gender>
        <Class>4g6g</Class>
        <MajorDia>7.866</MajorDia>
        <PitchDia>7.1225</PitchDia>
        <MinorDia>6.467</MinorDia>
      </Thread>
    </Designation>
  </ThreadSize>
  ```