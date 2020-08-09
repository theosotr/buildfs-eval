#! /bin/bash

# Script to run BuildFS in offline mode to get the results of RQ1 using our
# trace data.

if [ -z $1 ]; then
  echo "You have to provide the directory of benchamrks as the first argument".
  exit 1
fi

if [ -z $2 ]; then
  echo "You have to provide the directory to store the results."
  exit 1
fi


dir=$(dirname $0)
data=$(realpath $1)
out_dir=$(realpath $2)


function extract_times()
{
  local file
  file=$1
  project_name=$(basename $file)
  rm -f $file/$project.times
  atime=$(grep -oP 'Analysis time: [0-9.]+' $file/$project_name.faults |
    sed -r 's/Analysis time: ([0-9.]+)/\1/g')
  btime=$(grep -oP 'Bug detection time: [0-9.]+' $file/$project_name.faults |
    sed -r 's/Bug detection time: ([0-9.]+)/\1/g')
  echo "$atime,$btime" >> $file/$project_name.times
}


function analyze_benchmarks()
{
  local bench_dir project_out totals counter
  bench_dir=$1
  project_out=$out_dir/$bench_dir
  totals=$project_out/faults.csv

  mkdir -p $project_out

  echo "project,min,mout,ov" > $totals

  counter=1
  for project in $data/$bench_dir/*; do
    name=$(basename $project)

    if [ $name = "faults.csv" ]; then
      continue
    fi

    mkdir -p $project_out/$name

    echo "$counter: Analyzing $name..."
    if [ $bench_dir = "gradle-projects" ]; then
      buildfs gradle-build \
        -mode offline \
        -print-stats \
        -trace-file $project/$name.strace \
        -build-dir $(cat $project/$name.path) \
        > $project_out/$name/$name.faults
    else
      buildfs make-build \
        -mode offline \
        -print-stats \
        -trace-file $project/$name.strace \
        -build-db $project/$name.makedb \
        -build-dir "$(cat $project/$name.path)" > $project_out/$name/$name.faults
    fi
    extract_times "$project_out/$name"
    if [ -d $project/times ]; then
      cp $project/times/build-buildfs.times $project_out/$name
    else
      cp $project/build-buildfs.times $project_out/$name
    fi
    counter=$((counter + 1))
  done
}

mkdir -p $out_dir
sudo chown buildfs:buildfs -R $out_dir

echo "Analyzing Gradle projects..."
echo "============================"
echo
analyze_benchmarks "gradle-projects"
$dir/compute-summary-results.sh "$out_dir/gradle-projects"

echo "Analyzing Make projects..."
echo "=========================="
echo
analyze_benchmarks "make-projects"
$dir/compute-summary-results.sh "$out_dir/make-projects"
