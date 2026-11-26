import json
import os
import sys
import urllib.request


def call_service(method: str, payload: dict) -> dict:
    addr = os.environ.get("ANTIGRAVITY_LS_ADDRESS", "")
    token = os.environ.get("ANTIGRAVITY_CSRF_TOKEN", "")
    if not addr or not token:
        raise RuntimeError("Missing ANTIGRAVITY_LS_ADDRESS or ANTIGRAVITY_CSRF_TOKEN")
    req = urllib.request.Request(
        f"http://{addr}/product.v1.ConversationService/{method}",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Connect-Protocol-Version": "1",
            "x-antigravity-csrf-token": token,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw.strip() else {}


def has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cid = os.environ.get("ANTIGRAVITY_CONVERSATION_ID", "")
    if not cid:
        print("SKIP: missing ANTIGRAVITY_CONVERSATION_ID")
        return 0

    if len(sys.argv) > 1:
        new_title = " ".join(sys.argv[1:]).strip()
        if not new_title:
            print("ERROR: empty title argument")
            return 1
        call_service(
            "UpdateConversation",
            {"conversationId": cid, "annotations": {"title": new_title}},
        )
        verify = call_service("GetConversation", {"conversationId": cid})
        actual = verify.get("annotations", {}).get("title", "")
        print(f"UPDATED: {actual}")
        return 0

    convo = call_service("GetConversation", {"conversationId": cid})
    if convo.get("metadata", {}).get("parentConversationId"):
        print("SKIP_SUBAGENT")
        return 0

    title = convo.get("annotations", {}).get("title", "")
    summary = convo.get("state", {}).get("summary", "").replace("\n", " ").strip()
    if title and has_cjk(title):
        print(f"OK: {title}")
        return 0

    print(f"NEEDS_ZH: title={title!r} summary={summary[:120]!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
