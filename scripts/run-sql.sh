#!/usr/bin/env bash

set -eux

function run_sqlcmd {
  /opt/mssql-tools/bin/sqlcmd -U SA -P "$MSSQL_SA_PASSWORD" "$@"
}


case $1 in
init-db) run_sqlcmd -i /sql/Friendsurance_CreateData.sql
  ;;
task-1)
  run_sqlcmd -i /sql/01_Sum_Sales_For_Period.sql -o /output/01_Sum_Sales_For_Period.txt "${@:2}"
  ;;
task-2)
  run_sqlcmd -i /sql/02_Find_Last_Doc.sql -o /output/02_Find_Last_Doc.txt "${@:2}"
  ;;
task-3)
  run_sqlcmd -i /sql/03_Sum_Sales_And_Pivot.sql -o /output/03_Sum_Sales_And_Pivot.txt "${@:2}"
  ;;
*)
  echo 'Unknown command! Choose one of [init-db, task-1, task-2, task-3]'
  exit 1
  ;;
esac
