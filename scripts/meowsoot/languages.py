from .editor import underline_faint
from .text_style import BOLD, ITALIC, inherit, style


def java(c):
    return {
        "ENUM_CONST": style(c.peach),
        "STATIC_FINAL_FIELD_ATTRIBUTES": style(c.peach),
        "STATIC_FIELD_ATTRIBUTES": inherit("DEFAULT_STATIC_FIELD"),
        "STATIC_METHOD_ATTRIBUTES": inherit("DEFAULT_STATIC_METHOD"),
        "CONSTRUCTOR_CALL_ATTRIBUTES": style(c.lavender),
        "CONSTRUCTOR_DECLARATION_ATTRIBUTES": style(c.lavender),
        "TYPE_PARAMETER_NAME_ATTRIBUTES": style(c.lavender, font=ITALIC),
        "ANNOTATION_NAME_ATTRIBUTES": inherit("DEFAULT_METADATA"),
        "ANNOTATION_ATTRIBUTE_NAME_ATTRIBUTES": style(c.fg, font=ITALIC),
        "IMPLICIT_ANONYMOUS_CLASS_PARAMETER_ATTRIBUTES": style(c.fg, effect=underline_faint(c)),
    }


def kotlin(c):
    smart_cast = style(background=c.tint(c.cyan, 0.12))
    return {
        "KOTLIN_LABEL": style(c.cyan),
        "KOTLIN_NAMED_ARGUMENT": style(c.fg_mute),
        "KOTLIN_CONSTRUCTOR": style(c.lavender),
        "KOTLIN_ENUM_ENTRY": style(c.peach),
        "KOTLIN_TYPE_PARAMETER": inherit("TYPE_PARAMETER_NAME_ATTRIBUTES"),
        "KOTLIN_CLOSURE_DEFAULT_PARAMETER": style(c.cyan, font=ITALIC),
        "KOTLIN_PACKAGE_FUNCTION_CALL": inherit("DEFAULT_FUNCTION_CALL"),
        "KOTLIN_FUNCTION_LITERAL_BRACES_AND_ARROW": style(c.fg_faint, font=BOLD),
        "KOTLIN_MUTABLE_VARIABLE": style(effect=underline_faint(c)),
        "KOTLIN_BACKING_FIELD_VARIABLE": style(c.fg),
        "KOTLIN_SMART_CAST_VALUE": smart_cast,
        "KOTLIN_SMART_CAST_RECEIVER": smart_cast,
        "KOTLIN_SMART_CONSTANT": smart_cast,
        "KOTLIN_EXCLEXCL": style(c.red, font=BOLD),
    }


def scala(c):
    return {
        "Scala Type Alias": style(c.lavender),
        "Scala Type parameter": style(c.lavender, font=ITALIC),
        "Scala Named Argument": style(c.fg_mute),
        "Interpolated String Injection": style(c.peach),
    }


def groovy(c):
    return {
        "Static method access": inherit("DEFAULT_STATIC_METHOD"),
        "Static property reference ID": inherit("DEFAULT_STATIC_FIELD"),
        "Groovy method declaration": inherit("DEFAULT_FUNCTION_DECLARATION"),
        "Closure braces": inherit("DEFAULT_BRACES"),
    }


def javascript(c):
    return {
        "JS.GLOBAL_VARIABLE": inherit("DEFAULT_GLOBAL_VARIABLE"),
        "JS.GLOBAL_FUNCTION": inherit("DEFAULT_FUNCTION_DECLARATION"),
        "JS.INSTANCE_MEMBER_FUNCTION": inherit("DEFAULT_INSTANCE_METHOD"),
        "JS.LOCAL_VARIABLE": inherit("DEFAULT_LOCAL_VARIABLE"),
        "JS.PARAMETER": inherit("DEFAULT_PARAMETER"),
        "JS.REGEXP": style(c.yellow),
        "JS.DECORATOR": inherit("DEFAULT_METADATA"),
        "JS.JSX_CLIENT_COMPONENT": style(c.lavender),
        "TS.TYPE_PARAMETER": style(c.lavender, font=ITALIC),
        "TS.MODULE_NAME": style(c.lavender),
        "COFFEESCRIPT.GLOBAL_VARIABLE": inherit("DEFAULT_GLOBAL_VARIABLE"),
    }


