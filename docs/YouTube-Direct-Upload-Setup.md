# YouTube Direct Upload Setup

**What this does:** Lets you automatically upload videos to your YouTube channel from your computer — no manual uploading, no third-party services, completely free.

**Time needed:** About 15-20 minutes (one-time setup, then it works forever)

**What you'll get:** 3 secret keys that let your computer talk to YouTube on your behalf

---

## Before You Start

You need:
- A Google account that has a YouTube channel
- A web browser (Chrome, Safari, Firefox — any works)
- A place to temporarily paste and save some text (Notes app, a text file, or even a piece of paper)

---

## Part 1: Go to Google Cloud Console

Google Cloud Console is a free website where Google lets you create little "apps" that can talk to YouTube. Don't worry — you're not building anything complicated. You're just telling Google: "Hey, let my computer upload videos to my YouTube channel."

### Step 1: Open the website

Open your web browser. In the address bar at the very top (where you normally type website addresses), type this and press Enter:

```
console.cloud.google.com
```

### Step 2: Sign in

Google will show you a sign-in page. **Use the same Google account that owns your YouTube channel.** This is important — if you use a different account, it won't work.

If you're already signed in to Google, it might skip this step.

### Step 3: Accept terms (first time only)

If it's your first time visiting Google Cloud Console, you'll see a page asking you to agree to their terms of service.

**What you'll see on screen:**

```
┌─────────────────────────────────────────────────┐
│                                                 │
│   Welcome to Google Cloud                       │
│                                                 │
│   ☐ I agree to the Google Cloud Terms           │
│      of Service...                              │
│                                                 │
│              [ Agree and Continue ]              │
│                                                 │
└─────────────────────────────────────────────────┘
```

Check the box, then click the blue **"Agree and Continue"** button.

### What you should see now

You'll land on the Google Cloud dashboard. It looks like this:

