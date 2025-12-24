#!/usr/bin/env bash

# Download the JDK tarball
curl "https://download.oracle.com/java/25/latest/jdk-25_linux-x64_bin.tar.gz" -o java.tar.gz

# Extract components to the current directory
tar xzf java.tar.gz --strip-components=1

# Clean up
rm java.tar.gz