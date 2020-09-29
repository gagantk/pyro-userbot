#!/bin/bash

. init/logbot/logbot.sh
. init/utils.sh
. init/checks.sh

trap handleSigTerm TERM
trap handleSigInt INT

initGaganRobot() {
    printLogo
    assertPrerequisites
    sendMessage "Initializing GaganRobot ..."
    assertEnvironment
    editLastMessage "Starting GaganRobot ..."
    printLine
}

startGaganRobot() {
    runPythonModule gaganrobot "$@"
}

stopGaganRobot() {
    sendMessage "Exiting GaganRobot ..."
}

handleSigTerm() {
    log "Exiting With SIGTERM (143) ..."
    stopGaganRobot
    endLogBotPolling
    exit 143
}
handleSigInt() {
    log "Exiting With SIGINT (130) ..."
    stopGaganRobot
    endLogBotPolling
    exit 130
}

runGaganRobot() {
    initGaganRobot
    startLogBotPolling
    startGaganRobot "$@"
    stopGaganRobot
}