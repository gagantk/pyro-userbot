#!/bin/bash

. init/logbot/logbot.sh
. init/utils.sh
. init/checks.sh

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

runGaganRobot() {
    initGaganRobot
    startLogBotPolling
    startGaganRobot "$@"
    stopGaganRobot
}