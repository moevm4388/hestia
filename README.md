<div align = center>
    
# hestia

Система компьютерной алгебры

&ensp;[<kbd> <br> Веб-интерфейс <br> </kbd>](https://moevm4388.github.io/hestia/web/overview)&ensp;
&ensp;[<kbd> <br> CLI <br> </kbd>](https://moevm4388.github.io/hestia/cli/overview)&ensp;

</div>

## Установка

### pip

> [!note]
> Если вы используете Linux, `pip` не позволит установить пакет без
> виртуального окружения. Используйте
> [`pipx`](https://repology.org/project/pipx/versions).

1.  Установите пакет при помощи `pip`:
    ```sh
    pip install git+https://github.com/moevm4388/hestia.git
    ```
2.  Запустите Hestia командой:
    ```
    hestia --help
    ```

### AppImage

> [!note]
> Для запуска исполняемый файлов в формате AppImage необходимо наличие библиотеки `libfuse2` (на многих системах она установлена по умолчанию).

1.  Скачайте [`hestia-x86_64.AppImage`](https://github.com/moevm4388/hestia/releases/latest/download/hestia-x86_64.AppImage).
2.  Установите файл командой ниже (укажите путь до скачанного файла):
    ```sh
    sudo install -m 755 /путь/до/hestia-x86_64.AppImage /usr/local/bin/hestia
    ```
3.  Запустите:
    ```sh
    hestia --help
    ```

### Docker

Вы можете запустить Hestia, используя [Docker](https://www.docker.com/) или [Podman](https://podman.io/).

1.  Скачайте образ:
    ```sh
    docker pull ghcr.io/moevm4388/hestia:latest
    ```
2. Запустите контейнер:
   ```sh
   docker run ghcr.io/moevm4388/hestia:latest --help
   ```

## Использование

Общий синтаксис команды:

```sh
hestia --function <NAME> --args <ARGS>
```

Где:
- `<NAME>` — Вызываемая функция. Можно передать как название (например, `ADD_NN_N`), так и номер (`N-4`).
- `<ARGS>` — Аргументы, передаваемые в функцию, указанные через пробел.

Ниже приведены примеры команд.

```sh
hestia --function ADD_NN_N --args 99999999999999999999999999999999 1
```

```
hestia --function P-1 --args "4 1 3" "1 2"
```

> [!note]
> Многочлены передаются в виде коэффициентов канонической формы, начиная со свободного члена.
>
> Например, запись
> 
> ```
> 1 0 1 2 3
> ```
>
> Считывается как
>
> ```
> 3x⁴ + 2x³ + x² + 1
> ```

## О проекте

Подробную информацию о проекте, его архитектуре и проч. можно узнать в разделе [Wiki](https://github.com/moevm4388/hestia/wiki).
