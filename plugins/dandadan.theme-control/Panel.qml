import QtQuick
import QtQuick.Layouts
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Ui

Panel {
  id: root
  moduleName: "dandadan.theme-control"
  ipcTarget: "dandadan.theme-control"
  manageIpc: false

  property var anchorItem: null
  property var hostWidget: null
  property var widget: null
  readonly property var barIdentity: hostWidget || root

  readonly property string home: Quickshell.env("HOME")
  readonly property string themeDir: home + "/.local/state/omarchy/current/theme"
  readonly property string currentBg: widget ? widget.activeBgPath : ""
  readonly property string currentIdx: widget ? widget.activeIndex : "01"
  readonly property string currentVibe: widget ? widget.activeVibe : "Dandadan Vibe"

  property string musicStatus: "Stopped"
  property string musicTitle: "No media playing"
  property string musicArtist: "Idle"
  property int animTick: 0

  Process {
    id: musicProc
    command: ["python3", root.themeDir + "/scripts/dandadan-music.py", "status"]
    stdout: StdioCollector {
      onStreamFinished: {
        try {
          var d = JSON.parse(text)
          root.musicStatus = d.status || "Stopped"
          root.musicTitle = d.title || "No media playing"
          root.musicArtist = d.artist || "Idle"
        } catch (e) {}
      }
    }
  }

  Timer {
    interval: 2000
    running: root.opened
    repeat: true
    triggeredOnStart: true
    onTriggered: {
      root.animTick = (root.animTick + 1) % 100
      if (!musicProc.running) musicProc.running = true
    }
  }

  KeyboardPanel {
    id: panel
    anchorItem: root.anchorItem
    owner: root.barIdentity
    bar: root.bar
    open: root.opened
    centerOnBar: true
    contentWidth: Style.space(380)
    contentHeight: Style.space(530)

    Rectangle {
      anchors.fill: parent
      color: Color.popups.background
      radius: Style.radius(12)
      clip: true

      // Gradient accent border overlay
      Rectangle {
        anchors.fill: parent
        color: "transparent"
        radius: Style.radius(12)
        border.color: Color.accent
        border.width: Math.max(1, Style.space(1.5))
      }

      ColumnLayout {
        anchors.fill: parent
        anchors.margins: Style.space(16)
        spacing: Style.space(12)

        // Header Row
        RowLayout {
          Layout.fillWidth: true
          spacing: Style.space(10)

          Rectangle {
            width: Style.space(38)
            height: Style.space(38)
            radius: Style.radius(8)
            color: Qt.rgba(Color.accent.r, Color.accent.g, Color.accent.b, 0.22)
            border.color: Color.accent
            border.width: 1

            Text {
              anchors.centerIn: parent
              text: "󰄛"
              font.family: Style.font.family
              font.pixelSize: Style.font.title
              color: Color.accent
            }
          }

          ColumnLayout {
            Layout.fillWidth: true
            spacing: 2

            Text {
              text: "DANDADAN THEME CONTROL"
              font.family: Style.font.family
              font.pixelSize: Style.font.caption
              font.letterSpacing: 1.5
              font.bold: true
              color: Color.accent
            }

            Text {
              Layout.fillWidth: true
              text: "Wallpaper #" + root.currentIdx + " · " + root.currentVibe
              font.family: Style.font.family
              font.pixelSize: Style.font.body
              color: Color.popups.text
              elide: Text.ElideRight
            }
          }

          // Close button
          Rectangle {
            width: Style.space(26)
            height: Style.space(26)
            radius: Style.radius(6)
            color: closeMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.12) : "transparent"

            Text {
              anchors.centerIn: parent
              text: "✕"
              font.pixelSize: Style.font.caption
              color: Color.popups.text
            }

            MouseArea {
              id: closeMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: root.close()
            }
          }
        }

        // Active Wallpaper Preview Thumbnail
        Rectangle {
          Layout.fillWidth: true
          Layout.preferredHeight: Style.space(140)
          radius: Style.radius(8)
          color: Color.background
          clip: true
          border.color: Qt.rgba(Color.accent.r, Color.accent.g, Color.accent.b, 0.4)
          border.width: 1

          Image {
            id: bgPreview
            anchors.fill: parent
            fillMode: Image.PreserveAspectCrop
            source: root.currentBg ? "file://" + root.currentBg : ""
            cache: false
            asynchronous: true
          }

          // Badge on bottom-right of preview
          Rectangle {
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.margins: 8
            width: badgeText.implicitWidth + 14
            height: Style.space(22)
            radius: Style.radius(4)
            color: Qt.rgba(0.06, 0.07, 0.1, 0.85)
            border.color: Color.accent
            border.width: 1

            Text {
              id: badgeText
              anchors.centerIn: parent
              text: "WALLPAPER " + root.currentIdx + " / 52"
              font.family: Style.font.family
              font.pixelSize: Style.font.caption * 0.9
              font.bold: true
              font.letterSpacing: 1
              color: Color.accent
            }
          }
        }

        // Color Palette Swatches Bar
        RowLayout {
          Layout.fillWidth: true
          spacing: Style.space(6)

          Repeater {
            model: [
              Color.accent,
              Color.popups.border,
              Color.background,
              "#384166",
              "#7E859E",
              "#FFFFFF"
            ]

            Rectangle {
              required property color modelData
              Layout.fillWidth: true
              height: Style.space(18)
              radius: Style.radius(4)
              color: modelData
              border.color: Qt.rgba(1, 1, 1, 0.15)
              border.width: 1
            }
          }
        }

        // Anime Music Player Card & Visualizer
        Rectangle {
          Layout.fillWidth: true
          height: Style.space(64)
          radius: Style.radius(8)
          color: Qt.rgba(0, 0, 0, 0.3)
          border.color: root.musicStatus === "Playing" ? Color.accent : Qt.rgba(1, 1, 1, 0.12)
          border.width: 1

          RowLayout {
            anchors.fill: parent
            anchors.margins: Style.space(8)
            spacing: Style.space(10)

            // Equalizer Bars Box
            Rectangle {
              width: Style.space(36)
              height: Style.space(36)
              radius: Style.radius(6)
              color: root.musicStatus === "Playing" ? Qt.rgba(Color.accent.r, Color.accent.g, Color.accent.b, 0.22) : Qt.rgba(1, 1, 1, 0.06)
              border.color: root.musicStatus === "Playing" ? Color.accent : "transparent"
              border.width: 1

              Row {
                anchors.centerIn: parent
                spacing: 2.5

                Repeater {
                  model: 4
                  Rectangle {
                    required property int index
                    width: 3
                    height: root.musicStatus === "Playing" ? (6 + (((index + root.animTick) * 7) % 16)) : 4
                    radius: 1
                    color: root.musicStatus === "Playing" ? Color.accent : Color.popups.text

                    Behavior on height {
                      NumberAnimation { duration: 160 }
                    }
                  }
                }
              }
            }

            // Track & Artist Info
            ColumnLayout {
              Layout.fillWidth: true
              spacing: 1

              Text {
                Layout.fillWidth: true
                text: root.musicTitle
                font.family: Style.font.family
                font.pixelSize: Style.font.caption
                font.bold: true
                color: Color.popups.text
                elide: Text.ElideRight
              }

              Text {
                Layout.fillWidth: true
                text: (root.musicArtist || "Dandadan Music") + (root.musicStatus === "Playing" ? " · 󰐊 Playing" : "")
                font.family: Style.font.family
                font.pixelSize: Style.font.caption * 0.85
                color: Qt.darker(Color.popups.text, 1.4)
                elide: Text.ElideRight
              }
            }

            // Playback Controls
            RowLayout {
              spacing: Style.space(4)

              // Prev
              Rectangle {
                width: Style.space(26)
                height: Style.space(26)
                radius: Style.radius(4)
                color: mPrevMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.15) : "transparent"

                Text {
                  anchors.centerIn: parent
                  text: "󰒮"
                  font.family: Style.font.family
                  font.pixelSize: Style.font.caption
                  color: Color.popups.text
                }

                MouseArea {
                  id: mPrevMouse
                  anchors.fill: parent
                  hoverEnabled: true
                  cursorShape: Qt.PointingHandCursor
                  onClicked: {
                    Quickshell.execDetached(["python3", root.themeDir + "/scripts/dandadan-music.py", "prev"])
                    musicProc.running = true
                  }
                }
              }

              // Play / Pause
              Rectangle {
                width: Style.space(30)
                height: Style.space(30)
                radius: Style.radius(6)
                color: Color.accent

                Text {
                  anchors.centerIn: parent
                  text: root.musicStatus === "Playing" ? "󰏤" : "󰐊"
                  font.family: Style.font.family
                  font.pixelSize: Style.font.body
                  color: "#FFFFFF"
                }

                MouseArea {
                  id: mPlayMouse
                  anchors.fill: parent
                  hoverEnabled: true
                  cursorShape: Qt.PointingHandCursor
                  onClicked: {
                    Quickshell.execDetached(["python3", root.themeDir + "/scripts/dandadan-music.py", "toggle"])
                    musicProc.running = true
                  }
                }
              }

              // Next
              Rectangle {
                width: Style.space(26)
                height: Style.space(26)
                radius: Style.radius(4)
                color: mNextMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.15) : "transparent"

                Text {
                  anchors.centerIn: parent
                  text: "󰒭"
                  font.family: Style.font.family
                  font.pixelSize: Style.font.caption
                  color: Color.popups.text
                }

                MouseArea {
                  id: mNextMouse
                  anchors.fill: parent
                  hoverEnabled: true
                  cursorShape: Qt.PointingHandCursor
                  onClicked: {
                    Quickshell.execDetached(["python3", root.themeDir + "/scripts/dandadan-music.py", "next"])
                    musicProc.running = true
                  }
                }
              }
            }
          }
        }

        // Action Buttons Grid
        GridLayout {
          Layout.fillWidth: true
          columns: 2
          rowSpacing: Style.space(8)
          columnSpacing: Style.space(8)

          // Button 1: Next Wallpaper
          Rectangle {
            Layout.fillWidth: true
            height: Style.space(38)
            radius: Style.radius(6)
            color: btnNextMouse.containsMouse ? Color.accent : Qt.rgba(Color.accent.r, Color.accent.g, Color.accent.b, 0.15)
            border.color: Color.accent
            border.width: 1

            RowLayout {
              anchors.centerIn: parent
              spacing: Style.space(6)
              Text {
                text: "󰒭"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: btnNextMouse.containsMouse ? "#FFFFFF" : Color.popups.text
              }
              Text {
                text: "Next Wallpaper"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                font.bold: true
                color: btnNextMouse.containsMouse ? "#FFFFFF" : Color.popups.text
              }
            }

            MouseArea {
              id: btnNextMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: {
                Quickshell.execDetached(["python3", root.themeDir + "/scripts/cycle-wallpaper.py", "next"])
              }
            }
          }

          // Button 2: Previous Wallpaper
          Rectangle {
            Layout.fillWidth: true
            height: Style.space(38)
            radius: Style.radius(6)
            color: btnPrevMouse.containsMouse ? Color.accent : Qt.rgba(Color.accent.r, Color.accent.g, Color.accent.b, 0.15)
            border.color: Color.accent
            border.width: 1

            RowLayout {
              anchors.centerIn: parent
              spacing: Style.space(6)
              Text {
                text: "󰒮"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: btnPrevMouse.containsMouse ? "#FFFFFF" : Color.popups.text
              }
              Text {
                text: "Previous Wallpaper"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                font.bold: true
                color: btnPrevMouse.containsMouse ? "#FFFFFF" : Color.popups.text
              }
            }

            MouseArea {
              id: btnPrevMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: {
                Quickshell.execDetached(["python3", root.themeDir + "/scripts/cycle-wallpaper.py", "prev"])
              }
            }
          }

          // Button 3: Random Vibe
          Rectangle {
            Layout.fillWidth: true
            height: Style.space(38)
            radius: Style.radius(6)
            color: btnRandMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.16) : Qt.rgba(1, 1, 1, 0.06)
            border.color: Qt.rgba(1, 1, 1, 0.12)
            border.width: 1

            RowLayout {
              anchors.centerIn: parent
              spacing: Style.space(6)
              Text {
                text: "󰄛"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
              Text {
                text: "Random Vibe"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
            }

            MouseArea {
              id: btnRandMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: {
                Quickshell.execDetached(["python3", root.themeDir + "/scripts/cycle-wallpaper.py", "random"])
              }
            }
          }

          // Button 4: Visual Gallery Picker
          Rectangle {
            Layout.fillWidth: true
            height: Style.space(38)
            radius: Style.radius(6)
            color: btnPickMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.16) : Qt.rgba(1, 1, 1, 0.06)
            border.color: Qt.rgba(1, 1, 1, 0.12)
            border.width: 1

            RowLayout {
              anchors.centerIn: parent
              spacing: Style.space(6)
              Text {
                text: "󰋩"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
              Text {
                text: "Gallery Picker"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
            }

            MouseArea {
              id: btnPickMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: {
                root.close()
                Quickshell.execDetached(["omarchy-menu-images"])
              }
            }
          }

          // Button 5: Toggle Bar Transparency
          Rectangle {
            Layout.fillWidth: true
            height: Style.space(38)
            radius: Style.radius(6)
            color: btnTransMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.16) : Qt.rgba(1, 1, 1, 0.06)
            border.color: Qt.rgba(1, 1, 1, 0.12)
            border.width: 1

            RowLayout {
              anchors.centerIn: parent
              spacing: Style.space(6)
              Text {
                text: "󰔎"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
              Text {
                text: "Toggle Bar Alpha"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
            }

            MouseArea {
              id: btnTransMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: {
                Quickshell.execDetached(["omarchy-shell", "shell", "toggleBarTransparency"])
              }
            }
          }

          // Button 6: Recolor Desktop & Sync
          Rectangle {
            Layout.fillWidth: true
            height: Style.space(38)
            radius: Style.radius(6)
            color: btnRecolorMouse.containsMouse ? Qt.rgba(1, 1, 1, 0.16) : Qt.rgba(1, 1, 1, 0.06)
            border.color: Qt.rgba(1, 1, 1, 0.12)
            border.width: 1

            RowLayout {
              anchors.centerIn: parent
              spacing: Style.space(6)
              Text {
                text: ""
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
              Text {
                text: "Recolor Desktop"
                font.family: Style.font.family
                font.pixelSize: Style.font.body
                color: Color.popups.text
              }
            }

            MouseArea {
              id: btnRecolorMouse
              anchors.fill: parent
              hoverEnabled: true
              cursorShape: Qt.PointingHandCursor
              onClicked: {
                Quickshell.execDetached(["python3", root.themeDir + "/update_wallpaper_colors.py"])
              }
            }
          }
        }
      }
    }
  }
}
