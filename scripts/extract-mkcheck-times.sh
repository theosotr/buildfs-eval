#! /bin/bash


if [ -z $1 ]; then
  echo "You have to provide the directory of Make benchmarks"
  exit 1
fi


bench_dir=$(realpath $1)
out_dir=$(realpath $2)

rm -f $out_dir/mkcheck-performance.csv
for file in $bench_dir/*; do
    project=$(basename $file)

    if [ ! -f $file/mkcheck/$project.time ]; then
      continue
    fi

    len=$(wc -l < $file/mkcheck/$project.time)
    if [ "$len" -ne 3 ]; then
      continue
    fi
    btime=$(cat $file/mkcheck/$project.time | head -1)
    ftime=$(cat $file/mkcheck/$project.time | head -2 | tail -1)
    rtime=$(cat $file/mkcheck/$project.time | tail -1)
    echo "$project,$btime,$ftime,$rtime" >> $out_dir/mkcheck-performance.csv
done
