#!/bin/bash

declare -r pVer=$(sed -E 's/\w+ ([2-3])\.([0-9]+)\.([0-9]+)/\1.\2.\3/g' < <(python3.8 -V))

log() {
    local text="$*"
    test ${#text} -gt 0 && test ${text::1} != '~' \
        && echo -e "[$(date +'%d-%b-%y %H:%M:%S') - INFO] - init - ${text#\~}"
}

quit() {
    local err="\t:: ERROR :: $1\nExiting With SIGTERM ..."
    if (( getMessageCount )); then
        replyLastMessage "$err"
    else
        log "$err"
    fi
    exit 1
}

runPythonCode() {
    python${pVer%.*} -c "$1"
}

runPythonModule() {
    python${pVer%.*} -m "$@"
}

gitInit() {
    git init &> /dev/null
}

gitClone() {
    git clone "$@" &> /dev/null
}

addUpstream() {
    git remote add $UPSTREAM_REMOTE ${UPSTREAM_REPO%.git}.git
}

updateUpstream() {
    git remote rm $UPSTREAM_REMOTE && addUpstream
}

fetchUpstream() {
    git fetch $UPSTREAM_REMOTE &> /dev/null
}

upgradePip() {
    pip3 install -U pip &> /dev/null
}

installReq() {
    pip3 install -r $1/requirements.txt &> /dev/null
}

printLine() {
    echo ========================================================
}

printLogo() {
    printLine
    echo '
    
       ______                        ____        __          __ 
      / ____/___ _____ _____ _____  / __ \____  / /_  ____  / /_
     / / __/ __ `/ __ `/ __ `/ __ \/ /_/ / __ \/ __ \/ __ \/ __/
    / /_/ / /_/ / /_/ / /_/ / / / / _, _/ /_/ / /_/ / /_/ / /_  
    \____/\__,_/\__, /\__,_/_/ /_/_/ |_|\____/_.___/\____/\__/  
               /____/                                           

    '
    printLine
}