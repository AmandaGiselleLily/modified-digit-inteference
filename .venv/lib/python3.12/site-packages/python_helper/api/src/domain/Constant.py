from python_helper.api.src.domain import FileOperation

LOG =       '[LOG    ] '
INFO =      '[INFO   ] '
STATUS =    '[STATUS ] '
SUCCESS =   '[SUCCESS] '
SETTING =   '[SETTING] '
DEBUG =     '[DEBUG  ] '
WARNING =   '[WARNING] '
FAILURE =   '[FAILURE] '
WRAPPER =   '[WRAPPER] '
ERROR =     '[ERROR  ] '
TEST =      '[TEST   ] '

BACK_SLASH = '\\'
NEW_LINE = '\n'
BAR_N = f'{BACK_SLASH}n'
NOTHING = ''
BLANK = ''
SPACE = ' '
SINGLE_QUOTE = "'"
DOUBLE_QUOTE = '"'
TRIPLE_SINGLE_QUOTE = f"{3*SINGLE_QUOTE}"
TRIPLE_DOUBLE_QUOTE = f'{3*DOUBLE_QUOTE}'

PIPE = '|'
BACK_SLASH_SINGLE_QUOTE = "\'"
BACK_SLASH_DOUBLE_QUOTE = '\"'
SLASH = '/'
FOWARD_SLASH = '/'
DOUBLE_SLASH = f'{2*FOWARD_SLASH}'
HASH_TAG = '#'
DASH = '-'
SPACE_DASH_SPACE = f'{SPACE}{DASH}{SPACE}'
UNDERSCORE = '_'
DOUBLE_UNDERSCORE = f'{2 * UNDERSCORE}'
DOLLAR = '$'
ARROBA = '@'
AND = '&'
PLUS = '+'
EQUALS = '='
PERCENT = '%'
ASTERISK = '*'

DOT = '.'
DOT_SPACE = f'{DOT}{SPACE}'
COMA = ','
COMA_SPACE = f'{COMA}{SPACE}'
COLON = ':'
COLON_SPACE = f'{COLON}{SPACE}'
SPACE_COLON_SPACE = f'{SPACE}{COLON}{SPACE}'
SEMI_COLON = ';'
SEMI_COLON_SPACE = f'{SEMI_COLON}{SPACE}'
QUESTION_MARK = '?'
QUESTION_MARK_SPACE = f'{QUESTION_MARK}{SPACE}'
EXCLAMATION_MARK = '!'
EXCLAMATION_MARK_SPACE = f'{EXCLAMATION_MARK}{SPACE}'

LOG_CAUSE = f'Cause{COLON_SPACE}'
DOT_SPACE_CAUSE = f'{DOT_SPACE}{LOG_CAUSE}'

TAB_UNITS = 4
TAB = TAB_UNITS * SPACE
SYSTEM_TAB = '\t'

NONE = 'None'

TRUE = 'True'
FALSE = 'False'

BOOLEAN = 'bool'
STRING = 'str'
INTEGER = 'int'
TUPLE = 'tuple'
LIST = 'list'
DICT = 'dict'

OPEN_TUPLE = '('
CLOSE_TUPLE = ')'
OPEN_LIST = '['
CLOSE_LIST = ']'
OPEN_DICTIONARY = '{'
CLOSE_DICTIONARY = '}'
OPEN_SET = '{'
CLOSE_SET = '}'
LESSER = '<'
BIGGER = '>'

UNKNOWN = 'Unknown'

TYPE_TYPE = 'type'
TYPE_MODULE = 'module'
TYPE_CLASS = 'class'
TYPE_METHOD = 'method'
TYPE_FUNCTION = 'function'
TYPE_BUILTIN_FUNCTION_OR_METHOD = 'builtin_function_or_method'
TYPE_BOOLEAN = 'bool'
TYPE_STRING = 'str'
TYPE_INTEGER = 'int'
TYPE_FLOAT = 'float'
TYPE_TUPLE = 'tuple'
TYPE_LIST = 'list'
TYPE_DICT = 'dict'
TYPE_SET = 'set'

