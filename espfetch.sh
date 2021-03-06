#!/bin/bash

IFS='_' read -a params <<< "${0}"

host=`echo ${params[1]}`
source=`echo ${params[2]}`
param=`echo ${params[3]}`

if [[ ! $host ]]; then
    echo 'No parameters found. You should create symlink with name like espfetch_<esp_host>_<source_index>_<param_name>'
fi

script_filename=`readlink ${0}`
script_filename=`dirname "$script_filename"`
script_path=$script_filename/esp_fetch.py

case $1 in
   config)
        munin_title=`python "$script_path" $host --source $source --param $param --munin-title-only`
        echo graph_category house
        echo graph_title $munin_title
        echo graph_vlabel Metric
        echo metric.label metric
        exit 0;;
esac

echo metric.value `python $script_path $host --source $source --param $param`
