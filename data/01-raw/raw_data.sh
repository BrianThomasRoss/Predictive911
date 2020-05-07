#! /bin/bash
# This script should download the latest set of data availbe from the 
# city of Detroit's open data portal
curl -L "https://opendata.arcgis.com/datasets/2dab2f70653f4bb8b4f2b51619ec8329_0.csv" \
-o "test.csv"
