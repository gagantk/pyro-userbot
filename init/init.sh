#!/bin/bash

. init/logbot/logbot.sh
. init/proc.sh
. init/utils.sh
. init/checks.sh

trap 'handleSig SIGHUP' HUP
trap 'handleSig SIGTERM' TERM
trap 'handleSig SIGINT' INT
trap '' USR1

handleSig() {
    log "Exiting With $1 ..."
    killProc
}

initGaganRobot() {
    printLogo
    assertPrerequisites
    sendMessage "Initializing GaganRobot ..."
    assertEnvironment
    editLastMessage "Starting GaganRobot ..."
    printLine
}

startGaganRobot() {
    startLogBotPolling
    runPythonModule gaganrobot "$@"
}

stopGaganRobot() {
    sendMessage "Exiting GaganRobot ..."
    endLogBotPolling
}

runGaganRobot() {
    initGaganRobot
    startGaganRobot "$@"
    local code=$?
    stopGaganRobot
    return $code
}
