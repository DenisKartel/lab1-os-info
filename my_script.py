#!/usr/bin/env python3
"""
Лабораторная работа 1
Скрипт определяет ОС, собирает параметры текущей системы
и сохраняет результат в JSON-файл.
Используются только стандартные модули Python.
"""

import json
import os
import platform
import socket
import sys
from datetime import datetime, timezone


def detect_os() -> str:
    """Определяет семейство операционной системы."""
    system = platform.system()
    if system == "Linux":
        return "Linux"
    if system == "Darwin":
        return "macOS"
    if system == "Windows":
        return "Windows"
    return f"Other ({system})"


def _get_username() -> str:
    """Безопасно получает имя текущего пользователя."""
    # os.getlogin() может падать в неинтерактивных сессиях / контейнерах
    try:
        return os.getlogin()
    except (OSError, AttributeError):
        pass
    for key in ("USER", "USERNAME", "LOGNAME"):
        value = os.environ.get(key)
        if value:
            return value
    return "unknown"


def collect_system_info() -> dict:
    """
    Собирает параметры текущей ОС.
    Источники данных — только стандартные модули:
    platform, os, sys, socket, datetime.
    """
    os_family = detect_os()

    info = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "os": {
            "family": os_family,
            "system": platform.system(),          # Linux / Darwin / Windows
            "release": platform.release(),        # версия ядра / номер сборки
            "version": platform.version(),        # подробная строка версии
            "platform": platform.platform(),      # полная строка платформы
            "machine": platform.machine(),        # архитектура (x86_64, arm64, ...)
            "processor": platform.processor() or "unknown",
            "architecture": platform.architecture(),  # (bits, linkage)
        },
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler(),
            "build": platform.python_build(),
            "executable": sys.executable,
            "path": sys.path[:5],  # первые 5 путей (чтобы не раздувать файл)
        },
        "runtime": {
            "hostname": socket.gethostname(),
            "username": _get_username(),
            "cwd": os.getcwd(),
            "pid": os.getpid(),
            "cpu_count_logical": os.cpu_count(),
            "env_path_separator": os.pathsep,
            "line_separator": repr(os.linesep),
        },
        "paths": {
            "home": os.path.expanduser("~"),
            "temp": os.environ.get("TEMP") or os.environ.get("TMP") or os.environ.get("TMPDIR") or "/tmp",
        },
    }

    # Дополнительная информация, зависящая от ОС (через platform / os, без утилит)
    if os_family == "Linux":
        info["os"]["libc"] = platform.libc_ver()
        # Читаем /etc/os-release, если доступен (это файл, а не утилита)
        os_release = {}
        try:
            with open("/etc/os-release", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if "=" in line and not line.startswith("#"):
                        key, _, value = line.partition("=")
                        os_release[key] = value.strip('"')
            if os_release:
                info["os"]["distro"] = {
                    "name": os_release.get("NAME"),
                    "version": os_release.get("VERSION"),
                    "id": os_release.get("ID"),
                    "pretty_name": os_release.get("PRETTY_NAME"),
                }
        except (FileNotFoundError, PermissionError, OSError):
            info["os"]["distro"] = None

    elif os_family == "macOS":
        info["os"]["mac_ver"] = platform.mac_ver()

    elif os_family == "Windows":
        info["os"]["win32_ver"] = platform.win32_ver()
        info["os"]["win32_edition"] = platform.win32_edition() if hasattr(platform, "win32_edition") else None

    return info


def save_to_json(data: dict, filename: str = "system_info.json") -> str:
    """Записывает словарь в JSON-файл с отступами."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    return os.path.abspath(filename)


def main() -> None:
    print("Определение операционной системы и сбор параметров...")
    data = collect_system_info()

    print(f"Обнаружена ОС: {data['os']['family']} ({data['os']['platform']})")
    print(f"Архитектура:   {data['os']['machine']}")
    print(f"Python:        {data['python']['version']} ({data['python']['implementation']})")

    output_path = save_to_json(data)
    print(f"\nРезультат сохранён в файл:\n{output_path}")


if __name__ == "__main__":
    main()
