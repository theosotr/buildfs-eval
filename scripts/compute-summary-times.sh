#! /bin/bash


if [ -z $1 ]; then
  echo "You have to provide the directory of faults"
fi

if [ -z $2 ]; then
  echo "You have to provide the directory to output the results"
fi


project_dir=$(realpath $1)
out_dir=$(realpath $2)
dir=$(dirname $0)

mkdir -p $out_dir

function extract_times()
{
  rm -f $out_dir/$1-performance.csv
  for file in $project_dir/$1/*; do
    base=$(basename $file)

    if [ -d $file/times ]; then
      time_file=$file/times/$base.times
      build_time_file=$file/times/build-buildfs.times
    elif [ -f $file/$base.times ]; then
      time_file=$file/$base.times
      build_time_file=$file/build-buildfs.times
    else
      continue
    fi

    avg=$(cat $time_file | $dir/average.py)
    btime=$(cat $build_time_file | $dir/average.py)
    atime=$(echo $avg | cut -f1 -d ' ')
    ftime=$(echo $avg | cut -f2 -d ' ')

    echo "$base,$btime,$atime,$ftime" >> $out_dir/$1-performance.csv
  done
}


extract_times "gradle-projects"
extract_times "make-projects"