```
┌──────────────────────────────────────────────────────────┐
│ ☰  Google Cloud   [Select a project ▾]    🔍 Search...  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│   Dashboard                                              │
│                                                          │
│   Welcome! Here are some things you can do...            │
│                                                          │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│   │  Empty   │  │  Empty   │  │  Empty   │              │
│   │  panels  │  │  panels  │  │  panels  │              │
│   └──────────┘  └──────────┘  └──────────┘              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

The important thing is the top bar — you'll use it in the next step.

---

## Part 2: Create a New Project

Think of a "project" like a folder — it keeps everything organized. You'll create one folder just for YouTube uploading.

### Step 1: Open the project picker

Look at the very top of the page. In the dark blue/black bar, you'll see text that says either **"Select a project"** or shows the name of some existing project. It has a small **down arrow ▾** next to it.

```
┌──────────────────────────────────────────────────────────┐
│ ☰  Google Cloud   [ Select a project ▾ ]   🔍 Search   │
│                     ↑↑↑ CLICK THIS ↑↑↑                  │
└──────────────────────────────────────────────────────────┘
```

**Click on that text** (the part that says "Select a project" with the arrow).

### Step 2: Click "New Project"

A popup window appears in the center of your screen. It looks like this:

```
┌────────────────────────────────────────────┐
│  Select a project                          │
│                                            │
│  Recent   |   All                          │
│                                            │
│  (empty or list of existing projects)      │
│                                            │
│                        [ NEW PROJECT ]  ← CLICK THIS
│                                            │
└────────────────────────────────────────────┘
```

Look for the **"New Project"** button — it's usually in the **top-right corner** of this popup. It might be blue text or a button. Click it.

### Step 3: Fill in the project name

You'll see a simple form:

```
┌────────────────────────────────────────────┐
│  New Project                               │
│                                            │
│  Project name *                            │
│  ┌──────────────────────────────────────┐  │
│  │ My First Project                     │  │ ← DELETE this and type
│  └──────────────────────────────────────┘  │   "YouTube Uploader"
│                                            │
│  Organization                              │
│  No organization                           │ ← DON'T TOUCH this
│                                            │
│  Location                                  │
│  No organization                           │ ← DON'T TOUCH this
│                                            │
│            [ Cancel ]  [ CREATE ]           │
│                                            │
└────────────────────────────────────────────┘
```

- **Project name**: Delete whatever is in the box and type: `YouTube Uploader`
- **Organization**: Don't touch this — leave it as "No organization"
- **Location**: Don't touch this either

Click the blue **"Create"** button.

### Step 4: Select your new project

Wait about 5-10 seconds. A notification will pop up in the top-right corner:

```
┌──────────────────────────────────┐
│ 🔔 Notifications                 │
│                                  │
│ ✓ Create Project:                │
│   YouTube Uploader               │
│                                  │
│   [ SELECT PROJECT ]  ← CLICK   │
│                                  │
└──────────────────────────────────┘
```

Click **"Select Project"** in that notification.

**If you missed the notification:** No problem! Click the project dropdown at the top of the page again (same place as Step 1). You'll see "YouTube Uploader" in the list. Click on it.

### What you should see now

The top bar now shows your project name:

```
┌──────────────────────────────────────────────────────────┐
│ ☰  Google Cloud   [ YouTube Uploader ▾ ]   🔍 Search   │
└──────────────────────────────────────────────────────────┘
```

If you see "YouTube Uploader" up there, you're in the right place.

---

## Part 3: Turn On the YouTube Feature

Now you need to tell Google: "I want this project to be able to talk to YouTube."

### Step 1: Open the API Library

There are two ways to get there:

**Option A (Search — easier):** Click the **search bar** at the top of the page (where it says "Search" with a magnifying glass 🔍). Type:

```
YouTube Data API v3
```

You'll see it appear in the results. Click on it and skip to Step 3.

**Option B (Menu):** Look at the left side of the page. You'll see a sidebar menu:

```
┌─────────────────────┐
│ ▸ APIs & Services    │ ← CLICK THIS
│ ▸ IAM & Admin       │
│ ▸ Compute Engine    │
│ ▸ ...               │
└─────────────────────┘
```

If you don't see the sidebar, click the **three horizontal lines ☰** (hamburger menu) at the very top left corner of the page.

Click **"APIs & Services"**. Then click **"Library"** in the submenu that appears.

### Step 2: Search for the YouTube API

You'll see a page full of API cards with a search box at the top:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   API Library                                        │
│                                                      │
│   🔍 [ Search for APIs & Services              ]    │
│                                                      │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐            │
│   │ Maps    │  │ Drive   │  │ Gmail   │            │
│   │   API   │  │   API   │  │   API   │            │
│   └─────────┘  └─────────┘  └─────────┘            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

In the search box, type: `YouTube Data API v3`

### Step 3: Enable the API

Click on **"YouTube Data API v3"** in the search results. It has the red YouTube play button logo next to it.

You'll land on a page that looks like this:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   ▶ YouTube Data API v3                              │
│   Google                                             │
│                                                      │
│   Add YouTube features to your application...        │
│                                                      │
│              [ ENABLE ]  ← CLICK THIS BIG            │
│                            BLUE BUTTON               │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Click the blue **"Enable"** button. Wait a few seconds.

### What you should see now

The page changes to show an API dashboard with some graphs (all zeros — that's normal, you haven't used it yet):

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   YouTube Data API v3                                │
│   ✓ API enabled                                      │
│                                                      │
│   Traffic ──────────── 0                             │
│   Errors  ──────────── 0                             │
│                                                      │
└──────────────────────────────────────────────────────┘
```

You're doing great. The YouTube API is now turned on.

---

## Part 4: Set Up the Permission Screen

When you connect your YouTube account for the first time, Google will show you a screen asking "Do you want to allow this app to upload videos?" This step sets up what that screen looks like.

**Don't worry — only YOU will ever see this screen, and only once.**

### Step 1: Go to the OAuth consent screen

Use the search bar at the top of the page. Type:

```
OAuth consent screen
```

Click the result that says **"OAuth consent screen"** (under APIs & Services).

Or use the sidebar: **APIs & Services** → **OAuth consent screen**.

### Step 2: Start the setup

You'll see a setup page. It might look slightly different depending on when you visit, but you'll see either a **"Get Started"** button or a **"Configure Consent Screen"** button.

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   OAuth consent screen                               │
│                                                      │
│   To create an OAuth client, you must first          │
│   configure your consent screen.                     │
│                                                      │
│             [ GET STARTED ]  ← CLICK                 │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Click whichever button you see.

