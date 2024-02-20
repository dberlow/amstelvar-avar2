About AmstelvarA2
=================

*introductory text about the AmstelvarA2 project (draft)*

### Differences in relation to Amstelvar

All parametric sources were redone from scratch from a new revised default. Changes include denesting components, changing point structures, fixing contour directions, adding traps, etc.

### Blending

Blending allows us to define *synthetic axes* using the parametric ones. This is achieved with `<mapping>` elements in the designspace file, which map an input in blended axes to an output in parametric axes. 

To see the advantage of this approach, compare the avar1 and avar2 versions of the AmstelvarA2 designspace: in avar1 the extrema of `opsz` `wght` `wdth` need to exist as UFO sources\*, in avar2 they don't.

\* instances of the parametric designspace, reinserted as sources.

### Measuring

In the original Amstelvar project, measuring was done with [ParamaRoundup](#). In AmstelvarA2 we are using a new measuring tool which is part of the VariableValues extension. 

we take various measurements (parameters) from all sources, and use these to create the parametric designspace and place the sources at the right locations. we also measure the original opsz wght wdth extrema to define their parametric 'recipes' (blends). 

### Technical requirements

macOS 13 is needed for avar2 fonts to work. then it's available via the OS to the browser, DrawBot, TextEdit etc.

The fonts are developed in “RoboFontra” with assistance from additional tools and scripts.

- [RoboFont 4.5b (latest beta)](http://robofont.com/)
- [Fontra (latest build)](http://fontra.xyz/)
- [VariableValues](http://github.com/gferreira/fb-variable-values)
