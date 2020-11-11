Artifact for "A Model for Detecting Faults in Build Specifications" (OOPSLA'20)
===============================================================================

This is the artifact for the OOPSLA'20 paper titled
"A Model for Detecting Faults in Build Specifications".

* Thodoris Sotiropoulos, Stefanos Chaliasos, Dimitris Mitropoulos, and Diomidis Spinellis. 2020.
  [A Model for Detecting Faults in Build Specifications](https://doi.org/10.1145/3428212).
  In Proceedings of the ACM on Programming Languages (OOPSLA '20), 2020, Virtual, USA,
  30 pages. 
  ([doi:10.1145/3428212](https://doi.org/10.1145/3428212))


Requirements
============

* A Unix-like operating system (tested on Ubuntu)

* A Docker installation

* At least 150GB of available disk space

* A good network connection (the artifact involves many downloads)


Setup
=====

To get the artifact, run

```bash
git clone --recursive https://github.com/theosotr/buildfs-eval ~/buildfs-eval
```

## Overview

The artifact contains the instructions and scripts to re-run the evaluation
described in our paper. The artifact has the following structure:

* `scripts`: This is the directory that contains the scripts needed to re-run
the experiments presented in our paper.
* `data/gradle-projects.txt`: The list of Gradle projects
that we considered in our evaluation
(along with the version we analyzed).
* `data/make-projects.txt`: The list of Make projects that we analyzed.
The projects come from two ecosystems: Github and Debian.
For Debian packages, we provide the version of the package that we analyzed.
For Github projects, we provide the commit hash
(similar to Gradle projects).
* `buildfs`: Contains the source code of the tool (provided as a git submodule)
used in our paper for running and analyzing build executions,
namely `BuildFS`.

Note that `BuildFS` is available as open-source software under
the GNU General Public License v3.0., and can also be reached
through the following Repository : https://github.com/theosotr/buildfs

Inside the `buildfs` directory, there are the following directories

* `src`: The source code of `BuildFS` written in OCaml.
* `make-instrumentation`: Shell scripts for instrumenting Make builds as explained
  in our paper (Section 4.3).
* `gradle-instrumentation`: The Gradle plugin used to instrument Gradle builds
  (Section 4.3)
* `sbuild`: Helper scripts and configuration files for
  building Debian packages using the [sbuild's](https://wiki.debian.org/sbuild) workflow.
* `mkcheck-sbuild`: Helper scripts and configuration files for
  analyzing Debian packages using the `sbuild` workflow and `mkcheck`.
* `entrypoint`: Contains the entrypoint script of the corresponding Docker image.

## Install Docker Images

We provide a `Dockerfile` to build images that contain:

* An intallation of `BuildFS`. To do so, the image fetches the OCaml compiler 4.07
and all the required `opam` packages for building `BuildFS` from source.

* An installation of [strace](https://strace.io/).

* An installation of Gradle and GNU Make.

* (Optionally) an installation of the Kotlin compiler for building our Gradle plugin.

* (Optionally) an installation of the Android SDK (this is required by many
Gradle projects).

* (Optionally) an installation of [sbuild](https://wiki.debian.org/sbuild)
for analyzing Debian packages using the sbuild's workflow. Note that
in our evaluation, we used `sbuild` to build Debian Make packages
in a reproducible way.

* (Optionally) an installation of [mkcheck](https://github.com/nandor/mkcheck.git)
(version [09f520c](https://github.com/nandor/mkcheck/commit/09f520ce5ceceb42c2371d9df6f83b045223f260))
for comparing `BuildFS` against it.

* A user named `buildfs` with sudo privileges.

Τwo Docker images are required to evaluate this artifact.
The first image is used to analyze all Gradle projects
and non-Debian Make packages using either `BuildFS` or `mkcheck`.
The second image contains an installation of `sbuild`
to analyze Debian packages using the workflow of `sbuild`.

### Build Images from Source

**NOTE**:
If you do not want build the images on your own, please skip this step
and proceed to the next section ("Pull Images from Dockerhub")

To build the first image (named `buildfs`), run the following command
(estimated running time: 30-50 minutes)

```
docker build -t buildfs --build-arg IMAGE_NAME=ubuntu:18.04 \
  --build-arg SBUILD=no --build-arg GRADLE=yes --build-arg MKCHECK=yes .
```

Notice that we passed four arguments to the build process of the image
(through the `--build-arg` option). The argument `IMAGE_NAME` refers to
the base Docker image from which we set up the environment. The remaining
arguments indicate whether Docker installs the corresponding tool or not.
For example, the argument `GRADLE=yes` indicates that we use this image to analyze both
Make and Gradle projects. So, Docker will also install the Kotlin compiler
and Android SDK.

For the second image (named `buildfs-sbuild`), run the following command
(estimated running time: 40-60 minutes)

```bash
docker build -t buildfs-sbuild --build-arg IMAGE_NAME=debian:stable \
    --build-arg SBUILD=yes --build-arg GRADLE=no --build-arg MKCHECK=yes .
```

This image is built upon `debian:stable`
and installs both `sbuild` and `mkcheck`.
It does not install `gradle`.


**NOTE:**
We have two separate images, because there are several difficulties
in having a `gradle` and `sbuild` installation on the same image.
The second image (`buildfs-sbuild`) is used **only** for
analyzing Debian packages.
In practice, we will use this image only for the last step of the artifact.

After building all Docker images successfully,
please navigate to the root directory of the artifact


```bash
cd ~/buildfs-eval
```


### Pull Images from Dockerhub

You can also download the docker images from Dockerhub by using the
following commands


```bash
docker pull schaliasos/buildfs
docker pull schaliasos/buildfs-sbuild
# Rename the images to be consistent with our scripts
docker tag schaliasos/buildfs buildfs
docker tag schaliasos/buildfs-sbuild buildfs-sbuild
```

We have two separate images, because there are several difficulties
in having a `gradle` and `sbuild` installation on the same image.

**NOTE**:
We have two separate images, because there are several difficulties
in having a `gradle` and `sbuild` installation on the same image.
The second image (`buildfs-sbuild`) is used **only** for
analyzing Debian packages.
In practice, we will use this image only for the last step of the artifact.

After downloading all Docker images successfully,
please navigate to the root directory of the artifact


```bash
cd ~/buildfs-eval
```


Getting Started
===============

## Navigating through the Docker Image

Before running our examples,
let's explore the contents of our freshly-created Docker
image (i.e., `buildfs`).
Run the following command to create a new container.
```bash
docker run -ti --rm  --privileged buildfs
```
After executing the command,
you will be able to enter the home directory
(i.e., `/home/buildfs`) of the `buildfs` user.
This directory contains the `buildfs_src`
where the source code of our tool is stored.

To build `buildfs` on your own, run

```bash
buildfs@6d0b7b1affcd:~$ cd ~/buildfs_src
buildfs@6d0b7b1affcd:~$ dune clean
buildfs@6d0b7b1affcd:~$ dune build -p buildfs
buildfs@6d0b7b1affcd:~$ dune install
```

### Usage

```
❯ buildfs help
Detecting Faults in Parallel and Incremental Builds.

  buildfs SUBCOMMAND

=== subcommands ===

  gradle-build  This is the sub-command for analyzing and detecting faults in
                Gradle scripts
  make-build    This is the sub-command for analyzing and detecting faults in
                Make scripts
  version       print version information
  help          explain a given subcommand (perhaps recursively)
```

For analyzing Gradle builds

```
❯ buildfs gradle-build -help
This is the sub-command for analyzing and detecting faults in Gradle scripts

  buildfs gradle-build

=== flags ===

  -build-dir Build        directory
  -mode Analysis          mode; either online or offline
  [-build-task Build]     task to execute
  [-dump-tool-out File]   to store output from Gradle execution (for debugging
                          only)
  [-graph-file File]      to store the task graph inferred by BuildFS.
  [-graph-format Format]  for storing the task graph of the BuildFS program.
  [-print-stats]          Print stats about execution and analysis
  [-trace-file Path]      to trace file produced by the 'strace' tool.
  [-help]                 print this help text and exit
                          (alias: -?)
```

For analyzing Make builds


```
❯ buildfs make-build -help
This is the sub-command for analyzing and detecting faults in Make scripts

  buildfs make-build

=== flags ===

  -build-dir Build        directory
  -mode Analysis          mode; either online or offline
  [-build-db Path]        to Make database
  [-dump-tool-out File]   to store output from Make execution (for debugging
                          only)
  [-graph-file File]      to store the task graph inferred by BuildFS.
  [-graph-format Format]  for storing the task graph of the BuildFS program.
  [-print-stats]          Print stats about execution and analysis
  [-trace-file Path]      to trace file produced by the 'strace' tool.
  [-help]                 print this help text and exit
                          (alias: -?)
```

You can exit from the Docker container by running

```bash
buildfs@6d0b7b1affcd:~$ exit
```

## Running example builds

Let's see how we run and analyze real-world builds using `BuildFS`.
To do so, we will use the Docker image we created in the
previous step so that we can perform the build in a fresh environment.
Recall that this image contains all necessary dependencies for
running the builds.
The image contains an entrypoint script that expects the following
options:

* `-p`: A URL pointing to the *git* repository of the project
        that we want to run and analyze or a Debian package name
        (when using `-t sbuild` or `-t sbuild-mkcheck`).
* `-v`: A commit hash, a tag, or a branch that indicates the version of the
        project that we want to analyze (default `latest`).
* `-t`: The type of the project (`gradle` or `make` or `sbuild` or `mkcheck`
        or `sbuild-mkcheck`).
* `-b`: This option expects a path (relative to the directory of the project)
        where the build is performed.
* `-k`: Number of builds to perform (default 1).
* `-s`: If this is flag is not provided, we run the build without performing
        any analysis (either through `BuildFS` or `mkcheck`).
* `-o`: A flag that when it is provided, beyond online analysis through `BuildFS`,
        the container also performs an offline analysis on the trace stemming
        from the execution of the build. This option was used in our experiments
        to estimate the amount of time spent on the analysis of BuildFS programs.


### Example1: Make Build

**NOTE**:
This example corresponds to the first motivating example discussed in our paper
(Figure 1).

To analyze an example Make build, run the following command
(estimated running time: less than 30 seconds):

```bash
docker run --rm -ti --privileged \
  -v $(pwd)/out:/home/buildfs/data buildfs \
  -p "https://github.com/dspinellis/cqmetrics.git" \
  -v "5e5495499863921ba3133a66957f98b192004507" \
  -s -t make \
  -b src
```

Some explanations:

The Docker option `--privileged` is used to enable tracing inside the
Docker container. The option `-v` is used to mount a local volume inside
the Docker container. This is used to store all the files produced
from the analysis of the build script into the given volume `$(pwd)/out`.
Specifically,
for Make builds,
`BuildFS` produces the following files inside this directory.

* `cqmetrics/build-buildfs.times`: This file contains the time spent for building
  the project using `BuildFS`. This file is generated if we run the container
  with the option `-s`.
* `cqmetrics/base-build.times`: This file contains the time spent for building
  the project *without* `BuildFS`. This file is  generated if the option
  `-s` is *not* provided.
* `cqmetrics/cqmetrics.times`: This file is a CSV that includes the time spent
  on the analysis of BuildFS programs and fault detection. This file is generated
  if the option `-o` (offline analysis) is provided.
* `cqmetrics/cqmetrics.faults`: This file is the report that contains the faults
  detected by `BuildFS`. This file is generated if we run the container
  with the option `-s`.
* `cqmetrics/cqmetrics.makedb`: This file is the database of the Make build
  produced by running `make -pn`. This is used for an offline analysis of a Make
  project. This file is generated if we run the container with the option `-s`.
* `cqmetrics/cqmetrics.path`: This file contains the path where we performed
  the build. This file is generated if we run the container with the option `-s`.
* `cqmetrics/cqmetrics.strace`: a system call trace corresponding
  to the build execution. This file is generated if we run the container with
  the option `-s`.

If we inspect the contents of the resulting `out/cqmetrics/cqmetrics.faults`
file, we will see something similar to the following:

```bash

❯ cat out/cqmetrics/cqmetrics.faults
Info: Start tracing command: fsmake-make ...
Statistics
----------
Trace entries: 19759
Tasks: 8
Files: 342
Conflicts: 4
DFS traversals: 41
Analysis time: 2.81151819229
Bug detection time: 0.0152561664581
------------------------------------------------------------
Number of Missing Inputs (MIN): 3

Detailed Bug Report:
  ==> [Task: /home/buildfs/cqmetrics/src:header.tab]

    Fault Type: MIN
      - /home/buildfs/cqmetrics/src/QualityMetrics.h: Consumed by /home/buildfs/cqmetrics/src:header.tab ( openat at line 21068 )

  ==> [Task: /home/buildfs/cqmetrics/src:header.txt]

    Fault Type: MIN
      - /home/buildfs/cqmetrics/src/QualityMetrics.h: Consumed by /home/buildfs/cqmetrics/src:header.txt ( openat at line 22386 )

  ==> [Task: /home/buildfs/cqmetrics/src:qmcalc.o]

    Fault Type: MIN
      - /home/buildfs/cqmetrics/src/BolState.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18631 )
      - /home/buildfs/cqmetrics/src/CKeyword.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18633 )
      - /home/buildfs/cqmetrics/src/CMetricsCalculator.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18563 )
      - /home/buildfs/cqmetrics/src/CharSource.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18565 )
      - /home/buildfs/cqmetrics/src/Cyclomatic.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18767 )
      - /home/buildfs/cqmetrics/src/Descriptive.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18769 )
      - /home/buildfs/cqmetrics/src/Halstead.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 19361 )
      - /home/buildfs/cqmetrics/src/NestingLevel.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 19365 )
      - /home/buildfs/cqmetrics/src/QualityMetrics.h: Consumed by /home/buildfs/cqmetrics/src:qmcalc.o ( openat at line 18711 )
```

Specifically, `BuildFS` detected three missing inputs (MIN) related to three
build tasks of the project. For example, the following fragment shows that
the task `/home/buildfs/cqmetrics/src:header.txt` has a missing input on one file
(i.e., `/home/buildfs/cqmetrics/src/QualityMetrics.h`). This means that
whenever the latter is updated, Make does not re-trigger the execution of
the task. As discussed in our paper, this leads to stale targets.

```bash
==> [Task: /home/buildfs/cqmetrics/src:header.txt]

  Fault Type: MIN
    - /home/buildfs/cqmetrics/src/QualityMetrics.h: Consumed by /home/buildfs/cqmetrics/src:header.txt ( openat at line 22386 )
```


### Example2: Gradle Build

**NOTE**:
This example corresponds to the second motivating example discussed in our
paper (Figure 2).

For running and analyzing a Gradle project using our Docker image,
run the following (estimated running time: 6-10 minutes):

```bash
docker run --rm -ti --privileged \
  -v $(pwd)/out:/home/buildfs/data buildfs \
  -p "https://github.com/seqeralabs/nf-tower.git" \
  -v "997985c2f7e603342189effdfea122bab53a6bae" \
  -s \
  -t gradle
```

This will fetches and instruments the specified Gradle repository
as explained in Section 4.3.
In turn,
the container uses `BuildFS` to build and analyze the Gradle project.
For Gradle builds,
the container generates the same files inside the `out` directory except for
the `*.makedb` file, as this file is required only for Make builds.

If you inspect the produced `out/nf-tower/nf-tower.faults` file,
you are expected to see the following report:

```bash
❯ cat out/nf-tower/nf-tower.faults
Info: Start tracing command: ./gradlew build --no-parallel ...
Statistics
----------
Trace entries: 897251
Tasks: 18
Files: 2877
Conflicts: 2614
DFS traversals: 10
Analysis time: 214.29347682
Bug detection time: 0.146173000336
------------------------------------------------------------
Number of Ordering Violations (OV): 3

Detailed Bug Report:
  ==> [Task: tower-backend:shadowJar] | [Task: tower-backend:distTar]

    Fault Type: OV
      - /home/buildfs/nf-tower/tower-backend/build/libs/tower-backend-19.08.0.jar: Produced by tower-backend:shadowJar ( openat at line 280041 ) and Consumed by tower-backend:distTar ( lstat at line 151875 )

  ==> [Task: tower-backend:shadowJar] | [Task: tower-backend:distZip]

    Fault Type: OV
      - /home/buildfs/nf-tower/tower-backend/build/libs/tower-backend-19.08.0.jar: Produced by tower-backend:shadowJar ( openat at line 280041 ) and Consumed by tower-backend:distZip ( lstat at line 161551 )

  ==> [Task: tower-backend:shadowJar] | [Task: tower-backend:jar]

    Fault Type: OV
      - /home/buildfs/nf-tower/tower-backend/build/libs/tower-backend-19.08.0.jar: Produced by tower-backend:shadowJar ( openat at line 280041 ) and Produced by tower-backend:jar ( openat at line 139411 )
      - /home/buildfs/nf-tower/tower-backend/build/libs/tower-backend-19.08.0.jar: Produced by tower-backend:shadowJar ( openat at line 280041 ) and Produced by tower-backend:jar ( openat at line 139411 )
```

`BuildFS` detected three ordering violations (OV).
For example, there is an ordering violations between the tasks
`tower-backend:shadowJar`,
`tower-backend:jar`.
These tasks conflict on two files
(e.g., `/home/buildfs/nf-tower/tower-backend/build/libs/tower-backend-19.08.0.jar`),
and no dependency has been specified between these tasks.


**NOTE**: In general,
Gradle builds take longer as they involve the download of JAR
dependencies and the configuration of the Gradle Daemon.

Step by Step Instructions
==========================

## Benchmarks

**NOTE**: Ensure that you have at least 100GB of available
disk space before running this step.

To reproduce the results of our paper,
you first need to fetch the system call traces
that stem from the build execution of all the projects
we examined in our evaluation.
You can fetch the data by runnning

```bash
wget -O benchmarks.zip "https://zenodo.org/record/4063156/files/benchmarks.zip?download=1"
```

**MD5 Checksum**: cf5eae673c9ff089a662e3f600b7d8da

to extract the data, run

```bash
unzip benchmarks.zip
```

this will create the directory `benchmarks`. This directory contains
the following sub-directories:

* `gradle-projects`: A directory containing data from 312 Gradle projects
that we considered for our evaluation.
* `make-projects`: A directory containing data from 300 Make projects
that we considered for our evaluation.


### Gradle Benchmarks

For each Gradle project (i.e., `benchmarks/gradle-projects/<project-name>`),
you are expected to find the following files:

* `<project-name>.strace`: This file
contains the system call trace corresponding to the build execution
of the Gradle project.

* `<project-name>.path`: This file holds the path where the build of the
project was performed.

* `times/build-buildfs.times`: This file contains the time spent on building
the Gradle project using `BuildFS`.

* `times/base-build.times`: This file contains the time spent on building
the Gradle project without `BuildFS`.

* `times/<project-name>.times`: This file contains the times spent on
the analysis of the BuildFS program and fault detection.
Each row has two columns: the first one is the time spent on the
analysis of BuildFS programs, while the second one is the time
spent on fault detection.

### Make Benchmarks

For each Make project (i.e., `data/make-projects/<project-name>`),
you are expected to find the following files:

* `<project-name>.strace`: This file
contains the system call trace corresponding to the build execution
of the Make project.

* `<project-name>.path`: This file holds the path where the build of the
project was performed.

* `<project-name>.makedb`: This is the database associated with the Make project.
It is required for analyzing the Make trace offline.

* `times/build-buildfs.times`: This file contains the time spent on building
the Make project using `BuildFS`.

* `times/base-build.times`: This file contains the time spent on building
the Make project without `BuildFS`.

* `times/<project-name>.times`: This file contains the times spent on
the analysis of the BuildFS program and fault detection.
Each row has two columns: the first one is the time spent on the
analysis of BuildFS programs, while the second one is the time
spent on fault detection.

Furthermore, a Make project may contain a directory named `mkcheck`
that includes data from the analysis of the project using `mkcheck`
(See section 5.6). Some Make projects may not contain this directory
indicating that `mkcheck` failed to produce data for this project
due to a crash. The directory of `mkcheck` contains the following

* `<project-name>.fuzz`: Fault report generated by `mkcheck` in `fuzz` mode.
* `<project-name>.race`: Fault report generated by `mkcheck` in `race` mode.
* `<project-name>.time`: This file contains the times spent on building
and detecting faults using `mkcheck`. The first row is the time needed
to build the project with  `mkcheck`,
the second one stands for the time spent on build fuzzing,
while the third row is the time spent on race testing.


## RQ1

For the first research question, we will use `BuildFS` (in offline mode) to
analyze the system call traces of all the projects (both Make and Gradle)
examined in our evaluation.
To do so, run the following to create and enter a `buildfs` container.

```bash
docker run -ti --rm  \
  --privileged \
  -v $(pwd)/benchmarks:/home/buildfs/benchmarks \
  -v $(pwd)/rq1-results:/home/buildfs/out \
  -v $(pwd)/scripts:/home/buildfs/scripts buildfs
```

Note that we mounted three local volumes inside the container.
The first volume stands for the benchmarks we fetched earlier,
the second one is the volume to store the results of the RQ1
(i.e., `$(pwd)/rq1-results`),
while the third volume corresponds to the evaluation scripts of
the artifact.

After entering the container, run the following script
(estimated running time: 45 - 60 minutes).

```bash
buildfs@852dd25dfc98:~$ ./scripts/analyze-benchmarks-offline.sh benchmarks out
```

This script employs `BuildFS` to analyze the system call trace of all Gradle
and Make projects using the provided traces. The second argument of the script
is the directory (namely `out`) to store the results from the analysis.
Specifically, after succesuuly running the above script,
the `out` directory contains a sub-directory for each category of
project (e.g., `gradle-projects`).
Each sub-directory contains three files:

* `<project-name>.faults`: Faults detected by `BuildFS`.
* `<project-name>.times`: Times spent on analysis and fault detection.
* `build-buildfs.times`: Time spent on building the project with `BuildFS`.
This file was *not* computed as we did not run the build again.
We copied it from the `benchmarks` directory.

Furthermore, for each category of projects (e.g., `make-projects`), the script
generates a CSV file that gives the summary of fault detection results.
For instance, the `out/make-projects/faults.csv` file contains the
summary results for Make projects.


As a final step, run the following to get the metrics mentioned
in RQ1 of the paper (Table 1).

```bash
buildfs@852dd25dfc98:~$ ./scripts/rq1.py \
  out/gradle-projects/faults.csv \
  out/make-projects/faults.csv
```

Note that the first argument of the script is the fault detection results
for Gradle projects, while the second one is the fault detection results
for Make projects.

Now exit the container to proceed to RQ2.

```bash
buildfs@852dd25dfc98:~$ exit
```

## RQ2


For the second research question, we will estimate the number of
the detected faults confirmed and fixed by the developers.

### Examining the pull requests

As a starting point, you can take a look to the
patches we provided and the response we got
from the developers. Run:

```bash
./scripts/dump_fixed.py data/fixed_projects.csv
```

This will dump the links pointing to the bug reports we sent to
47 open-source projects. The resulting list contains two open-source
projects not mentioned in the paper, as their developers responded to us
while the paper was under review.

**NOTE:** Notice that we opened two pull requests for the `cqmetrics` project
(i.e., `pull/13` and `pull/14`).

### Computing the number of fixes

To compute the number of faults that are fixed due to our patches
and issue reports, we exploit the data stored in
the `data/fixed_projects.csv` file. Specifically,
we have created a script that builds / analyzes every project of this file
using `BuildFS`. To do so,
the script uses the `buildfs` Docker image
as documented earlier (See the "Getting Started" section.).

Note that this script builds and analyzes the version of the project
**after** applying our fix.
This version is taken from the `project_version` column of
the `data/fixed_projects.csv` file.
In turn, the script estimates the number of fixed faults by comparing the
reported faults with the reports computed by
`BuildFS` **before** applying the patch.
The fault reports corresponding to the version of the project before the fix
were computed in RQ1 (inside the `rq1-results` directory).

Run this script through (estimated running time: 2-4 hours)

```bash
./scripts/analyze-rq2-projects.sh data/fixed_projects.csv rq2-results
```

To run the above script on a small sub-set of projects (e.g., 10),  run

```bash
cat data/fixed_projects.csv | tail -n +2 | shuf -n 10 > data/small_fixed.csv
./scripts/analyze-rq2-projects.sh data/small_fixed.csv rq2-results
```

After that, you can create the Table 2 of the paper by running

```bash
./scripts/rq2.py \
  rq1-results/gradle-projects/faults.csv \
  rq1-results/make-projects/faults.csv \
  rq2-results/faults.csv
```

The expected table can be found in `data/rq2_table.txt`.


**Remarks**:
* Two projects (namely `helios` and `LuaJIT`) are expected to produce entries
  where all columns are 0.
  Specifically, although the developers of `helios` accepted our patch,
  the issue still remains even after applying our fix. The reason is that
  unfortunately, our patch didn't solve the issue.
  The developers of `LuaJIT` accepted our patch and the reported issue was indeed fixed.
  However, the recent version of `LuaJIT` contains a fault that was not in the version
  of `LuaJIT` we initially analyzed.
* The developers of `goomph` have confirmed the issue,
but they have not fixed it yet. So this project is excluded from the analysis.
* There are slight variations in four Gradle projects due to an error from our
  part in the initial submission.


## RQ4

For this research question, we compute the performance
characteristics of `BuildFS`.

### Analysis and Fault Detection Times

To re-produce the exact metrics mentioned in the paper,
we have to extract the times from the `times/` directory of
the fetched benchmarks. To do so, run
(estimated running time: 30-60 seconds)

```bash
./scripts/compute-summary-times.sh benchmarks rq4-results
```

This will produce two files inside the `rq4-results` directory:

* `gradle-projects-performance.csv`: This gives the performance
characteristics of `BuildFS` for every Gradle project.
* `make-projects-performance.csv`: This gives the performance
characteristics of `BuildFS` for every Make project.

To dump the metrics mentioned in Section 5.5, run

```bash
./scripts/rq4.py \
  rq4-results/gradle-projects-performance.csv \
  rq4-results/make-projects-performance.csv
```

To compute the peformance characteristics of `BuildFS` on your
machine, you have to extract the performance metrics as computed
in RQ1. Therefore, run

```bash
./scripts/compute-summary-times.sh rq1-results rq4-results
```

and then

```bash
./scripts/rq4.py \
  rq4-results/gradle-projects-performance.csv
  rq4-results/make-projects-performacne.csv
```

You are expected to find similar trends with those mentioned in the paper
(e.g., the analysis takes longer than fault detection,
the analysis of Gradle projects takes longer that the analysis
of Make projects, etc.).


### Build Slowdown

Before proceeding to this step, you need to install some helper Python
packages. In a Python virtualenv run the following:

```bash
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt
```

Now you are able to compute the slowdown that `BuildFS` imposes on the builds
by running the following command

```bash
./scripts/compute-build-slowdown.sh benchmarks
```

the expected output is

```
The slowdown for Gradle builds is 2.62X (90th percentile)
The slowdown for Make builds is 1.68X (90th percentile)
```

**NOTE:**
this command uses the time data from the `benchmarks` directory.
To compute your own data, you have to re-run the builds
(See "Re-running Builds" Section).

## RQ5

For this research question, we will compare the performance of `BuildFS`
against [`mkcheck`](https://github.com/nandor/mkcheck).
To produce the Table 3 of the paper, run:

```bash
# This produces the peformance of BuildFS for every project
# as we did for the previous research question.
./scripts/compute-summary-times.sh benchmarks rq5-results
# This produces the performance of Mkcheck for every Make project
# that mkcheck produced results (see rq5-results/mkcheck-performance.csv).
./scripts/extract-mkcheck-times.sh benchmarks/make-projects rq5-results
./scripts/rq5_table.py \
  rq5-results/make-projects-performance.csv \
  rq5-results/mkcheck-performance.csv
```

to produce Figure 15, run (inside the Python virtual environment we created
earlier)

```bash
# install the requirements of this script
./scripts/rq5_figure.py \
  rq5-results/make-projects-performance.csv \
  rq5-results/mkcheck-performance.csv \
  rq5-results
```

this script generates the Figure 15 of our paper inside the directory given
as the third argument of the script (i.e., `rq5-results/figure15.pdf`).
The script also dumps some metrics presented in the paper
regarding the speedup of `BuildFS`
over `mkcheck`.

**NOTE:**
this command uses the time data from the `benchmarks` directory.
To compute your own data, you have to re-run builds
(See "Re-running Builds" Section).


# Re-running Builds


So far, we have used the system calls traces from
the execution of the examined builds
(see the `benchmarks` directory) to re-produce the results of
the paper. You can use this artifact
in order to re-run the builds of the inspected projects using both
`BuildFS` and `mkcheck`.
After collecting your own data, you can follow each step described
in the "Step by Step Instructions" again to produce the results based on
the new build executions.
Although some builds are not fully deterministic, you
are expected to find similar (if not exact) results to the ones
computed earlier.

First, we create a directory to store the new-benchmarks

```bash
mkdir new-benchmarks
```

## Gradle Builds

To re-run Gradle builds, execute (estimated running time: 4-7 days)

```bash
./scripts/run-gradle-builds data/gradle-projects.txt new-benchmarks/gradle-projects 1
```

The first argument is the list of Gradle projects (along with their version)
to analyze, the second argument is the output directory, while
the third argument indicates whether the script runs the builds without
`BuildFS` (i.e., the value `1` runs the build *both* with and without
`BuildFS`, while `0` runs the build only through `BuildFS`).

To run it on smaller inputs (e.g., 20 Gradle projects), run

```bash
cat data/gradle-projects.txt | shuf -n 20 > data/small-gradle-projects.txt
./scripts/run-gradle-builds \
  data/small-gradle-projects.txt \
  new-benchmarks/gradle-projects 1
```

## Make Builds (BuildFS)

To re-run the full experiments for Make project you need the two Docker images
that we created at the first step of the artifact (namely, `buildfs`,
and `buildfs-sbuild`). Specifically, all Debian packages are run in containers
spawned by the `buildfs-sbuild` image. `sbuild` is a Debian tool to build
Debian packages automatically. First, it creates a clean environment using
`chroot`, then downloads and installs the selected package's dependencies,
and finally, it builds the package.
`sbuild` provides us with hooks over this workflow
so that we can run our custom scripts and tools during
the build of the project.
Therefore,
instead of the standard build,
we exploit these hooks,
and employ `BuildFS` (or `mkcheck`) to analyze the build of the project.

To re-run the builds of Make projects, execute
(estimated running times: 3-6 days)

```bash
./scripts/run-make-builds \
  data/make-projects.txt \
  new-benchmarks/make-projects 1
```

for running and analyzing a subset of Make projects
(e.g., 20 Make projects), run,

```bash
cat data/make-projects.txt | shuf -n 20 > data/small-make-projects.txt
./scripts/run-make-builds \
  data/small-make-projects.txt \
  new-benchmarks/make-projects 1
```

**NOTE**: You can safely ignore any "E: Build failure (dpkg-buildpackage died)"
message produced by `sbuild`.
This means that the Debian binary package was not created,
e.g., due to a lint error
reported by the [Lintian](https://lintian.debian.org/).
However, our `BuildFS` analysis and the build of the project
were still done successfully.

## Make Builds (mkcheck)

To apply `mkcheck` to the examined Make projects, you have
to execute the following command (estimated running time: 2-2.5 weeks)

```bash
./scripts/run-mkcheck-builds data/make-projects.txt new-benchmarks/make-projects
```

To run `mkcheck` on a smaller number of Make projects
(e.g., the `data/small-make-projects.txt` file created in the previous step),
run

```bash
./scripts/run-mkcheck-builds \
  data/small-make-projects.txt \
  new-benchmarks/make-projects
```