### Step 3: Fill in app information

You'll see a form asking about your app:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   App information                                    │
│                                                      │
│   App name *                                         │
│   ┌──────────────────────────────────────────┐       │
│   │                                          │       │ ← Type:
│   └──────────────────────────────────────────┘       │   "YouTube Uploader"
│                                                      │
│   User support email *                               │
│   ┌──────────────────────────────────────────┐       │
│   │ your.email@gmail.com              ▾      │       │ ← Click the dropdown
│   └──────────────────────────────────────────┘       │   and select your email
│                                                      │
└──────────────────────────────────────────────────────┘
```

- **App name**: Type `YouTube Uploader`
- **User support email**: Click the dropdown arrow and select your email address from the list

### Step 4: Choose audience type

You'll see a choice about who can use this app:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Audience                                           │
│                                                      │
│   ○ Internal  (only for Google Workspace users)      │
│   ● External  ← SELECT THIS ONE                     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Select **"External"**. (If you have a regular Gmail account, this is the only option anyway.)

Click **"Next"** or **"Create"** to continue.

### Step 5: Add the YouTube upload permission (Scope)

Now you need to give your app permission to upload videos. Scopes are just permissions — what your app is allowed to do.

Look at the **left sidebar** of the OAuth consent screen. You'll see several options:

```
┌─────────────────────┐
│ Branding            │
│ Audience            │
│ Data Access         │ ← CLICK THIS
│ ...                 │
└─────────────────────┘
```

Click **"Data Access"** in the left sidebar. You'll see a page about scopes:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Data Access                                        │
│                                                      │
│   These scopes define the level of access...         │
│                                                      │
│   [ ADD OR REMOVE SCOPES ]  ← CLICK THIS            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Click **"Add or Remove Scopes"**. A panel slides open from the right side:

```
                        ┌──────────────────────────────┐
                        │   Update selected scopes     │
                        │                              │
                        │   🔍 Filter [ youtube.upload ]│ ← TYPE THIS
                        │                              │
                        │   ☐ .../youtube.upload        │
                        │     Manage your YouTube       │ ← CHECK THIS
                        │     videos                    │   BOX
                        │                              │
                        │                              │
                        │                              │
                        │         [ UPDATE ]            │ ← THEN CLICK
                        │                              │
                        └──────────────────────────────┘
```

1. In the filter/search box at the top of that panel, type: `youtube.upload`
2. You'll see one result: something with `youtube.upload` and "Manage your YouTube videos"
3. **Check the checkbox** next to it (click the empty box ☐ so it becomes ☑)
4. Scroll down in that panel and click the **"Update"** button

Now click **"Save"** at the bottom of the page.

### Step 6: Add yourself as a test user

Now look at the **left sidebar** again. Click **"Audience"**:

```
┌─────────────────────┐
│ Branding            │
│ Audience            │ ← CLICK THIS
│ Data Access         │
│ ...                 │
└─────────────────────┘
```

On the Audience page, you'll see a section for test users:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Audience                                           │
│                                                      │
│   User type: External                                │
│                                                      │
│   Test users                                         │
│   While publishing status is "Testing", only         │
│   test users can access the app.                     │
│                                                      │
│   [ + ADD USERS ]  ← CLICK THIS                     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

1. Click **"+ Add Users"**
2. A text box appears. Type **your Gmail address** (the one connected to your YouTube channel)
3. Click **"Add"**
4. Click **"Save"**

### Step 7: Finish

You're done with the OAuth consent screen. Everything is set up.

### What you should see now

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   OAuth consent screen                               │
│                                                      │
│   Publishing status: ○ Testing                       │
│   App name: YouTube Uploader                         │
│   User type: External                                │
│                                                      │
│   Test users: your.email@gmail.com                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

The status says "Testing" — this is exactly right. For personal use, you never need to change this.

---

## Part 5: Create Your First Two Keys (Client ID & Client Secret)

Now you'll get 2 of your 3 keys. These are like a username and password for your app.

### Step 1: Go to Credentials

In the left sidebar, click **"APIs & Services"** → then click **"Credentials"**.

Or search for `Credentials` in the top search bar.

### Step 2: Create new credentials

At the top of the page, you'll see a button:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Credentials                                        │
│                                                      │
│   [ + CREATE CREDENTIALS ▾ ]  ← CLICK THIS          │
│                                                      │
│   (empty list — no credentials yet)                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Click **"+ Create Credentials"**. A dropdown menu appears:

```
┌──────────────────────┐
│ API key              │
│ OAuth client ID      │ ← CLICK THIS
│ Service account      │
└──────────────────────┘
```

Click **"OAuth client ID"**.

### Step 3: Fill in the form

You'll see a form with a few fields:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Create OAuth client ID                             │
│                                                      │
│   Application type *                                 │
│   ┌──────────────────────────────────────────┐       │
│   │ -- Select --                        ▾    │       │ ← Click and select
│   └──────────────────────────────────────────┘       │   "Web application"
│                                                      │
└──────────────────────────────────────────────────────┘
```

