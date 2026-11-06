from .hsl import with_alpha
from .tokens import PROJECT_GRADIENT_ACCENTS


def swing_defaults(c):
    return {
        "*.textForeground": c.fg,
        "*.caretForeground": c.fg,
        "*.selectionForegroundInactive": c.fg,
        "*.textBackground": c.bg_0,
        "*.selectionBackgroundInactive": c.by_mode(c.bg_3, c.bg_1),
        "text": c.fg,
        "textText": c.fg,
        "controlText": c.fg,
        "infoText": c.fg,
        "textInactiveText": c.fg_faint,
        "control": c.bg_1,
        "window": c.bg_1,
        "activeCaption": c.bg_3,
        "inactiveCaption": c.bg_2,
        "Label.selectedForeground": c.fg,
        "OptionPane.messageForeground": c.fg,
        "TitledBorder.titleColor": c.fg,
        "MenuItem.acceleratorSelectionForeground": c.fg,
        "PopupMenu.translucentBackground": c.bg_1,
        "SplitPane.highlight": c.bg_1,
    }


def controls(c):
    focus = c.tint(c.pink, 0.6)
    return {
        "Component.focusColor": focus,
        "Component.focusedBorderColor": focus,
        "Tree.selectionBorderColor": focus,
        "CombinedDiff.BlockBorder.selectedActiveColor": focus,
        "CombinedDiff.BlockBorder.selectedInactiveColor": c.bg_4,
        "ComboBox.ArrowButton.iconColor": c.fg_mute,
        "ComboBox.ArrowButton.disabledIconColor": c.fg_faint,
        "SpeedSearch.foreground": c.fg,
        "Counter.background": c.pink,
        "Counter.foreground": c.bg_0,
        "Slider.tickColor": c.fg_faint,
        "Slider.trackColor": c.bg_4,
        "Slider.buttonColor": c.fg_mute,
        "Slider.buttonBorderColor": c.bg_1,
        "TabbedPane.disabledUnderlineColor": c.fg_faint,
        "EditorTabs.underlineColor": c.pink,
        "EditorTabs.inactiveUnderlineColor": c.fg_faint,
        "ToolWindow.HeaderTab.selectedBackground": c.by_mode(c.bg_3, c.bg_1),
        "ToolWindow.HeaderTab.selectedInactiveBackground": c.bg_2,
        "MainWindow.Tab.background": c.frame,
        "MainWindow.FullScreeControl.Background": c.bg_4,
        "StatusBar.LightEditBackground": c.tint(c.blue, 0.2),
        "ScreenView.defaultBorderColor": c.bg_4,
        "ScreenView.selectedBorderColor": c.pink,
        "ScreenView.hoveredBorderColor": c.pink,
        "WelcomeScreen.Projects.actions.background": c.bg_1,
        "WelcomeScreen.Projects.actions.selectionBorderColor": c.pink,
        "HelpBrowser.titleHighlightForeground": c.pink,
        "MemoryIndicator.usedBackground": c.tint(c.blue, 0.3),
        "MemoryIndicator.allocatedBackground": c.bg_2,
    }


def text_on_tinted_backgrounds(c):
    return {
        "SearchEverywhere.Tab.selectedForeground": c.fg,
        "ToolWindow.Button.selectedForeground": c.fg,
        "ParameterInfo.currentParameterForeground": c.fg,
        "PresentationAssistant.Bright.Popup.foreground": c.by_mode(c.fg, c.bg_0),
        "PresentationAssistant.Pale.Popup.foreground": c.fg,
        "GotItTooltip.iconBorderColor": c.fg,
        "Tooltip.Learning.iconBorderColor": c.fg,
    }


