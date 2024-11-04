#!/usr/bin/env bash

SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
STDOUT_DIR=$SCRIPT_DIR/stdout
TEST_WORKSPACE_DIR=$SCRIPT_DIR/test_workspace

cd $SCRIPT_DIR

python -m venv venv
source venv/bin/activate
pip install $SCRIPT_DIR/../..

rm -r $SCRIPT_DIR/$STDOUT_DIR
rm -r $SCRIPT_DIR/$TEST_WORKSPACE_DIR

mkdir $STDOUT_DIR
mkdir $TEST_WORKSPACE_DIR
cd $TEST_WORKSPACE_DIR

#
# Help
#

construction_utils --help > $STDOUT_DIR/help.output
construction_utils create_project --help > $STDOUT_DIR/create_project.output
construction_utils generate_docs --help > $STDOUT_DIR/generate_docs.output

#
# Create project
#

construction_utils create_project test_project_one > $STDOUT_DIR/create_project.output
construction_utils -vv create_project test_project_two > $STDOUT_DIR/create_project_verbose.output

#
# Extract layers
#

construction_utils generate_docs > $STDOUT_DIR/generate_docs.output
construction_utils -vv generate_docs > $STDOUT_DIR/generate_docs_verbose.output


echo -e "\nResults can be found in \"$STDOUT_DIR\""