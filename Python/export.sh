#!/usr/bin/env bash
BASEDIR=$(cd "$(dirname "$0")/."; pwd)
HOME_PROFILE_PYTHONPATH=$HOME'/.bash_profile'
HOME_RML_FILEPATH=$HOME'/.rml.env'

export_python_script()
{
    if [ $# -eq 0 ]; then
        echo "Invalid function call (export_python_script)"
        exit 1
    fi
    path=$1
    echo "===> exporting '${path}'"
    if [ "$path" != "" ]; then
        path="/${path}"
    fi
    echo "export PYTHONPATH=\$PYTHONPATH:$BASEDIR${path}" >> $HOME_PROFILE_PYTHONPATH
    echo "PYTHONPATH=$BASEDIR${path}" >> $HOME_RML_FILEPATH
}

echo '
# RML scripts, executed: export.sh' >> $HOME_PROFILE_PYTHONPATH
export_python_script 'rmlib'

source $HOME_PROFILE_PYTHONPATH