def python(c):
    return {
        "PY.SELF_PARAMETER": style(c.cyan, font=ITALIC),
        "PY.KEYWORD_ARGUMENT": style(c.fg_mute),
        "PY.BUILTIN_NAME": style(c.pink, font=ITALIC),
        "PY.PREDEFINED_DEFINITION": style(c.pink, font=ITALIC),
        "PY.PREDEFINED_USAGE": style(c.pink, font=ITALIC),
        "PY.DECORATOR": style(c.peach_br, font=ITALIC),
        "PY.ANNOTATION": style(c.lavender),
    }


def go(c):
    return {
        "GO_BUILTIN_FUNCTION_CALL": style(c.pink, font=ITALIC),
        "GO_BUILTIN_TYPE_REFERENCE": style(c.lavender, font=ITALIC),
        "GO_BUILTIN_CONSTANT": style(c.peach),
        "GO_BUILTIN_VARIABLE": style(c.cyan, font=ITALIC),
        "GO_PACKAGE": style(c.lavender),
        "GO_METHOD_RECEIVER": style(c.cyan, font=ITALIC),
        "GO_PACKAGE_EXPORTED_CONSTANT": style(c.peach),
        "GO_PACKAGE_LOCAL_CONSTANT": style(c.peach),
        "GO_LOCAL_CONSTANT": style(c.peach),
        "GO_EXPORTED_FUNCTION": inherit("DEFAULT_FUNCTION_DECLARATION"),
        "GO_LOCAL_FUNCTION": inherit("DEFAULT_FUNCTION_DECLARATION"),
        "GO_EXPORTED_FUNCTION_CALL": inherit("DEFAULT_FUNCTION_CALL"),
        "GO_LOCAL_FUNCTION_CALL": inherit("DEFAULT_FUNCTION_CALL"),
        "GO_TYPE_REFERENCE": inherit("DEFAULT_CLASS_REFERENCE"),
        "GO_COMMENT_REFERENCE": inherit("DEFAULT_DOC_COMMENT_TAG_VALUE"),
        "GO_SHADOWING_VARIABLE": inherit("DEFAULT_LOCAL_VARIABLE"),
    }


def rust(c):
    return {
        "org.rust.MACRO": style(c.pink, font=ITALIC),
        "org.rust.LIFETIME": style(c.peach, font=ITALIC),
        "org.rust.SELF_PARAMETER": style(c.cyan, font=ITALIC),
        "org.rust.SELF_EXPRESSION": style(c.cyan, font=ITALIC),
        "org.rust.CRATE": style(c.lavender),
        "org.rust.ENUM_VARIANT": style(c.peach),
        "org.rust.TYPE_PARAMETER": style(c.lavender, font=ITALIC),
        "org.rust.STATIC": style(c.peach),
        "org.rust.Q_OPERATOR": style(c.peach),
        "org.rust.MUT_BINDING": style(effect=underline_faint(c)),
        "org.rust.UNSAFE_CODE": style(effect=c.red),
        "org.rust.CFG_DISABLED_CODE": style(c.fg_faint),
    }


def data_formats(c):
    return {
        "JSON.PROPERTY_KEY": style(c.fg),
        "YAML_SCALAR_KEY": style(c.fg),
        "YAML_ANCHOR": style(c.peach),
        "org.toml.KEY": style(c.fg),
        "PROPERTIES.KEY": style(c.fg),
        "PROPERTIES.KEY_VALUE_SEPARATOR": style(c.fg_faint),
        "PROPERTIES.VALID_STRING_ESCAPE": inherit("DEFAULT_VALID_STRING_ESCAPE"),
        "PROPERTIES.INVALID_STRING_ESCAPE": inherit("DEFAULT_INVALID_STRING_ESCAPE"),
    }


def markup(c):
    attributes = {}
    for language in ("XML", "HTML"):
        attributes.update({
            f"{language}_TAG": style(c.fg_faint),
            f"{language}_TAG_NAME": style(c.cyan),
            f"{language}_CUSTOM_TAG_NAME": style(c.lavender),
            f"{language}_ATTRIBUTE_NAME": style(c.fg, font=ITALIC),
            f"{language}_ATTRIBUTE_VALUE": inherit("DEFAULT_STRING"),
            f"{language}_ENTITY_REFERENCE": style(c.peach),
        })
    attributes.update({
        "XML_NS_PREFIX": style(c.lavender),
        "XML_PROLOGUE": style(c.fg_faint),
        "XML_TAG_DATA": style(c.fg),
    })
    return attributes


