# Tutorial 2: Setting up a convectively unstable LES ABL calculation

<!-- NOTE: The tutorial is actually generated by {makescript} -->

<!--INTROTEXTSETUP-->
## Introduction

This tutorial will demonstrate the following features: 
- How to use `amrwind-frontend` to set up an LES ABL case.

### Background

The desired conditions for this ABL case are derived from the IEA29
REF1 conditions measured off of the coast of Denmark.  

| Parameter                 | Value                             |
| ---                       | ---                               |
| Turbine hub height        | {ABLForcing_abl_forcing_height} m |
| Hub height wind speed     | {ABL_windspeed} m/s               |
| Hub height wind direction | {ABL_winddir} degrees             |
| Hub height TI             | 0.068                             |
| Hub height shear exponent | 0.0025                            |
<!--INTROTEXTEND-->

## Simulation settings

In the **Simulation** tab, go to the **Simulation type** window, and 
choose `{incflo_physics}` for **Physics models**.

Then under the **Time control** section, set the following parameters:

| Parameter  | Value            |
| ---        | ---              |
| Max time   | {time_stop_time} |
| Max steps  | {time_max_step}  |
| March with | `{time_control}` |
| dt         | {time_fixed_dt}  |

Under **Restart parameters**, set **Check file** to `{io_check_file}`
and **Checkpoint interval** to `{time_checkpoint_interval}`.
Then the settings at the top of the tab should look like:  

![{img_time_settings}]({img_time_settings})

Now in the **Fluid and transport properties** section, set the
following:

| Parameter         | Value                 |
| ---               | ---                   |
| Dynamic viscosity | {transport_viscosity} |

In the **Godunov parameters** section and the **Turbulence
parameters** section, set the following parameters:

| Parameter        | Value                 |
| ---              | ---                   |
| Use godunov      | {incflo_use_godunov}  |
| Godunov type     | {incflo_godunov_type} |
| Turbulence model | {turbulence_model}    |
| TKE source terms | {TKE_source_terms}    |

After setting these variables, the bottom part of the tab should look
like:

![{img_turb_settings}]({img_turb_settings})

## Domain and boundary conditions

In the **Domain** tab, we'll set the computational domain and boundary
conditions.

| Parameter       | Value              | Comment                               |
| ---             | ---                | ---                                   |
| Domain corner 1 | {geometry_prob_lo} |                                       |
| Domain corner 2 | {geometry_prob_hi} |                                       |
| Mesh size       | {amr_n_cell}       | Number of cells in X, Y, Z directions |
| Periodic in X   | {is_periodicx}     |                                       |
| Periodic in Y   | {is_periodicy}     |                                       |
| Periodic in Z   | {is_periodicz}     | Z is not periodic                     |


![{img_domain_settings}]({img_domain_settings})

Now we'll set the boundary conditions on the upper and lower Z
surfaces. Press **[show]** next to **Boundary conditions on Z faces**,
then use these parameter values in the following fields, and you can
leave the remainder of them blank.

| Parameter       | Value                  | Comment                          |
| ---             | ---                    | ---                              |
| zlo velocity BC | {zlo_type}             |                                  |
| zlo temp BC     | {zlo_temperature_type} |                                  |
| zlo TKE BC      | {zlo_tke_type}         |                                  |
| zhi velocity BC | {zhi_type}             |                                  |
| zhi temp BC     | {zhi_temperature_type} |                                  |
| zhi temperature | {zhi_temperature}      | This is actually the dT/dz value |


It should look like this in the front-end interface:
	
![{img_zBC_settings}]({img_zBC_settings})

## ABL settings

In the **ABL** tab, we'll add the necessary physical values for an ABL
simulation.  First in the **ABL Forcing** window, check the following
items:

| Parameter              | Value               |
| ---                    | ---                 |
| add ABL Forcing        | {ABLForcing}        |
| add Coriolis forces    | {CoriolisForcing}   |
| add Boussinesq forcing | {BoussinesqForcing} |

