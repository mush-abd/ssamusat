# Satellite Socio-Economic Analysis and GDP Prediction Project

## Overview:
This project focuses on leveraging satellite imagery, particularly night-time lights, to analyze the socio-economic conditions of different regions and predict the GDP per capita. By employing image processing techniques and machine learning algorithms in Python, we aim to extract meaningful features from satellite images and correlate them with various socio-economic indicators. Additionally, we seek to build predictive models to estimate the GDP per capita of a region based on satellite-derived data.

## Objectives:
- Utilize satellite imagery data, especially night-time lights, for socio-economic analysis.
- Develop image processing algorithms to extract relevant features from satellite images.
- Correlate satellite-derived data with socio-economic indicators such as population density, economic activity, and infrastructure development.
- Build machine learning models to predict the GDP per capita of regions based on satellite-derived features.
- Visualize and interpret the results to gain insights into the socio-economic conditions and predict the economic status of different regions.

## Folder Hierarchy:
ssamusat\
├── data\
│   ├── city_coordinates\
│   ├── satellite_images\
│   │   └── snap.jpg\
│   └── shapefiles\
├── gps_utils\
│   ├── gpstran.py\
│   └── __init__.py\
├── image_processing\
│   ├── improc.py\
│   └── __init__.py\
├── main.py\
├── main__.py\
├── output\
│   ├── binary_images_thresholding\
│   │   └── contour-out-th100.jpg\
│   └── contour_results\
└── scripts


## Project Directory Structure

- **data:** Contains various data files used in the project, including city coordinates, satellite images, and shapefiles.
  - **city_coordinates:** Stores data related to city coordinates.
  - **satellite_images:** Contains satellite images, with "snap.jpg" being one of them.
  - **shapefiles:** Holds shapefiles used for geographical data representation.
- **gps_utils:** Contains utility modules related to GPS functionalities.
  - **gpstran.py:** Module for GPS transformations.
  - **__init__.py:** Initialization file for the gps_utils package.
- **image_processing:** Contains modules related to image processing.
  - **improc.py:** Module for image processing functionalities.
  - **__init__.py:** Initialization file for the image_processing package.
- **output:** Stores output files generated during the project execution.
  - **binary_images_thresholding:** Directory for binary images generated across dif-2 thresholding.
    - **contour-out-th100.jpg:** Example of a binary image output.
  - **contour_results:** Directory for contour results generated during processing.
- **scripts:** Location for various script files used in the project.
- **main.py:** Main Python script for executing the project.
- 


## Usage:

1. Clone this repository to your local machine.
2. Place raw satellite imagery data in the **data/** directory.
3. Run the scripts in the **scripts/** directory sequentially to preprocess the data, extract features, perform analysis, build predictive models, evaluate the models, and visualize the results.
4. Explore the **output/** directory for processed data, analysis outputs, and model predictions.

## Dependencies:

- Python 3.x
- Libraries: numpy, pandas, fiona, rasterio, matplotlib, statsmodels, scikit-learn, tqdm, etc. (See requirements.txt for a full list of dependencies)
- Installing command :pip install -r requirements.txt



  ## Project Supervisor:
- Adeeba Ali @ZHCET Aligarh Muslim University

## Contributors:

- Mohammad Arquam 
- Musharraf Abdullah

