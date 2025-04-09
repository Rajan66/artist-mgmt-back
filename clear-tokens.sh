#!/bin/bash

export PGPASSWORD="root"

echo "Connecting to db and clearing the blacklisted refresh tokens"
psql -U rajan -d db_ams -c "DELETE FROM authentication_tokenblacklist;"

exit 0
