from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QMenu
from typing import Callable, Optional
from app.models.chat_model import Chat
from app.models.user_model import User
from datetime import datetime

def attach_messaging(ui, current_user_getter: Optional[Callable[[], Optional[int]]] = None):
    """
    Attach messaging behavior to `ui`.
    ui must provide: chatsList (QListWidget), messagesList (QListWidget), messageInput (QLineEdit),
                     sendMessageButton (QPushButton), newChatButton (QPushButton)
    current_user_getter: callable returning current user id (int) or None. If None, ui.set_current_user(id) can be used.
    Adds methods on ui:
      - set_current_user(user_id)
      - populate_chats()
      - populate_messages(chat_id)
      - send_message()
      - new_chat()
      - edit_message(message_id)
      - delete_message(message_id)
    """
    # minimal checks
    if not all(hasattr(ui, name) for name in ("chatsList", "messagesList", "messageInput", "sendMessageButton", "newChatButton")):
        return

    ui._messaging_current_user = None
    ui._messaging_current_chat = None

    def _get_current_user():
        if callable(current_user_getter):
            try:
                v = current_user_getter()
                if v is not None:
                    return int(v)
            except Exception:
                pass
        # fallback to ui attribute if set externally
        return getattr(ui, "current_user_id", None)

    def set_current_user(user_id):
        ui._messaging_current_user = int(user_id) if user_id is not None else None
        try:
            populate_chats()
        except Exception:
            pass
    ui.set_current_user = set_current_user

    def populate_chats():
        ui.chatsList.clear()
        uid = _get_current_user()
        if not uid:
            ui.chatsList.addItem("No user selected")
            return
        try:
            rows = Chat.get_chats(uid) or []
        except Exception:
            rows = []
        for r in rows:
            name = (f"{r.get('first_name') or ''} {r.get('last_name') or ''}".strip()
                    or r.get('other_username') or f"User {r.get('other_user_id')}")
            last = (r.get('last_message') or "")[:80]
            label = f"{name} — {last}"
            if int(r.get('unread_count') or 0):
                label = f"[{r.get('unread_count')}] {label}"
            it = QtWidgets.QListWidgetItem(label)
            it.setData(QtCore.Qt.UserRole, r.get('chat_id'))
            ui.chatsList.addItem(it)
    ui.populate_chats = populate_chats

    def _resolve_sender_name(sender_id):
        try:
            u = User.get_by_id(sender_id)
            if u:
                return f"{u.first_name} {u.last_name}".strip() or u.username or str(sender_id)
        except Exception:
            pass
        return str(sender_id)

    def populate_messages(chat_id):
        ui.messagesList.clear()
        if not chat_id:
            ui.messagesList.addItem("Select a chat")
            return
        ui._messaging_current_chat = int(chat_id)
        try:
            msgs = Chat.get_messages(chat_id) or []
        except Exception:
            msgs = []
        for m in msgs:
            # m may be dict from JSON or DB row; normalize access
            mid = int(m.get("id") or m.get("id", 0))
            sender = m.get("sender_id") or m.get("sender") or m.get("sender_id")
            sender_name = _resolve_sender_name(sender)
            text = ""
            if m.get("deleted") or m.get("deleted", False):
                text = "[deleted]"
                ts = m.get("deleted_at") or ""
                display = f"{sender_name}: {text} ({ts})"
            else:
                txt = m.get("message") or ""
                edited = m.get("edited") or False
                ts = m.get("sent_at") or m.get("created_at") or ""
                display = f"{sender_name}: {txt}" + (" (edited)" if edited else "") + (f" — {ts}" if ts else "")
            item = QtWidgets.QListWidgetItem(display)
            # store message meta on item for edit/delete
            item.setData(QtCore.Qt.UserRole, {"message_id": mid, "sender_id": int(sender)})
            ui.messagesList.addItem(item)
        # mark messages read (best-effort)
        try:
            cur_user = _get_current_user()
            if cur_user:
                Chat.mark_messages_read(chat_id, cur_user)
                populate_chats()
        except Exception:
            pass
    ui.populate_messages = populate_messages

    def _on_chat_selected():
        item = ui.chatsList.currentItem()
        if not item:
            return
        cid = item.data(QtCore.Qt.UserRole)
        try:
            populate_messages(cid)
        except Exception:
            pass
    ui.chatsList.itemSelectionChanged.connect(_on_chat_selected)

    def send_message():
        item = ui.chatsList.currentItem()
        if not item:
            QMessageBox.warning(None, "Send Message", "Select a chat first.")
            return
        chat_id = item.data(QtCore.Qt.UserRole)
        text = ui.messageInput.text().strip()
        if not text:
            return
        try:
            cur_user = _get_current_user()
            ok = Chat.send_message(chat_id, cur_user, text)
        except Exception:
            ok = False
        if ok:
            ui.messageInput.clear()
            try:
                populate_messages(chat_id)
                populate_chats()
            except Exception:
                pass
        else:
            QMessageBox.warning(None, "Send Message", "Failed to send message.")
    ui.sendMessageButton.clicked.connect(send_message)
    ui.send_message = send_message

    def new_chat():
        username, ok = QInputDialog.getText(None, "New Chat", "Enter username to start chat:")
        if not ok or not username.strip():
            return
        other = User.get_by_username(username.strip())
        if not other:
            QMessageBox.warning(None, "New Chat", "User not found.")
            return
        try:
            cur_user = _get_current_user()
            cid = Chat.get_or_create_chat(cur_user, other.user_id)
        except Exception:
            cid = None
        if cid:
            populate_chats()
            # select created chat
            for i in range(ui.chatsList.count()):
                it = ui.chatsList.item(i)
                if it.data(QtCore.Qt.UserRole) == cid:
                    ui.chatsList.setCurrentRow(i)
                    break
    ui.newChatButton.clicked.connect(new_chat)
    ui.new_chat = new_chat

    # Context menu for messages: edit/delete for sender only
    def _on_message_context(point):
        item = ui.messagesList.itemAt(point)
        if not item:
            return
        meta = item.data(QtCore.Qt.UserRole) or {}
        mid = meta.get("message_id")
        sender_id = meta.get("sender_id")
        cur_user = _get_current_user()
        menu = QMenu(ui.messagesList)
        if cur_user and int(sender_id) == int(cur_user):
            edit_act = menu.addAction("Edit")
            delete_act = menu.addAction("Delete")
            act = menu.exec_(ui.messagesList.mapToGlobal(point))
            if act == edit_act:
                _edit_message(mid, cur_user)
            elif act == delete_act:
                _delete_message(mid, cur_user)
        else:
            menu.addAction("No actions available").setDisabled(True)
            menu.exec_(ui.messagesList.mapToGlobal(point))

    def _edit_message(message_id, cur_user):
        # load current text (best-effort)
        current_text = ""
        # try fetch single message
        try:
            msgs = Chat.get_messages(ui._messaging_current_chat) or []
            for m in msgs:
                if int(m.get("id")) == int(message_id):
                    current_text = m.get("message") or ""
                    break
        except Exception:
            pass
        new_text, ok = QInputDialog.getText(None, "Edit Message", "Edit message:", text=current_text)
        if not ok:
            return
        try:
            ok2 = Chat.edit_message(message_id, cur_user, new_text)
        except Exception:
            ok2 = False
        if ok2:
            populate_messages(ui._messaging_current_chat)
            populate_chats()
        else:
            QMessageBox.warning(None, "Edit Message", "Failed to edit message.")

    def _delete_message(message_id, cur_user):
        reply = QMessageBox.question(None, "Delete Message", "Delete this message?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        try:
            ok = Chat.delete_message(message_id, cur_user)
        except Exception:
            ok = False
        if ok:
            populate_messages(ui._messaging_current_chat)
            populate_chats()
        else:
            QMessageBox.warning(None, "Delete Message", "Failed to delete message.")

    # attach context menu
    ui.messagesList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    ui.messagesList.customContextMenuRequested.connect(_on_message_context)

    # initial population if UI has current_user_id already
    try:
        if getattr(ui, "current_user_id", None):
            set_current_user(ui.current_user_id)
    except Exception:
        pass
