#! /bin/bash

dir=$(dirname $0)
bench_dir=$(realpath $1)

function compute_slowdown()
{
  rm -f tmp.txt
  for project in $bench_dir/$1/*; do
    base=$(basename $project)
    if [ -d $project/times ]; then
      avg_base=$(cat $project/times/base-build.times | $dir/average.py)
      avg_buildfs=$(cat $project/times/build-buildfs.times | $dir/average.py)
    else
      avg_base=$(cat $project/base-build.times | $dir/average.py)
      avg_buildfs=$(cat $project/build-buildfs.times | $dir/average.py)
    fi
    echo "$base,$avg_base,$avg_buildfs" >> tmp.txt
  done
  cat tmp.txt | $dir/build-slowdown.py
  rm tmp.txt
}

echo "The slowdown for Gradle builds is $(compute_slowdown make-projects) (90th percentile)"
echo "The slowdown for Make builds is $(compute_slowdown gradle-projects) (90th percentile)"