def popups(c):
    raised = c.by_mode(c.bg_3, c.bg_1)
    return {
        "Editor.ToolTip.selectionBackground": c.bg_3,
        "ParameterInfo.background": c.bg_1,
        "ParameterInfo.foreground": c.fg,
        "ParameterInfo.infoForeground": c.fg_mute,
        "ParameterInfo.disabledForeground": c.fg_faint,
        "ParameterInfo.borderColor": c.bg_4,
        "ParameterInfo.lineSeparatorColor": c.bg_3,
        "ParameterInfo.currentOverloadBackground": c.bg_3,
        "PresentationAssistant.Pale.PopupBackground": raised,
        "PresentationAssistant.Pale.Popup.border": c.bg_4,
        "PresentationAssistant.Pale.keymapLabel": c.fg_faint,
        "PresentationAssistant.Bright.keymapLabel": c.fg_faint,
        "Notification.errorBackground": c.tint(c.red, 0.12),
        "Notification.errorBorderColor": c.tint(c.red, 0.4),
        "FlameGraph.Tooltip.scaleBackground": raised,
        "FlameGraph.Tooltip.scaleColor": c.blue,
    }


def links(c):
    return {
        "Hyperlink.linkColor": c.cyan,
        "Link.activeForeground": c.cyan,
        "Link.hoverForeground": c.cyan_br,
        "Link.pressedForeground": c.cyan_br,
        "Link.visitedForeground": c.lavender,
        "Link.secondaryForeground": c.fg_faint,
    }


def progress_bars(c):
    return {
        "ProgressBar.progressColor": c.pink,
        "ProgressBar.indeterminateStartColor": c.tint(c.pink, 0.5),
        "ProgressBar.indeterminateEndColor": c.pink,
        "ProgressBar.passedColor": c.green,
        "ProgressBar.passedEndColor": c.tint(c.green, 0.5),
        "ProgressBar.failedColor": c.red,
        "ProgressBar.failedEndColor": c.tint(c.red, 0.5),
        "ProgressBar.progressCounterBackground": c.pink,
        "ProgressBar.progressCounterForeground": c.bg_0,
    }


def tags_and_badges(c):
    raised = c.by_mode(c.bg_3, c.bg_1)
    return {
        "Tag.background": raised,
        "List.Tag.background": raised,
        "List.Tag.foreground": c.fg_mute,
        "Badge.blueSecondaryBackground": c.tint(c.blue, 0.3),
        "Badge.greenSecondaryBackground": c.tint(c.green, 0.3),
        "Badge.purpleSecondaryBackground": c.tint(c.lavender, 0.3),
        "Badge.graySecondaryBackground": raised,
        "Badge.graySecondaryForeground": c.fg,
        "Badge.disabledBackground": c.bg_2,
        "Badge.disabledForeground": c.fg_faint,
        "Bookmark.iconBackground": c.yellow,
        "Bookmark.Mnemonic.iconBackground": c.tint(c.yellow, 0.2),
        "Bookmark.Mnemonic.iconBorderColor": c.yellow,
        "Bookmark.Mnemonic.iconForeground": c.fg,
    }


def file_colors(c):
    return {
        "FileColor.Blue": c.tint(c.blue, 0.14),
        "FileColor.Green": c.tint(c.green, 0.14),
        "FileColor.Orange": c.tint(c.peach, 0.14),
        "FileColor.Rose": c.tint(c.pink, 0.14),
        "FileColor.Violet": c.tint(c.lavender, 0.14),
        "FileColor.Yellow": c.tint(c.yellow, 0.14),
        "FileColor.Gray": c.bg_2,
    }


def drag_and_drop(c):
    return {
        "DragAndDrop.areaBorderColor": c.pink,
        "DragAndDrop.areaForeground": c.fg_mute,
        "DragAndDrop.areaBackground": with_alpha(c.pink, 0.1),
        "DragAndDrop.rowBackground": with_alpha(c.pink, 0.15),
        "ToolWindow.Button.DragAndDrop.buttonDropBackground": with_alpha(c.pink, 0.5),
        "ToolWindow.DragAndDrop.areaBackground": with_alpha(c.pink, 0.3),
    }


def debugger(c):
    return {
        "Debugger.Variables.valueForeground": c.peach,
        "Debugger.Variables.typeForeground": c.fg_faint,
        "Debugger.Variables.collectingDataForeground": c.fg_faint,
        "Debugger.Variables.evaluatingExpressionForeground": c.fg_faint,
        "Debugger.Variables.changedValueForeground": c.blue,
        "Debugger.Variables.modifyingValueForeground": c.blue,
        "Debugger.Variables.errorMessageForeground": c.red,
        "Debugger.Variables.exceptionForeground": c.red,
    }


