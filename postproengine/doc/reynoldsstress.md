# reynoldsstress

Reynolds-Stress average netcdf sample planes
## Inputs: 
```
  name                : An arbitrary name (Required)
  ncfile              : NetCDF sampling file (Required)
  tavg                : Which times to average over (Optional, Default: [])
  meanpklfile         : Name of pickle file which contains mean results (Optional, Default: '')
  savepklfile         : Name of pickle file to save results (Optional, Default: '')
  group               : Which group to pull from netcdf file (Optional, Default: None)
  varnames            : Variables to extract from the netcdf file (Optional, Default: ['velocityx', 'velocityy', 'velocityz'])
```

## Actions: 
```
  radial_stress       : ACTION: Computes the radial Reynolds shear stress from the Cartesian stresses (Optional)
    iplane            : List of iplane values. Default is all planes in ncfile. (Optional, Default: None)
    yc                : Specified lateral center of wake, yc (Optional, Default: 0)
    zc                : Specified vertical center of wake, zc (Optional, Default: 0)
    wake_center_files : csv files containing time series of wake centers for each iplane. yc and zc will be compute based on mean centers over the specified time interval (Optional, Default: None)
  turbulent_fluxes    : ACTION: Computes the turbulent fluxes (Optional)
    iplane            : List of iplane values. Default is all planes in ncfile. (Optional, Default: None)
    include_radial    : Boolean to compute radial reynolds shear stress flux. (Optional, Default: None)
  contourplot         : ACTION: Plot rotor averaged planes (Optional)
    dpi               : Figure resolution (Optional, Default: 125)
    figsize           : Figure size (inches) (Optional, Default: [12, 8])
    savefile          : Filename to save the picture (Optional, Default: '')
    clevels           : Color levels (eval expression) (Optional, Default: '41')
    iplane            : Which plane to pull from netcdf file (Optional, Default: 0)
    xaxis             : Which axis to use on the abscissa (Optional, Default: 'x')
    yaxis             : Which axis to use on the ordinate (Optional, Default: 'y')
    xlabel            : Label on the X-axis (Optional, Default: 'X [m]')
    ylabel            : Label on the Y-axis (Optional, Default: 'Y [m]')
    title             : Title of the plot (Optional, Default: '')
    plotfunc          : Function to plot (lambda expression) (Optional, Default: 'lambda db: 0.5*(db["uu_avg"]+db["vv_avg"]+db["ww_avg"])')
  interpolate         : ACTION: Interpolate data from an arbitrary set of points (Optional)
    pointlocationfunction: Function to call to generate point locations. Function should have no arguments and return a list of points (Required)
    pointcoordsystem  : Coordinate system for point interpolation.  Options: XYZ, A1A2 (Required)
    varnames          : List of variable names to extract. (Required)
    savefile          : Filename to save the interpolated data (Optional, Default: '')
    method            : Interpolation method [Choices: linear, nearest, slinear, cubic, quintic, pchip] (Optional, Default: 'linear')
    iplane            : Which plane to interpolate on (Optional, Default: 0)
    iters             : Which time iterations to interpolate from (Optional, Default: None)
  circavg             : ACTION: Circumferential average data into radial profiles (Optional)
    centerpoint       : Center point to use for radial averaging (Required)
    r1                : Inner radius (Required)
    r2                : Outer radius (Required)
    Nr                : Number of points in radial direction (Required)
    pointcoordsystem  : Coordinate system for point interpolation.  Options: XYZ, A1A2 (Required)
    varnames          : List of variable names to average. (Required)
    savefile          : Filename to save the radial profiles (Required)
    iplane            : Which plane(s) to interpolate on (Optional, Default: 0)
    theta1            : Theta start (Optional, Default: 0.0)
    theta2            : Theta end (Optional, Default: 6.283185307179586)
    Ntheta            : Number of points in theta (Optional, Default: 180)
```

## Example
```yaml
reynoldsstress:
  name: Example YZ plane
  ncfile: YZcoarse_103125.nc
  tavg: [27950,28450]
  group: T0_YZdomain

  radial_stress:
    yc: 1000
    zc: 150
    iplane: 
      - 5
    wake_center_files: 
      - ./wake_meandering/wake_center_5.csv
      
  contourplot:
    #plotfunc: 'lambda db: 0.5*(db["uu_avg"]+db["vv_avg"]+db["ww_avg"])'
    plotfunc: 'lambda db: (-db["ux_avg_uxur_avg"])'
    savefile: test_rs.png
    xaxis: y
    yaxis: z
    xlabel: 'Y [m]'
    ylabel: 'Z [m]'
    iplane: 5

```
