from .text_style import BOLD, BOLD_ITALIC, BOXED, DOTTED, ITALIC, STRIKE, WAVE, inherit, style


def caret_selection_and_gutter(c):
    return {
        "CARET_COLOR": c.pink,
        "CARET_ROW_COLOR": c.bg_2,
        "SELECTION_BACKGROUND": c.bg_3,
        "SELECTION_BACKGROUND_INACTIVE": c.tint(c.bg_3, 0.6),
        "SELECTION_FOREGROUND": "",
        "GUTTER_BACKGROUND": c.bg_0,
        "EDITOR_GUTTER_BACKGROUND": "",
        "LINE_NUMBERS_COLOR": c.fg_faint,
        "LINE_NUMBER_ON_CARET_ROW_COLOR": c.fg,
        "CONSOLE_BACKGROUND_KEY": c.bg_0,
    }


def guides_and_separators(c):
    return {
        "INDENT_GUIDE": c.indent,
        "SELECTED_INDENT_GUIDE": c.tint(c.fg_faint, 0.7),
        "MATCHED_BRACES_INDENT_GUIDE_COLOR": c.tint(c.lavender, 0.5),
        "VISUAL_INDENT_GUIDE": c.bg_2,
        "STRING_CONTENT_INDENT_GUIDE": c.bg_2,
        "RIGHT_MARGIN_COLOR": c.bg_2,
        "WHITESPACES": c.bg_4,
        "WHITESPACES_MODIFIED_LINES_COLOR": c.tint(c.peach, 0.4),
        "SOFT_WRAP_SIGN_COLOR": c.fg_faint,
        "METHOD_SEPARATORS_COLOR": c.bg_3,
        "TEARLINE_COLOR": c.bg_3,
        "SELECTED_TEARLINE_COLOR": c.fg_faint,
        "FOLDED_TEXT_BORDER_COLOR": c.bg_3,
        "DOC_COMMENT_GUIDE": c.bg_3,
        "DOC_COMMENT_LINK": c.cyan,
        "DIFF_SEPARATORS_BACKGROUND": c.bg_1,
        "DIFF_SEPARATOR_WAVE": c.bg_4,
        "GRID_STRIPE_COLOR": c.bg_2,
    }


def popups_and_hints(c):
    return {
        "LOOKUP_COLOR": c.bg_1,
        "DOCUMENTATION_COLOR": c.bg_1,
        "NOTIFICATION_BACKGROUND": c.bg_1,
        "PROMOTION_PANE": c.bg_1,
        "INFORMATION_HINT": c.bg_1,
        "QUESTION_HINT": c.diff_change,
        "ERROR_HINT": c.diff_delete,
        "HINT_BORDER": c.bg_4,
        "RECENT_LOCATIONS_SELECTION": c.bg_2,
        "READONLY_FRAGMENT_BACKGROUND": c.bg_1,
        "RECURSIVE_CALL_ATTRIBUTES": c.tint(c.peach, 0.2),
        "INLINE_REFACTORING_SETTINGS_DEFAULT": c.bg_3,
        "INLINE_REFACTORING_SETTINGS_FOCUSED": c.bg_3,
        "INLINE_REFACTORING_SETTINGS_HOVERED": c.bg_3,
        "ActionButton.hoverBackground": c.bg_3,
        "ActionButton.pressedBackground": c.bg_4,
        "ActionButton.iconTextForeground": c.fg_mute,
        "Table.hoverBackground": c.bg_2,
        "Bookmark.iconBackground": c.yellow,
        "Bookmark.Mnemonic.iconBackground": c.tint(c.yellow, 0.2),
        "Bookmark.Mnemonic.iconBorderColor": c.yellow,
        "Bookmark.Mnemonic.iconForeground": c.fg,
    }


