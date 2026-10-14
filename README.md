<div align="center">

**English** / [Русский](README_ru.md)

# EwokVPN

</div>

EwokVPN is a multi-platform proxy and VPN client built on the [sing-box](https://github.com/SagerNet/sing-box) tool-chain. It supports VLESS, VMess, Reality, TUIC, Hysteria, WireGuard, SSH and other protocols, and imports sing-box, V2Ray, Clash and Clash Meta subscriptions.

## Based on Hiddify

EwokVPN is a fork of **[Hiddify](https://github.com/hiddify/hiddify-app)** by the Hiddify team. All credit for the original app goes to Hiddify and its contributors.

- Original project: https://github.com/hiddify/hiddify-app
- Original license: [Hiddify Extended GNU General Public License v3](https://github.com/hiddify/hiddify-app/blob/main/LICENSE.md)
- Core library: [hiddify-core](https://github.com/hiddify/hiddify-core), used unmodified and distributed under [its own license](https://github.com/hiddify/hiddify-core/blob/v3/LICENSE.md)

EwokVPN is not affiliated with or endorsed by Hiddify.

## Changes from Hiddify

The list below is kept up to date with every change this fork makes to the original code.

### Rebranding to meet the license terms

- Renamed the app to EwokVPN on every platform: app name, window title, tray tooltip, Android notification, iOS VPN profile name and desktop entries.
- Changed the Android application ID to `com.ewokvpn.app`, the Linux application ID to `com.ewokvpn.app`, and the Windows installer ID and MSIX identity so EwokVPN installs alongside Hiddify instead of replacing it.
- Renamed the Windows executable to `EwokVPN.exe` and the Linux executable and package to `ewokvpn`.
- Pointed the GitHub, license, release and update-check links to this repository and reset `appcast.xml`.
- Replaced "Made with ❤️ by Hiddify" on the intro screen with "Based on Hiddify" in all languages.
- Renamed release files to `EwokVPN-*` and updated the release notes template, issue template and download shortcuts.
- Turned off automatic builds on push; the CI workflow now runs manually. Releases are still built only by GitHub Actions when a `v*` tag is pushed. WinGet and Microsoft Store publishing, which use Hiddify's store identifiers, now run manually only.
- Replaced this README and removed the translated Hiddify READMEs.

The app's features are unchanged from Hiddify.

## Download

Releases are published on the [Releases](https://github.com/HunterEwok/ewokvpn-hiddify-app/releases) page and are built only by GitHub Actions.

## Building

See [CONTRIBUTING.md](CONTRIBUTING.md) for the build steps inherited from Hiddify.

## Acknowledgements

- [Hiddify](https://github.com/hiddify/hiddify-app) and [hiddify-core](https://github.com/hiddify/hiddify-core)
- [sing-box](https://github.com/SagerNet/sing-box), [sing-box for Android](https://github.com/SagerNet/sing-box-for-android), [sing-box for Apple](https://github.com/SagerNet/sing-box-for-apple)
- [Clash](https://github.com/Dreamacro/clash), [Clash Meta](https://github.com/MetaCubeX/Clash.Meta), [FClash](https://github.com/Fclash/Fclash)
- [Vazirmatn font by Saber Rastikerdar](https://github.com/rastikerdar/vazirmatn)
- [Other dependencies](./pubspec.yaml)

## License

EwokVPN is distributed under the same license as Hiddify, the [Hiddify Extended GNU General Public License v3](LICENSE.md), including its additional conditions: the source stays open as a GitHub fork of Hiddify, releases are built with GitHub Actions, and the app may not be used commercially without the Hiddify team's written consent.