Next we'll set the ABL wind speed and direction.  In the **ABL
physics** section, check the **Use speed & dir instead** checkbox,
then use the following variables:

| Parameter      | Value                           |
| ---            | ---                             |
| Wind speed     | {ABL_windspeed}                 |
| Wind direction | {ABL_winddir}                   |
| Forcing height | {ABLForcing_abl_forcing_height} |

 Then hit the **[Calc W. Vec]** button, and it should automatically
 calculate the correct wind vector to use.  Under the **ABL
 properties** section, fill in the following values:
 
| Parameter            | Value                       |
| ---                  | ---                         |
| kappa                | {ABL_kappa}                 |
| ABL normal direction | {ABL_normal_direction}      |
| z0 roughness         | {ABL_surface_roughness_z0}  |
| ABL ref temp         | {ABL_reference_temperature} |
| surf temp rate       | {ABL_surface_temp_rate}     |
| surf temp flux       | {ABL_surface_temp_flux}     |
| M.O. beta_m          | {ABL_mo_beta_m}             |
| M.O. gamma_m         | {ABL_mo_gamma_m}            |
| M.O. gamma_h         | {ABL_mo_gamma_h}            |
 

In the **Coriolis forces** and **Boussinesq forces** sections, put in
the following parameters:

| Parameter             | Value                                      |
| ---                   | ---                                        |
| Latitude              | {CoriolisForcing_latitude}                 |
| Reference Temperature | {BoussinesqBuoyancy_reference_temperature} |

The top part of the **ABL** tab should then look like:  

![{img_ABL_settings1}]({img_ABL_settings1})

Scrolling down the same tab, next we'll specify the initial
temperature profile in the **ABL temperature profiles** section:

| Parameter        | Value                     |
| ---              | ---                       |
| Temp profile z   | {ABL_temperature_heights} |
| Temp profile val | {ABL_temperature_values}  |

In the **ABL perturbations** tab, we're going to override the amr-wind
frontend defaults, by putting `None` in a number of fields.  Using
`None` will prevent these parameters from appearing in the final input
file.

| Parameter               | Value                    |
| ---                     | ---                      |
| Ref z for vel perturb   | {ABL_perturb_ref_height} |
| Num of periods in x     | {ABL_Uperiods}           |
| Num of periods in y     | {ABL_Vperiods}           |
| Amp. of U fluct.        | {ABL_deltaU}             |
| Amp. of V fluct.        | {ABL_deltaV}             |
| Amp. of T perturbations | {ABL_theta_amplitude}    |
| Max T perturb height    | {ABL_cutoff_height}      |

In the **ABL output parameters** section, put in the following inputs.

| Parameter        | Value                        |
| ---              | ---                          |
| Output frequency | {ABL_stats_output_frequency} |
| Output format    | {ABL_stats_output_format}    |


![{img_ABL_settings2}]({img_ABL_settings2})

## IO settings

In this section, we're going to be specifying the outputs and the
sampling probes in the simulation.  In the **IO** tab, we'll first set
some generic parameters in the **Plot Ouputs** section:  

| Parameter     | Value                |
| ---           | ---                  |
| Verbosity     | {incflo_verbose}     |
| Plot interval | {time_plot_interval} |

Under **Post processing**, select `{incflo_post_processing}`.  Then
in the **Sampling probes** section, set the following values:  

| Parameter   | Value                       |
| ---         | ---                         |
| Output freq | {sampling_output_frequency} |
| Variables   | {sampling_fields}           |

The tab should then looks something similar to:  

![{img_IO_settings}]({img_IO_settings})

Now we're going to set up 3 different sets of sampling planes.  One
set will be for hub-height X-Y planes, another for the X boundary
planes, and one for the Y boundary planes.  To set up the hub height
planes, click on the **[New]** in the **Sampling probes** section,
then put in the following information at the top:

| Parameter | Value       |
| ---       | ---         |
| Name      | {phub_name} |
| Type      | {phub_type} |

![{img_phub_settings1}]({img_phub_settings1})

Click on the **[show]** button under **Sample plane specifications**
and then put in the following details:  