def version_control_colors(c):
    return {
        "ADDED_LINES_COLOR": c.green,
        "MODIFIED_LINES_COLOR": c.blue,
        "DELETED_LINES_COLOR": c.red,
        "IGNORED_ADDED_LINES_BORDER_COLOR": c.green,
        "IGNORED_MODIFIED_LINES_BORDER_COLOR": c.blue,
        "IGNORED_DELETED_LINES_BORDER_COLOR": c.red,
        "REVIEW_CHANGED_LINES_COLOR": c.lavender,
        "ANNOTATIONS_COLOR": c.fg_faint,
        "ANNOTATIONS_LAST_COMMIT_COLOR": c.fg,
        "VCS_ANNOTATIONS_COLOR_1": c.tint(c.lavender, 0.40),
        "VCS_ANNOTATIONS_COLOR_2": c.tint(c.lavender, 0.30),
        "VCS_ANNOTATIONS_COLOR_3": c.tint(c.lavender, 0.22),
        "VCS_ANNOTATIONS_COLOR_4": c.tint(c.lavender, 0.14),
        "VCS_ANNOTATIONS_COLOR_5": c.tint(c.lavender, 0.07),
        "MODIFIED_TAB_ICON": c.pink,
    }


def file_status_colors(c):
    statuses = {
        c.green: ["ADDED", "COPIED", "addedOutside"],
        c.blue: ["MODIFIED", "RENAMED", "modifiedOutside", "NOT_CHANGED_IMMEDIATE", "NOT_CHANGED_RECURSIVE"],
        c.fg_faint: ["DELETED", "IDEA_FILESTATUS_DELETED_FROM_FILE_SYSTEM"],
        c.peach_dim: ["IDEA_FILESTATUS_IGNORED", "OBSOLETE"],
        c.lavender: ["MERGED"],
        c.red: [
            "IDEA_FILESTATUS_MERGED_WITH_CONFLICTS",
            "IDEA_FILESTATUS_MERGED_WITH_BOTH_CONFLICTS",
            "IDEA_FILESTATUS_MERGED_WITH_PROPERTY_CONFLICTS",
            "changelistConflict",
        ],
        c.peach: ["UNKNOWN"],
        c.yellow: ["HIJACKED"],
        c.cyan: ["SWITCHED"],
    }
    return {f"FILESTATUS_{status}": color for color, names in statuses.items() for status in names}


def terminal_block_colors(c):
    return {
        "BLOCK_TERMINAL_BLOCK_BACKGROUND_START": c.bg_1,
        "BLOCK_TERMINAL_BLOCK_BACKGROUND_END": c.bg_0,
        "BLOCK_TERMINAL_ERROR_BLOCK_STROKE_COLOR": c.red,
        "BLOCK_TERMINAL_GENERATE_COMMAND_CARET_COLOR": c.lavender,
        "BLOCK_TERMINAL_GENERATE_COMMAND_PLACEHOLDER_FOREGROUND": c.tint(c.lavender, 0.6),
        "BLOCK_TERMINAL_INACTIVE_SELECTED_BLOCK_BACKGROUND": c.bg_2,
        "BLOCK_TERMINAL_INACTIVE_SELECTED_BLOCK_STROKE_COLOR": c.bg_4,
        "BLOCK_TERMINAL_PROMPT_SEPARATOR_COLOR": c.bg_3,
        "BLOCK_TERMINAL_SELECTED_BLOCK_BACKGROUND": c.tint(c.pink, 0.14),
        "BLOCK_TERMINAL_SELECTED_BLOCK_STROKE_COLOR": c.pink,
    }


def editor_colors(c):
    return {
        **caret_selection_and_gutter(c),
        **guides_and_separators(c),
        **popups_and_hints(c),
        **version_control_colors(c),
        **file_status_colors(c),
        **terminal_block_colors(c),
    }


def underline_faint(c):
    return c.tint(c.fg_faint, 0.8)


