#!/usr/bin/env bash
BASEDIR=$(cd "$(dirname "$0")/."; pwd)
if [[ "$OSTYPE" == "darwin"* ]]; then
    HOME_PROFILE_PYTHONPATH=$HOME'/.zshrc' # we are not supporting mac os older than catalina
else
    HOME_PROFILE_PYTHONPATH=$HOME'/.bashrc'
fi
HOME_RML_FILEPATH=$HOME'/.rml.env'

export_python_library()
{
    if [ $# -eq 0 ]; then
        echo "Invalid function call (export_python_library)"
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
export_python_library 'rmlib'

source $HOME_PROFILE_PYTHONPATH
