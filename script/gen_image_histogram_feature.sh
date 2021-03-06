#!/bin/bash

# This script is to generate image feature
# Prerequisite: ../data/data_files/image_itemPairs_train.csv and ../data/data_files/image_itemPairs_test.csv
# To generate them, execute: cd ../data && python image_item_pair.py

# Generate image feature in parallel
function work(){
pv --rate -i 5 \
 | csvcut -c 'index,images_array_1,images_array_2' | csvjson --stream \
  | parallel --gnu -k --pipe -N 20  --jobs 16 python -m feature.image_histogram_feature

}

# Generate image feature for training data set and testing data set
cat data/data_files/image_itemPairs_train.csv | work > data/data_files/image_histogram_feature_train.csv
cat data/data_files/image_itemPairs_test.csv | work > data/data_files/image_historgram_feature_test.csv