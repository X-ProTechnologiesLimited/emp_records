#!/usr/bin/env bash
filestamp=`date +%H%M%S`
filename=emp_manager.log
get_project_dir() { # Gets the root directory of the repository
    cd "${BASH_SOURCE[0]%*/*}/.." && pwd
}
PROJECT_DIR=$(get_project_dir)
if [[ "$1" == '--new' ]];then
    source $PROJECT_DIR/utils/app_run.config && export $(cut -d= -f1 $PROJECT_DIR/utils/app_run.config)
    rm -rf $PROJECT_DIR/lib/db.sqlite
    python3 $PROJECT_DIR/initialise_db.py
    printf "Created new database for application...\n"
    python3 -m flask run --host=0.0.0.0 >> $PROJECT_DIR/logs/$filename 2>&1 &
     
elif [[ "$1" == '--old' ]];then
    source $PROJECT_DIR/utils/app_run.config && export $(cut -d= -f1 $PROJECT_DIR/utils/app_run.config)
    printf "Using the existing database...\n"
    echo "Using the existing database..." >> $PROJECT_DIR/logs/$filename
    python3 -m flask run --host=0.0.0.0 >> $PROJECT_DIR/logs/$filename 2>&1 &

else
    echo "Error: Incorrect Database Creation option specified.."
    printf "Please use correct flags for database creation...\n"
    printf "start_app.sh --new : [This will create a new database before starting the app]\n"
    printf "start_app.sh --old : [This will use existing/old database before starting the app]\n"
    exit
fi

printf "Waiting for the application to initialise....\n"
sleep 5
printf "Application Started Successfully\n"
printf "To Shutdown Application, press Ctrl+C AND run /utils/shutdown.sh (For Standalone and Detached Containers)\n"
