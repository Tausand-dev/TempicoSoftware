# ============================================================
# STAGE 1: base — Python 3.12 + Qt6 system dependencies
# ============================================================
FROM python:3.9-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN pip install --upgrade pip

# Qt6/PyQt6 runtime dependencies (xcb platform plugin requirements)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libfontconfig1 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libegl1 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxcb-shape0 \
    libxcb-icccm4 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-image0 \
    libgssapi-krb5-2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
ENV PYTHONPATH=/app/src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

# ============================================================
# STAGE 2: dev — GUI development with X11 forwarding
# ============================================================
FROM base AS dev

ENV DISPLAY=:0
ENV QT_QPA_PLATFORM=xcb

CMD ["python", "-m", "main"]

# ============================================================
# STAGE 3: test — Headless testing with Xvfb
# ============================================================
FROM base AS test

RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    "pytest>=7.0" \
    "pytest-qt>=4.2"

ENV QT_QPA_PLATFORM=xcb

COPY tests/ ./tests/

CMD ["xvfb-run", "--auto-servernum", \
     "--server-args=-screen 0 1920x1080x24", \
     "pytest", "tests/", "-v"]

# ============================================================
# STAGE 4: build — PyInstaller Linux binary
# ============================================================
FROM base AS build

RUN apt-get update && apt-get install -y --no-install-recommends \
    binutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "pyinstaller>=6.0"

CMD ["pyinstaller", "src/main.py", \
     "--name", "SignalViewer", \
     "--onefile", "--windowed", \
     "--distpath", "/app/dist"]
