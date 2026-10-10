# Soul

Soul — проект форка официальных клиентов Telegram для Android, Windows, Linux и macOS.

## Первая версия

- Основа: официальные исходники Telegram Android и Telegram Desktop.
- Название приложения: Soul.
- Единственная новая функция: проверка и установка новых версий Soul, опубликованных в GitHub Releases.

## Структура

- `patches/android.patch` — изменения для [Telegram Android](https://github.com/DrKLO/Telegram).
- `patches/desktop.patch` — изменения для [Telegram Desktop](https://github.com/telegramdesktop/tdesktop).
- `scripts/bootstrap.sh` — загрузка закреплённых версий исходников и применение патчей.
- `android/` и `desktop/` создаются локально и не хранятся в этом репозитории.

## Получение исходников

```bash
bash scripts/bootstrap.sh
```

Для загрузки нужен доступ к `github.com`. Скрипт проверяет версии исходников и
не перезаписывает существующие каталоги с другой версией. Повторный запуск
после применения патчей безопасен. Подмодули исходных проектов могут занимать
несколько гигабайт.

## Текущее состояние

- Код Android и Desktop настроен на проверку новых версий Soul в GitHub Releases.
  Desktop использует отдельные ключи подписи обновлений.
- Генераторы манифеста Android и ленты Desktop находятся в `scripts/`.
- Полная сборка и установка обновления ещё не проверены: на текущей машине нет
  Android SDK и зависимостей для CMake Desktop.
- Для выпуска нужны собственные Telegram API ID и API hash и конфигурация
  Google Services для Android package ID `com.molexalex.soul` либо адаптация
  сборки без Google Services.

Обновления по умолчанию берутся из `MolexAlex/Soul`. Android-сборка принимает другой адрес манифеста через
параметр Gradle `-PSOUL_UPDATE_MANIFEST_URL=https://github.com/OWNER/Soul/releases/latest/download/android-update.json`.

Для Android-релиза приложите APK и манифест с именем `android-update.json` к
одному выпуску GitHub Releases. Создать манифест можно командой:

```bash
python3 scripts/make-android-update.py --repository MolexAlex/Soul --tag v1.0.0 \
  --version 12.10.6 --version-code 71129 --apk Soul-android.apk
```

Android сверяет SHA-256, идентификатор пакета и код версии APK перед передачей
файла системному установщику. Сборка Soul использует свой постоянный Android
ключ вместо тестового ключа Telegram. На новой машине создайте его командой
`python3 scripts/create-android-key.py`; путь к файлу свойств можно изменить
через `SOUL_ANDROID_SIGNING_PROPERTIES`. Рабочий ключ на машине автора лежит в
`~/.local/share/Soul/signing` и не публикуется. Сделайте его резервную копию:
без этого ключа уже установленные APK Soul нельзя будет обновить. Отдельный
идентификатор пакета `com.molexalex.soul` уже задан для standalone-сборки;
поменять его можно Gradle-параметром `SOUL_APP_PACKAGE`. Замените
`android/TMessagesProj_AppStandalone/google-services.json` конфигурацией
Firebase для этого package ID. Для входа в Telegram передайте свои
`SOUL_API_ID` и `SOUL_API_HASH` через Gradle-свойства, например переменные
`ORG_GRADLE_PROJECT_SOUL_API_ID` и `ORG_GRADLE_PROJECT_SOUL_API_HASH`.
Пример кода версии выше относится к текущей сборке `afatStandalone`;
для релиза он должен совпадать с фактическим `versionCode` APK.

Desktop использует собственные ключи обновлений Soul. Публичный ключ и
подписанный манифест применяются из `patches/desktop.patch`; приватные ключи
не входят в репозиторий. Рабочие ключи на машине автора находятся в
`~/.local/share/Soul/signing`. Сделайте их резервную копию до публикации
первого релиза. Для сборки Desktop адрес
репозитория задаётся CMake-параметром `SOUL_RELEASE_REPOSITORY`.

Для каждого Desktop-релиза нужно собрать и подписать пакеты `td-update-*`
штатным Packer из Telegram Desktop. Для отдельной упаковки уже собранных файлов
есть `scripts/pack-desktop-update.py`; он использует ключ
`~/.local/share/Soul/signing/release-private.pem` или переменную
`SOUL_RELEASE_KEY`. Пример для Linux:

```bash
python3 scripts/pack-desktop-update.py --packer /path/to/Packer \
  --target linux --version 7003002 \
  --file /path/to/Telegram --file /path/to/Updater
```

Затем создайте файлы `current2` и `current6`:

```bash
python3 scripts/make-desktop-feed.py --version 7003002 \
  --asset linux=td-update-linux-x64-7003002 \
  --output-dir release-assets
```

Пакеты и оба файла `current*` прикрепляются к одному выпуску GitHub Releases.
Числовая версия должна совпадать с `AppVersion` в исходниках Desktop.
Релизные скрипты Telegram Desktop требуют его внутренние серверы и средства
подписи приложения; для Soul пакеты можно готовить отдельно через указанный
скрипт. Ключи Soul пока существуют только на этой машине, поэтому сохраните
их резервную копию до публикации первого релиза.
