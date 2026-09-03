import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "dandadan.theme-control"

  property string home: Quickshell.env("HOME")
  property string bgLink: home + "/.local/state/omarchy/current/background"
  property string activeBgPath: ""
  property string activeIndex: "01"
  property string activeVibe: "Okarun & Turbo Granny Golden Spark"

  function updateWallpaperInfo() {
    var raw = bgFile.text().trim()
    var path = raw
    if (!path) path = root.activeBgPath
    root.activeBgPath = path

    var match = path.match(/([0-9]{2,3})\.(png|jpg|jpeg)/i)
    if (match) {
      root.activeIndex = match[1]
    }
    try {
      var data = JSON.parse(highlightsFile.text())
      var key = root.activeIndex.length === 3 && root.activeIndex.charAt(0) === '0'
        ? root.activeIndex.substring(1)
        : root.activeIndex
      if (data && data[key] && data[key].vibe) {
        root.activeVibe = data[key].vibe
      }
    } catch (e) {}
  }

  FileView {
    id: bgFile
    path: root.bgLink
    watchChanges: true
    onLoaded: root.updateWallpaperInfo()
    onFileChanged: { reload(); root.updateWallpaperInfo() }
  }

  FileView {
    id: highlightsFile
    path: root.home + "/.local/state/omarchy/current/theme/wallpaper_highlights.json"
    watchChanges: true
    onLoaded: root.updateWallpaperInfo()
  }

  Component.onCompleted: updateWallpaperInfo()

  function injectPanel() {
    var target = panelLoader.item
    if (!target) return
    if ("bar" in target) target.bar = root.bar
    if ("settings" in target) target.settings = root.settings
    if ("anchorItem" in target) target.anchorItem = button
    if ("hostWidget" in target) target.hostWidget = root
    if ("widget" in target) target.widget = root
  }

  function togglePanel() {
    if (panelLoader.item && panelLoader.item.toggle) panelLoader.item.toggle()
  }

  readonly property bool opened: panelLoader.item ? panelLoader.item.opened === true : false

  function open() {
    if (panelLoader.item && panelLoader.item.open) panelLoader.item.open()
  }

  function close() {
    if (panelLoader.item && panelLoader.item.close) panelLoader.item.close()
  }

  onBarChanged: injectPanel()
  onSettingsChanged: injectPanel()

  IpcHandler {
    target: "dandadan.theme-control"

    function open(): void { root.open() }
    function close(): void { root.close() }
    function show(): void { root.open() }
    function hide(): void { root.close() }
    function toggle(): void { root.togglePanel() }
    function next(): void { Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "next"]) }
    function prev(): void { Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "prev"]) }
    function random(): void { Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "random"]) }
  }

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.vertical ? "" : "󰄛 " + root.activeIndex
    active: root.opened
    tooltipText: "Dandadan Theme Control (" + root.activeVibe + ")\nLeft-Click: Open Theme Control Center\nRight-Click: Next Wallpaper\nScroll: Cycle Wallpapers"
    horizontalMargin: 8.5
    verticalPadding: 6

    onWheelMoved: function(delta) {
      if (delta > 0) {
        Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "next"])
      } else if (delta < 0) {
        Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "prev"])
      }
    }

    onPressed: function(btn) {
      if (btn === Qt.RightButton) {
        Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "next"])
      } else if (btn === Qt.MiddleButton) {
        Quickshell.execDetached(["python3", root.home + "/.local/state/omarchy/current/theme/scripts/cycle-wallpaper.py", "random"])
      } else {
        root.togglePanel()
      }
    }

    Column {
      visible: root.vertical
      anchors.centerIn: parent
      spacing: 2

      Text {
        text: "󰄛"
        font.family: button.fontFamily
        font.pixelSize: Style.font.body
        color: button.foreground
        horizontalAlignment: Text.AlignHCenter
      }

      Text {
        text: root.activeIndex
        font.family: button.fontFamily
        font.pixelSize: Style.font.caption
        font.bold: true
        color: Color.accent
        horizontalAlignment: Text.AlignHCenter
      }
    }
  }

  Loader {
    id: panelLoader
    active: true
    source: Qt.resolvedUrl("Panel.qml")
    visible: false
    onLoaded: root.injectPanel()
  }
}
