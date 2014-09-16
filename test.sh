#!/bin/bash
URL="http://37ecbb60.ngrok.com/"
TIMEOUT=10000
screenstory screen.js -c firefox --url $URL --saucelabs --timeout $TIMEOUT
screenstory screen.js -c chrome --url $URL --saucelabs --timeout $TIMEOUT
screenstory screen.js -c '{"browserName": "internet explorer", "version": "11"}' --url $URL --saucelabs --timeout $TIMEOUT
screenstory screen.js -c '{"browserName": "internet explorer", "version": "10"}' --url $URL --saucelabs --timeout $TIMEOUT
screenstory screen.js -c '{"browserName": "internet explorer", "version": "9"}' --url $URL --saucelabs --timeout $TIMEOUT
screenstory screen.js -c '{"browserName": "internet explorer", "version": "8"}' --url $URL --saucelabs --timeout $TIMEOUT
screenstory screen.js -c '{"browserName": "opera"}' --url $URL --saucelabs --timeout $TIMEOUT

find tests/screenshots/ -name "*.png" -exec echo "<p><img src=\"{}\" alt=\"{}\" /><span>{}</span><p>" \; > tests.html

echo "Open \"$(pwd)/test.html\""