| Parameter        | Value         |
| ---              | ---           |
| Plane num points | {phub_Npts}   |
| Plane origin     | {phub_origin} |
| Plane axis1      | {phub_axis1}  |
| Plane axis2      | {phub_axis2}  |
| Plane normal     | {phub_normal} |
| Plane offsets    | {phub_offset} |

That part of the windows should then look like:  

![{img_phub_settings2}]({img_phub_settings2})

Then click **[Save & Close]**.

Now to set up the X boundary sample planes, click on **[New]** again
and put in these values at the top:

| Parameter | Value      |
| ---       | ---        |
| Name      | {xbc_name} |
| Type      | {xbc_type} |

![{img_xbc_settings1}]({img_xbc_settings1})

And in the **Sample plane specifications**, put in these values: 

| Parameter        | Value        |
| ---              | ---          |
| Plane num points | {xbc_Npts}   |
| Plane origin     | {xbc_origin} |
| Plane axis1      | {xbc_axis1}  |
| Plane axis2      | {xbc_axis2}  |
| Plane normal     | {xbc_normal} |
| Plane offsets    | {xbc_offset} |

which will look like this in the window: 

![{img_xbc_settings2}]({img_xbc_settings2})

Then click **[Save & Close]**.  For the Y boundary planes, use these inputs 

| Parameter | Value      |
| ---       | ---        |
| Name      | {ybc_name} |
| Type      | {ybc_type} |

![{img_ybc_settings1}]({img_ybc_settings1})

And these geometry settings: 

| Parameter        | Value        |
| ---              | ---          |
| Plane num points | {ybc_Npts}   |
| Plane origin     | {ybc_origin} |
| Plane axis1      | {ybc_axis1}  |
| Plane axis2      | {ybc_axis2}  |
| Plane normal     | {ybc_normal} |
| Plane offsets    | {ybc_offset} |

![{img_ybc_settings2}]({img_ybc_settings2})

Then click **[Save & Close]**.  

## Expert settings

In the last settings for the simulation, we'll put in a few details in
the **Expert** tab.  This is optional, and mostly to keep things
consistent with previous ABL solutions.  Put in the following values
in the **Tolerances** section:  

| Parameter                     | Value                           |
| ---                           | ---                             |
| nodal_proj.mg_rtol            | {nodal_proj_mg_rtol}            |
| nodal_proj.mg_atol            | {nodal_proj_mg_atol}            |
| mac_proj.mg_rtol              | {mac_proj_mg_rtol}              |
| mac_proj.mg_atol              | {mac_proj_mg_atol}              |
| diffusion.mg_rtol             | {diffusion_mg_rtol}             |
| diffusion.mg_atol             | {diffusion_mg_atol}             |
| temperature_diffusion.mg_rtol | {temperature_diffusion_mg_rtol} |
| temperature_diffusion.mg_atol | {temperature_diffusion_mg_atol} |

In the **Numerics** section, put in the following values: 

| Parameter             | Value                   |
| ---                   | ---                     |
| Random Gauss mean     | {ABL_random_gauss_mean} |
| Random Gauss Variance | {ABL_random_gauss_var}  |

The resulting tab should then look like: 

![{img_expert_settings}]({img_expert_settings})

## Plot of the domain

To visualize the domain with the ABL forcing and the sampling planes,
click on the menu bar's **Plot** --> **Plot domain** option.  Then
under the **Select sample probes** section, choose **[Select all]**:  

![{img_plotDomainWin_samplingzone}]({img_plotDomainWin_samplingzone})

Now press **[Plot Domain]** and you should see the following plotted: 

![{img_plotDomainFig_sampling}]({img_plotDomainFig_sampling})

## Writing the input file

To see what the AMR-Wind input file would look like, you can go to the
menu bar, select **Run** --> **Preview Input File**, to see the
preview window.  Then, once you're satisfied with the way things look,
you can hit **File** --> **Save input file as** to save it to a file.

The result should be similar to 

<details>
  <summary>[input file]</summary>
<pre>
{amrwindinput1}
</pre>
</details>