NATIVE_TYPES = [
    TYPE_TYPE,
    TYPE_MODULE,
    TYPE_CLASS,
    TYPE_METHOD,
    TYPE_FUNCTION,
    TYPE_BUILTIN_FUNCTION_OR_METHOD,
    TYPE_BOOLEAN,
    TYPE_STRING,
    TYPE_INTEGER,
    TYPE_FLOAT,
    TYPE_TUPLE,
    TYPE_LIST,
    TYPE_DICT,
    TYPE_SET
]

NULL_VALUE = 'null'
TRUE_VALUE = 'true'
FALSE_VALUE = 'false'

ENCODING = FileOperation.UTF_8             ###- deprecated
UTF_8 = FileOperation.UTF_8                ###- deprecated
OVERRIDE = FileOperation.OVERRIDE_TEXT     ###- deprecated
READ = FileOperation.READ_TEXT             ###- deprecated
WRITE = FileOperation.WRITE_TEXT           ###- deprecated

CSI = '\x1B['
BRIGHT_DIGIT = 1
DARK_DIGIT = 0
DEFAULT_COLOR = CSI + '0m'

DARK_BLACK = CSI + f'{DARK_DIGIT};30m'
BRIGHT_BLACK = CSI + f'{BRIGHT_DIGIT};30m'

DARK_RED = CSI + f'{DARK_DIGIT};31m'
BRIGHT_RED = CSI + f'{BRIGHT_DIGIT};31m'

DARK_GREEN = CSI + f'{DARK_DIGIT};32m'
BRIGHT_GREEN = CSI + f'{BRIGHT_DIGIT};32m'

DARK_YELLOW = CSI + f'{DARK_DIGIT};33m'
BRIGHT_YELLOW = CSI + f'{BRIGHT_DIGIT};33m'

DARK_BLUE = CSI + f'{DARK_DIGIT};34m'
BRIGHT_BLUE = CSI + f'{BRIGHT_DIGIT};34m'

DARK_MAGENTA = CSI + f'{DARK_DIGIT};35m'
BRIGHT_MAGENTA = CSI + f'{BRIGHT_DIGIT};35m'

DARK_CYAN = CSI + f'{DARK_DIGIT};36m'
BRIGHT_CYAN = CSI + f'{BRIGHT_DIGIT};36m'

WHITE = CSI + '1m'
DARK_WHITE = CSI + f'{DARK_DIGIT};37m'
BRIGHT_WHITE = CSI + f'{BRIGHT_DIGIT};37m'

RESET_COLOR = DEFAULT_COLOR
MUTTED_COLOR = BRIGHT_BLACK

IMPLEMENTED_PROMP_COLORS = [
    DEFAULT_COLOR,
    DARK_BLACK,
    BRIGHT_BLACK,
    DARK_RED,
    BRIGHT_RED,
    DARK_GREEN,
    BRIGHT_GREEN,
    DARK_YELLOW,
    BRIGHT_YELLOW,
    DARK_BLUE,
    BRIGHT_BLUE,
    DARK_MAGENTA,
    BRIGHT_MAGENTA,
    DARK_CYAN,
    BRIGHT_CYAN,
    WHITE,
    DARK_WHITE,
    BRIGHT_WHITE,
    RESET_COLOR,
    MUTTED_COLOR
]

OPEN_COLLECTION = 'OPEN_COLLECTION'
CLOSE_COLLECTION = 'CLOSE_COLLECTION'
WITH_COLOR = True
WITHOUT_COLOR = False

NATIVE_PROMPT_COLOR = {
    TYPE_MODULE : BRIGHT_BLUE,
    TYPE_CLASS : DARK_BLUE,
    TYPE_METHOD : BRIGHT_BLUE,
    TYPE_BUILTIN_FUNCTION_OR_METHOD : BRIGHT_BLUE,
    TYPE_FUNCTION : BRIGHT_BLUE,
    TYPE_BOOLEAN : BRIGHT_WHITE,
    TYPE_STRING : DARK_YELLOW,
    TYPE_INTEGER : DARK_GREEN, ###- BRIGHT_BLACK, ###-
    TYPE_FLOAT : DARK_GREEN ###- BRIGHT_BLACK ###-
}
NONE_PROMP_COLOR = DARK_MAGENTA
QUOTE_PROMPT_COLOR = DARK_MAGENTA
COLLECTION_PROMPT_COLOR = BRIGHT_BLACK
COMA_PROMPT_COLOR = BRIGHT_BLACK
COLON_PROMPT_COLOR = BRIGHT_BLACK

