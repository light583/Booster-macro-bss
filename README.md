© 2026 [light583]. All Rights Reserved.


# Booster Macro v1.0 (macOS)

Lightweight automation tool for Bee Swarm Simulator on macOS. Automates Stinger and Jelly Bean upkeeps alongside Scorching Star activation detection using pixel buffer monitoring.

---

## Prerequisites

* macOS (Apple Silicon or Intel)
* Python 3.9+
* IDLE, VS Code, or Terminal

---

## Setup & Installation

### 1. Clone the repository

```bash
git clone [https://github.com/YourUsername/your-repo-name.git](https://github.com/YourUsername/your-repo-name.git)
cd your-repo-name
```

### 2. Install dependencies

Run this command in Terminal to install the required computer vision and input libraries:

```bash
pip3 install mss opencv-python numpy pynput
```

*(Note: If you encounter an `externally-managed-environment` error on newer macOS versions, run:)*
```bash
pip3 install mss opencv-python numpy pynput --break-system-packages
```

---

## macOS Permissions (Required)

macOS requires explicit permissions for keyboard simulation and screen reading.

1. Open **System Settings** > **Privacy & Security**.
2. Under **Accessibility**: Enable **IDLE** (or **Terminal** / **VS Code**, depending on what you run the script from).
3. Under **Screen Recording**: Enable the same application.
4. Restart IDLE, your editor, or Terminal after enabling permissions.

---

## In-Game Configuration

* Set Roblox to **maximized** or **full-screen**.
* Hotbar slots:
  * **Slot 1**: Jelly Beans (spammed every start of scorch)
  * **Slot 2**: Stingers (spammed every ~10s)
  * **Slot 3**: Clouds (fired alongside Jelly Beans during Scorch activation)
  * **5th Ability Slot**: Scorching Star passive icon

---

## How to Run

1. Open `macro.py` in **IDLE**.
2. Ensure `Scorch.png` remains in the exact same directory as `macro.py`.
3. Press **F5** (or click **Run > Run Module**).
4. Make sure Roblox is visible on your screen and Scorching Star is **off cooldown**.
5. Press `Cmd + Shift + M` anywhere to toggle the macro on/off.

---

## Troubleshooting & Support

* **File Error on Startup:** Ensure `Scorch.png` was not renamed or moved out of the repo folder.
* **Keystrokes Not Registering:** Double-check that Accessibility permissions are enabled for your IDE/Terminal.
* **Bug Reports:** Contact Discord `@light_0912`.
