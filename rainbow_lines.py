import sublime
import sublime_plugin

MAX_SCOPES = 8
REGION_PREFIX = "rl_"
LINE_BUFFER = 200

_FALLBACK_SCOPES = ["region.cyanish", "region.orangish"]


def _settings():
    return sublime.load_settings("rainbow_lines.sublime-settings")


def _get_scopes():
    s = _settings()
    palettes = s.get("palettes", {})
    name = s.get("palette", "rainbow")
    return palettes.get(name, _FALLBACK_SCOPES)


def _is_enabled(view):
    return view.settings().get("rl_enabled", _settings().get("enabled", True))


def _apply_colors(view):
    if not _is_enabled(view):
        return
    if view.is_loading():
        return

    scopes = _get_scopes()
    count = len(scopes)

    visible = view.visible_region()
    first_row, _ = view.rowcol(visible.begin())
    last_row, _ = view.rowcol(visible.end())

    buf_first = max(0, first_row - LINE_BUFFER)
    buf_last = min(last_row + LINE_BUFFER, view.rowcol(view.size())[0])

    scope_regions = [[] for _ in range(count)]
    for row in range(buf_first, buf_last + 1):
        line = view.line(view.text_point(row, 0))
        scope_regions[row % count].append(line)

    for i, regions in enumerate(scope_regions):
        view.add_regions(REGION_PREFIX + str(i), regions, scopes[i], flags=sublime.DRAW_NO_OUTLINE)


def _clear_colors(view):
    for i in range(MAX_SCOPES):
        view.erase_regions(REGION_PREFIX + str(i))


def _reload_all_views():
    for w in sublime.windows():
        for v in w.views():
            _clear_colors(v)
            _apply_colors(v)


class RainbowLinesListener(sublime_plugin.EventListener):

    def on_load_async(self, view):
        _apply_colors(view)

    def on_activated_async(self, view):
        _apply_colors(view)
        view.settings().set("rl_poll_active", True)
        sublime.set_timeout_async(lambda: self._poll_scroll(view), 80)

    def on_deactivated_async(self, view):
        view.settings().set("rl_poll_active", False)

    def on_modified_async(self, view):
        sublime.set_timeout_async(lambda: _apply_colors(view), 150)

    def _poll_scroll(self, view):
        if not view.settings().get("rl_poll_active"):
            return
        pos = view.viewport_position()
        prev = tuple(view.settings().get("rl_last_pos", [-1.0, -1.0]))
        if abs(pos[0] - prev[0]) > 0.5 or abs(pos[1] - prev[1]) > 0.5:
            view.settings().set("rl_last_pos", list(pos))
            _apply_colors(view)
        interval = _settings().get("poll_interval_ms", 80)
        sublime.set_timeout_async(lambda: self._poll_scroll(view), interval)


class RainbowLinesToggleCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        currently_enabled = _is_enabled(self.view)
        self.view.settings().set("rl_enabled", not currently_enabled)
        if currently_enabled:
            _clear_colors(self.view)
        else:
            _apply_colors(self.view)


class RainbowLinesToggleGlobalCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        s = _settings()
        currently_enabled = s.get("enabled", True)
        s.set("enabled", not currently_enabled)
        sublime.save_settings("rainbow_lines.sublime-settings")
        for w in sublime.windows():
            for v in w.views():
                v.settings().erase("rl_enabled")
                if currently_enabled:
                    _clear_colors(v)
                else:
                    _apply_colors(v)


class RainbowLinesSelectPaletteCommand(sublime_plugin.WindowCommand):
    def run(self):
        s = _settings()
        palettes = list(s.get("palettes", {}).keys())
        current = s.get("palette", "rainbow")
        idx = palettes.index(current) if current in palettes else 0

        def on_done(i):
            if i == -1:
                return
            s.set("palette", palettes[i])
            sublime.save_settings("rainbow_lines.sublime-settings")
            _reload_all_views()

        self.window.show_quick_panel(palettes, on_done, selected_index=idx)


class RainbowLinesCyclePaletteCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        s = _settings()
        palettes = list(s.get("palettes", {}).keys())
        if not palettes:
            return
        current = s.get("palette", "rainbow")
        if current in palettes:
            nxt = palettes[(palettes.index(current) + 1) % len(palettes)]
        else:
            nxt = palettes[0]
        s.set("palette", nxt)
        sublime.save_settings("rainbow_lines.sublime-settings")
        _reload_all_views()
