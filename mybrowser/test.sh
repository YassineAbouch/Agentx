# Tests examples for mybrowser

# 1. Start the server first
# npm start

# 2. Run these tests

echo "Testing mybrowser API..."
echo ""

# Test 1: Open a page
echo "1. Opening example.com..."
curl -X POST http://localhost:3000/open \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
echo ""
sleep 2

# Test 2: Get title
echo "2. Getting page title..."
curl http://localhost:3000/title
echo ""
sleep 1

# Test 3: Get page text
echo "3. Getting page text..."
curl http://localhost:3000/content/text | jq '.text' | head -20
echo ""
sleep 1

# Test 4: Get links
echo "4. Getting links..."
curl http://localhost:3000/links | jq '.links[0:5]'
echo ""
sleep 1

# Test 5: Screenshot
echo "5. Taking screenshot..."
curl http://localhost:3000/screenshot
echo ""
sleep 1

# Test 6: Status
echo "6. Checking status..."
curl http://localhost:3000/status
echo ""

echo ""
echo "✅ Tests completed!"
