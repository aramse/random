#!/bin/bash

RESOURCES_DIR=${1:-resources}

# k8s
FILE_PATTERN="*.y*ml"
EXCEPTIONS="exceptions.yaml"
VERSION_CHECK_CMD="kubectl explain"
VERSION_EXISTS_CMD="kubectl api-resources"

function get_fields(){
  local file=$1
  echo $(yq -r '[.kind,.apiVersion] | @csv' $file | sed 's/"//g')
}

function check_version(){
  local resource=$1
  echo $($VERSION_CHECK_CMD $resource | grep 'VERSION:' | cut -d ':' -f 2 | xargs)
}

# not used currently, need better way to find supported versions for a given resource
function check_version_exists(){
  local resource=$1
  local version=$2
  local cached=$([ $RESOURCES_CACHED -eq 1 ] && echo "--cached" || echo "")
  $VERSION_EXISTS_CMD $cached | grep $resource | grep $version
}

# initialize
RESOURCES_CACHED=0
FAILS=0
WARNS=0

# main

[ ! -d "$RESOURCES_DIR" ] && echo "directory not found: $RESOURCES_DIR" && exit 1 

echo "Checking version support for resources defined in files in directory: $RESOURCES_DIR"
echo ""

for f in $(ls $RESOURCES_DIR/$FILE_PATTERN); do
  for fields in $(get_fields $f); do
    resource=$(echo $fields | cut -d ',' -f 1)
    version=$(echo $fields | cut -d ',' -f 2)
  
    # check if exists
#    if [ ! $(check_version_exists $resource $version) ]; then
#      echo "FAIL: $f: Found unsupported version $version for resource $resource"
#      ((FAILS++))
#      RESOURCES_CACHED=1
#      continue
#    fi
#    RESOURCES_CACHED=1

    # compare with latest supported
    supported_version=$(check_version $resource)
    if [ "$version" != "$supported_version" ]; then
      [ -f "$EXCEPTIONS" ] && [ "$(yq -r .$resource $EXCEPTIONS)" != "null" ] && exceptions=$(yq -r ".$resource | @csv" $EXCEPTIONS | sed 's/"//g') || exceptions="null"
      if echo ",$exceptions," | grep ",$version," > /dev/null ; then
        e_type="INFO"
        e_msg="ignored due to exception in $EXCEPTIONS"
      else
        e_type="WARN"
        e_msg="current supported version is $supported_version"
        ((WARNS++))
      fi
      echo "$e_type: $f: Found deprecated/non-current version $version for resource $resource --> $e_msg"
    fi
  done
done

echo ""
echo "Finished resource version checking with $FAILS failures and $WARNS warnings"
exit $FAILS
