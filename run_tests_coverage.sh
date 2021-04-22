#!/bin/bash
echo "Clean up previous coverage record"
coverage erase
count=1
numOfModes=2
targetFile="pdsfile.py\|pdsgroup.py\|pdsgrouptable.py"

vol_rules=(
    "COCIRS_xxxx.py"
    "COISS_xxxx.py"
    "CORSS_8xxx.py"
    "COUVIS_0xxx.py"
    "COUVIS_8xxx.py"
    "COVIMS_0xxx.py"
    "COVIMS_8xxx.py"
    "EBROCC_xxxx.py"
    "GO_0xxx.py"
    "HSTxx_xxxx.py"
    "NHxxxx_xxxx.py"
    "VGISS_xxxx.py"
)
# We can expand the list and add more tests for rules here.
tests_in_rules=(
    "test_opus_products"
)

while [ $count -le $numOfModes ]
do
    echo "Run mode $count"
    rules_tests=""
    for vol in ${vol_rules[@]}; do
        for test in ${tests_in_rules[@]}; do
            rules_tests+=" rules/$vol::$test"
        done
    done
    # Run tests under tests/ and rules/ (specified in tests_in_rules)
    coverage run --parallel-mode -m pytest tests/ $rules_tests --mode $count
    count=`expr $count + 1`
done
echo "Combine results from all modes"
coverage combine
echo "Report coverage"
coverage report |grep $targetFile
echo "Generate html"
coverage html