def syntax(c):
    punctuation = ["OPERATION_SIGN", "PARENTHS", "BRACES", "BRACKETS", "COMMA", "SEMICOLON", "DOT"]
    return {
        "TEXT": style(c.fg, c.bg_0),
        "DEFAULT_IDENTIFIER": style(c.fg),
        "DEFAULT_KEYWORD": style(c.cyan),
        "DEFAULT_STRING": style(c.yellow),
        "DEFAULT_VALID_STRING_ESCAPE": style(c.peach),
        "DEFAULT_INVALID_STRING_ESCAPE": style(c.red, effect=c.red, effect_type=WAVE),
        "DEFAULT_NUMBER": style(c.peach_dim),
        "DEFAULT_CONSTANT": style(c.peach),
        "DEFAULT_PREDEFINED_SYMBOL": style(c.cyan, font=ITALIC),
        "DEFAULT_LINE_COMMENT": style(c.comment, font=ITALIC),
        "DEFAULT_BLOCK_COMMENT": style(c.comment, font=ITALIC),
        "DEFAULT_DOC_COMMENT": style(c.comment, font=ITALIC),
        "DEFAULT_DOC_COMMENT_TAG": style(c.fg_mute, font=BOLD_ITALIC),
        "DEFAULT_DOC_COMMENT_TAG_VALUE": style(c.fg_mute, font=ITALIC),
        "DEFAULT_DOC_MARKUP": style(c.fg_mute, font=ITALIC),
        **{f"DEFAULT_{name}": style(c.fg_faint) for name in punctuation},
        "DEFAULT_FUNCTION_DECLARATION": style(c.pink),
        "DEFAULT_FUNCTION_CALL": style(c.pink),
        "DEFAULT_INSTANCE_METHOD": inherit("DEFAULT_FUNCTION_CALL"),
        "DEFAULT_STATIC_METHOD": inherit("DEFAULT_FUNCTION_CALL"),
        "DEFAULT_CLASS_NAME": style(c.lavender),
        "DEFAULT_CLASS_REFERENCE": style(c.lavender),
        "DEFAULT_INTERFACE_NAME": style(c.lavender),
        "DEFAULT_LOCAL_VARIABLE": style(c.fg),
        "DEFAULT_REASSIGNED_LOCAL_VARIABLE": style(c.fg, effect=underline_faint(c)),
        "DEFAULT_PARAMETER": style(c.fg, font=ITALIC),
        "DEFAULT_REASSIGNED_PARAMETER": style(c.fg, font=ITALIC, effect=underline_faint(c)),
        "DEFAULT_INSTANCE_FIELD": style(c.fg),
        "DEFAULT_STATIC_FIELD": style(c.peach),
        "DEFAULT_GLOBAL_VARIABLE": style(c.fg),
        "DEFAULT_LABEL": style(c.cyan),
        "DEFAULT_METADATA": style(c.peach_br, font=ITALIC),
        "DEFAULT_ATTRIBUTE": style(c.fg, font=ITALIC),
        "DEFAULT_TAG": style(c.cyan),
        "DEFAULT_ENTITY": style(c.peach),
        "DEFAULT_TEMPLATE_LANGUAGE_COLOR": style(background=c.bg_1),
        "DEFAULT_HIGHLIGHTED_REFERENCE": style(effect=c.fg_faint),
        "CUSTOM_KEYWORD1_ATTRIBUTES": style(c.cyan),
        "CUSTOM_KEYWORD2_ATTRIBUTES": style(c.pink),
        "CUSTOM_KEYWORD3_ATTRIBUTES": style(c.lavender),
        "CUSTOM_KEYWORD4_ATTRIBUTES": style(c.peach),
        "CUSTOM_STRING_ATTRIBUTES": inherit("DEFAULT_STRING"),
        "CUSTOM_VALID_STRING_ESCAPE_ATTRIBUTES": inherit("DEFAULT_VALID_STRING_ESCAPE"),
        "CUSTOM_INVALID_STRING_ESCAPE_ATTRIBUTES": inherit("DEFAULT_INVALID_STRING_ESCAPE"),
        "CUSTOM_LINE_COMMENT_ATTRIBUTES": inherit("DEFAULT_LINE_COMMENT"),
        "CUSTOM_MULTI_LINE_COMMENT_ATTRIBUTES": inherit("DEFAULT_BLOCK_COMMENT"),
        "CUSTOM_NUMBER_ATTRIBUTES": inherit("DEFAULT_NUMBER"),
        "DOC_CODE_BLOCK": style(c.fg, c.bg_1, effect=c.bg_3, effect_type=BOXED),
        "DOC_CODE_INLINE": style(c.lavender, c.bg_1),
        "DOC_TIPS_SHORTCUT": style(c.fg, effect=c.fg_faint, effect_type=BOXED),
        "TODO_DEFAULT_ATTRIBUTES": style(c.peach, font=BOLD_ITALIC, stripe=c.peach),
        "TODO_ATTRIBUTES": inherit("TODO_DEFAULT_ATTRIBUTES"),
        **{f"RAINBOW_COLOR{index}": style(color) for index, color in enumerate(c.rainbow[:5])},
    }


