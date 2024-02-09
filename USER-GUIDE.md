How to conduct your own reporting and research on state trust lands
===================================================================

A guide to using Grist's database.
----------------------------------

![](https://grist.org/wp-content/uploads/2024/02/LGU-module3.jpg?quality=75&strip=all)

[Maria Parazo Rose](https://grist.org/author/maria-parazo-rose/)

Feb 07, 2024

**Contents**

-   Overview
-   What's in the database
-   Creative Commons license
-   Citation
-   File descriptions

* * * * *

Overview
--------

This user guide is designed for both general users and experienced researchers and coders. No coding skills are necessary to work with this dataset, but a basic working knowledge of tabular data files in Excel is required, and for more experienced users, knowledge of GIS. 

Over the past year, Grist has located all [state trust lands](https://en.wikipedia.org/wiki/State_Trust_Lands#cite_note-1) distributed through state enabling acts that currently send revenue to higher education institutions that [benefited from the Morrill Act](https://www.hcn.org/issues/52.4/indigenous-affairs-education-land-grab-universities). We've also identified their original Indigenous inhabitants and caretakers, and researched how much the United States would have paid for each parcel, based on an assessment of the cession history (according to the U.S. Forest Service's record of the land associated with each parcel). We reconstructed more than 8.2 million acres of state trust parcels taken from 123 tribes, bands, and communities through 121 different land cessions --- a legal term for the giving up of territory. 

It is important to note that land cession histories are incomplete and accurate only from the viewpoint of U.S. law and historical negotiations, not to Indigenous histories, epistemologies, or historic territories not captured by federal data. The U.S. Forest Service dataset, which is based on the Schedule of Indian Land Cessions compiled by Charles Royce for the [Eighteenth Annual Report of the Bureau of American Ethnology to the Secretary of the Smithsonian Institution (1896-1897)](https://www.loc.gov/collections/century-of-lawmaking/articles-and-essays/century-presentations/indian-land-cessions/), covers the period from 1787 to 1894.

This information represents a snapshot of trust land parcels and activity as of November 2023. We encourage exploration of the database and caution that this snapshot is likely very different from state inventories 20, 50, or even 100 years ago. Since, to our knowledge, no other database of this kind --- with this specific state trust land data benefitting land-grant universities --- exists, we are committed to making it publicly available and as robust as possible.

For additional information, users can read our [methodology](https://github.com/Grist-Data-Desk/land-grab-2/blob/main/METHODOLOGY.md) or go to [GitHub to view and download the code](https://github.com/Grist-Data-Desk/land-grab-2) used to generate this dataset. The various functions used within the program can also be adapted and repurposed for analyzing other kinds of state trust lands --- for example, those that send revenue to penitentiaries and detention centers, which is present in a number of states. 

**Note: If you use this data for your reporting, please be sure to credit Grist in the story and ****[please send us](mailto:landgrabu@grist.org)**** a link.**

The database administrator can be contacted at [landgrabu@grist.org.](mailto:landgrabu@grist.org)

What's in the database
----------------------

This database contains a GeoJSON and CSVs, as well as a multi-tab spreadsheet that aggregates and summarizes key data points. 

**GeoJSON**

1.  `National_STLs.geojson`

**CSVs**

1.  `National_STLs.csv`
2.  `Tribal_Summary.csv`
3.  `University_Summary.csv`

**Excel**

1.  `GRIST-LGU2_National-STL-Dataset.xlsx`, with protected tabs that include:

-- Main Spreadsheet\
-- Tribal Summary\
-- University Summary

The data can be spatially analyzed with the JSON file using GIS software (e.g. ArcGIS or QGIS), or analyzed with the CSVs or Excel main spreadsheet. To conduct analysis without using the spatial file, we recommend using the `National_STLs_ALL_Protected.xlsx` sheet, which includes tabs for the summary statistics sheets. The CSVs will mostly be useful for importing the files into GIS software or other types of software for analysis.

### Tips for using the database

#### **Summary statistics**

To understand the landscape of state trust land parcels at a quick glance, users can reference the summary statistics sheets. The `Tribal_Summary.csv` and the `University_Summary.csv` show the total acreage of trust lands associated with each tribe or university, as well as context on what cessions and tribes are affiliated with a particular university or, conversely, what universities and states are associated with individual tribal nations. 

For example, using the `University_Summary.csv` a user can easily generate the following text: 

> "New Mexico State University financially benefits from almost 186,000 surface acres and 253,500 subsurface acres, taken from the Apache Tribe of Oklahoma, Comanche Nation, Fort Sill Apache Tribe of Oklahoma, Jicarilla Apache Nation, Kiowa Tribe, Mescalero Apache Tribe, Navajo Nation, San Carlos Apache Tribe, Tonto Apache Tribe, and White Mountain Apache Tribe. Our data shows that this acreage came into the United States' possession through 8 Indigenous land cession events for which the U.S. paid approximately $59,000, though in many cases, nothing was paid. New Mexico engages primarily in oil and gas production, renewables, and agriculture and commercial leases."

![](https://grist.org/wp-content/uploads/2024/01/01-lgu-user-guide.jpg?quality=75&strip=all)

To do so, simply fill in the sections you need from the tabular data of the university summary tab: [column B] benefits from almost [column D] surface acres and [column C] subsurface acres, taken from [column H] tribe (or [column G] total number of tribes). Our data shows that this acreage came into the United States' possession through [column K] cessions (column K shows total number of cessions) for which the U.S. paid approximately [column F] though in many cases, nothing was paid. New Mexico engages primarily in [`National_STLs.csv`**,** column K].

Using `Tribal_Summary.csv` users can also center stories through Indigenous nations. For example: "The Cheyenne and Arapaho Tribes of Oklahoma ceded almost 66,000 surface acres and 82,500 subsurface acres, through 2 land cession events, for the benefit of Colorado State University, Oklahoma State University, and the University of Wyoming. For title to those acres, the United States paid the Cheyene and Arapaho Tribes approximately $6.00."

![](https://grist.org/wp-content/uploads/2024/01/02-lgu-user-guide.jpg?quality=75&strip=all)

Similarly to the university tab, one can plug in relevant information: [column B] ceded almost [column F] surface acres and [column E] subsurface acres, through [column C] land cession events, for the benefit of [column H].

To get information on how much the United States paid tribes, if anything, filter for the parcels of interest in the 'Main Spreadsheet' of the `National_STLs.xlsx` file and add the price paid per parcel column [column X].

#### **Navigating the data**

For users who want to conduct analysis on and understand the landscape of state trust lands without using the spatial file, they can use the protected Excel sheet. (The sheet is protected so that cell values are not accidentally rewritten while users search the information.) 

As an example, if users wanted to do research on a specific institution, they can adjust multiple columns at once in the Excel main spreadsheet to quickly isolate the parcels they are specifically interested in. 

Say a user wanted to figure out how many acres of state trust lands specifically affiliated with the Navajo Nation are used for grazing in Arizona. 

Start by opening the protected `National_STLs.xlsx` sheet. 

In column B, click the drop-down arrow and select so that only Arizona parcels are showing.

![](https://grist.org/wp-content/uploads/2024/01/03-lgu-user-guide.jpg?quality=75&strip=all)

Then, go to column K and use the drop-down menu to select parcels where "grazing" is listed as one of the activities. It's important to note that many parcels have multiple activities attached to them.

![](https://grist.org/wp-content/uploads/2024/01/04-lgu-user-guide.jpg?quality=75&strip=all)

Then, go through all of the `present_day_tribe` columns (AA, AE, AI, AM, AQ, AU, AY, BC) and filter for rows that list the Navajo Nation as one of the tribes. It is not always the case that tribes are present in all eight of the columns, and most parcels do not intersect with multiple cession areas. 

![](https://grist.org/wp-content/uploads/2024/01/05-lgu-user-guide.jpg?quality=75&strip=all)

When filtering through a column for specific entries, like selecting all parcels with any grazing present (even if other activities are there), we recommend users open up the filtering drop-down menu, unselect all entries, and then type the query you're interested in in the search bar, and select the results that show up. 

We find a total of 20,278 acres in Arizona that have grazing activity on Navajo land.

![](https://grist.org/wp-content/uploads/2024/01/06-lgu-user-guide.jpg?quality=75&strip=all)

This kind of approach can be used to filter for any combination of parcels, and we encourage you to explore the data this way. 

#### **Visualizing parcels**

To visualize this data, users can use the GeoJSON file in a GIS program of their choice. If users are unfamiliar with how to filter for specific parcels through those programs, they can identify the exact parcels they want in Excel and then use that to select parcels in a GIS program. 

First, identify the specific parcels of interest using filters (like in the situation described above), and then copy the list of relevant object IDs (in column A) into its own CSV file.

![](https://grist.org/wp-content/uploads/2024/01/07-lgu-user-guide.jpg?quality=75&strip=all)

Then, in the GIS software, import the CSV file and join it to the original `National_STLs.geojson` file. 

![](https://grist.org/wp-content/uploads/2024/01/08-lgu-user-guide.jpg?quality=75&strip=all)

![](https://grist.org/wp-content/uploads/2024/01/09-lgu-user-guide.jpg?quality=75&strip=all)

![](https://grist.org/wp-content/uploads/2024/01/10-lgu-user-guide.jpg?quality=75&strip=all)

![](https://grist.org/wp-content/uploads/2024/01/11-lgu-user-guide.jpg?quality=75&strip=all)

After the file is joined, there will be an additional column to the `National_STLs` layer, and users can filter out the blank rows (which would be blank because they did not match with parcels of interest in the CSV file) and select the polygons that represent the parcels the user is interested in. 

![](https://grist.org/wp-content/uploads/2024/01/12-lgu-user-guide.jpg?quality=75&strip=all)

![](https://grist.org/wp-content/uploads/2024/01/13-lgu-user-guide.jpg?quality=75&strip=all)

In QGIS, you can use the "Zoom to Layer" button to visualize the resulting query.

![](https://grist.org/wp-content/uploads/2024/01/14-lgu-user-guide.jpg?quality=75&strip=all)

As an alternative to performing the filtering in Excel and executing the self-join as described above, users may also filter the dataset directly in the GIS program of their choice using structured queries. For example, to replicate the query illustrated above, use the following filter expression in QGIS on the main GeoJSON file:

![](https://grist.org/wp-content/uploads/2024/01/15-lgu-user-guide.jpg?quality=75&strip=all)

#### **Calculating acreage**

The acreage of trust lands within a state has been determined as consisting of acres with surface rights or subsurface rights. For further background on this process, please see our [methodology documentation](https://github.com/Grist-Data-Desk/land-grab-2/blob/main/METHODOLOGY.md). 

We also included a column for net acreage, since in some places --- like North Dakota and Idaho --- the state only has partial ownership over some of the parcels. If the field is blank, the state has 100 percent ownership of the parcel. To calculate this, we multiplied the acreage of a parcel by percentage of ownership. 

#### **Missing cession payment**

We do not yet have financial information for cession ID [717](https://www.loc.gov/resource/g3701em.gct00002/?sp=61) in Washington. The cession in question is 1,963.92 acres, and its absence means that the figures for price paid per acre or price paid per parcel are not complete for Washington. 

It is also important to note that when documenting Indigenous land cessions in the continental United States, the Royce cession areas are extensive but incomplete. Although they are a standard source and are often treated as authoritative, they do not contain any cessions made after 1894 and likely miss or in other ways misrepresent included cessions prior to that time. We have made efforts to correct errors (primarily misdated cessions) when found, but have, in general, relied on the U.S. Forest Service digital files of the Royce dataset. A full review, revision, and expansion of the Royce land cession dataset is beyond the scope of this project. 

#### **Missing Oklahoma lands**

It's important to note that we could not find information for 871 surface acres and 5,982 subsubsurface acres in Oklahoma, because they have yet to be mapped, digitally, or because of how they are sectioned on the land grid. We understand that this acreage does exist based on lists of activities kept by the state. However, those lists do not provide mappable data to fill these gaps. In order to complete reporting on Oklahoma, researchers will need to read and digitize physical maps and plats held by the state --- labor this team has been unable to provide.

#### **Additional WGS84 files in data generation**

In addition to the GeoJSON files output at each step, our workflow produces a version of each GeoJSON file using the World Geodetic System 84 (WGS84) datum and a spherical geographic coordinate system (EPSG:4326). This is the standard coordinate reference system (CRS) for all GeoJSON files [according to the specification](https://datatracker.ietf.org/doc/html/rfc7946#section-4); prior versions of the specification supported alternate CRSs, but have since been deprecated. In the source code, we rely on [GeoPandas'](https://geopandas.org/en/latest/docs/reference/api/geopandas.GeoDataFrame.to_crs.html) `.to_crs` method to perform the transformation to EPSG:4326.

WGS84 versions of GeoJSON files are necessary when mapping datasets using popular web-mapping libraries like Leaflet, Mapbox, MapLibre, and D3. These libraries all expect data to be encoded using EPSG:4326; they expose various projection APIs to reproject data on-the-fly in a browser. You should use the `_wgs84` versions of the pipeline's GeoJSON files if you're trying to visualize the datasets using one of these libraries. For QGIS users, ensure your project CRS is set to EPSG:4326 before uploading these GeoJSON files.

#### **Using the code**

Users will be able to explore the codebase on the [GitHub repository](https://github.com/Grist-Data-Desk/land-grab-2), which will be made public upon the lifting of Grist's embargo. Further details on how to run each step and an explanation of all required files are available in the `README.md` document.

Creative Commons license
------------------------

This data is shared under a Creative Commons BY-NC 4.0 license ("Attribution-NonCommercial 4.0 International"). The CC BY-NC license means you are free to copy and redistribute the material in any medium or format; and remix, transform, and build upon the material. Grist cannot revoke these freedoms as long as you follow the license terms. These terms include giving appropriate credit, providing a link to the license, and indicating if changes were made. You may do so in any reasonable manner. Furthermore, you may not use the material for commercial purposes, and you may not apply legal terms or technological measures that legally restrict others from doing anything the license permits. 

More information is available at the [CC BY-NC 4.0 deed.](https://creativecommons.org/licenses/by-nc/4.0/)

Citation
--------

If you republish this data or draw on it as a source for publication, cite as: *Parazo Rose, Maria, et al. "Enabling Act Indigenous Land Parcels Database," Grist.org, February 2024.*

File Descriptions
-----------------

### National_STLs.geojson

The schema for this document is the same as the `National_STLs.csv`and `National_STLs_Protected.xlsx`files. 

This spreadsheet contains 41,792 parcels of state trust lands that benefit 14 universities. Each row describes the location of a unique parcel, along with information about the entities currently managing the land, what rights type and extractive activities are associated with the parcel, which university benefits from the revenues, and its historic acquisition by the United States, as well as the original Indigenous caretakers and the current tribal nations in the area. 

An important note about rights type: Washington categorizes timber rights as distinct from surface rights, and we present the data here accordingly. Note that other states do not adhere to this distinction, and thus timber parcels in other states are considered surface parcels. If you would like to generate national summaries of surface rights in a more colloquial sense, consider adding Washington's timber parcels to your surface calculations.

The file contains the following columns:

`object_id`

-   A unique, Grist-assigned identifier for the specific state trust land parcel

`state`

-   State where parcel is located

`state_enabling_act`

-   Name of the enabling act that granted new territories statehood, along with stipulations of bestowing Indigenous land as a part of the state trust land policy

`trust_name`

-   Beneficiaries of state trust land revenue can be identified within state government structure by the trust name; we used the trust name to identify the funds that were specifically assigned to the universities we focused on

`managing_agency`

-   Name of the state agency that manages the state trust land parcels

`university`

-   Land-grant university that receives the revenue from the associated state trust land parcel

`acres`

-   Reported acreage of the state trust land parcel from the original data source by the state

`gis_acres`

-   Acreage calculated by analyzing the parcels in QGIS

`net_acres`

-   The net acreage of a parcel, determined by the percentage of state ownership related to that parcel specifically. 

`rights_type`

-   Indicates whether the state/beneficiary manages the surface or subsurface rights of the land within the parcel, or both

`reported_county`

-   County where parcel is located, as reported by the original data source

`census_bureau_county_name`

-   County where parcel is located, based on a comparative analysis against Census Bureau data

`meridian`

-   A line, similar to latitude and longitude lines, that runs through an initial point, which together with the baseline form the highest level framework for all rectangular surveys in a given area. It is also the reference or beginning point for measuring east or west ranges.

`township`

-   36 sections arranged in a 6-by-6 square, measuring 6 miles by 6 miles. Sections are numbered beginning with the northeasternmost section (#1), proceeding west to 6, then south along the west edge of the township and to the east (#36 is in the SE corner)

`range`

-   A measure of the distance east or west from a referenced principal meridian, in units of 6 miles, that is assigned to a township by measuring east or west of a principal meridian

`section`

-   The basic unit of the system, a square piece of land 1 mile by 1 mile containing 640 acres

`aliquot`

-   Indicates the aliquot part, e.g. NW for northwest corner or E½SW for east half of southwest corner, or the lot number. 

`block`

-   A parcel of land within a platted subdivision bounded on all sides by streets or avenues, other physical boundaries such as a body of water, or the exterior boundary of a platted subdivision.

`data_source`

-   Data on state parcels was acquired either from a records request to state agencies or from requests to a state server; if a state server was used, the website is recorded here

`parcel_count`

-   In our merge process, we combined some parcels, particularly in Minnesota, and this column captures how many parcels were aggregated together, to maintain accurate parcel count and acreage 

`agg_acres_agg`

-   The sum of acres across all parcels contained in a given row. For most states, this field will equal that of the *acres* field. For Minnesota, some small parcels were combined during the spatial deduplication process, and this field reflects the sum of the corresponding *acres* field for each parcel. (See [methodology](https://github.com/Grist-Data-Desk/land-grab-2/blob/main/METHODOLOGY.md) for more information.) 

`all_cession_numbers`

-   Refers to all the land cessions (areas where the federal government took the Indigenous land that later supplied state land) that overlap with this given parcel

`price_paid_for_parcel`

-   The total price paid by the U.S. government to tribal nations

`cession_num_01-08`

-   A single cession that overlaps a given parcel

`price_paid_per_acre`

-   The price the U.S. paid (or didn't pay) per acre, according to the specific cession history

`C1[-C8]_present_day_tribe`

-   As listed by the U.S. Forest Service, the present day tribe(s) associated with the parcel

`C1[-C8]_tribe_named_in_land_cessions_1784-1894`

-   As listed by the U.S. Forest Service, the tribal nation(s) named in the land cession associated with the parcel

### Tribal_Summary.csv

This spreadsheet shows summary statistics for all state trust land data we gathered, organized by the present-day tribes listed by the U.S. Forest Service.

`present_day_tribe`

-   As listed by the U.S. Forest Service, the present day tribe(s) 

`cession_count`

-   Total number of cessions associated with a present-day tribe

`cession_number`

-   List of cessions associated with a present-day tribe

`subsurface_acres`

-   Total number of subsurface acres associated with a present-day tribe

`surface_acres`

-   Total number of surface acres associated with a present-day tribe

`timber_acres`

-   Total number of timber acres associated with a present-day tribe (only relevant in Washington state)

`unknown_acres`

-   Total number of acres with an unknown rights type (only relevant for two parcels in South Dakota)

`university`

-   Universities that receive revenue from the parcels associated with a present-day tribe

`state`

-   States where the parcels associated with a present-day tribe are located

-   Total number of acres with an unknown rights type (only relevant for two parcels in South Dakota)

`university`

-   Universities that receive revenue from the parcels associated with a present-day tribe

`state`

-   States where the parcels associated with a present-day tribe are located

### University_Summary.csv

This spreadsheet shows summary statistics for all state trust land data we gathered, organized by land-grant university.

`university`

-   Land-grant institution that receives revenue from specific state trust land parcels

`subsurface_acres`

-   Total number of subsurface acres associated with a present-day tribe

`surface_acres`

-   Total number of surface acres associated with a present day tribe

`timber_acres`

-   Total number of timber acres associated with a present day tribe (only relevant in Washington state)

`unknown_acres`

-   Total number of acres with an unknown rights type (only relevant for two parcels in South Dakota state)

`price_paid`

-   Sum of the price that the U.S. federal government paid to tribes for all the parcels associated with a particular university (the sum of the price paid per parcel column) 

`present_day_tribe_count`

-   Total number of present-day tribes associated with a land-grant university

`present_day_tribe`

-   List of present-day tribes associated with a land-grant university

`tribes_named_in_cession_count`

-   Total number of present-day tribes associated with a land-grant university

`tribes_named_in_cession`

-   List of present-day tribes associated with a university

`cession_count`

-   Total number of cessions associated with a land-grant university

`all_cessions`

-   List of cessions associated with a land-grant university
