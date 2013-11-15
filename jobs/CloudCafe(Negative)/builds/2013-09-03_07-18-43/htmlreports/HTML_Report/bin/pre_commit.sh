
#Setting environment variables for old lunr_env_smoke test

#Run CloudCAFE lunr_env_smoke test
./runner.py blockstorage qe -m novashell_smoke
LUNR_ENV_RESULT=$?

#Run CloudCAFE lunr_api_smoke tests
./runner.py blockstorage qe -m lapi*_smoke
LUNR_API_RESULT=$?

echo "CloudCAFE lunr_env_smoke returned errorcode $LUNR_ENV_RESULT"
echo "CloudCAFE lunr_api_smoke returned errorcode $LUNR_API_RESULT"

ERRORS=$(($LUNR_ENV_RESULT + $LUNR_API_RESULT))
if [ $ERRORS -eq 0 ]; then
    echo "No errors in any tests. You can commit your changes."
else
    echo "There were errors in the test run. Please fix these before committing your changes." 
fi