def diagnostics(c):
    info = c.tint(c.yellow, 0.55)
    return {
        "ERRORS_ATTRIBUTES": style(effect=c.red, effect_type=WAVE, stripe=c.red),
        "WARNING_ATTRIBUTES": style(effect=c.yellow, effect_type=WAVE, stripe=c.yellow),
        "INFO_ATTRIBUTES": style(effect=info, effect_type=WAVE, stripe=info),
        "GENERIC_SERVER_ERROR_OR_WARNING": style(effect=c.peach, effect_type=WAVE, stripe=c.peach),
        "FILESTATUS_ERRORS": style(effect=c.red, effect_type=WAVE, stripe=c.red),
        "WRONG_REFERENCES_ATTRIBUTES": style(c.red),
        "NOT_USED_ELEMENT_ATTRIBUTES": style(c.fg_faint),
        "DEPRECATED_ATTRIBUTES": style(effect=c.fg_mute, effect_type=STRIKE),
        "MARKED_FOR_REMOVAL_ATTRIBUTES": style(effect=c.red, effect_type=STRIKE),
        "TYPO": style(effect=c.cyan, effect_type=WAVE),
        "GRAMMAR_ERROR": style(effect=c.blue, effect_type=WAVE),
        "TEXT_STYLE_ERROR": style(effect=c.red, effect_type=DOTTED),
        "TEXT_STYLE_WARNING": style(effect=c.yellow, effect_type=DOTTED),
        "TEXT_STYLE_SUGGESTION": style(effect=c.cyan, effect_type=DOTTED),
        "RUNTIME_ERROR": style(effect=c.red, effect_type=DOTTED, stripe=c.red),
        "BAD_CHARACTER": style(c.red, effect=c.red, effect_type=WAVE),
        "Unresolved reference access": style(c.fg_faint, effect=c.fg_faint, effect_type=DOTTED),
        "NO_ANALYSIS": style(stripe=c.fg_faint),
        "DO_NOT_SHOW": style(stripe=c.green),
    }


def highlighting(c):
    return {
        "MATCHED_BRACE_ATTRIBUTES": style(c.lavender, c.bg_3, font=BOLD),
        "UNMATCHED_BRACE_ATTRIBUTES": style(c.red, c.diff_delete, font=BOLD),
        "MATCHED_TAG_NAME": style(background=c.bg_3),
        "IDENTIFIER_UNDER_CARET_ATTRIBUTES": style(background=c.bg_3, stripe=c.lavender),
        "WRITE_IDENTIFIER_UNDER_CARET_ATTRIBUTES": style(background=c.tint(c.pink, 0.2), stripe=c.pink),
        "SEARCH_RESULT_ATTRIBUTES": style(background=c.search, stripe=c.yellow),
        "WRITE_SEARCH_RESULT_ATTRIBUTES": style(background=c.search_current, stripe=c.peach),
        "TEXT_SEARCH_RESULT_ATTRIBUTES": style(background=c.search, stripe=c.yellow),
        "REGEXP_MATCHED_GROUPS": style(background=c.by_mode(c.bg_4, c.bg_3)),
        "BLINKING_HIGHLIGHTS_ATTRIBUTES": style(effect=c.fg_faint, effect_type=BOXED),
        "BOOKMARKS_ATTRIBUTES": style(stripe=c.lavender),
        "INJECTED_LANGUAGE_FRAGMENT": style(background=c.bg_1),
        "LIVE_TEMPLATE_ATTRIBUTES": style(effect=c.pink, effect_type=BOXED),
        "LIVE_TEMPLATE_INACTIVE_SEGMENT": style(effect=c.fg_faint, effect_type=BOXED),
        "TEMPLATE_VARIABLE_ATTRIBUTES": style(c.lavender),
        "DUPLICATE_FROM_SERVER": style(background=c.tint(c.yellow, 0.15)),
    }