def version_control(c):
    raised = c.by_mode(c.bg_3, c.bg_1)
    branch_highlight = c.tint(c.blue, 0.12)
    return {
        "VersionControl.GitLog.headIconColor": c.yellow,
        "VersionControl.GitLog.localBranchIconColor": c.green,
        "VersionControl.GitLog.remoteBranchIconColor": c.lavender,
        "VersionControl.GitLog.tagIconColor": c.fg_mute,
        "VersionControl.GitLog.otherIconColor": c.fg_faint,
        "VersionControl.HgLog.headIconColor": c.pink,
        "VersionControl.HgLog.branchIconColor": c.green,
        "VersionControl.HgLog.closedBranchIconColor": c.red,
        "VersionControl.HgLog.bookmarkIconColor": c.lavender,
        "VersionControl.HgLog.localTagIconColor": c.cyan,
        "VersionControl.HgLog.mqTagIconColor": c.blue,
        "VersionControl.HgLog.tagIconColor": c.fg_mute,
        "VersionControl.HgLog.tipIconColor": c.yellow,
        "VersionControl.GitCommits.graphColor": c.fg_faint,
        "VersionControl.Log.Commit.currentBranchBackground": branch_highlight,
        "VersionControl.FileHistory.Commit.selectedBranchBackground": branch_highlight,
        "VersionControl.Log.Commit.hoveredBackground": c.bg_2,
        "VersionControl.Log.Commit.unmatchedForeground": c.fg_faint,
        "VersionControl.Log.Commit.Reference.foreground": c.fg_mute,
        "VersionControl.MarkerPopup.borderColor": c.bg_4,
        "VersionControl.Merge.Status.NoConflicts.foreground": c.green,
        "Review.Branch.Background": raised,
        "Review.Branch.Background.Hover": c.by_mode(c.bg_4, c.bg_3),
        "Review.State.Background": raised,
        "Review.State.Foreground": c.fg_mute,
        "Review.ChatItem.Hover": with_alpha(c.bg_4, 0.2),
    }


def trial_widget(c):
    def state(name, background, hover_background, foreground, border):
        return {
            f"TrialWidget.{name}.background": background,
            f"TrialWidget.{name}.hoverBackground": hover_background,
            f"TrialWidget.{name}.foreground": foreground,
            f"TrialWidget.{name}.hoverForeground": foreground,
            f"TrialWidget.{name}.borderColor": border,
            f"TrialWidget.{name}.hoverBorderColor": border,
        }

    def accented(name, color):
        return state(name, c.tint(color, 0.15), c.tint(color, 0.25), color, c.tint(color, 0.5))

    return {
        **state("Default", c.bg_1, c.bg_3, c.fg, c.fg_faint),
        **state("Progress", c.bg_1, c.bg_3, c.fg_faint, c.bg_4),
        **accented("Active", c.green),
        **accented("Alert", c.yellow),
        **accented("Expiring", c.red),
    }


def recent_projects(c):
    keys = {}
    for index, accent in enumerate(PROJECT_GRADIENT_ACCENTS.values(), start=1):
        color = getattr(c, accent)
        keys.update({
            f"RecentProject.Color{index}.Avatar.Start": color,
            f"RecentProject.Color{index}.Avatar.End": c.tint(color, 0.75),
            f"RecentProject.Color{index}.MainToolbarGradientStart": c.tint(color, 0.3),
        })
    return keys


GROUPS = [
    swing_defaults,
    controls,
    text_on_tinted_backgrounds,
    popups,
    links,
    progress_bars,
    tags_and_badges,
    file_colors,
    drag_and_drop,
    debugger,
    version_control,
    trial_widget,
    recent_projects,
]


def ui_keys(c):
    keys = {}
    for group in GROUPS:
        keys.update(group(c))
    return keys
