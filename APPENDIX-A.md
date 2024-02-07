Appendix A
==========

Data processing for Oklahoma and South Dakota
---------------------------------------------

[Maria Parazo Rose](https://grist.org/author/maria-parazo-rose/)

Feb 07, 2024

### Oklahoma

The Oklahoma Commissioners of the Land Office gave us a file that had records of all state trust land parcels that had Oklahoma State University as the trust beneficiary. We then split that file into four separate CSVs based on the lease types: agricultural, short-term commercial, long-term commercial, and mineral. According to officials, we could categorize the agricultural, short-term commercial, and long-term commercial parcels as surface parcels. The mineral parcels were to be counted as subsurface parcels.

They were not able to provide spatial data, so we instead queried state REST API servers.

The state assigns each parcel a Holding Detail ID, which is a unique identifier. This is the field we used to match between the REST API servers and the state-supplied file of OSU holdings, since the parcels have the same identifier across different resources.

The three surface files were matched to the Oklahoma [Real Estate Subdivisions](https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/2) layer.

The one subsurface file was matched to the [Unleased Minerals](https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/10) and [Mineral Subdivisons](https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/3) layers.

The resulting data frames from these join queries were deduplicated in the same manner as the other state files. For the surface rights-type files, we made sure to capture the name of the lease type (agriculture, short term or long term commercial lease) as the activity of the parcel, based on the raw data.

For the subsurface files, we had additional processes to follow. We queried the state's [Mineral Leases](https://gis.clo.ok.gov/arcgis/rest/services/Public/OKLeaseData_ExternalProd/MapServer/1) layer for parcels that were associated with OSU, and then joined the results of that query to the Mineral Subdivisions data frame, to add additional nuance to the activity field of those parcels, reporting that there was an existing mineral lease. After that joining process, we combined the Unleased Minerals layer to it.

After this process, we identified the parcels that did not get a spatial data match in the state servers and searched for them in other state PLSS servers.

The Oklahoma Commissioners of the Land Office was clear that not all of the parcels that we were looking for had been saved as spatial data. Users should bear this in mind when analyzing OK data -- that, for this state, our dataset is incomplete.

As of November 2023, the state reported that there should be this number of parcels:

Agriculture: 736

Long term commercial: 9

Short term commercial: 13

Mineral: 2155

* * * * *

### South Dakota

This document explains the steps for processing the South Dakota data that was provided to us. There was no spatial data and we were given limited information on the MTRSA numbers, so we had to do significant processing to track the information down on the state's [PLSS server](https://arcgis.sd.gov/arcgis/rest/services/SD_All/Boundary_PLSS_QuarterQuarter/MapServer/0). We cleaned the ID information associated with the parcels and then queried for those adjusted IDs in this state spatial data server. The following files can be found in the [`sd_data`](https://github.com/Grist-Data-Desk/land-grab-2/tree/main/land_grab_2/stl_dataset/step_1/only_south_dakota_stl_input_gen/sd_data) folder and its parent directory.

Files

-   `Original_SD Electronic Mineral Book.xlsx`

-   `Original_University Surface Land.xlsx`

    -   The two documents above are the original copies of what the [South Dakota School and Public Lands department](https://sdpubliclands.sd.gov) supplied when we requested data for state trust land parcels.

-   `SD-Reported_Subsurface_A-Parcels.xlsx`

-   `SD-Reported_All_STLs.xlsx`

-   `Subsurface_Simple.csv`

-   `Surface_Simple.csv`

    -   The two documents above contain concatenated versions of SD-reported state trust land parcel ID numbers, and are used in the sd_parcel_match.py file

-   `PLSS Divisions.xlsx`

    -   Reference file for understanding how PLSS sections are divided

FOLDER: `sd_parcel_match_SAMPLE_FILES`

-   `done.csv`

-   `sd_subsurface.csv`

-   `sd_surface.csv`

FOLDER: `sd_parcel_match_report_SAMPLE_FILES`

-   `match_report.csv`

-   `unmatch_subsurface.csv`

-   `unmatch_surface.csv`

-   `sd_parcel_match.py`

-   `sd_parcel_match_report.py`

-   `export_to_json.py`

Data Acquisition and Cleaning

-   Subsurface data: In the `Original_SD Electronic Mineral Book` document, select rows that have an "A" listed in the aliquot/lot details column. This indicates the beneficiary is South Dakota State University. Must go to each county, stored in separate tabs (refer to document `SD-Reported_Subsurface_A-Parcels` for A-specific subsurface parcels).

-   Surface data: In the `Original_University Surface Land` document, all relevant surface parcels are listed.

-   Concatenate TRS fields into a single digit, which will then be used to match against South Dakota's PLSS Quarter Quarter server in order to get spatial data. (Refer to document `SD-Reported_All_STLs`.)

-   PLSS formatting notes

    -   Full PLSS format for South Dakota: 

        -   (SD xx) (xxx 0 D) (xxx 0 D) (0) (SN xx) (0) (A or L xxxx)

        -   Meridian, township + direction, range + direction, SPACE, section number, SPACE, aliquot or lot (aliquot will have 4 digits following)

        -   Ex. SD051100N0670W0SN030ASWNW

        -   SD05   110   0  N  067  0  W  0  SN 03  0  ASWNW

    -   Adjusted subsurface format: 

        -   xxx xxx SN xx A or L xxx

        -   Ex. 110 067 SN03 ASWNW

    -   Adjusted surface format: 

        -   xxx 0D xxx 0D 0 SN xx A or L xxxx

        -   Ex. 1100N 0670W 0 SN03 ASWNW

    -   Be sure to clean extra spaces, convert numbers in the aliquot field appropriately (4 becomes nothing, 2 becomes ½), use the delimiter on the Aliquot/Lot field and separate on the comma so a new row is created, replicating the rest of the data in the row except for the adjusted A/L value. 

    -   Make sure township and range values are 3 digits long, that the SN value is 2 digits long with "SN" at the front, and that an "A" is in front of aliquot values or an "L" is in front of lot values. 

        -   Aliquot values include directional characters (ex. NESW); Lots are numbers only. 

Parcel Processing

-   Run `sd_parcel_match.py` with files `Subsurface_Simple` and `Surface_Simple`

    -   This file is used to reformat all the Grist-generated PLSS numbers so that the Aliquot value matches the quarter-quarter format (indicated in the ALI_SPLITS list at the top of the file). 

        -   For example, SSW translates to the southern half of the southwest quarter. In reality, this refers to two separate parcels: SWSW and SESW (southwest quarter of the southwest quarter and southeast quarter of the southwest quarter). We must convert all aliquot values to this format to get as close as possible to finding all parcels. (Refer to `PLSS Divisions` document for help).

    -   This file will also match the reformatted Grist-generated PLSS numbers against PLSS numbers from the [South Dakota state PLSS server ](https://arcgis.sd.gov/arcgis/rest/services/SD_All/Boundary_PLSS_QuarterQuarter/MapServer/0)by calling each row in the server (the SECDIVID field specifically) and converting that into both the surface and subsurface formats we created, and then downloading it if there is a match. 

    -   Three files will be generated: 

        -   `sd_subsurface.csv` and `sd_surface.csv` are adjusted versions of the two input files we used that now include the reformatted aliquot value. 

        -   `done.csv` is a list of all the rows that were matched from the server.

        -   Refer to the `sd_parcel_match_SAMPLE_FILES` folder to see results of my query.

-   Run `sd_parcel_match_report.py` file with the three files just generated to create:

    -   1) A list of all the matching parcels downloaded from the server that indicates the rights-type of the parcel, surface, subsurface, or both. This will be called `match_report.csv`.

    -   2) `unmatch_surface.csv` and `unmatch_subsurface.csv`. These are lists of Grist-generated PLSS numbers that did not find a match in the server. Some of this can be fixed, as I did with 15 out of the 24 unmatched surface parcels. A few of the PLSS ids are formatted incorrectly and some of them need to be compared against the FRSTDIVID field instead of the SECDIVID field because the parcel refers to the entire section.

-   Run `export_to_json.py` file to get the spatial data

    -   This file reads the `match_report.csv` to keep track of the rights-type information and joins this information to `done.csv` file to get the spatial information. It formats the information to be read as spatial data AND it combines some of the missing unmatched surface parcels that I found (refer to `parcels_data` folder).

    -   Output of this file is `complete.geojson`, which includes all South Dakota state trust lands (except for a few unmatched subsurface parcels that I still need to find). 

        -   CRS assigned in the file is `EPSG:4326`. If it doesn't show up, transform in QGIS to `EPSG:3857`.

    -   Combine this SD state file with the rest of the state files in the `dataset-merge` step of the program.
