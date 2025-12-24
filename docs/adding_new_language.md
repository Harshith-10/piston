# Adding a New Language or Version

This guide explains how to add a new language or a new version of an existing language to Piston.

## Prerequisites

- Fork the `piston` repository.
- Basic knowledge of Bash scripting.
- Understanding of how to install the target language on Linux.

## Directory Structure

Languages are located in the `packages` directory. The structure is as follows:

```
packages/
  ├── [language]/
  │   ├── [version]/
  │   │   ├── build.sh
  │   │   ├── run
  │   │   ├── environment (optional)
  │   │   ├── test.[extension]
  │   │   └── metadata.json
```

## Step-by-Step Guide

### 1. Create the Directory

Create a new directory for your language version.

```bash
mkdir -p packages/[language]/[version]
```

**Example (Java 16.0.0):**
```bash
mkdir -p packages/java/16.0.0
```

### 2. Create `build.sh`

This script is responsible for downloading and installing the language runtime. It should install everything into the current directory.

-   **File:** `packages/[language]/[version]/build.sh`
-   **Permissions:** Executable (`chmod +x build.sh`)

**Example (`packages/java/16.0.0/build.sh`):**

```bash
#!/usr/bin/env bash

# Download the JDK tarball
curl "https://download.java.net/java/GA/jdk16/7863e8c753234954b3064e7c6530a66d/36/GPL/openjdk-16_linux-x64_bin.tar.gz" -o java.tar.gz

# Extract components to the current directory
tar xzf java.tar.gz --strip-components=1

# Clean up
rm java.tar.gz
```

### 3. Create `run`

This script defines how to execute code in this language. It receives the source file as the first argument (`$1`).

-   **File:** `packages/[language]/[version]/run`
-   **Permissions:** Executable (`chmod +x run`)

**Example (`packages/java/16.0.0/run`):**

```bash
#!/usr/bin/env bash

# Rename the input file to have the correct extension (required by Java)
mv $1 $1.java
filename=$1.java
shift

# Compile (if needed) and run
# For single-file source code, newer Java versions can run directly:
java $filename "$@"
```

### 4. Create `metadata.json`

This file defines metadata for the package.

-   **File:** `packages/[language]/[version]/metadata.json`

**Example:**

```json
{
    "language": "java",
    "version": "16.0.0",
    "aliases": []
}
```

### 5. Create `environment` (Optional)

If your language requires specific environment variables (like `PATH` or `JAVA_HOME`), define them here.

-   **File:** `packages/[language]/[version]/environment`

**Example:**

```bash
#!/usr/bin/env bash

export PATH=$PWD/bin:$PATH
```

### 6. Create a Test File

Create a simple "Hello World" program to verify the installation.

-   **File:** `packages/[language]/[version]/test.java` (or appropriate extension)

**Example:**

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("OK");
    }
}
```

### 7. Build and Test

Run the Piston CLI tools to build and test your package.

```bash
# Build the package
./piston build-pkg [language] [version]

# Install it locally for testing (simulated)
./piston ppman install [language]=[version]

# Run the test
./piston run [language] -l [version] packages/[language]/[version]/test.java
```

If the output is `OK`, your package is ready!

### 8. Commit and Push

Commit your changes:

```bash
git add packages/[language]/[version]
git commit -m "pkg([language]-[version]): Added [language] [version]"
```
