# AI guidance for `app` (renderer / UI)

## Styling: rely on the La Suite kit, keep custom CSS minimal

This app depends on two La Suite packages, both already installed:

- `@gouvfr-lasuite/cunningham-react` (v4.4.0) — form/widget library
- `@gouvfr-lasuite/ui-kit` (v0.28.1) — app-shell/navigation library

**Before writing a new custom CSS class or a new styled wrapper, check
whether one of these already provides it.** Verified findings (checked
against `node_modules/@gouvfr-lasuite/*/dist/index.d.ts` directly — don't
trust memory, re-check if a package version bumps):

### What `cunningham-react` actually exports

Form/data/modal widgets: `Alert`, `Button`, `Calendar`, `CalendarRange`,
`Checkbox`, `CheckboxGroup`, `ConfirmationModal`, `CunninghamProvider`,
`DataGrid`, `DataList`, `DatePicker`, `DateRangePicker`,
`DeleteConfirmationModal`, `Field`, `FileUploader`, `Input`,
`InputPassword`, `LabelledBox`, `Loader`, `MessageModal`, `Modal`,
`ModalInner`, `ModalProvider`, `Pagination`, `Popover`, `ProgressBar`,
`Radio`, `RadioGroup`, `Select`, `SelectMono`, `SelectMulti`,
`SimpleDataGrid`, `Switch`, `TextArea`, `Toast`, `ToastProvider`, `Tooltip`.

**No** `Box`, `Card`, `Flex`, `Avatar`, `Bubble`/message component, or
`Typography`/`Text` component exists here. This package is not a layout
system — don't go looking for one in it.

### What `ui-kit` actually exports

`MainLayout`, `LeftPanel`, `Header`, `Footer`, `Hero`, `HomeGutter`,
`HorizontalSeparator`, `VerticalSeparator`, `Icon`/`IconSvg`, `Badge`,
`Alert`, `Spinner`, `UserAvatar` (+ `getUserColor`, `getUserInitials`,
`AVATAR_COLORS`), `UserRow`, `UserMenu`, `DropdownMenu`, `ContextMenu`,
`TreeView`/`TreeViewItem`, `SmartScroller`, `AudioPlayer`/`VideoPlayer`,
`FilePreview`/`ImageViewer`/`PreviewMessage`, `CustomTabs`, `QuickSearch*`,
`FeedbackForm`, `ShareModal*`, `LanguagePicker`, `Filter`, `SearchFilter`.

**No** `Box`, `Card`, `List`, or chat bubble/message component exists here
either. `UserAvatar`, `Badge`, `Spinner`, and `HorizontalSeparator` are the
pieces most likely to be reusable in chat UI.

**Conclusion, confirmed by reading the reference project
(`suitenumerique/conversations`, cloned at
`C:\Users\Camille\Documents\Git\conversations`) — it hits the exact same
wall:** neither package ships a general layout primitive or a chat-bubble
component. The reference project's own answer was to hand-roll one small
shared `Box`/`Text` primitive (styled-components based, at
`src/frontend/apps/conversations/src/components/Box.tsx` /`Text.tsx`) and
reuse the kits only for actual widgets (`Button`, `Modal`, `Loader`,
`HorizontalSeparator`, `UserAvatar`, `Badge`). It did **not** eliminate
custom CSS for bubbles/flex layout — nobody has solved that for us. So:

- **Do** reach for a kit component first for anything widget-shaped:
  buttons, inputs, loaders/spinners, avatars, badges, separators, modals.
- **Don't** invent a custom class for something a kit component already
  does (e.g. don't build a spinner div — use `Loader` from
  `cunningham-react` or `Spinner` from `ui-kit`).
- **Do** accept that layout containers and bubble-style elements need their
  own minimal CSS — there's nothing to import for that. Keep it small: one
  class per structural role, no BEM modifier classes — use a `data-*`
  attribute for variants instead (e.g. `data-role="user"` selected via
  `.chat-message[data-role='user']`) rather than
  `.chat-message--user`/`.chat-message--assistant`.

### Design tokens — use the CSS custom properties, don't hardcode values

`ui-kit`'s stylesheet (imported once in `main.tsx` via
`@gouvfr-lasuite/ui-kit/style`) defines CSS custom properties across three
namespaces. Always prefer these over hardcoded colors/spacing/font sizes:

- `--c--globals--spacings--*` (e.g. `--md`, `--sm`) — spacing scale
- `--c--theme--colors--*` (e.g. `--greyscale-100`, `--primary-200`) — theme
  colors, `--c--theme--font--sizes--*` — font sizes
- `--c--contextuals--*` — semantic/contextual tokens, e.g.
  `--c--contextuals--background--surface--primary/secondary/tertiary`,
  `--c--contextuals--background--semantic--{brand,error,info,neutral,success,warning}--{primary,secondary,tertiary}[-hover]`,
  `--c--contextuals--background--palette--{blue-1,blue-2,brand,brown,gray,green,orange,pink,purple,red,yellow}--{primary,secondary,tertiary}`,
  `--c--contextuals--border--*`
- `--c--components--*` — per-component tokens, e.g. `--c--components--button--*`,
  `--c--components--badge--*`, `--c--components--alert--*`

These are richer than what's currently used in `styles/app.css` — check
here before adding a new hardcoded color or spacing value.

### Current state

`src/renderer/src/styles/app.css` follows this: one small stylesheet, no
BEM modifiers (uses `data-role` for the message-bubble variant), and the
chat "sending" indicator uses `Loader` from `cunningham-react` instead of a
hand-rolled dots animation. See
`src/renderer/src/features/chat/components/ChatWindow.tsx` for the pattern
to follow when adding new chat UI.

See also `docs/architecture-reference-conversations.md` for the broader
folder-structure rationale this app follows.
