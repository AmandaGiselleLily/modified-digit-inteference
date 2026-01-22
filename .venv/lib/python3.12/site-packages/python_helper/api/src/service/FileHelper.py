from python_helper.api.src.domain import FileOperation
from python_helper.api.src.service import LogHelper


def getFileLines(filePath: str, operation: str = FileOperation.READ_TEXT, encoding: str = FileOperation.UTF_8):
    lines = []
    try:
        with open(filePath, operation, encoding=encoding) as readder :
            lines = readder.readlines()
    except Exception as exception:
        LogHelper.failure(getFileLines, f'Not possible to operate "{operation}" over the "{filePath}" file lines', exception, muteStackTrace=True)
        raise exception
    return lines


def writeContent(filePath: str, content, operation: str = FileOperation.WRITE_TEXT, encoding: str = FileOperation.UTF_8):
    try:
        with open(filePath, operation, encoding=encoding) as writter:
            writter.write(content)
    except Exception as exception:
        LogHelper.failure(overrideFileLines, f'Not possible to operate "{operation}" over the "{filePath}" file content', exception, muteStackTrace=True)
        raise exception


def writeFileLines(filePath: str, lines: list, operation: str = FileOperation.WRITE_TEXT, encoding: str = FileOperation.UTF_8):
    try:
        with open(filePath, operation, encoding=encoding) as writter:
            writter.writelines(lines)
    except Exception as exception:
        LogHelper.failure(writeFileLines, f'Not possible to operate "{operation}" over the "{filePath}" file lines', exception, muteStackTrace=True)
        raise exception


def overrideContent(filePath: str, content, encoding: str = FileOperation.UTF_8, **kwargs):
    return writeContent(filePath, content, operation = FileOperation.OVERRIDE_TEXT, encoding = encoding)


def overrideFileLines(filePath: str, lines: list, encoding: str = FileOperation.UTF_8, **kwargs):
    return writeFileLines(filePath, lines, operation = FileOperation.OVERRIDE_TEXT, encoding = encoding)
