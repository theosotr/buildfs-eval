#! /bin/bash

if [ -z $1 ]; then
  echo "You have to provide the csv of the fixed projects (i.e., data/fixed_projects.csv)"
  exit 1
fi

if [ -z $2 ]; then
  echo "You have provide the directory to store the results"
  exit 1
fi

counter=1
projects=$(realpath $1)
out_dir=$(realpath $2)
dir=$(dirname $0)

for i in $(cat $projects); do
  project="$(cut -d ',' -f 1 <<<$i)"
  repo="$(cut -d ',' -f 2 <<<$i)"
  git_hash="$(cut -d ',' -f 3 <<<$i)"
  build_system="$(cut -d ',' -f 4 <<<$i)"

  if [ "$project" = "project" ]; then
    # We are processing the header of the csv file.
    continue
  fi

  if [ "$git_hash" = "-" ]; then
    # The project has not been fixed yet.
    continue
  fi

  base_cmd="sudo docker run --rm -ti --privileged \
    -v $out_dir:/home/buildfs/data"

  if [ "$project" = "tsar" ]; then
    echo "make" > /tmp/tmp-script.sh
    echo "make clean" >> /tmp/tmp-script.sh
    chmod +x /tmp/tmp-script.sh
    base_cmd="$base_cmd -v /tmp/tmp-script.sh:/home/buildfs/pre-script.sh"
  fi

  if [ "$project" = "webdis" ]; then
    echo "sudo apt install -y libevent-dev" > /tmp/tmp-script.sh
    chmod +x /tmp/tmp-script.sh
    base_cmd="$base_cmd -v /tmp/tmp-script.sh:/home/buildfs/pre-script.sh"
  fi

  cmd="$base_cmd buildfs \
    -p "$repo.git" \
    -v "$git_hash" \
    -s -t $build_system"

  if [ "$project" = "cqmetrics" ]; then
    # For cqmetrics we need to enter the src directory.
    cmd="$cmd -b src"
  fi

  if [ "$project" = "joystick" ]; then
    # For joystick we need to enter the src directory.
    cmd="$cmd -b utils"
  fi

  echo "$counter: Building and analyzing $project.."
  eval $cmd

  if [ "$project" = "joystick" ]; then
    # Joystick is stored in a repo whose basename is named 'code'.
    # So, we need to rename things a little bit.
    rm -rf $out_dir/joystick
    mv $out_dir/code $out_dir/joystick
    mv $out_dir/joystick/code.faults $out_dir/joystick/joystick.faults
    mv $out_dir/joystick/code.strace $out_dir/joystick/joystick.strace
    mv $out_dir/joystick/code.path $out_dir/joystick/joystick.path
    mv $out_dir/joystick/code.makedb $out_dir/joystick/joystick.makedb
  fi

  counter=$((counter + 1))
done

$dir/compute-summary-results.sh $out_dir