COLLECTION_TYPE = {
    TYPE_DICT : {
        OPEN_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{OPEN_DICTIONARY}{RESET_COLOR}',
            WITHOUT_COLOR : OPEN_DICTIONARY
        },
        CLOSE_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{CLOSE_DICTIONARY}{RESET_COLOR}',
            WITHOUT_COLOR : CLOSE_DICTIONARY
        }
    },
    TYPE_SET : {
        OPEN_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{OPEN_DICTIONARY}{RESET_COLOR}',
            WITHOUT_COLOR : OPEN_DICTIONARY
        },
        CLOSE_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{CLOSE_DICTIONARY}{RESET_COLOR}',
            WITHOUT_COLOR : CLOSE_DICTIONARY
        }
    },
    TYPE_LIST : {
        OPEN_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{OPEN_LIST}{RESET_COLOR}',
            WITHOUT_COLOR : OPEN_LIST
        },
        CLOSE_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{CLOSE_LIST}{RESET_COLOR}',
            WITHOUT_COLOR : CLOSE_LIST
        }
    },
    TYPE_TUPLE : {
        OPEN_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{OPEN_TUPLE}{RESET_COLOR}',
            WITHOUT_COLOR : OPEN_TUPLE
        },
        CLOSE_COLLECTION : {
            WITH_COLOR : f'{COLLECTION_PROMPT_COLOR}{CLOSE_TUPLE}{RESET_COLOR}',
            WITHOUT_COLOR : CLOSE_TUPLE
        }
    }
}


SYMBOLS = {
    "@",
    '©',
    '®',
    '™',
    '℠',
    "#",
    "$",
    "%",
    "&",
    "=",
    "|",
    "_",
    "/",
    "*",
    "-",
    "+"
}
PUNCTUATIONS = {
    DOT,
    COMA,
    COLON,
    SEMI_COLON,
    QUESTION_MARK,
    EXCLAMATION_MARK,
    OPEN_TUPLE,
    CLOSE_TUPLE,
    OPEN_LIST,
    CLOSE_LIST,
    OPEN_DICTIONARY,
    CLOSE_DICTIONARY
}
PUNCTUATION = set(list(PUNCTUATIONS)) ###- deprecated
NUMBERS = {
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9"
}
A = {
    "À",
    "Á",
    "Ã",
    "Â",
    "à",
    "á",
    "ã",
    "â",
    "Ä",
    "ä"
}
E = {
    "È",
    "É",
    "Ê",
    "è",
    "é",
    "ê",
    "Ë",
    "ë"
}
I = {
    "Ì",
    "Í",
    "Î",
    "ì",
    "í",
    "î",
    "Ï",
    "i"
}
O = {
    "Ò",
    "Ó",
    "Õ",
    "Ô",
    "ò",
    "ó",
    "õ",
    "ô",
    "Ö",
    "ö"
}
U = {
    "Ù",
    "Ú",
    "Û",
    "ù",
    "ú",
    "û",
    "Ü",
    "ü"
}
C = {
    "Ç"
    "ç"
}
LOWER_CASE = {
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
}
UPPER_CASE = {
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z"
}
CHARACTERES = tuple(set([*A, *E, *I, *O, *U, *C, *LOWER_CASE, *UPPER_CASE, SPACE]))
UPPER_CASE_CHARACTERES = tuple(set([char for char in CHARACTERES if char == char.upper() and char == char.strip()]))
ALL_SYMBOLS = tuple(set([*CHARACTERES, *SYMBOLS, *PUNCTUATION, *NUMBERS]))

OPEN_QUOTES = '“'
CLOSE_QUOTES = '”'