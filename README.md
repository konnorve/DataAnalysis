# DataAnalysis
#### Used by Harland Lab of UC Berkeley
#### Authored by Konnor von Emster

## Description
Program used in conjuction with [videoProcessor](https://github.com/konnorve/videoAnalysis) to analysis behavioral recordings from the jellyfish Cassiopea. This program processes data required

### Description of Jelly Dreamer Project
Conceptualized by Dr. Michael Abrams, our research is intended to uncover the biological underpinnings of sleep. 
In being able to track jellyfish pulse initiation we can study jellyfish behavior down to their ganglia. 

<!--- ## Table of Contents --->

## Installation

## Usage

## Scripts
### DataFrameCreationMethods.py
`def calculateDistance(c1, c2)`
 Distance Formula, calculates how far the jellyfish has moved by finding the distance between two centroids.
 
 `distanceBetween(a1, a2)`
 Returns the shortest difference in degrees betwene two positive, bounded angles. 
 
 `centerChanged(a1, a2, sensativity)`
Determines if the center has changed between two center values where each center value is an angle.
Distance between the two centers is calculated using distance().
If the distance between the two is less than or equal to the
sensativity interval this indicates the center has not changed and
thus false is returned.

Sensativity is the integer value determining whether the center will or not.

`createComplexDF(angleDataPath, orientationDF, FRAMERATE, STARTDATETIME, DAYLIGHTSAVINGS = False)`

`getXtickDF_hour(complexDF)`

`getXtickDF_minute(complexDF)`

`getXtickDF_10minute(complexDF)`

`createActigramArr(complexDF, FRAMERATE, INTERVAL = 5, pulseExtension = 1/2)`

`createDayNightMovementBar(complexDF, width = 4, movementColor = [255, 0, 0], dayColor = [255, 255, 0], nightColor = [0,0,127])`

`createCompressedActigram(actigramCSV, compression_factor)`

`createCompressedMovementDayNightBar(barArr, compression_factor)`

`dfConcatenator(firstDF, firstDFstarttime, secondDF, secondDFstarttime, framerate = 120)`

### plottingMethods.py
`plotInterpulseInterval(outdir, jelly_title, dfComplex, dfxTicks, yfigurelen, xfigurelen)`
`plotInterpulseIntervalWithBar(outdir, jelly_title, dfComplex, dfxTicks, barArr, yfigurelen, xfigurelen)`
`plotCenterHistogramVertical(outdir, jelly_title, dfComplex, yfigurelen, xfigurelen)`

### figures.py

## How it works

## Credits

## License

