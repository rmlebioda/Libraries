#!/usr/bin/env bash
BASEDIR=$(cd "$(dirname "$0")/."; pwd)
HOME_PROFILE_PYTHONPATH=$HOME'/.bash_profile'

export_python_script()
{
    echo "===> exporting $1"
    echo "export PYTHONPATH=\$PYTHONPATH:$BASEDIR/$1" >> $HOME_PROFILE_PYTHONPATH
}

echo '

# RML scripts, executed: export.sh' >> $HOME_PROFILE_PYTHONPATH
export_python_script 'pages_downloader'
export_python_script 'os_ascii_remover'

source $HOME_PROFILE_PYTHONPATH
