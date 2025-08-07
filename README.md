# Password Management Tools

Convert your browser-exported passwords to Bitwarden format with intelligent name detection and organization features.

When you import your standard passrods from Google into Bitdefender, you'll notice some stuff missing.
- What are these *--*? I can Favorite them? What does *reprompt* mean?

Well, this program tries to make the transition as smooth as possible, with efficiency as my top priority.

## 🚀 Quick Start

### Install Python (Beginners)
1. **Download Python** from [python.org](https://www.python.org/downloads/)
   - Choose the latest version for your operating system
   - ✅ **Important:** Check "Add Python to PATH" during installation
2. **Verify installation** by opening Command Prompt/Terminal and typing:
   ```
   python --version
   ```

### Install Dependencies
This project uses only **built-in Python libraries** - no extra installations needed! 🎉

### Usage
1. **Export your passwords** from your browser as CSV file
2. **Rename the file** to `Passwords.csv` and place it in this folder
3. Change the directory to the folder with the file
4. **Run the converter:**
   ```
   python csv_to_bitwarden.py
   ```
5. **Follow the interactive prompts** to organize your passwords
6. **Sort your passwords**:
   ```
   python sort.py
   ```
7. **Import the resulting** `Sorted_Pswds.csv` into Bitwarden

---

## 📁 File Overview

### 🔧 Core Tools

#### `csv_to_bitwarden.py` - **Main Conversion Tool**
The heart of the project! Converts CSV password exports from Chrome/Edge and compatible browsers to Bitwarden format.

**✨ Key Features:**
- **Interactive name selection** with smart suggestions
- **Android app support** - handles mobile app passwords with clean names  
- **Folder organization** - create and organize folders on-the-fly
- **Express mode** - skip optional fields for faster bulk processing
- **Fuzzy matching** - helps fix typos in folder names
- **Input validation** - ensures your CSV file is in the correct format

#### `uri_mapping.py` - **URI Mapping Dictionary**
Maps cryptic package names and URLs to readable names.

**Examples:**
- `com.zhiliaoapp.musically` → "TikTok"
- `com.facebook.katana` → "Facebook"  
- `org.ankidroid` → "AnkiDroid"

**Easily extensible** - add new app mappings as needed!

#### `sort.py` - **Password Organizer**  
Sorts your converted passwords by multiple criteria with hierarchical organization.

**✨ Features:**
- **Multi-level sorting** - sort by name, then folder, then username
- **Interactive selection** - choose which fields to sort by
- **Efficient algorithm** - uses binary search for optimal performance
- **Debug output** - see exactly how entries are being compared

### 📄 Expected CSV Files

- **`Passwords.csv`** - Your input file (from browser export)
  - Expected fields: `url`, `username`, `password`
- **`Bitwarden_Pswds.csv`** - Generated output for Bitwarden import
- **`Sorted_Pswds.csv`** - Final organized password list
  - This is useful to better see similar fields of your choice, and make any small edits

---

## 🎯 Typical Workflow

1. **Export** passwords from your browser → save as `Passwords.csv`
2. **Convert** with interactive name selection:
   ```
   python csv_to_bitwarden.py
   ```
3. **Sort** your organized passwords:
   ```
   python sort.py
   ```
4. **Import** `Sorted_Pswds.csv` into Bitwarden

### Express Mode
For bulk processing with minimal interaction:
- Choose "Express Mode" when prompted
- Skip optional fields (favorites, notes, TOTP)
- Faster processing with basic organization

---

## 🌟 Smart Features

### Intelligent Name Detection
- **Website URLs:** `https://docs.google.com/` → suggests "Docs", "Google"  
- **Android Apps:** `android://hash@com.instagram.android/` → suggests "Instagram", "Android"
- **Streamlined selection:** Auto-generated options accept instantly, custom names get confirmation
- **Custom names:** Always option to enter your own

### Folder Management
- **Pre-loaded categories:** Personal, Work, Social Media, Banking, etc.
- **Fuzzy matching:** Types "Bankng" → suggests "Banking"
- **Create on-the-fly:** New folders created during conversion process

### Android App Support
- **Automatic recognition** of `android://` protocol URLs
- **Package name mapping** using the companion dictionary
- **Clean, readable names** instead of cryptic package identifiers

---

## 🔧 System Requirements

- **Python 3.6+** (uses only standard library)
- **Any operating system** (Windows, macOS, Linux)
- **Compatible browser** (Chrome, Edge, or Chromium-based browsers)

---

## 🤝 Help Build the Database

**Want to make this tool better?** 

I'm building a **community-driven database** of app and website mappings. If you encounter apps or websites that show cryptic names like:
- `com.mysterious.app.package` instead of "MyFavoriteApp"
- `weird-subdomain.confusing-domain.com` instead of "CleanSiteName"

**Please contribute!** Here's how:

### Fork & Add Mappings
1. **Fork this repository**
2. **Edit `uri_mapping.py`** - add your mappings to:
   - `ANDROID_MAPPING` for Android apps
   - `HREF_MAPPING` for websites
3. **Submit a pull request** 

**Example contributions:**
```python
# Android Apps
"com.newapp.android": ["NewApp"],
"tv.streaming.service": ["StreamingTV"],

# Websites  
"secure-login.bankname.com": ["BankName"],
"shop.retailer.co.uk": ["Retailer", "Shopping"],
```

### Guidelines for Mappings
- **Keep it minimal**: Use base domains like `facebook.com` (not `m.facebook.com` or `mobile.facebook.com`)
- **Preserve distinct services**: Keep specific subdomains like `docs.google.com` when they're separate services
- **Use clean names**: `["Facebook"]` not `["Facebook Inc."]` or `["FB"]`

### What I'm Looking For
- **Popular apps** missing from the database
- **Banking/financial sites** with complex subdomains  
- **Regional websites** from different countries
- **Work/enterprise tools** with cryptic domain names

Every contribution helps users get cleaner, more organized password imports.

---

## 📝 Supported Export Formats

This tool works with password exports from:
- ✅ **Google Chrome**
- ✅ **Microsoft Edge** 
- ✅ **Chromium-based browsers** (Brave, Vivaldi, Opera - usually work)
- ❓ **Other browsers** - Check if your export has `url,username,password` headers

**Note:** Firefox and Safari use different export formats and may need manual header adjustment.

---

## Need Help?

**Common Issues:**
- **"Must be a Microsoft or Google csv file"** → Check your CSV has `url,username,password` headers (Firefox/Safari exports may need manual header editing)
- **Python not recognized** → Make sure Python was added to PATH during installation
- **Empty usernames** → Tool will prompt you to enter missing information

**Pro Tips:**
- Use **Express Mode** for large password lists (500+ entries)
- **List folders** anytime during conversion to see available options
- **Skip entries** that are problematic - you can always re-run later

---


*Convert your passwords with confidence! 🔐*


