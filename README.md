
# 🔒 Focus Lock

**A free Windows app that keeps you inside your online class until your timer ends.**
**অনলাইন ক্লাসে মনোযোগ ধরে রাখার একটি ফ্রি Windows প্রোগ্রাম, যা টাইমার শেষ না হওয়া পর্যন্ত তোমাকে ক্লাসেই আটকে রাখে।**


---

<a id="-english"></a>
# 🇬🇧 English

## 📖 Table of contents
1. [The problem](#1-the-problem)
2. [The solution](#2-the-solution)
3. [Features](#3-features)
4. [Download and install](#4-download-and-install)
5. [How to use (step by step)](#5-how-to-use-step-by-step)
6. [Settings explained](#6-settings-explained)
7. [What happens during a lock](#7-what-happens-during-a-lock)
8. [FAQ and troubleshooting](#8-faq-and-troubleshooting)
9. [Privacy and safety](#9-privacy-and-safety)
10. [Limitations (honest list)](#10-limitations-honest-list)
11. [Build the .exe yourself](#11-build-the-exe-yourself)
12. [How it works (technical)](#12-how-it-works-technical)
13. [Contributing, license and contact](#13-contributing-license-and-contact)

## 1. The problem
When you study online, it is easy to lose focus. In the middle of a class your mind says:

> "Just 5 minutes on Instagram."

Those 5 minutes quietly become an hour. The live class is missed, recorded lectures pile up, and by night you feel bad about it. Willpower alone often isn't enough, because the distraction is only one click away.

## 2. The solution
**Focus Lock** adds a little friction between you and distractions. You choose:

- the **class app** you must stay in (for example, your learning app),
- any **other apps** that are still allowed (for example, WhatsApp),
- a **time** (for example, 45 minutes).

When you press **START LOCK**, any app that isn't allowed is minimized the moment it appears, and your class app is brought straight back to the front. When the timer ends, everything returns to normal.

### 📸 Screenshots

| Setup screen | While locked (timer in the top-right corner) |
|---|---|
| ![Focus Lock setup screen](<img width="400" height="598" alt="setup" src="https://github.com/user-attachments/assets/81752071-983c-4768-94d1-5cacf5fc30da" />


) | ![Focus Lock running with a class app in front](<img width="1715" height="1070" alt="locked" src="https://github.com/user-attachments/assets/2debcfd1-72e8-48f5-8836-f968b4921556" />
) |

## 3. Features
- ⏱️ **Countdown timer** from 1 to 600 minutes, shown in a small always-on-top window.
- 🎯 **Class app stays in front.** If you switch away, it comes back within a fraction of a second.
- ✅ **Allowed apps list.** Keep important apps such as WhatsApp usable.
- 🚫 **Blocked words.** Block any window whose title contains words like `instagram` or `youtube`. This is very useful if your class runs inside a web browser.
- 🔁 **Auto-reopen.** If you close the class app, Focus Lock launches it again.
- 🛑 **Protected timer window.** You can't close it while the lock is running.
- 🧠 **Emergency stop with friction.** To quit early you must type a random 40-character text exactly. This gives you a moment to think before giving up.
- 💾 **Remembers your settings** for next time.
- 🪶 **Lightweight, offline, no account, no ads.**

## 4. Download and install

### Option A: ready-made `.exe` (easiest, no Python needed)
1. Go to the **[Releases](../../releases)** page of this repository.
2. Download **`FocusLock.zip`**.
3. Right-click the zip → **Extract All**.
4. Double-click **`FocusLock.exe`**.

> ⚠️ **"Windows protected your PC" warning?** This is normal for new, unsigned programs. Click **More info → Run anyway**. See the [FAQ](#8-faq-and-troubleshooting) for details.

### Option B: run from source (needs Python)
1. Install [Python 3.8 or newer](https://www.python.org/downloads/) and **tick "Add Python to PATH"** during installation.
2. Download these files into one folder: `focus_lock.py`, `START_FocusLock.bat`.
3. Double-click **`START_FocusLock.bat`**.

(Or open a terminal in the folder and run `python focus_lock.py`.)

**Requirements:** Windows 10 or 11. No extra Python packages are needed, because the app only uses Python's built-in libraries.

## 5. How to use (step by step)
1. **Open your class app first** (and WhatsApp, or anything else you want to allow).
2. Open **Focus Lock**.
3. Click **Refresh app list**. All your currently open apps appear.
4. In box **1**, choose your **class app**.
5. In box **2**, tick the **other apps** you still want to allow (Ctrl + click to select several). Your class app is always allowed automatically.
6. *(Optional)* Edit the **blocked words** and **allowed words** (see [Settings explained](#6-settings-explained)).
7. Set the **minutes**.
8. Press **START LOCK**. A small timer appears in the top-right corner. Now study! 📚
9. When the timer reaches zero, you'll see a "Time is up" message and you're free.

> 💡 **Tip:** Do a quick **2-minute test lock** the first time, to make sure your apps behave the way you expect.

## 6. Settings explained

| Setting | What it does | Example |
|---|---|---|
| **Class app** | The app that is forced to stay in front, and reopened if closed. | `acs.exe` |
| **Other apps allowed** | Apps you can still switch to during the lock. | `whatsapp.exe` |
| **Always block (title words)** | Any window whose title contains one of these words is minimized, *even if its app is allowed*. Separate words with commas. Default: `instagram, facebook, youtube, tiktok` | `instagram, reddit` |
| **Also allow (title words)** | Any window whose title contains one of these words is allowed. Handy for Microsoft Store apps. Default: `whatsapp` | `whatsapp, calculator` |
| **Minutes** | How long the lock lasts. | `45` |

**Important:** *blocked words win over allowed ones.* If a window matches a blocked word, it is minimized no matter what.

### Using Focus Lock when your class runs in a web browser
If your classes open in Chrome, Edge or Firefox, allowing the browser would also allow Instagram in the same browser. To handle this:
1. Allow the browser.
2. Keep sites you want to avoid in the **Always block** words (`instagram`, `facebook`, `youtube`, `tiktok`, and so on).

Browser tab titles contain the site name, so those windows get minimized. This works well but isn't perfect, because a tab title can occasionally hide the site name.

## 7. What happens during a lock

| You do this | Focus Lock does this |
|---|---|
| Switch to a non-allowed app | Minimizes it and brings the class app back (about 0.3 seconds) |
| Press the Windows key, Alt + Tab, or click the taskbar | Pulls focus back to the class app |
| Close the class app | Reopens it (checked every few seconds) |
| Try to close the timer window | Nothing (it beeps) |
| Click **Emergency stop** | Asks you to type a random 40-character text |
| Timer reaches 00:00:00 | Unlocks and shows "Time is up" |

## 8. FAQ and troubleshooting

**Why does Windows show a blue "SmartScreen" warning?**
Windows warns about programs that are new and don't have a paid code-signing certificate. It does **not** mean the program is harmful. Click **More info → Run anyway**. The full source code is in this repository so you can read it yourself.

**My antivirus flags the `.exe`. Is it a virus?**
Some antivirus tools wrongly flag any program built with PyInstaller. You can read `focus_lock.py` (it's short) and confirm it only watches which window is in front. If you prefer, run it from source using Option B.

**My class app isn't in the list.**
Open the class app first, then click **Refresh app list**.

**WhatsApp (Microsoft Store version) gets minimized.**
Store apps run through a shared host called `ApplicationFrameHost.exe`. Add `whatsapp` to the **Also allow (title words)** box.

**My class app is a Microsoft Store app and doesn't reopen when I close it.**
Auto-reopen doesn't work for apps hosted by `ApplicationFrameHost.exe`. The app is still forced to the front when it is open.

**I can't take a screenshot during a lock.**
The Snipping Tool counts as "another app". Use **Windows key + PrtScn**, which saves a screenshot to *Pictures → Screenshots* without opening any window. Or allow `SnippingTool.exe` / `ScreenClippingHost.exe` in the allowed list.

**The timer window is in the way.**
It sits at the top-right corner. You can drag it elsewhere while the lock is running.

**I need to stop in an emergency.**
Use **Emergency stop** and type the shown text. If something goes seriously wrong, you can also end the program from Task Manager. (See [Limitations](#10-limitations-honest-list).)

**Where are my settings stored?**
In a small file at `C:\Users\<your name>\.focus_lock.json`. Delete it to reset everything.

**Does it work on Mac, Linux, Android or iPhone?**
No. It is Windows only.

## 9. Privacy and safety
- ✅ **Works fully offline.** The app never connects to the internet.
- ✅ **Collects no data.** No analytics, no accounts, no ads.
- ✅ **Only reads window information:** which window is in front, its title, and the name of its program. This is used only to decide whether to minimize it.
- ✅ **Open source.** Read every line in `focus_lock.py`.
- ✅ Saves only your own settings in a local file (see above).

## 10. Limitations (honest list)
- It's a **self-discipline helper, not a security lock.** You can still end it through Task Manager or by restarting your computer. The goal is to add enough friction to get past the "just 5 minutes" urge.
- It can't control your **phone**. If your phone is your main distraction, use its built-in focus mode too.
- A very quick window flash may be visible before it is minimized, because the check runs about three times a second.
- Windows only (Windows 10/11).
- Title-word blocking depends on what the window title shows.

## 11. Build the `.exe` yourself
1. Install Python (tick **Add Python to PATH**).
2. Put `focus_lock.py` and `MAKE_EXE.bat` in one folder.
3. Double-click **`MAKE_EXE.bat`**.
4. Your program appears at `dist\FocusLock.exe`.

(Manual command: `pip install pyinstaller` then `pyinstaller --onefile --noconsole --name FocusLock focus_lock.py`.)

## 12. How it works (technical)
- Built with **Python** and **Tkinter** (the window), plus **ctypes** to call the Windows API. There are no third-party dependencies.
- A loop runs about every 300 ms and reads the foreground window (`GetForegroundWindow`), its process (`QueryFullProcessImageNameW`), its title and its class name.
- If the window is blocked or not on the allowed list, it is minimized (`ShowWindow`) and the class app is brought forward (`SetForegroundWindow`, with a brief Alt key tap so Windows allows the focus change).
- Windows shell pieces (taskbar, Start menu, Alt + Tab view) are not minimized. Focus is simply pulled back to the class app.
- Every few seconds it checks that the class app still has a window, and relaunches it from its saved path if not.

## 13. Contributing, license and contact
- 🐞 Found a bug or have an idea? Open an **[Issue](../../issues)**.
- 🔧 Pull requests are welcome.
- 📄 **License:** MIT. Free to use, share and modify.
- 📩 **Contact / get the app:** WhatsApp **[+880 1848-670737](https://wa.me/8801848670737)**: message me for help, feedback or a copy of the app.

⭐ If this helped you focus, please star the repository and share it with a friend who studies online!

---