def folding_inlays_and_hints(c):
    return {
        "FOLDED_TEXT_ATTRIBUTES": style(c.fg_mute, c.bg_1),
        "INLAY_DEFAULT": style(c.fg_faint, c.bg_1, font=ITALIC),
        "INLAY_TEXT_WITHOUT_BACKGROUND": style(c.fg_faint, font=ITALIC),
        "INLINE_PARAMETER_HINT": style(c.fg_faint, c.bg_1, font=ITALIC),
        "INLINE_PARAMETER_HINT_HIGHLIGHTED": style(c.fg, c.bg_3, font=ITALIC),
        "INLINE_PARAMETER_HINT_CURRENT": style(c.pink, c.tint(c.pink, 0.18), font=ITALIC),
        "INLINE_SUGGESTION": style(c.fg_faint, font=ITALIC),
        "INLAY_BUTTON_DEFAULT": style(c.fg_mute, effect=c.bg_4, effect_type=BOXED),
        "INLAY_BUTTON_FOCUSED": style(c.fg_mute, effect=c.fg_faint, effect_type=BOXED),
        "INLAY_BUTTON_HOVERED": style(c.fg_mute, effect=c.fg_faint, effect_type=BOXED),
        "INLAY_BUTTON_HINT": style(c.fg_faint),
        "CODE_LENS_BORDER_COLOR": style(effect=c.by_mode(c.bg_4, c.fg_faint), effect_type=BOXED),
        "BREADCRUMBS_DEFAULT": style(c.fg_mute),
        "BREADCRUMBS_CURRENT": style(c.fg, c.bg_3),
        "BREADCRUMBS_HOVERED": style(c.fg, c.bg_3),
        "BREADCRUMBS_INACTIVE": style(c.fg_faint),
    }


def ai_assistance(c):
    return {
        "AI_INLAY_BUTTON_DEFAULT": style(c.fg_mute, effect=c.lavender, effect_type=BOXED),
        "AI_INLAY_BUTTON_FOCUSED": style(c.fg_mute, effect=c.lavender_br, effect_type=BOXED),
        "AI_INLAY_BUTTON_HOVERED": style(c.fg_mute, effect=c.lavender_br, effect_type=BOXED),
        "INLINE_PROMPT": style(c.lavender),
        "INLINE_PROMPT_PROGRESS_DARK": style(c.lavender),
        "INLINE_PROMPT_PROGRESS_LIGHT": style(c.tint(c.lavender, 0.5)),
    }


def links(c):
    return {
        "HYPERLINK_ATTRIBUTES": style(c.cyan, effect=c.cyan),
        "FOLLOWED_HYPERLINK_ATTRIBUTES": style(c.lavender, effect=c.lavender),
        "INACTIVE_HYPERLINK_ATTRIBUTES": style(effect=c.fg_faint),
        "CTRL_CLICKABLE": style(c.cyan, effect=c.cyan),
    }


def debugger_and_coverage(c):
    coverage_strength = c.by_mode(0.45, 0.35)
    return {
        "BREAKPOINT_ATTRIBUTES": style(background=c.diff_delete, stripe=c.red),
        "EXECUTIONPOINT_ATTRIBUTES": style(background=c.tint(c.blue, 0.32)),
        "NOT_TOP_FRAME_ATTRIBUTES": style(background=c.diff_change),
        "INLINE_STACK_FRAMES": style(background=c.tint(c.lavender, 0.2)),
        "DEBUGGER_INLINED_VALUES": style(c.fg_faint, font=ITALIC),
        "DEBUGGER_INLINED_VALUES_MODIFIED": style(c.peach, font=ITALIC),
        "DEBUGGER_INLINED_VALUES_EXECUTION_LINE": style(c.blue, font=ITALIC),
        "DEBUGGER_SMART_STEP_INTO_SELECTION": style(
            background=c.tint(c.lavender, 0.35), effect=c.lavender, effect_type=BOXED
        ),
        "DEBUGGER_SMART_STEP_INTO_TARGET": style(background=c.tint(c.lavender, 0.18)),
        "EVALUATED_EXPRESSION_ATTRIBUTES": style(background=c.bg_3),
        "EVALUATED_EXPRESSION_EXECUTION_LINE_ATTRIBUTES": style(background=c.bg_4),
        "LINE_FULL_COVERAGE": style(c.tint(c.green, coverage_strength), font=BOLD),
        "LINE_PARTIAL_COVERAGE": style(c.tint(c.yellow, coverage_strength), font=BOLD),
        "LINE_NONE_COVERAGE": style(c.tint(c.red, coverage_strength), font=BOLD),
    }


