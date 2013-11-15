#Run CloudCAFE lava_api smoke test
./runner.py bigdata lab -p smoke
LAVA_SMOKE_RESULT=$?

echo "CloudCAFE lunr_api_smoke returned errorcode $LAVA_SMOKE_RESULT"

if [ $LAVA_SMOKE_RESULT -eq 0 ]; then
    echo "No errors in any tests. You can commit your changes."
else
    echo "There were errors in your test run. Please review output and fix tests before committing."
fi
