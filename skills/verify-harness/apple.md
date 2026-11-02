# Apple-platform recipe

Measured on Xcode 27 with an iOS app on the Simulator (NovelReader pilot, 2026-11). When the Xcode major version changes, re-check flags against `xcodebuild -help`, `xcrun simctl help`, and `xcrun xcresulttool help`.

## Instance

- A dedicated Simulator named `<App> Verify`, created on first `launch`. During the interview, list existing ones (`xcrun simctl list devices`): Simulators the user keeps for screenshots, performance, or manual testing stay untouched.
- Choose the device type first, then the newest runtime whose `supportedDeviceTypes` includes it (`xcrun simctl list runtimes -j`). The newest runtime can be device-specific: iOS 27.1 shipped for iPhone Duo only, and creating an iPhone 17 Pro on it failed with `Incompatible device` (code 403).
- `xcrun simctl bootstatus <udid> -b` boots and waits. Record whether this run booted it; `cleanup` shuts down only that case.
- The first `launch` (create, boot, build) took over 3 minutes. Say so in the generated skill so the next agent does not read it as a hang.

## Build and install

- `xcodebuild build-for-testing -project <App>.xcodeproj` (or `-workspace`) `-scheme <scheme> -destination "platform=iOS Simulator,id=<udid>" -derivedDataPath <ignored dir>/DerivedData`, with the log written to the evidence directory.
- Products: the app at `Build/Products/Debug-iphonesimulator/<App>.app`, the test plan at `Build/Products/<scheme>_*iphonesimulator*.xctestrun`. Install with `xcrun simctl install <udid> <app>`.
- `doctor` compares `CFBundleShortVersionString` and `CFBundleVersion` of the installed app (`xcrun simctl get_app_container <udid> <bundle-id> app`) with the built one.

## Seed and state

- `xcrun simctl get_app_container <udid> <bundle-id> data` is the data container. Seed by writing the files the app reads, with the app terminated, using the repo's fixture generator when one exists.
- `state <label>` copies the persisted files into the evidence directory; diff the before and after copies for data-writing changes.

## Drive

`simctl` cannot tap. Options, in order:

1. **Existing XCUITest**: `xcodebuild test-without-building -xctestrun <file> -destination "platform=iOS Simulator,id=<udid>" -resultBundlePath <evidence>/<label>.xcresult -parallel-testing-enabled NO -only-testing:<Target>/<Class>/<method>`.
2. **New XCUITest** in the UI test target. With file-system synchronized groups (`PBXFileSystemSynchronizedRootGroup` in the project file) a new `.swift` file compiles without a project edit. Rebuild with `launch`, not `--skip-build`.
3. **Deep link**, when the app declares one (`CFBundleURLTypes`, `onOpenURL`, `application(_:open:options:)`): `xcrun simctl openurl <udid> <url>`.
4. **Launch state**: `xcrun simctl launch --terminate-running-process <udid> <bundle-id> <args…>`, then `shot`.
5. **Exploration** with sim-use, below.

Launch arguments:

- `-AppleLanguages "(zh-Hant)" -AppleLocale zh_TW` pins the UI language. Tests that match localized labels depend on it; new tests pass it explicitly.
- `-<key> <value>` overrides a `UserDefaults` key through the argument domain. Values arrive as strings, so a key read with `as? Bool` ignores `NO`; use the settings UI for those.

Before writing selectors, reuse the existing UI tests' helpers: how they dismiss first-run or migration alerts, which accessibility identifiers exist, and how they flip SwiftUI `Toggle` rows. A tap at a `Toggle` row's center does not flip it; tap the switch near the trailing edge.

## Verdict

- `xcodebuild` prints `** TEST EXECUTE SUCCEEDED **` and exits 0 when every selected test skipped. Judge from `xcrun xcresulttool get test-results summary --path <bundle> --compact`: pass only when `failedTests == 0`, `skippedTests == 0`, and `passedTests > 0`. Older tests often call `XCTSkip` on missing data, so a skip means a broken precondition.
- `xcrun xcresulttool export attachments --path <bundle> --output-path <dir>` exports what tests attached (`XCTAttachment` with `lifetime = .keepAlways`). A test that attaches nothing proves only its assertions; pair it with `shot` when the proof needs a picture.
- Red-gate candidates: an existing test that skips on the fixture, or an `-only-testing` id that does not exist.

## Evidence capture

- Screenshot: `xcrun simctl io <udid> screenshot <file>.png`.
- Logs: `xcrun simctl spawn <udid> log show --last 2m --style compact --predicate 'process == "<App>"'`. During XCUITest this held about 17k lines of framework and accessibility noise in 2 minutes; keep the window short and grep for the app's own messages.

## Exploration with sim-use (optional)

[sim-use](https://github.com/lycorp-jp/sim-use) reads the accessibility tree and taps or swipes a booted Simulator without writing a test. Use it only when `command -v sim-use` finds it; installing it is the user's decision. It answers "does this reproduce, what does this screen do" quickly. A journey worth keeping becomes an XCUITest, which stays the proof of record.

- Right after boot, `sim-use ui` can report no frontmost application. Retry after a few seconds.
- `✓ Tap completed` means the event was sent. Read state before claiming a result or choosing the next step: `sim-use ui | grep '<id>'` for one element, `sim-use ui --json --no-raw` for values.
- Prefer `#<accessibility-id>` selectors. Coordinate taps and swipes carry no check of their own, so read after each one. For known flows, `sim-use ios batch --wait-timeout 5 --step "…" --step "…"` waits for each selector's element, which also checks the previous step.
- Releases ship breaking changes (0.16 changed the coordinate space). Record the tested version in the generated skill.

## Runtime gates

Watch apps and WatchConnectivity, BLE and other hardware, real iCloud/CloudKit, real StoreKit purchases and ad fill, background lifecycle timing, audio output, and device performance remain runtime gates on a real device, even when every Simulator drive passes.
