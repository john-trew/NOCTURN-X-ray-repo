# NSF NOCTURN Metadata

Welcome to the **NOCTURN Metadata** project! This repository is dedicated to streamlining non-clinical tomographic imaging workflows across various facilities, while keeping each facility's code and configurations separated into their own Git branches.

## Table of Contents

1. [Overview](#overview)
2. [Project Structure](#project-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Branch Strategy](#branch-strategy)
6. [Contributing](#contributing)
7. [License](#license)

---

## Overview

The **NOCTURN Metadata** project aims to:
- Automate the collection and processing of X-ray Computed Tomography (CT) imaging data.
- Provide facility-specific configurations in separate branches.
- Centralize shared code and actions in the main branch, making collaboration seamless.

---

## Project Structure

```plaintext

my-nocturn-xray-repo/
├─ README.md                   # General project overview
├─ docs/                       # Documentation files
│   └─ index.md
├─ agent/                      # Core agent code for processing
│   └─ main_agent.py
├─ .github/
│   └─ workflows/
│       └─ agent_actions.yml   # GitHub Actions workflow
├─ facility-1-branch           # Branch in GitHub (not a folder)
├─ facility-2-branch           # Branch in GitHub (not a folder)
└─ facility-n-branch           # Branch in GitHub (not a folder)
```

## Installation

This section describes how to install and configure **NOCTURN Metadata Parser** on a Raspberry Pi using an `.iso` file. This method provides a quick, standardized setup with minimal manual steps.

### Prerequisites
- **Raspberry Pi** (Pi 3, Pi 4, or similar)  
- **SD Card** (16 GB or larger)  
- **Raspberry Pi Imager** SD card flashing tool (https://www.raspberrypi.com/software/) 
- **Windows machine** with a shared folder (read-only) for metadata   (e.g. .pca file)
- **Network Connectivity** (Ethernet or Wi-Fi)

---

### Step 1: Download the Raspberry Pi ISO

1. Go to this repository's **[Releases](../../releases)** page (or wherever the `.iso` is hosted).  
2. Download the latest `.iso` file (for example, `nocturn-xray-raspi.iso`).

---

### Step 2: Flash the ISO to an SD Card

1. Insert your SD card into your computer.  
2. Open **Raspberry Pi Imager** (or another flashing tool).  
3. Select the downloaded `.iso` file as the **source**.  
4. Choose the SD card as the **target**.  
5. Click **Write** (or equivalent) to begin flashing.  
6. Wait until the process completes, eject SD card.

---

### Step 3: Configure the Pi via the `.txt` Template

1. Locate the `facility-config-template.txt` file in this repository (e.g., under `docs/` or `config/`).  
2. Click **Download** on `facility-config-template.txt`.  
3. Open the file in a text editor and fill in the required fields, for example:

   ```plaintext
   # Facility Configuration for Nocturn Xray

   # GitHub Repository (for logging, updates, etc.)
   GITHUB_REPO_URL=https://github.com/johntrue15/NOCTURN-X-ray-repo/tree/American-Museum-of-Natural-History

   # Facility Name
   FACILITY_NAME=American-Museum-of-Natural-History

   # X-ray User ORCID
   XRAY_USER_ORCID=0000-0001-2345-6789

   # iDigBio / Morphosource Mapping Fields
   IDIGBIO_COLLECTION_CODE=XYZ
   MORPHOSOURCE_PROJECT=MyMorphoProject

   # Windows Shared Folder Path (UNC)
   SHARED_FOLDER_PATH=//WINDOWS-MACHINE/MySharedFolder

   # Additional notes:
   # This folder should contain the metadata files that the Pi will read.
   # The Pi will only need "read" permissions.
   ```


4. Save the file as a `.txt` into the shared folder on the CT Workstation.

---

### Step 4: Set Up a Read-Only Shared Folder on Windows

1. **Create** a folder on your Windows machine (e.g., `C:\NocturnXrayData`).  
2. Right-click → **Properties** → **Sharing** tab → **Advanced Sharing**.  
3. Check **Share this folder**, and give it a share name (e.g., `MySharedFolder`).  
4. Click **Permissions** and ensure **Read** is enabled (and **Write** is disabled if you only want read-only access).  
5. Make sure your Windows network settings allow the Pi to see shared folders (enable Network Discovery).  
6. Note the UNC path: `\\YOUR-WINDOWS-MACHINE\MySharedFolder`. In your `.txt` config, you might use `//YOUR-WINDOWS-MACHINE/MySharedFolder` for the Pi.

---

### Step 5: Insert the SD Card and Power On

1. Safely **eject** the SD card from the flashing computer.  
2. Insert the SD card into your Raspberry Pi.  
3. Connect the Pi to the network (Ethernet or configured Wi-Fi).  
4. **Power on** the Pi.  
5. It will automatically:  
   - **Read** the `facility-config-template.txt`.  
   - **Mount** the shared folder in read-only mode.  
   - **Start** Xray processing tasks using metadata from the shared folder.

---

## Usage

After **Installation**, you can perform a quick test to ensure your Raspberry Pi is reading the shared folder and publishing metadata correctly:

1. **Place a `.pca` file** in your Windows shared folder.  
   - For instance, use a copy of a `.pca` file.

2. **Wait** a few moments while the Raspberry Pi detects and processes the `.pca` file.  
   - Under normal operation, the Pi will automatically pick up new files in the shared folder.

3. **Check** your facility branch in GitHub.  
   - The Pi should publish metadata (or logs) related to the `.pca` file to your designated branch.  
   - The exact commit message or metadata structure may depend on your facility's configuration.

4. **Verify** everything ran smoothly:  
   - Look for any resulting metadata in your GitHub repository (e.g., a JSON file, CSV, or updated logs).

5. **Troubleshoot** if needed:  
   - Ensure the Pi is connected to your network and can access the shared folder.  
   - Check logs on the Pi (if accessible) to confirm the `.pca` file was detected and processed.  
   - Make sure your branch permissions (and any GitHub tokens or credentials) allow the Pi to push changes.

This simple test verifies the end-to-end workflow:  
- The Pi has read access to the shared folder.  
- Your facility branch in GitHub is updated with metadata for each `.pca` file.  
- Nocturn Xray can automatically handle imaging data with minimal manual intervention.


---

## Branch Strategy

We maintain separate branches for each facility:

- **main**: Shared resources and base functionality, including CI/CD workflows.  
- **facility-1-branch**, **facility-2-branch**, etc.  
  - Contain facility-specific customizations.  
  - Merge or rebase from `main` to keep updated with new changes.  
  - If a facility adds a general improvement, open a Pull Request back into `main`.

---

## Contributing

1. **Fork** this repository.  
2. **Create** a new branch for your facility (e.g., `main/University-of-...`).  
3. **Commit** your changes and push to your fork.  
4. **Open a Pull Request** into `main`.  

We welcome enhancements, bug fixes, and feedback! Check out our **Code of Conduct** if applicable.

---

## License

This project is licensed under the [MIT License](LICENSE). By contributing, you agree that your contributions will be licensed under MIT as well.

---

<p align="center">
  <i>Thank you for installing and using NOCTURN Metadata Parser! We hope this streamlined Raspberry Pi setup accelerates your imaging workflows.</i>
</p>

# NOCTURN X-ray Repository

This repository contains automated workflows for collecting and validating X-ray CT data from MorphoSource.

## Workflows and Scripts

### Daily Check (`daily.yml`)
Runs daily to check for new records on MorphoSource.

**Associated Scripts:**
- `.github/scripts/daily.py` - Checks for new records
- `.github/scripts/collect.py` - Collects new records when found

### Monthly Collection (`monthly.yml`)
Runs monthly to collect all X-ray CT records and generate statistics.

**Associated Scripts:**
- `.github/scripts/monthly.py` - Collects and processes monthly data
- `.github/scripts/release_analyzer.py` - Analyzes collected data for release

### Test Workflows

#### Daily Test (`test_daily.yml`)
Tests the daily check and collection process.

**Associated Scripts:**
- `.github/scripts/test_daily.py` - Simulates daily check process
- `.github/scripts/daily.py` - Used for testing daily checks

#### Dimension Test (`dimension_test.yml`)
Tests data dimensions and integrity.

**Associated Scripts:**
- `.github/scripts/dimension_test.py` - Validates data dimensions

## Directory Structure