Click the **"Application type"** dropdown and select **"Web application"**.

More fields will appear:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   Name                                               │
│   ┌──────────────────────────────────────────┐       │
│   │ Web client 1                             │       │ ← Change to:
│   └──────────────────────────────────────────┘       │   "YouTube Uploader Client"
│                                                      │
│   Authorized JavaScript origins                      │
│   (leave this empty — don't add anything here)       │
│                                                      │
│   Authorized redirect URIs                           │
│   [ + ADD URI ]  ← CLICK THIS                       │
│                                                      │
└──────────────────────────────────────────────────────┘
```

1. **Name**: Change it to `YouTube Uploader Client`
2. **Authorized JavaScript origins**: DON'T TOUCH — leave empty
3. **Authorized redirect URIs**: Click **"+ Add URI"**

A text box appears under "Authorized redirect URIs":

```
│   Authorized redirect URIs                           │
│                                                      │
│   URIs 1                                             │
│   ┌──────────────────────────────────────────┐       │
│   │                                          │       │ ← PASTE THIS EXACT URL:
│   └──────────────────────────────────────────┘       │
```

Paste this **exact** URL into that box (copy it carefully — every character matters):

```
https://developers.google.com/oauthplayground
```

**Double-check:** No extra spaces before or after. No missing letters. It must match exactly.

### Step 4: Create it

Click the blue **"Create"** button at the bottom.

### Step 5: Copy your two keys

A popup window appears in the center of your screen showing your two keys:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   OAuth client created                               │
│                                                      │
│   Your Client ID                                     │
│   ┌──────────────────────────────────────────┐ 📋    │
│   │ 123456789-abcdef.apps.googleusercontent… │       │
│   └──────────────────────────────────────────┘       │
│                                                      │
│   Your Client Secret                                 │
│   ┌──────────────────────────────────────────┐ 📋    │
│   │ GOCSPX-AbCdEfGhIjKlMnOpQrSt             │       │
│   └──────────────────────────────────────────┘       │
│                                                      │
│                                    [ OK ]            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**This is important!** Copy each value:

1. Click the **copy icon 📋** next to "Your Client ID" — paste it into your Notes app
   - Label it: `CLIENT ID:`
   - It looks like: `123456789-abcdef.apps.googleusercontent.com`

2. Click the **copy icon 📋** next to "Your Client Secret" — paste it into your Notes app
   - Label it: `CLIENT SECRET:`
   - It looks like: `GOCSPX-AbCdEfGhIjKlMnOpQrSt`

3. Click **"OK"** to close the popup

**Closed it without copying? Don't panic!**
1. You're on the Credentials page
2. Look under "OAuth 2.0 Client IDs" — you'll see "YouTube Uploader Client"
3. Click on it
4. Your Client ID is shown at the top
5. Your Client Secret is shown below it (you might need to click "Show" to reveal it)

### What you should see now

Your Notes app has 2 keys saved:

```
CLIENT ID: 123456789-abcdef.apps.googleusercontent.com
CLIENT SECRET: GOCSPX-AbCdEfGhIjKlMnOpQrSt
```

(Your values will be different — these are just examples.)

---

## Part 6: Get Your Third Key — The Refresh Token

This is the most important step. You'll use a special Google tool called "OAuth Playground" to get your third and final key. This key is what lets your computer upload to YouTube without you having to sign in every time.

### Step 1: Open OAuth Playground

Open a **new browser tab** (keep your Google Cloud Console tab open — you might need it).

Type this address and press Enter:

```
developers.google.com/oauthplayground
```

### What you'll see

The page is split into two halves:

```
┌──────────────────────────────┬───────────────────────────┐
│                              │                           │
│  Step 1                      │   Request / Response      │
│  Select & authorize APIs     │                           │
│                              │   (empty right now)       │
│  ▸ Ad Exchange Buyer API     │                           │
│  ▸ Ad Exchange Seller API    │                           │
│  ▸ Admin SDK API             │                           │
│  ▸ ...                       │                           │
│  ▸ ...                       │                           │
│  ▸ YouTube Analytics API     │                           │
│  ▸ YouTube Data API v3  ←   │                    ⚙️     │
│  ▸ ...                       │              gear icon ↗  │
│                              │                           │
│  [ Authorize APIs ]          │                           │
│                              │                           │
└──────────────────────────────┴───────────────────────────┘
```

The left side has a long list of Google APIs. The right side is empty. There's a **gear icon ⚙️** in the top-right area.

### Step 2: Open settings and use your own credentials

Click the **gear icon ⚙️** in the top-right corner. A settings panel drops down:

```
┌──────────────────────────────────────────┐
│  OAuth 2.0 configuration                │
│                                          │
│  OAuth flow: Server-side                 │
│                                          │
│  ☐ Use your own OAuth credentials        │ ← CHECK THIS BOX
│                                          │
└──────────────────────────────────────────┘
```

**Check the box** that says "Use your own OAuth credentials." Two text boxes appear:

```
┌──────────────────────────────────────────┐
│  OAuth 2.0 configuration                │
│                                          │
│  ☑ Use your own OAuth credentials        │
│                                          │
│  OAuth Client ID                         │
│  ┌──────────────────────────────────┐    │
│  │                                  │    │ ← PASTE your Client ID
│  └──────────────────────────────────┘    │   from Part 5
│                                          │
│  OAuth Client secret                     │
│  ┌──────────────────────────────────┐    │
│  │                                  │    │ ← PASTE your Client Secret
│  └──────────────────────────────────┘    │   from Part 5
│                                          │
│              [ Close ]                   │
│                                          │
└──────────────────────────────────────────┘
```

1. Paste your **Client ID** (from Part 5) into the first box
2. Paste your **Client Secret** (from Part 5) into the second box
3. Click **"Close"** or click anywhere outside the panel to close it

### Step 3: Select the YouTube upload permission

Look at the **left side** of the page. You'll see a long alphabetical list of Google APIs.

**Scroll ALL the way down** — almost to the bottom — until you find **"YouTube Data API v3"**.

```
│  ▸ YouTube Analytics API                 │
│  ▾ YouTube Data API v3  ← CLICK THIS    │
│    TO EXPAND IT                          │
```

Click on **"YouTube Data API v3"** to expand it. You'll see options appear underneath:

```
│  ▾ YouTube Data API v3                                    │
│    ☐ https://www.googleapis.com/auth/youtube              │ ← DO NOT CHECK THIS ONE
│    ☐ https://www.googleapis.com/auth/youtube.upload  ←    │ ← CHECK ONLY THIS ONE
│    ☐ https://www.googleapis.com/auth/youtube.readonly     │ ← DO NOT CHECK THIS ONE
```

**Check ONLY the box** next to the one that ends with `youtube.upload` (the line that contains the word "upload").

⚠️ **Common mistake:** Do NOT check the one that just says `youtube` (without `.upload` at the end). If you check both, you'll get an "Access blocked: Authorization Error" with `invalid_scope`. **Only ONE box should be checked — the `youtube.upload` one.**

### Step 4: Authorize

Click the blue **"Authorize APIs"** button at the bottom of the left panel:

```
│                                          │
│  [ Authorize APIs ]  ← CLICK THIS       │
│                                          │
```

### Step 5: Sign in to your YouTube account

A Google sign-in window pops up (or the page redirects you). 

**Sign in with the same Google account that owns your YouTube channel.**

If you're already signed in, you'll see your account — click on it.

### Step 6: Handle the "unverified app" warning

You'll see a page that looks a bit scary:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   ⚠️ Google hasn't verified this app                  │
│                                                      │
│   This app hasn't been verified by Google yet.        │
│   Only proceed if you know and trust the developer.  │
│                                                      │
│                               [ Back to safety ]     │
│                                                      │
│   Advanced  ← CLICK THIS SMALL TEXT                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

**This is completely normal and safe.** It's YOUR app that YOU just created 5 minutes ago. Google shows this warning for all apps that haven't gone through their review process (which you don't need for personal use).

1. Click **"Advanced"** (small text at the bottom)
2. More text appears. Click **"Go to YouTube Uploader (unsafe)"**

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   ⚠️ Google hasn't verified this app                  │
│                                                      │
│   Advanced ▾                                         │
│                                                      │
│   This app is not yet verified. You should only       │
│   continue if you know and trust the developer.      │
│                                                      │
│   Go to YouTube Uploader (unsafe)  ← CLICK THIS     │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Despite the word "unsafe" — this is perfectly fine. It's YOUR app.

### Step 7: Grant permission

Google asks you to grant permission:

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│   YouTube Uploader wants to access                   │
│   your Google Account                                │
│                                                      │
│   This will allow YouTube Uploader to:               │
│                                                      │
│   ✓ Manage your YouTube videos                       │
│                                                      │
│        [ Cancel ]    [ Continue ]  ← CLICK           │
│                                                      │
└──────────────────────────────────────────────────────┘
```

Click **"Continue"** (or "Allow").

### Step 8: Exchange the code for your token

You'll be sent back to the OAuth Playground. Notice the left side now says **"Step 2"**:

```
┌──────────────────────────────┬───────────────────────────┐
│                              │                           │
│  Step 2                      │   Authorization code:     │
│  Exchange authorization      │   4/0AX4XfW...            │
│  code for tokens             │                           │
│                              │                           │
│  [ Exchange authorization    │                           │
│    code for tokens ]         │                           │
│    ↑↑↑ CLICK THIS ↑↑↑       │                           │
│                              │                           │
└──────────────────────────────┴───────────────────────────┘
```

Click the blue button: **"Exchange authorization code for tokens"**

### Step 9: Copy your Refresh Token

After clicking, the **right side** of the page fills with a response that looks like this:

```
┌───────────────────────────────────────────┐
│                                           │
│  HTTP/1.1 200 OK                          │
│                                           │
│  {                                        │
│    "access_token": "ya29.a0AfH6...",      │ ← IGNORE this one
│    "refresh_token": "1//0eXxYyZz...",     │ ← THIS IS YOUR KEY!
│    "token_type": "Bearer",                │   COPY THIS VALUE
│    "expires_in": 3600                     │
│  }                                        │
│                                           │
└───────────────────────────────────────────┘
```

Find the line that says **`"refresh_token"`**. The value next to it (the long string between the quotes) is your **THIRD AND FINAL KEY**.

**How to copy it:**
1. Find `"refresh_token": "1//0eXxYyZz..."` on the right side
2. The value starts with `1//` followed by a long string of random letters and numbers
3. Carefully select ONLY the value between the quotes (not the quotes themselves)
4. Copy it (Ctrl+C on Windows, Cmd+C on Mac)
5. Paste it into your Notes app and label it: `REFRESH TOKEN:`

**DO NOT copy the `access_token`** — that one expires in 1 hour and is useless to save. You ONLY need the **`refresh_token`**.

### What you should see now

Your Notes app has all 3 keys:

```
CLIENT ID: 123456789-abcdef.apps.googleusercontent.com
CLIENT SECRET: GOCSPX-AbCdEfGhIjKlMnOpQrSt
REFRESH TOKEN: 1//0eAbCdEfGhIjKlMnOpQrStUvWxYz
```

(Your values will look different — these are examples.)

**Congratulations! The hard part is done. You never need to do any of this again.**

---

## Part 7: Add Your Keys to the Video Factory

You're almost done! Now you just need to put these 3 keys into a settings file so the video pipeline can use them.

**If you're using the YT Video Factory pipeline**, ask Claude (or your AI agent) to add these to your `.env` file:

```
YOUTUBE_CLIENT_ID=paste_your_client_id_here
YOUTUBE_CLIENT_SECRET=paste_your_client_secret_here
YOUTUBE_REFRESH_TOKEN=paste_your_refresh_token_here
```

**Replace** `paste_your_..._here` with the actual values you saved.

**Important formatting rules:**
- No quotes around the values
- No spaces before or after the `=` sign
- Each key on its own line

**Example (with fake values):**

```
YOUTUBE_CLIENT_ID=123456789-abcdef.apps.googleusercontent.com
YOUTUBE_CLIENT_SECRET=GOCSPX-AbCdEfGhIjKlMnOpQrSt
YOUTUBE_REFRESH_TOKEN=1//0eAbCdEfGhIjKlMnOpQrStUvWxYz
```

**That's it. Setup is complete. Your computer can now upload videos to YouTube automatically.**

---

## Part 8: Test That It Works

After saving your keys, run this quick test:

```bash
cd yt-video-factory
PYTHONPATH=. python3 -c "
from lib.youtube_client import get_access_token
token = get_access_token()
print('SUCCESS - YouTube connection works!' if token else 'FAILED')
"
```

**If you see "SUCCESS"** — everything is working. The pipeline will now upload videos directly to your YouTube channel as private drafts.

**If you see an error** — double-check that you pasted all 3 keys correctly into the `.env` file. Common mistakes:
- Extra spaces around the `=` sign
- Accidentally copied the quotes from the OAuth Playground
- Used the wrong Google account (different from your YouTube channel)

---

## Frequently Asked Questions

### How many videos can I upload per day?
YouTube gives you a free quota of about **6 uploads per day**. For most people, this is plenty. If you need more, you can request a quota increase from Google (it's free, they usually approve it within a few days).

### Will my videos go live immediately?
**No.** Videos are uploaded as **private drafts**. They appear in your YouTube Studio where you can review the title, description, and thumbnail before making them public. Nothing goes live unless you choose to publish it.

### Is this safe?
Yes. You're using Google's official system — the same one that YouTube's own apps use. Your keys are stored locally on your computer. No third party ever sees them.

### What if I want to stop this completely?
1. Open your browser and go to: `myaccount.google.com/permissions`
2. Look for "YouTube Uploader" in the list of apps
3. Click on it
4. Click **"Remove Access"**
5. Done — the keys stop working instantly. Your YouTube channel is unaffected.

### What if I have multiple YouTube channels?
Each channel needs its own Refresh Token. Repeat Part 6 (the OAuth Playground step) while signed into the other channel's Google account. You'll get a different Refresh Token for each channel.

### Do these keys ever expire?
- **Client ID and Client Secret** — never expire
- **Refresh Token** — never expires UNLESS you manually revoke it (see above) or you don't use it for 6 months

### I messed up somewhere. Can I start over?
Yes! Go to Google Cloud Console → Credentials → delete the OAuth client you created → start again from Part 5. Or delete the entire project and start from Part 2.

---

## Final Checklist

Go through this list to make sure you didn't miss anything:

- [ ] Created a Google Cloud project called "YouTube Uploader"
- [ ] Enabled the "YouTube Data API v3" in the API Library
- [ ] Set up the OAuth consent screen (External, added your Gmail as test user)
- [ ] Created an OAuth Client ID with type "Web application"
- [ ] Added the redirect URI: `https://developers.google.com/oauthplayground`
- [ ] Copied the **Client ID** from the popup
- [ ] Copied the **Client Secret** from the popup
- [ ] Went to `developers.google.com/oauthplayground`
- [ ] Clicked the gear icon and checked "Use your own OAuth credentials"
- [ ] Pasted Client ID and Client Secret into the settings
- [ ] Found and expanded "YouTube Data API v3" in the left panel
- [ ] Checked the box next to `youtube.upload`
- [ ] Clicked "Authorize APIs"
- [ ] Signed in and granted permission (clicked through the "unverified" warning)
- [ ] Clicked "Exchange authorization code for tokens"
- [ ] Copied the **Refresh Token** from the response
- [ ] Added all 3 keys to the `.env` file
- [ ] Ran the test command and saw "SUCCESS"

**You're done! Enjoy automated YouTube uploads.**