def diff(c):
    return {
        "DIFF_INSERTED": style(background=c.diff_add, stripe=c.green),
        "DIFF_MODIFIED": style(background=c.diff_change, stripe=c.blue),
        "DIFF_DELETED": style(background=c.diff_delete, stripe=c.red),
        "DIFF_CONFLICT": style(background=c.tint(c.peach, 0.18), stripe=c.peach),
        "DIFF_ABSENT": style(background=c.bg_1),
        "DIFF_DELETED_FROM_FS": style(background=c.tint(c.blue, 0.3)),
        "DIFF_UNKNOWN": style(background=c.tint(c.green, 0.2)),
        "DELETED_TEXT_ATTRIBUTES": style(c.fg_faint, c.diff_delete, effect=c.fg_faint, effect_type=STRIKE),
    }


def console(c):
    return {
        "CONSOLE_NORMAL_OUTPUT": style(c.fg),
        "CONSOLE_ERROR_OUTPUT": style(c.red),
        "CONSOLE_SYSTEM_OUTPUT": style(c.fg_mute),
        "CONSOLE_USER_INPUT": style(c.cyan, font=ITALIC),
        "CONSOLE_OUTPUT": style(background=c.bg_1),
        "CONSOLE_RANGE_TO_EXECUTE": style(effect=c.green, effect_type=BOXED),
        "LOG_ERROR_OUTPUT": style(c.red),
        "LOG_WARNING_OUTPUT": style(c.yellow),
        "LOG_INFO_OUTPUT": style(c.blue),
        "LOG_VERBOSE_OUTPUT": style(c.fg_mute),
        "LOG_DEBUG_OUTPUT": style(c.fg_faint),
        "LOG_EXPIRED_ENTRY": style(c.fg_faint),
    }


def terminal(c):
    return {
        "BLOCK_TERMINAL_COMMAND": style(c.fg, font=BOLD),
        "BLOCK_TERMINAL_SEARCH_ENTRY": style(c.fg, c.search),
        "BLOCK_TERMINAL_CURRENT_SEARCH_ENTRY": style(c.fg, c.search_current),
        "BLOCK_TERMINAL_GENERATE_COMMAND_PROMPT_TEXT": style(c.lavender),
        "TERMINAL_COMMAND_TO_RUN_USING_IDE": style(background=c.tint(c.green, 0.2)),
        "TERMINAL_CLASS_NAME_LOG_REFERENCE": style(effect=c.fg_faint, effect_type=DOTTED),
    }


def ansi_colors(c):
    ansi = {
        "BLACK": (c.bg_3, c.fg_faint),
        "RED": (c.red, c.red_br),
        "GREEN": (c.green, c.green_br),
        "YELLOW": (c.yellow, c.yellow_br),
        "BLUE": (c.blue, c.blue_br),
        "MAGENTA": (c.pink, c.pink_br),
        "CYAN": (c.cyan, c.cyan_br),
        "WHITE": (c.fg_mute, c.fg),
    }
    attributes = {
        "CONSOLE_BLACK_OUTPUT": style(c.bg_3),
        "CONSOLE_DARKGRAY_OUTPUT": style(c.fg_faint),
        "CONSOLE_GRAY_OUTPUT": style(c.fg_mute),
        "CONSOLE_WHITE_OUTPUT": style(c.fg),
    }
    for name, (normal, bright) in ansi.items():
        attributes[f"BLOCK_TERMINAL_{name}"] = style(normal)
        attributes[f"BLOCK_TERMINAL_{name}_BRIGHT"] = style(bright)
        if name not in ("BLACK", "WHITE"):
            attributes[f"CONSOLE_{name}_OUTPUT"] = style(normal)
            attributes[f"CONSOLE_{name}_BRIGHT_OUTPUT"] = style(bright)
    return attributes


def rainbow_brackets(c):
    return {
        f"{kind}_BRACKETS_RAINBOW_COLOR{index}": style(color)
        for kind in ("ROUND", "SQUARE", "SQUIGGLY", "ANGLE")
        for index, color in enumerate(c.rainbow[:5])
    }


GROUPS = [
    syntax,
    diagnostics,
    highlighting,
    folding_inlays_and_hints,
    ai_assistance,
    links,
    debugger_and_coverage,
    diff,
    console,
    terminal,
    ansi_colors,
    rainbow_brackets,
]


def editor_attributes(c):
    attributes = {}
    for group in GROUPS:
        attributes.update(group(c))
    return attributes
