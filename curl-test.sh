#!/bin/bash

BASE_URL="http://localhost:5000/api/timeline_post"
RANDOM_ID=$RANDOM
NAME="TestUser$RANDOM_ID"
EMAIL="test$RANDOM_ID@example.com"
CONTENT="Automated test post $RANDOM_ID"

echo "Creating a timeline post..."
POST_RESPONSE=$(curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"$NAME\",\"email\":\"$EMAIL\",\"content\":\"$CONTENT\"}")

echo "POST response: $POST_RESPONSE"

POST_ID=$(echo "$POST_RESPONSE" | grep -o '"id":[0-9]*' | grep -o '[0-9]*')

if [ -z "$POST_ID" ]; then
  echo "FAIL: Could not extract post ID from response"
  exit 1
fi

echo "Created post with ID: $POST_ID"

echo "Fetching timeline posts..."
GET_RESPONSE=$(curl -s "$BASE_URL")

if echo "$GET_RESPONSE" | grep -q "\"content\":\"$CONTENT\""; then
  echo "PASS: New post found in GET response"
else
  echo "FAIL: New post not found in GET response"
  exit 1
fi

echo "Deleting test post with ID: $POST_ID"
DELETE_RESPONSE=$(curl -s -X DELETE "$BASE_URL/$POST_ID")
echo "DELETE response: $DELETE_RESPONSE"

echo "Verifying deletion..."
GET_AFTER_DELETE=$(curl -s "$BASE_URL")

if echo "$GET_AFTER_DELETE" | grep -q "\"content\":\"$CONTENT\""; then
  echo "FAIL: Post still exists after deletion"
  exit 1
else
  echo "PASS: Post successfully deleted"
fi

echo "All tests passed."