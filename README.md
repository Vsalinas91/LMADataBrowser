LMA Data Browser
---------------

This web application serves as an alternative to the out-of-the-box data browser that is used to view archived raw (.dat) LMA files.

Using the Holoviz Panels package, this LMA data browser allows for a more customizable, and user friendly data exploration. To get rid of the hassle of viewing data on more dated image, this browser allows for specific 
data time selections, map overlays, point-source and grid plotting, and even data processing and flash-sorting.

Data structure will vary by LMA network. As an example, data files are included in the repo with the following structure encouraged to be used:
server: /data/[path]/raw/[YYYY]/[MM]/[DD]/*.dat.gz
YYYY=Year 
MM = Month e.g. Jan, Jul, Aug, etc
DD = Day

If structure is different, ensure that raw files exist at least in a Year->Month->Day Heirarchy

Requirments:
xlma-python  -- For LMA flash sorting and gridding

Note: This Project remains a work in progress. 
Wishlist: Data/Loading/Plotting Indicators 
          Basemap Selection
          Remove Flash-Sorting Points -- Keep grids
          Update Processing Widget Callbacks

Screenshots:
![raw](examples/raw_data_grid.png)
