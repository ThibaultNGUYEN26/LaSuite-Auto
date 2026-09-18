"""Drive tree-listing specialist."""

from typing import Any

from agent.base import DelegationContext, SpecialistAgent
from agent.errors import DriveAPIError
from services.drive import list_drive_items


def _render_drive_overview(result: dict[str, Any]) -> str:
    """Render a concise user-facing overview without another model round-trip."""
    items = result.get("items")
    if not isinstance(items, list):
        return "I couldn't read the Drive listing."

    top_level = [
        item
        for item in items
        if isinstance(item, dict) and item.get("depth") == 0
    ]
    descendant_counts: dict[str, int] = {}
    for item in items:
        if not isinstance(item, dict):
            continue
        path = item.get("path")
        if isinstance(path, list) and len(path) > 1 and isinstance(path[0], str):
            descendant_counts[path[0]] = descendant_counts.get(path[0], 0) + 1

    folders: list[str] = []
    files: list[str] = []
    for item in top_level:
        name = item.get("title") or item.get("filename") or "Untitled"
        if not isinstance(name, str):
            name = str(name)
        url = item.get("url_permalink")
        display_name = f"[{name}]({url})" if isinstance(url, str) and url else name
        if item.get("type") == "folder":
            child_count = descendant_counts.get(name, 0)
            suffix = (
                f" — {child_count} item{'s' if child_count != 1 else ''} found inside"
                if result.get("recursive") is True
                else ""
            )
            folders.append(f"- {display_name}{suffix}")
        else:
            files.append(f"- {display_name}")

    if result.get("recursive") is True:
        heading = (
            f"Here's your Drive overview: **{result.get('count', len(items))} items "
            f"scanned**, including **{result.get('top_level_count', len(top_level))} "
            "at the top level**."
        )
    else:
        heading = (
            f"Here's your Drive overview: **{result.get('top_level_count', len(top_level))} "
            "top-level items**."
        )
    sections = [heading]
    if folders:
        sections.extend(("### Folders", "\n".join(folders)))
    if files:
        sections.extend(("### Files", "\n".join(files)))
    limitation = result.get("limitation")
    if isinstance(limitation, str) and limitation:
        sections.append(limitation)
    return "\n\n".join(sections)


class DriveListItemsAgent(SpecialistAgent):
    name = "drive_list_items"
    description = (
        "List the authenticated user's files and folders in La Suite Drive, including "
        "nested folder contents by default. Use this to discover item UUIDs before "
        "reading a Drive PDF. This reads Drive, not the computer's local filesystem."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "purpose": {
                "type": "string",
                "enum": ["answer_user", "locate_item"],
                "description": (
                    "Use answer_user when the user's request is only to browse or "
                    "list Drive contents. Use locate_item when this listing is an "
                    "intermediate step before reading, changing, or downloading an item."
                ),
            },
            "limit": {"type": "integer", "minimum": 1, "maximum": 500},
            "recursive": {
                "type": "boolean",
                "description": (
                    "Defaults to false for a quick user overview and true when "
                    "locating an item for another operation."
                ),
            },
            "max_depth": {
                "type": "integer",
                "minimum": 0,
                "maximum": 5,
                "description": "Maximum traversal depth. The hard limit is 5.",
            },
            "folder_id": {"type": "string", "format": "uuid"},
        },
        "required": ["purpose"],
        "additionalProperties": False,
    }

    def __init__(self, base_url: str, session_id: str | None) -> None:
        self.base_url = base_url
        self.session_id = session_id

    def execute(self, arguments: dict[str, Any], context: DelegationContext) -> dict[str, Any]:
        del context
        limit = arguments.get("limit", 100)
        if not isinstance(limit, int) or isinstance(limit, bool):
            raise DriveAPIError("limit must be an integer")
        recursive = arguments.get(
            "recursive", arguments.get("purpose") != "answer_user"
        )
        if not isinstance(recursive, bool):
            raise DriveAPIError("recursive must be a boolean")
        max_depth = arguments.get("max_depth", 5)
        if not isinstance(max_depth, int) or isinstance(max_depth, bool):
            raise DriveAPIError("max_depth must be an integer")
        folder_id = arguments.get("folder_id")
        if folder_id is not None and not isinstance(folder_id, str):
            raise DriveAPIError("folder_id must be a string")
        result = list_drive_items(
            self.base_url, self.session_id or "", limit=limit, recursive=recursive,
            max_depth=max_depth, folder_id=folder_id,
        )
        if arguments.get("purpose") == "answer_user":
            result["_assistant_response"] = _render_drive_overview(result)
        return result