def stylesheets(c):
    return {
        "CSS.TAG_NAME": style(c.cyan),
        "CSS.CLASS_NAME": style(c.lavender),
        "CSS.HASH": style(c.lavender),
        "CSS.PSEUDO": style(c.cyan),
        "CSS.PROPERTY_NAME": style(c.fg),
        "CSS.PROPERTY_VALUE": style(c.peach),
        "CSS.FUNCTION": style(c.pink),
        "CSS.COLOR": style(c.peach),
        "CSS.URL": style(c.cyan, effect=c.cyan),
        "CSS.IMPORTANT": style(c.red, font=BOLD),
        "CSS.KEYWORD": style(c.cyan),
        "LESS_VARIABLE": style(c.fg),
        "SASS_VARIABLE": style(c.fg),
        "SASS_MIXIN": style(c.pink),
        "SASS_ATTRIBUTE": style(c.fg),
        "SASS_COMMENT": inherit("DEFAULT_LINE_COMMENT"),
        "SASS_CONSTANT": inherit("DEFAULT_CONSTANT"),
        "SASS_DIRECTIVE": inherit("DEFAULT_KEYWORD"),
        "SASS_RULE": inherit("DEFAULT_KEYWORD"),
    }


def markdown(c):
    link = style(c.cyan, effect=c.cyan)
    return {
        "MARKDOWN_HEADER": style(c.pink, font=BOLD),
        "MARKDOWN_HEADER_BOLD": style(c.pink, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_1": style(c.pink, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_2": style(c.pink, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_3": style(c.peach, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_4": style(c.peach, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_5": style(c.yellow, font=BOLD),
        "MARKDOWN_HEADER_LEVEL_6": style(c.yellow, font=BOLD),
        "MARKDOWN_BOLD": style(c.peach, font=BOLD),
        "MARKDOWN_ITALIC": style(c.yellow, font=ITALIC),
        "MARKDOWN_BOLD_MARKER": style(c.fg_faint),
        "MARKDOWN_ITALIC_MARKER": style(c.fg_faint),
        "MARKDOWN_CODE_SPAN": style(c.lavender, c.bg_1),
        "MARKDOWN_CODE_SPAN_MARKER": style(c.fg_faint, c.bg_1),
        "MARKDOWN_CODE_FENCE": style(c.fg_faint),
        "MARKDOWN_LINK_TEXT": style(c.lavender),
        "MARKDOWN_LINK_LABEL": style(c.lavender),
        "MARKDOWN_LINK_DESTINATION": link,
        "MARKDOWN_LINK_TITLE": style(c.yellow),
        "MARKDOWN_AUTO_LINK": link,
        "MARKDOWN_REFERENCE_LINK": style(c.lavender),
        "MARKDOWN_IMAGE": style(c.lavender),
        "MARKDOWN_LIST_MARKER": style(c.cyan),
        "MARKDOWN_BLOCK_QUOTE_MARKER": style(c.fg_faint),
        "MARKDOWN_BLOCK_QUOTE": style(c.fg_mute, font=ITALIC),
        "MARKDOWN_HRULE": style(c.fg_faint),
        "MARKDOWN_TABLE_SEPARATOR": style(c.fg_faint),
    }


def shell(c):
    return {
        "BASH.SHEBANG": style(c.comment, font=ITALIC),
        "BASH.EXTERNAL_COMMAND": style(c.pink),
        "BASH.INTERNAL_COMMAND": style(c.pink, font=ITALIC),
        "BASH.FUNCTION_DEF_NAME": style(c.pink),
        "BASH.FUNCTION_CALL": style(c.pink),
        "BASH.HERE_DOC_START": style(c.cyan),
        "BASH.HERE_DOC_END": style(c.cyan),
        "BASH.CONDITIONAL": style(c.cyan),
    }


def regexp(c):
    return {
        "REGEXP.CHAR_CLASS": style(c.peach),
        "REGEXP.META": inherit("DEFAULT_KEYWORD"),
        "REGEXP.ESC_CHARACTER": inherit("DEFAULT_VALID_STRING_ESCAPE"),
        "REGEXP.QUOTE_CHARACTER": inherit("DEFAULT_VALID_STRING_ESCAPE"),
        "REGEXP.REDUNDANT_ESCAPE": style(c.fg_faint),
        "REGEXP.BRACES": inherit("DEFAULT_BRACES"),
        "REGEXP.BRACKETS": inherit("DEFAULT_BRACKETS"),
        "REGEXP.PARENTHS": inherit("DEFAULT_PARENTHS"),
    }


LANGUAGES = [
    java,
    kotlin,
    scala,
    groovy,
    javascript,
    python,
    go,
    rust,
    data_formats,
    markup,
    stylesheets,
    markdown,
    shell,
    regexp,
]


def language_attributes(c):
    attributes = {}
    for language in LANGUAGES:
        attributes.update(language(c))
    return attributes
