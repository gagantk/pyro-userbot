#!/bin/bash

declare -r pVer=$(sed -E 's/\w+ 3\.8\.([0-9]+)/3.8.\1/g' < <(python3.8 -V 2> /dev/null))

log() {
    local text="$*"
    test ${#text} -gt 0 && test ${text::1} != '~' \
        && echo -e "[$(date +'%d-%b-%y %H:%M:%S') - INFO] - init - ${text#\~}"
}

quit() {
    local err="\t:: ERROR :: $1\nExiting With SIGTERM (143) ..."
    if (( getMessageCount )); then
        replyLastMessage "$err"
    else
        log "$err"
    fi
    exit 143
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

remoteIsExist() {
    grep -q $1 < <(git remote)
}
addHeroku() {
    git remote add heroku $HEROKU_GIT_URL
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

fetchBranches() {
    local r_bs l_bs
    r_bs=$(grep -oP '(?<=refs/heads/)\w+' < <(git ls-remote --heads $UPSTREAM_REMOTE))
    l_bs=$(grep -oP '\w+' < <(git branch))
    for r_b in $r_bs; do
        [[ $l_bs =~ $r_b ]] || git branch $r_b $UPSTREAM_REMOTE/$r_b &> /dev/null
    done
}

upgradePip() {
    pip3 install -U pip &> /dev/null
}

installReq() {
    pip3 install -r $1/requirements.txt &> /dev/null
}

replaceGaganRobot() {
    for filename in gaganrobot/plugins/unofficial/*.py; do
        sed -i "s/userge/gaganrobot/g" "${filename}"
    done
    for filename in gaganrobot/plugins/unofficial/plugins/*.py; do
        sed -i "s/userge/gaganrobot/g" "${filename}"
    done
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