# Лабораторная работа 1 — Сбор параметров ОС

## Описание

Скрипт `my_script.py` определяет операционную систему, на которой он запущен (Linux / macOS / Windows), собирает набор параметров текущей системы и сохраняет результат в файл `system_info.json`.

Скрипт написан с использованием **только стандартных модулей Python** (`platform`, `os`, `sys`, `socket`, `json`, `datetime`).  
Внешние модули и вызов стандартных утилит ОС (`uname`, `systeminfo`, `sw_vers` и т.п.) **не используются**.

## Запуск

```bash
python my_script.py
# или
python3 my_script.py
```

После выполнения в текущей директории появится файл `system_info.json`.

## Собираемые параметры

### 1. Общие
| Параметр | Описание | Источник |
|----------|----------|----------|
| `timestamp_utc` | Время сбора данных (UTC) | `datetime` |

### 2. Операционная система (`os`)
| Параметр | Описание | Источник |
|----------|----------|----------|
| `family` | Семейство ОС (Linux / macOS / Windows) | `platform.system()` + нормализация |
| `system` | Сырое имя системы | `platform.system()` |
| `release` | Версия ядра / номер сборки | `platform.release()` |
| `version` | Подробная строка версии | `platform.version()` |
| `platform` | Полная строка платформы | `platform.platform()` |
| `machine` | Архитектура процессора (x86_64, arm64, …) | `platform.machine()` |
| `processor` | Описание процессора | `platform.processor()` |
| `architecture` | (разрядность, тип связывания) | `platform.architecture()` |
| `distro` (только Linux) | Название, версия, ID дистрибутива | чтение `/etc/os-release` |
| `mac_ver` (только macOS) | Версия macOS | `platform.mac_ver()` |
| `win32_ver` / `win32_edition` (только Windows) | Версия и редакция Windows | `platform.win32_ver()`, `platform.win32_edition()` |
| `libc` (только Linux) | Версия libc | `platform.libc_ver()` |

### 3. Python (`python`)
| Параметр | Описание | Источник |
|----------|----------|----------|
| `version` | Версия интерпретатора | `platform.python_version()` |
| `implementation` | CPython / PyPy / … | `platform.python_implementation()` |
| `compiler` | Компилятор, которым собран Python | `platform.python_compiler()` |
| `build` | Информация о сборке | `platform.python_build()` |
| `executable` | Путь к интерпретатору | `sys.executable` |
| `path` | Первые 5 элементов `sys.path` | `sys.path` |

### 4. Среда выполнения (`runtime`)
| Параметр | Описание | Источник |
|----------|----------|----------|
| `hostname` | Имя хоста | `socket.gethostname()` |
| `username` | Имя текущего пользователя | `os.getlogin()` / переменные окружения |
| `cwd` | Текущая рабочая директория | `os.getcwd()` |
| `pid` | PID процесса | `os.getpid()` |
| `cpu_count_logical` | Количество логических ядер | `os.cpu_count()` |
| `env_path_separator` | Разделитель путей (`:` или `;`) | `os.pathsep` |
| `line_separator` | Разделитель строк | `os.linesep` |

### 5. Пути (`paths`)
| Параметр | Описание | Источник |
|----------|----------|----------|
| `home` | Домашняя директория пользователя | `os.path.expanduser("~")` |
| `temp` | Временная директория | переменные окружения `TEMP`/`TMP`/`TMPDIR` |

## Структура JSON (пример)

```json
{
  "timestamp_utc": "2026-10-15T19:50:00.123456+00:00",
  "os": {
    "family": "Linux",
    "system": "Linux",
    "release": "6.8.0-...",
    "version": "#1 SMP ...",
    "platform": "Linux-6.8.0-...-x86_64-with-glibc2.39",
    "machine": "x86_64",
    "processor": "x86_64",
    "architecture": ["64bit", "ELF"],
    "libc": ["glibc", "2.39"],
    "distro": {
      "name": "Ubuntu",
      "version": "24.04.1 LTS (Noble Numbat)",
      "id": "ubuntu",
      "pretty_name": "Ubuntu 24.04.1 LTS"
    }
  },
  "python": { ... },
  "runtime": { ... },
  "paths": { ... }
}
```

## Обоснование выбора модулей

Все используемые модули входят в **стандартную библиотеку Python**:
- `platform` — основной источник кроссплатформенной информации об ОС и Python;
- `os` — работа с путями, окружением, PID, количеством CPU;
- `sys` — информация об интерпретаторе;
- `socket` — получение имени хоста;
- `json` — сериализация результата;
- `datetime` — метка времени.

Внешние библиотеки (например, `psutil`) не применялись, чтобы соблюсти ограничение лабораторной работы.  
Чтение файла `/etc/os-release` на Linux — это прямой доступ к файлу, а не вызов утилиты ОС.

## Требования

- Python 3.6+
- Права на чтение `/etc/os-release` (Linux) — желательны, но не обязательны.

## Автор

Лабораторная работа выполнена в рамках учебного задания.
