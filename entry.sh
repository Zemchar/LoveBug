#!/bin/bash

set -e

host="$1"
port="$2"

until nc -z "$host" "$port"; do
  echo "Waiting for $host:$port to be available..."
  sleep 1
done

echo "$host:$port is now available. Starting the application..."
exec dotnet BugNest.dll
