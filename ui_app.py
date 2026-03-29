# * Copyright (C) 2023 Zenon Xiu


import os
import tkinter as tk
from tkinter import ttk, messagebox

from extract_xml import extract_reg_entries


SYS_REG_DIR = os.path.join(os.path.dirname(__file__), "sys_reg_xml")


def discover_xml_files(base_dir):
    files = []
    for root, _, filenames in os.walk(base_dir):
        for name in filenames:
            if name.lower().endswith(".xml"):
                files.append(os.path.join(root, name))
    return sorted(files)


def register_name_from_path(path):
    basename = os.path.basename(path)
    if "-" in basename:
        reg_part = basename.split("-", 1)[1]
    else:
        reg_part = basename
    return os.path.splitext(reg_part)[0].lower()


def main():
    root = tk.Tk()
    root.title("ARM System Register Decoder")
    root.geometry("900x600")

    # Left pane: file list
    left_frame = ttk.Frame(root, padding=10)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    ttk.Label(left_frame, text="Register XML files").pack(anchor=tk.W)

    search_var = tk.StringVar()
    search_entry = ttk.Entry(left_frame, textvariable=search_var)
    search_entry.pack(fill=tk.X, pady=(0, 6))

    file_listbox = tk.Listbox(left_frame, width=40, height=25, exportselection=False)
    file_scroll = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=file_listbox.yview)
    file_listbox.configure(yscrollcommand=file_scroll.set)
    file_listbox.pack(side=tk.LEFT, fill=tk.Y)
    file_scroll.pack(side=tk.LEFT, fill=tk.Y)

    all_files = []

    def render_files():
        file_listbox.delete(0, tk.END)
        query = search_var.get().strip().lower()
        for path in all_files:
            rel = os.path.relpath(path, SYS_REG_DIR)
            reg = register_name_from_path(path)
            if query and query not in reg and query not in rel.lower():
                continue
            file_listbox.insert(tk.END, rel)

    def refresh_files():
        all_files.clear()
        all_files.extend(discover_xml_files(SYS_REG_DIR))
        render_files()

    search_var.trace_add("write", lambda *args: render_files())
    refresh_files()

    # Right pane: controls and output
    right_frame = ttk.Frame(root, padding=10)
    right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    input_frame = ttk.Frame(right_frame)
    input_frame.pack(fill=tk.X, pady=(0, 10))

    ttk.Label(input_frame, text="Hex value (e.g. 0x1234 or 1234)").pack(anchor=tk.W)
    value_var = tk.StringVar()
    value_entry = ttk.Entry(input_frame, textvariable=value_var)
    value_entry.pack(fill=tk.X)

    # Feature toggles
    features_frame = ttk.LabelFrame(right_frame, text="Feature flags (toggle FEAT_xxx)")
    features_frame.pack(fill=tk.X, pady=(0, 10))

    feature_vars = {}
    feature_buttons = []
    decoded_entries = []

    def selected_features():
        return {name for name, var in feature_vars.items() if var.get()}

    def clear_feature_buttons():
        nonlocal feature_buttons
        for btn in feature_buttons:
            btn.destroy()
        feature_buttons = []
        feature_vars.clear()

    def build_feature_buttons(features):
        clear_feature_buttons()
        for feat in sorted(features):
            var = tk.BooleanVar(value=False)
            chk = ttk.Checkbutton(features_frame, text=feat, variable=var, command=render_table)
            chk.pack(side=tk.LEFT, padx=2, pady=2)
            feature_vars[feat] = var
            feature_buttons.append(chk)

    # Table for decoded fields
    table_frame = ttk.Frame(right_frame)
    table_frame.pack(fill=tk.BOTH, expand=True)

    columns = ("bits", "name", "value", "meaning")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    tree.heading("bits", text="Bits")
    tree.heading("name", text="Field")
    tree.heading("value", text="Value")
    tree.heading("meaning", text="Meaning")
    tree.column("bits", width=90, anchor=tk.CENTER)
    tree.column("name", width=140, anchor=tk.W)
    tree.column("value", width=170, anchor=tk.W)
    tree.column("meaning", width=520, anchor=tk.W, stretch=True)

    table_scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=table_scroll.set)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    table_scroll.pack(side=tk.LEFT, fill=tk.Y)

    # Detail pane for full meaning text
    detail_frame = ttk.LabelFrame(right_frame, text="Selected field details")
    detail_frame.pack(fill=tk.BOTH, expand=False, pady=(8, 0))
    detail_text = tk.Text(detail_frame, height=6, wrap=tk.WORD)
    detail_scroll = ttk.Scrollbar(detail_frame, orient=tk.VERTICAL, command=detail_text.yview)
    detail_text.configure(yscrollcommand=detail_scroll.set, state=tk.DISABLED)
    detail_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    detail_scroll.pack(side=tk.LEFT, fill=tk.Y)

    row_details = {}

    def show_detail(item_id):
        detail_text.configure(state=tk.NORMAL)
        detail_text.delete("1.0", tk.END)
        text = row_details.get(item_id, "Select a row to see details.")
        detail_text.insert(tk.END, text)
        detail_text.configure(state=tk.DISABLED)

    def on_select(event=None):
        selection = tree.selection()
        if selection:
            show_detail(selection[0])

    tree.bind("<<TreeviewSelect>>", on_select)

    def render_table():
        tree.delete(*tree.get_children())
        row_details.clear()
        active_feats = selected_features()
        for entry in decoded_entries:
            meaning_feats = entry.get("meaning_features", set()) or set()
            if meaning_feats and not meaning_feats.issubset(active_feats):
                continue

            bits = f"{entry['msb']}:{entry['lsb']}"
            field_name = entry.get("name", "")
            value_bin = entry.get("bit_value_bin", "")
            value_bits = entry.get("field_value_text", "")
            value_hex = f"0x{entry['bit_value']:x}"
            value_display = value_bin
            if value_bits:
                value_display = f"{value_bin} ({value_bits})"
            value_display = f"{value_display} = {value_hex}"

            meaning = entry.get("meaning_text") or entry.get("description") or ""
            condition = entry.get("condition_text") or ""
            full_meaning = meaning
            if condition:
                full_meaning = f"{meaning}\nCondition: {condition}" if meaning else f"Condition: {condition}"

            item_id = tree.insert("", tk.END, values=(bits, field_name, value_display, meaning))
            row_details[item_id] = full_meaning

        # reset detail pane when table refreshes
        show_detail(None)

    def decode():
        selection = file_listbox.curselection()
        if not selection:
            messagebox.showinfo("Select file", "Please choose a system register XML file from the list.")
            return

        rel_path = file_listbox.get(selection[0])
        file_path = os.path.join(SYS_REG_DIR, rel_path)
        if not os.path.isfile(file_path):
            messagebox.showerror("Missing file", f"Cannot find file: {file_path}")
            return

        value_text = value_var.get().strip()
        if not value_text:
            messagebox.showinfo("Missing value", "Enter a hex value to decode.")
            return

        try:
            value_int = int(value_text, 16)
        except ValueError:
            messagebox.showerror("Invalid value", "Hex value is not valid.")
            return

        reg_name = register_name_from_path(file_path)

        try:
            entries = extract_reg_entries(file_path, reg_name, value_int)
        except Exception as exc:
            messagebox.showerror("Decode failed", str(exc))
            return

        decoded_entries.clear()
        decoded_entries.extend(entries)

        # Build feature switches from all mentions
        all_features = set()
        for item in decoded_entries:
            feats = item.get("meaning_features") or set()
            all_features |= feats
        build_feature_buttons(all_features)

        render_table()

    decode_button = ttk.Button(input_frame, text="Decode", command=decode)
    decode_button.pack(anchor=tk.W, pady=(5, 0))

    refresh_button = ttk.Button(input_frame, text="Refresh file list", command=refresh_files)
    refresh_button.pack(anchor=tk.W, pady=(5, 0))

    root.mainloop()


if __name__ == "__main__":
    main()
