# -*- coding: utf-8 -*-
"""F3-01 (wp60) — validator + nghiem thu cho schema protocol da phien.

TEP NAY CO HAI CHE DO, co y de trong MOT tep vi write set cua packet #60 chi co mot duong dan:

  * che do VALIDATE (entrypoint that):
        python .github/checks/protocol_schema_test.py --schema S --document D [--format ...]
        python .github/checks/protocol_schema_test.py --check-form .github/ISSUE_TEMPLATE/mission.yml
        python .github/checks/protocol_schema_test.py --dump-document D
        python .github/checks/protocol_schema_test.py --trace-required --schema S --document D
    ma thoat: 0 hop le · 1 KHONG hop le · 2 khong doc/giai duoc dau vao (fail-closed).

  * che do SUITE (khong doi so): chay toan bo ca nghiem thu, in `PASS/FAIL <ten ca>` roi `N/N dat`.

Doctrine giong `.githooks/eol_policy_test.py`: MOI ca cua suite goi entrypoint QUA `subprocess` va doc
MA THOAT truc tiep tu tien trinh do. Truong `"ok"` trong JSON chi de nguoi doc; no KHONG phai cong -
mot cong xanh nho `rc=0` troi qua pipe la cong co the bi lua.

Phu thuoc: CHI thu vien chuan Python. Khong `jsonschema`, khong mang, chay duoc offline tren ca Windows
lan Linux. Ba manh ben trong deu tu viet vi khong duoc phep them phu thuoc:

  1. bo phan tich YAML tap con — dung du cho khoi YAML cua protocol va cua evidence that. No FAIL-CLOSED:
     gap TAB, anchor/alias/tag, nhieu document hay khoa lap thi NEM LOI dich danh chu khong doan y dinh.
     No cung KHONG duoc de dai hon YAML that: `#` sau khoang trang van la binh luan, y het moi bo phan
     tich YAML khac, nen tai lieu qua duoc o day cung qua duoc o cho khac.
  2. bo trich khoi ```yaml dau tien trong mot than Markdown — dung duong nay cho ca evidence that lan
     body ma Issue Form sinh ra.
  3. bo kiem JSON Schema tap con: type/required/properties/additionalProperties/items/contains/minItems/
     minLength/pattern/minimum/maximum/enum/const/oneOf/anyOf/allOf/if-then-else/$defs/$ref (ke ca $ref
     CHEO TEP). Loi mang duong dan JSON Pointer — do la thu lam cho «chi dung cho thieu `copyable_prompt`»
     kiem duoc. No FAIL-CLOSED tren TU KHOA LA: mot bo kiem tap con im lang bo qua tu khoa no khong hieu
     thi mot rang buoc go nham ten se bien mat ma cong van xanh, nen tu khoa la lam rc=2.

Schema o `.github/schemas/` CHI hinh thuc hoa tap TRUONG da normative trong `docs/PROTOCOL_DA_PHIEN.md`.
Tep nay khong dinh nghia them truong nao; `--check-form` con doi chieu NGUOC Issue Form ve chinh cac khoi
YAML trong protocol, nen mot ban sao bi lech se lam suite do thay vi im lang.

CHUA NOI VAO CI: `.github/workflows/ci.yml` thuoc write set cua #52, nen suite nay chua chay tu dong.
Viec noi day hoan sang #52 hoac F3-06 - ghi ra day de no la mot khoan no CO TEN, khong phai mot cho hong
im lang.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Suite dung lai chinh cay nguon nay; dung de `__pycache__` roi vao `.github/checks/`.
sys.dont_write_bytecode = True

_HERE = Path(__file__).resolve()
_ROOT = _HERE.parent.parent.parent
_SCHEMA_DIR = _ROOT / ".github" / "schemas"
_FORM_DIR = _ROOT / ".github" / "ISSUE_TEMPLATE"
_PROTOCOL_REL = Path("docs") / "PROTOCOL_DA_PHIEN.md"

RC_OK = 0
RC_INVALID = 1
RC_LOAD = 2


# ─────────────────────────────────────────────────────────────────────────────
# 1. YAML tap con — fail-closed
# ─────────────────────────────────────────────────────────────────────────────

class YamlError(Exception):
    pass


_RE_INT = re.compile(r"^-?[0-9]+$")
_RE_FLOAT = re.compile(r"^-?[0-9]+\.[0-9]+$")


def _indent_of(s):
    n = 0
    for ch in s:
        if ch != " ":
            break
        n += 1
    return n


def _strip_comment(line):
    """Cat binh luan theo DUNG nghia YAML: `#` mo binh luan khi o dau dong hoac sau khoang trang.

    Co y KHONG khoan hong hon YAML that. `- keep Mission #54 open` bi YAML cat thanh `keep Mission`;
    neu bo phan tich nay giu nguyen ca cau thi mot tai lieu do o day se HONG o moi cho khac, va suite
    se dang bao dam mot dieu khong dung.
    """
    out = []
    quote = None
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if quote is not None:
            if ch == "\\" and quote == '"' and i + 1 < n:
                out.append(ch)
                out.append(line[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = None
            out.append(ch)
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "#" and (i == 0 or line[i - 1] in " \t"):
            break
        out.append(ch)
        i += 1
    return "".join(out)


class _Cursor:
    def __init__(self, text):
        if "\t" in text:
            raise YamlError("YAML chua ky tu TAB - tu choi thay vi doan y dinh thut le")
        self.lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        for n, ln in enumerate(self.lines, 1):
            if ln.strip() in ("---", "..."):
                raise YamlError("YAML nhieu document (dong %d: %r) khong duoc ho tro" % (n, ln.strip()))
        self.i = 0

    def peek(self):
        """(indent, body) cua dong co nghia ke tiep. Bo qua dong trong va dong binh luan."""
        j = self.i
        while j < len(self.lines):
            body = _strip_comment(self.lines[j]).rstrip()
            if body.strip() == "":
                j += 1
                continue
            self.i = j
            return _indent_of(body), body.strip()
        self.i = j
        return None

    def advance(self):
        self.i += 1


def _unescape_double(s):
    out = []
    i = 0
    while i < len(s):
        if s[i] == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            out.append({"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\"}.get(nxt, nxt))
            i += 2
            continue
        out.append(s[i])
        i += 1
    return "".join(out)


def _scalar(s):
    s = s.strip()
    if s[:1] in ("&", "*", "!"):
        raise YamlError("anchor/alias/tag YAML khong duoc ho tro: %r" % s)
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return _unescape_double(s[1:-1])
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1].replace("''", "'")
    if s == "" or s == "~" or s.lower() == "null":
        return None
    if s in ("true", "True"):
        return True
    if s in ("false", "False"):
        return False
    if _RE_INT.match(s):
        return int(s)
    if _RE_FLOAT.match(s):
        return float(s)
    return s


def _skip_ws(s, i):
    while i < len(s) and s[i] == " ":
        i += 1
    return i


def _flow_value(s, i, stops):
    if i >= len(s):
        raise YamlError("cau truc flow ket thuc dot ngot")
    if s[i] in "[{":
        return _parse_flow(s, i)
    if s[i] in "\"'":
        q = s[i]
        j = i + 1
        buf = []
        closed = False
        while j < len(s):
            if s[j] == "\\" and q == '"' and j + 1 < len(s):
                buf.append(s[j:j + 2])
                j += 2
                continue
            if s[j] == q:
                closed = True
                break
            buf.append(s[j])
            j += 1
        if not closed:
            raise YamlError("chuoi trich dan khong dong trong cau truc flow")
        return _scalar(q + "".join(buf) + q), j + 1
    j = i
    while j < len(s) and s[j] not in stops:
        j += 1
    return _scalar(s[i:j]), j


def _parse_flow(s, i):
    if s[i] == "[":
        i += 1
        out = []
        while True:
            i = _skip_ws(s, i)
            if i >= len(s):
                raise YamlError("day flow khong dong")
            if s[i] == "]":
                return out, i + 1
            val, i = _flow_value(s, i, "],")
            out.append(val)
            i = _skip_ws(s, i)
            if i < len(s) and s[i] == ",":
                i += 1
                continue
            if i < len(s) and s[i] == "]":
                return out, i + 1
            raise YamlError("day flow thieu dau phay hoac dau dong")
    if s[i] == "{":
        i += 1
        out = {}
        while True:
            i = _skip_ws(s, i)
            if i >= len(s):
                raise YamlError("anh xa flow khong dong")
            if s[i] == "}":
                return out, i + 1
            key, i = _flow_value(s, i, ":,}")
            i = _skip_ws(s, i)
            if i >= len(s) or s[i] != ":":
                raise YamlError("anh xa flow thieu dau hai cham sau khoa %r" % (key,))
            i = _skip_ws(s, i + 1)
            val, i = _flow_value(s, i, ",}")
            key = key if isinstance(key, str) else str(key)
            if key in out:
                raise YamlError("khoa lap trong anh xa flow: %r" % key)
            out[key] = val
            i = _skip_ws(s, i)
            if i < len(s) and s[i] == ",":
                i += 1
                continue
            if i < len(s) and s[i] == "}":
                return out, i + 1
            raise YamlError("anh xa flow thieu dau phay hoac dau dong")
    raise YamlError("khong phai cau truc flow: %r" % s[i:])


def _scalar_or_flow(s):
    if s[:1] in ("[", "{"):
        val, pos = _parse_flow(s, 0)
        if s[pos:].strip():
            raise YamlError("con du lieu thua sau cau truc flow: %r" % s[pos:])
        return val
    return _scalar(s)


def _split_key(body):
    """Tra (key, phan_con_lai) hoac None neu dong khong phai cap khoa.

    Dau hai cham ket thuc khoa la dau hai cham DUOC THEO SAU boi khoang trang hoac ket dong. Nho vay
    `pr: https://github.com/...`, `issue_projection: state:reviewing` va `issued_at: 2026-08-08T09:21:20Z`
    deu tach dung - ba dang nay co that trong evidence da land.
    """
    if body[:1] in ('"', "'"):
        q = body[0]
        j = 1
        closed = False
        while j < len(body):
            if body[j] == "\\" and q == '"':
                j += 2
                continue
            if body[j] == q:
                closed = True
                break
            j += 1
        if not closed:
            raise YamlError("khoa trich dan khong dong: %r" % body)
        key = _scalar(body[:j + 1])
        rest = body[j + 1:]
        if not rest.startswith(":"):
            raise YamlError("thieu dau hai cham sau khoa trich dan: %r" % body)
        return key, rest[1:].strip()
    for j, ch in enumerate(body):
        if ch == ":" and (j + 1 == len(body) or body[j + 1] == " "):
            return body[:j].strip(), body[j + 1:].strip()
    return None


def _block_scalar(cur, indent, header):
    style = header[0]
    chomp = ""
    for ch in header[1:]:
        if ch in "-+":
            chomp = ch
        elif ch.isdigit():
            raise YamlError("chi so thut le tuong minh cua block scalar khong duoc ho tro: %r" % header)
        elif ch.strip() != "":
            raise YamlError("header block scalar la: %r" % header)
    body = []
    child = None
    while cur.i < len(cur.lines):
        raw = cur.lines[cur.i]
        if raw.strip() == "":
            body.append("")
            cur.i += 1
            continue
        ind = _indent_of(raw)
        if ind <= indent:
            break
        if child is None:
            child = ind
        if ind < child:
            break
        body.append(raw[child:])
        cur.i += 1
    while body and body[-1] == "":
        body.pop()
    text = "\n".join(body) if style == "|" else " ".join(body)
    if chomp != "-":
        text += "\n"
    return text


def _parse_value(cur, indent, rest):
    rest = rest.strip()
    if rest[:1] in ("|", ">"):
        return _block_scalar(cur, indent, rest)
    if rest == "":
        head = cur.peek()
        if head is None:
            return None
        ind, body = head
        if ind > indent:
            return _parse_node(cur, ind)
        if ind == indent and (body == "-" or body.startswith("- ")):
            return _parse_seq(cur, indent)
        return None
    return _scalar_or_flow(rest)


def _parse_map(cur, indent):
    out = {}
    while True:
        head = cur.peek()
        if head is None:
            break
        ind, body = head
        if ind < indent:
            break
        if ind > indent:
            raise YamlError("thut le lech trong anh xa tai %r" % body)
        if body == "-" or body.startswith("- "):
            break
        pair = _split_key(body)
        if pair is None:
            raise YamlError("dong khong phai cap khoa: %r" % body)
        key, rest = pair
        if key in out:
            raise YamlError("khoa lap: %r" % key)
        cur.advance()
        out[key] = _parse_value(cur, indent, rest)
    return out


def _parse_seq(cur, indent):
    out = []
    while True:
        head = cur.peek()
        if head is None:
            break
        ind, body = head
        if ind < indent:
            break
        if ind > indent:
            raise YamlError("thut le lech trong day tai %r" % body)
        if not (body == "-" or body.startswith("- ")):
            break
        if body == "-":
            cur.advance()
            nxt = cur.peek()
            out.append(None if nxt is None or nxt[0] <= indent else _parse_node(cur, nxt[0]))
            continue
        off = 1
        while off < len(body) and body[off] == " ":
            off += 1
        inner = ind + off
        item = body[off:]
        # Cau truc flow phai duoc nhan dien TRUOC `_split_key`: trong `- {run_id: 1, ...}` dau hai cham
        # dau tien nam BEN TRONG anh xa flow, nen tach khoa truoc se de ra khoa rac `{run_id`.
        pair = None if item[:1] in ("[", "{") else _split_key(item)
        cur.advance()
        if pair is None:
            out.append(_scalar_or_flow(item))
            continue
        node = {pair[0]: _parse_value(cur, inner, pair[1])}
        while True:
            nxt = cur.peek()
            if nxt is None or nxt[0] != inner:
                break
            body2 = nxt[1]
            if body2 == "-" or body2.startswith("- "):
                break
            pair2 = _split_key(body2)
            if pair2 is None:
                raise YamlError("dong khong phai cap khoa trong phan tu day: %r" % body2)
            if pair2[0] in node:
                raise YamlError("khoa lap trong phan tu day: %r" % pair2[0])
            cur.advance()
            node[pair2[0]] = _parse_value(cur, inner, pair2[1])
        out.append(node)
    return out


def _parse_node(cur, indent):
    head = cur.peek()
    if head is None:
        return None
    body = head[1]
    if body == "-" or body.startswith("- "):
        return _parse_seq(cur, indent)
    return _parse_map(cur, indent)


def load_yaml(text):
    cur = _Cursor(text)
    head = cur.peek()
    if head is None:
        return None
    value = _parse_node(cur, head[0])
    if cur.peek() is not None:
        raise YamlError("con noi dung chua phan tich tu dong %d" % (cur.i + 1))
    return value


# ─────────────────────────────────────────────────────────────────────────────
# 2. Trich khoi ```yaml tu Markdown
# ─────────────────────────────────────────────────────────────────────────────

def extract_yaml_block(markdown, which=0):
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    found = 0
    i = 0
    while i < len(lines):
        if lines[i].strip() in ("```yaml", "~~~yaml"):
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() not in ("```", "~~~"):
                body.append(lines[i])
                i += 1
            if i >= len(lines):
                raise YamlError("khoi ```yaml khong dong")
            if found == which:
                return "\n".join(body)
            found += 1
        i += 1
    raise YamlError("khong tim thay khoi ```yaml thu %d trong than Markdown" % (which + 1))


# ─────────────────────────────────────────────────────────────────────────────
# 3. JSON Schema tap con
# ─────────────────────────────────────────────────────────────────────────────

class SchemaError(Exception):
    pass


_TYPE_TESTS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _type_name(v):
    for name, test in _TYPE_TESTS.items():
        if name != "number" and test(v):
            return name
    return type(v).__name__


# Tu khoa CHU THICH: khong khang dinh gi, bo qua duoc an toan.
_ANNOTATION_KEYWORDS = frozenset((
    "$schema", "$id", "$comment", "$defs", "title", "description", "examples", "default", "deprecated",
))

# Tu khoa KHANG DINH ma bo kiem nay thuc su cuong che.
_ASSERTION_KEYWORDS = frozenset((
    "$ref", "type", "const", "enum", "minLength", "pattern", "minimum", "maximum",
    "required", "properties", "additionalProperties", "minItems", "items", "contains",
    "allOf", "anyOf", "oneOf", "if", "then", "else",
))


class _Registry:
    def __init__(self, base_dir, main_name, main_doc):
        self.base = Path(base_dir)
        self.docs = {main_name: main_doc}

    def load(self, name):
        if name not in self.docs:
            path = self.base / name
            if not path.is_file():
                raise SchemaError("khong tim thay schema duoc $ref toi: %s" % name)
            try:
                self.docs[name] = json.loads(path.read_text(encoding="utf-8"))
            except ValueError as exc:
                raise SchemaError("schema %s khong phai JSON hop le: %s" % (name, exc))
        return self.docs[name]


def _ref_parts(ref, cur_file):
    file_part, _, pointer = ref.partition("#")
    return (file_part or cur_file), pointer


def _resolve(ref, cur_file, reg):
    name, pointer = _ref_parts(ref, cur_file)
    node = reg.load(name)
    for token in [t for t in pointer.split("/") if t]:
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or token not in node:
            raise SchemaError("khong giai duoc $ref: %s" % ref)
        node = node[token]
    return node, name, pointer


def _join(ptr, key):
    return "%s/%s" % (ptr, str(key).replace("~", "~0").replace("/", "~1"))


def _err(errs, ptr, keyword, message):
    errs.append({"path": ptr or "/", "keyword": keyword, "message": message})


def _in_enum(value, enum):
    for item in enum:
        if value is None or item is None:
            if value is None and item is None:
                return True
            continue
        if isinstance(value, bool) != isinstance(item, bool):
            continue
        if value == item:
            return True
    return False


def _branch_name(sub, cur_file, reg, fallback):
    node = sub
    if isinstance(sub, dict) and "$ref" in sub:
        try:
            node, _, pointer = _resolve(sub["$ref"], cur_file, reg)
        except SchemaError:
            return sub["$ref"]
        return (node.get("title") if isinstance(node, dict) else None) or pointer or sub["$ref"]
    return (node.get("title") if isinstance(node, dict) else None) or fallback


def _depth(errs):
    return max((e["path"].count("/") for e in errs), default=0)


def _check(value, schema, dptr, sfile, sptr, reg, errs, trace):
    if schema is True:
        return
    if schema is False:
        _err(errs, dptr, "false", "schema tu choi moi gia tri tai day")
        return
    if not isinstance(schema, dict):
        raise SchemaError("manh schema khong phai object/boolean tai %s%s" % (sfile, sptr))

    # FAIL-CLOSED tren tu khoa la. Mot bo kiem tap con BO QUA tu khoa no khong hieu la mot cong
    # co the bi lua im lang: viet `uniqueItems` hay go nham `containss` vao schema thi rang buoc
    # bien mat ma khong ai biet. O day tu khoa la lam rc=2, khong phai rc=0.
    unknown = sorted(set(schema) - _ANNOTATION_KEYWORDS - _ASSERTION_KEYWORDS)
    if unknown:
        raise SchemaError("tu khoa schema khong duoc ho tro tai %s%s: %s" % (sfile, sptr, ", ".join(unknown)))

    if "$ref" in schema:
        target, nfile, nptr = _resolve(schema["$ref"], sfile, reg)
        _check(value, target, dptr, nfile, nptr, reg, errs, trace)

    if "type" in schema:
        wanted = schema["type"]
        wanted = wanted if isinstance(wanted, list) else [wanted]
        for name in wanted:
            if name not in _TYPE_TESTS:
                raise SchemaError("kieu khong ho tro: %r" % name)
        if not any(_TYPE_TESTS[name](value) for name in wanted):
            _err(errs, dptr, "type", "kieu sai: can %s, gap %s" % ("|".join(wanted), _type_name(value)))
            return

    if "const" in schema and not _in_enum(value, [schema["const"]]):
        _err(errs, dptr, "const", "phai bang %s" % json.dumps(schema["const"], ensure_ascii=False))
    if "enum" in schema and not _in_enum(value, schema["enum"]):
        _err(errs, dptr, "enum", "gia tri %s khong thuoc tap cho phep %s"
             % (json.dumps(value, ensure_ascii=False), json.dumps(schema["enum"], ensure_ascii=False)))

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            _err(errs, dptr, "minLength", "chuoi ngan hon %d ky tu" % schema["minLength"])
        if "pattern" in schema and not re.search(schema["pattern"], value):
            _err(errs, dptr, "pattern", "khong khop mau %s" % schema["pattern"])

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            _err(errs, dptr, "minimum", "nho hon %s" % schema["minimum"])
        if "maximum" in schema and value > schema["maximum"]:
            _err(errs, dptr, "maximum", "lon hon %s" % schema["maximum"])

    if isinstance(value, dict):
        for field in schema.get("required", []):
            if trace is not None:
                trace.append({
                    "schema_file": sfile,
                    "schema_pointer": sptr + "/required",
                    "field": field,
                    "document_pointer": dptr,
                })
            if field not in value:
                _err(errs, _join(dptr, field), "required", "thieu truong bat buoc")
        props = schema.get("properties", {})
        extra_ok = schema.get("additionalProperties", True)
        for key in value:
            if key in props:
                _check(value[key], props[key], _join(dptr, key), sfile,
                       sptr + "/properties/" + str(key), reg, errs, trace)
            elif extra_ok is False:
                _err(errs, _join(dptr, key), "additionalProperties", "truong khong duoc khai bao")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            _err(errs, dptr, "minItems", "can it nhat %d phan tu" % schema["minItems"])
        if "items" in schema:
            for n, item in enumerate(value):
                _check(item, schema["items"], "%s/%d" % (dptr, n), sfile, sptr + "/items", reg, errs, trace)
        if "contains" in schema:
            # Probe: khong dong gop loi con vao `errs`, khong ghi trace `required` — mot phan tu
            # khop la du. Dung cho `review_axes` phai co CA HAI truc cua khoi §7.
            hit = False
            for item in value:
                probe = []
                _check(item, schema["contains"], dptr, sfile, sptr + "/contains", reg, probe, None)
                if not probe:
                    hit = True
                    break
            if not hit:
                _err(errs, dptr, "contains", "khong phan tu nao khop rang buoc `contains`")

    for n, sub in enumerate(schema.get("allOf", [])):
        _check(value, sub, dptr, sfile, "%s/allOf/%d" % (sptr, n), reg, errs, trace)

    for keyword in ("anyOf", "oneOf"):
        if keyword not in schema:
            continue
        branches = schema[keyword]
        results = []
        for n, sub in enumerate(branches):
            probe = []
            _check(value, sub, dptr, sfile, "%s/%s/%d" % (sptr, keyword, n), reg, probe, None)
            results.append(probe)
        passing = [n for n, probe in enumerate(results) if not probe]
        if (keyword == "anyOf" and passing) or (keyword == "oneOf" and len(passing) == 1):
            # Chay lai DUY NHAT nhanh da khop de trace ghi dung cac `required` THUC SU duoc cuong che.
            n = passing[0]
            _check(value, branches[n], dptr, sfile, "%s/%s/%d" % (sptr, keyword, n), reg, [], trace)
        elif not passing:
            # Nhanh «gan nhat» = it loi nhat, va khi hoa thi uu tien nhanh co loi SAU hon. Khong co ve
            # sau, mot nhanh `{"type": "string"}` chi bao «kieu sai» o goc se luon thang nhanh object
            # dang chi dich danh truong con thieu - tuc la thong bao huu ich bi nhanh vo dung che mat.
            n = min(range(len(results)), key=lambda k: (len(results[k]), -_depth(results[k])))
            name = _branch_name(branches[n], sfile, reg, "%s/%s/%d" % (sptr, keyword, n))
            for item in results[n]:
                errs.append(dict(item, message="[bien the %s] %s" % (name, item["message"])))
            _err(errs, dptr, keyword, "khong bien the nao khop; gan nhat la `%s`" % name)
        else:
            names = ", ".join("`%s`" % _branch_name(branches[k], sfile, reg,
                                                    "%s/%s/%d" % (sptr, keyword, k)) for k in passing)
            _err(errs, dptr, keyword, "khop nhieu hon mot bien the: %s" % names)

    if "if" in schema:
        probe = []
        _check(value, schema["if"], dptr, sfile, sptr + "/if", reg, probe, None)
        branch = "then" if not probe else "else"
        if branch in schema:
            _check(value, schema[branch], dptr, sfile, sptr + "/" + branch, reg, errs, trace)


def validate(document, schema, schema_dir, schema_name, want_trace=False):
    reg = _Registry(schema_dir, schema_name, schema)
    errs = []
    trace = [] if want_trace else None
    _check(document, schema, "", schema_name, "", reg, errs, trace)
    return errs, trace


# ─────────────────────────────────────────────────────────────────────────────
# 4. Doc tai lieu / Issue Form
# ─────────────────────────────────────────────────────────────────────────────

def _auto_format(path):
    suffix = Path(path).suffix.lower()
    if suffix == ".json":
        return "json"
    if suffix in (".md", ".markdown"):
        return "markdown"
    return "yaml"


def load_document(path, fmt):
    raw = Path(path).read_text(encoding="utf-8")
    if fmt == "json":
        return json.loads(raw)
    if fmt == "markdown":
        return load_yaml(extract_yaml_block(raw))
    return load_yaml(raw)


_FORM_SECTION = {
    "mission.yml": "### 3.1 Mission Issue",
    "work-packet.yml": "### 3.2 Work Packet Issue",
    "change-request.yml": "#### 3.1.1 Mission Change Request",
}

# §3.2 liet ke mot khoi THU HAI ma «dispatcher bo sung, khong cho nguoi dung/agent tu khai».
# Form packet phai KHONG moi nguoi dien nhung truong nay.
_FORM_FORBIDDEN = {
    "work-packet.yml": ("change_policy_sha", "effective_write_set", "required_checks", "land_obligations"),
}


def protocol_block(root, heading):
    path = Path(root) / _PROTOCOL_REL
    if not path.is_file():
        raise SchemaError("khong doc duoc protocol normative: %s" % path)
    lines = path.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    try:
        start = lines.index(heading)
    except ValueError:
        raise SchemaError("khong tim thay muc %r trong %s" % (heading, path))
    tail = []
    for line in lines[start + 1:]:
        stripped = line.lstrip("#")
        depth = len(line) - len(stripped)
        if depth and depth <= level and stripped.startswith(" "):
            break
        tail.append(line)
    return extract_yaml_block("\n".join(tail))


def _skeleton(obj, prefix=""):
    out = set()
    if isinstance(obj, dict):
        for key in obj:
            out.add(prefix + "/" + key)
            out |= _skeleton(obj[key], prefix + "/" + key)
    elif isinstance(obj, list):
        for item in obj:
            out |= _skeleton(item, prefix + "/[]")
    return out


def _form_spec_item(form):
    if not isinstance(form, dict) or not isinstance(form.get("body"), list):
        raise SchemaError("Issue Form thieu danh sach `body`")
    for item in form["body"]:
        if isinstance(item, dict) and item.get("id") == "spec":
            return item
    raise SchemaError("Issue Form khong co input `id: spec`")


def _render_form_body(form):
    """Dung lai than issue ma GitHub sinh ra tu form, du de di qua CUNG duong trich khoi ```yaml."""
    chunks = []
    for item in form.get("body", []):
        if not isinstance(item, dict) or item.get("type") == "markdown":
            continue
        attrs = item.get("attributes") or {}
        label = attrs.get("label") or item.get("id") or ""
        value = attrs.get("value") or ""
        chunks.append("### %s\n" % label)
        if attrs.get("render"):
            chunks.append("```%s\n%s\n```\n" % (attrs["render"], value.rstrip("\n")))
        else:
            chunks.append("%s\n" % value)
    return "\n".join(chunks)


def check_form(form_path, root):
    """Doi chieu NGUOC Issue Form ve khoi YAML normative trong protocol. Tra danh sach loi."""
    path = Path(form_path)
    name = path.name
    if name not in _FORM_SECTION:
        raise SchemaError("khong biet muc protocol tuong ung cho form %s" % name)
    form = load_yaml(path.read_text(encoding="utf-8"))
    spec = _form_spec_item(form)
    errs = []

    attrs = spec.get("attributes") or {}
    if (spec.get("validations") or {}).get("required") is not True:
        _err(errs, "/body/spec/validations/required", "required", "input `spec` phai la bat buoc")
    if attrs.get("render") != "yaml":
        _err(errs, "/body/spec/attributes/render", "const", "input `spec` phai `render: yaml`")

    raw_default = attrs.get("value")
    if not isinstance(raw_default, str) or not raw_default.strip():
        _err(errs, "/body/spec/attributes/value", "required", "input `spec` phai co khoi YAML mac dinh")
        return errs

    want = _skeleton(load_yaml(protocol_block(root, _FORM_SECTION[name])))

    # (a) khoi mac dinh cua form
    got_default = _skeleton(load_yaml(raw_default))
    # (b) chinh than issue ma GitHub se sinh ra, di qua bo trich ```yaml giong evidence that
    got_rendered = _skeleton(load_yaml(extract_yaml_block(_render_form_body(form))))

    for label, got in (("khoi mac dinh", got_default), ("than issue duoc sinh", got_rendered)):
        for missing in sorted(want - got):
            _err(errs, missing, "required", "%s thieu truong normative cua %s" % (label, _FORM_SECTION[name]))
        for extra in sorted(got - want):
            _err(errs, extra, "additionalProperties",
                 "%s co truong khong nam trong %s" % (label, _FORM_SECTION[name]))

    for banned in _FORM_FORBIDDEN.get(name, ()):
        if "/" + banned in got_default:
            _err(errs, "/" + banned, "forbidden",
                 "truong phai sinh do dispatcher bo sung, form khong duoc moi nguoi dung khai")
    return errs


# ─────────────────────────────────────────────────────────────────────────────
# 5. CLI
# ─────────────────────────────────────────────────────────────────────────────

def _emit(args, payload, rc):
    if getattr(args, "json", False):
        print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
    else:
        if payload.get("ok"):
            print("ok: %s" % payload.get("subject", ""))
        else:
            print("KHONG HOP LE: %s" % payload.get("subject", ""))
            for item in payload.get("errors", []):
                print("  %s  [%s] %s" % (item["path"], item["keyword"], item["message"]))
            if payload.get("load_error"):
                print("  loi doc dau vao: %s" % payload["load_error"])
    return rc


def _run_validate(args):
    schema_path = Path(args.schema)
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        document = load_document(args.document, args.format or _auto_format(args.document))
    except (OSError, ValueError, YamlError) as exc:
        return _emit(args, {"ok": False, "subject": str(args.document),
                            "errors": [], "load_error": "%s: %s" % (type(exc).__name__, exc)}, RC_LOAD)
    try:
        errs, trace = validate(document, schema, schema_path.parent, schema_path.name,
                               want_trace=args.trace_required)
    except SchemaError as exc:
        return _emit(args, {"ok": False, "subject": str(args.document),
                            "errors": [], "load_error": "SchemaError: %s" % exc}, RC_LOAD)
    payload = {
        "ok": not errs,
        "subject": str(args.document),
        "schema": schema_path.name,
        "errors": errs,
        "error_count": len(errs),
    }
    if args.trace_required:
        seen, pairs = set(), []
        for item in trace or []:
            key = (item["schema_file"], item["schema_pointer"], item["field"], item["document_pointer"])
            if key not in seen:
                seen.add(key)
                pairs.append(item)
        payload["required_pairs"] = pairs
    return _emit(args, payload, RC_OK if not errs else RC_INVALID)


def _run_check_form(args):
    try:
        errs = check_form(args.check_form, args.root or _ROOT)
    except (OSError, ValueError, YamlError, SchemaError) as exc:
        return _emit(args, {"ok": False, "subject": str(args.check_form),
                            "errors": [], "load_error": "%s: %s" % (type(exc).__name__, exc)}, RC_LOAD)
    return _emit(args, {"ok": not errs, "subject": str(args.check_form),
                        "errors": errs, "error_count": len(errs)},
                 RC_OK if not errs else RC_INVALID)


def _run_dump(args):
    try:
        document = load_document(args.dump_document, args.format or _auto_format(args.dump_document))
    except (OSError, ValueError, YamlError) as exc:
        return _emit(args, {"ok": False, "subject": str(args.dump_document),
                            "errors": [], "load_error": "%s: %s" % (type(exc).__name__, exc)}, RC_LOAD)
    print(json.dumps(document, ensure_ascii=False, sort_keys=True))
    return RC_OK


def build_parser():
    parser = argparse.ArgumentParser(
        prog="protocol_schema_test.py",
        description="Validator + nghiem thu schema protocol da phien (docs/PROTOCOL_DA_PHIEN.md).")
    parser.add_argument("--schema", help="duong dan JSON schema trong .github/schemas/")
    parser.add_argument("--document", help="tai lieu can kiem (yaml/json/markdown)")
    parser.add_argument("--format", choices=("yaml", "json", "markdown"), help="ep dinh dang tai lieu")
    parser.add_argument("--check-form", help="doi chieu mot Issue Form ve khoi YAML normative")
    parser.add_argument("--dump-document", help="in tai lieu da phan tich duoi dang JSON")
    parser.add_argument("--root", help="goc kho de tra docs/PROTOCOL_DA_PHIEN.md (mac dinh: goc that)")
    parser.add_argument("--trace-required", action="store_true",
                        help="liet ke cac cap (schema required, vi tri tai lieu) THUC SU duoc cuong che")
    parser.add_argument("--json", action="store_true", help="in ket qua dang JSON")
    return parser


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        return run_suite()
    args = build_parser().parse_args(argv)
    modes = [bool(args.check_form), bool(args.dump_document), bool(args.schema or args.document)]
    if sum(1 for m in modes if m) != 1:
        print("dung mot trong ba che do: --schema/--document, --check-form, --dump-document",
              file=sys.stderr)
        return RC_LOAD
    if args.check_form:
        return _run_check_form(args)
    if args.dump_document:
        return _run_dump(args)
    if not (args.schema and args.document):
        print("che do validate can CA --schema lan --document", file=sys.stderr)
        return RC_LOAD
    return _run_validate(args)


# ─────────────────────────────────────────────────────────────────────────────
# 6. Evidence THAT da land — fixture doc nguoc
# ─────────────────────────────────────────────────────────────────────────────
#
# Bon than comment duoi day la evidence THAT cua wp57/F3-00 tren canonical `3910bd2c`. Nhung gi nhung
# vao day la doan BYTE-EXACT tu dau than den het khoi ```yaml (chuan hoa LF, khong newline cuoi).
# `case_provenance_doan_trich_khop_sha256` bam lai chinh chuoi nhung o day va doi chieu voi
# `excerpt_sha256`, nen mot loi chep tay se lam suite DO chu khong troi qua. `body_sha256` la bam cua
# TOAN BO than comment, de nguoi review tai lai tu URL va doi chieu doc lap.

_EX_HANDOFF_WP57 = """\
## Executor handoff — wp57 revision 3 / generation 3

```yaml
schema_version: 1
packet_id: wp57
revision: 3
generation: 3
spec_hash: 228ecb03adbaa1ac160fd1ea4b614c56300cbaab01809c8859aeef624f5de2fc
provider: codex
role: executor
session_id: codex-20260808-wp57-g3
superseded_head_sha: f27287c9379ba6640bc14604d4ccc9afe228861a
head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
tested_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
branch: codex/wp57-g3-f3-00-automation-first
pr: https://github.com/ducthangho/tra-luat/pull/59
status: done
verdict: ready_for_rereview
gate_tier: T2
full_fallback_reason: sensitive packet; legacy runner + manifest changed; selector pre-activation
changed_path_count: 8
remaining_work: []
next_role: reviewer
manual_next_action: create a fresh cross-provider Claude Reviewer on exact generation-3 head
executor_evidence_url: https://github.com/ducthangho/tra-luat/pull/59#issuecomment-5225389852
```"""

_EX_REVIEW_WP57 = """\
## Reviewer verdict — wp57 revision 3 / generation 3 — `approve`

```yaml
schema_version: 1
packet_id: wp57
mission_issue: 54
packet_issue: 57
revision: 3
generation: 3
spec_hash: 228ecb03adbaa1ac160fd1ea4b614c56300cbaab01809c8859aeef624f5de2fc
provider: claude
role: reviewer
session_id: claude-20260808-wp57-g3-review
base_sha: 0844c0bc24399fa4b8430750dc69f7388c23eb8b
reviewed_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
tested_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
branch: codex/wp57-g3-f3-00-automation-first
pr: https://github.com/ducthangho/tra-luat/pull/59
independence: fresh session; read-only; did not execute this packet; no write/commit/push/rebase
superseded_evidence_used: none
verdict: approve
assurance: cross_approved
axes: [spec, standards_security]
gate_tier: T2
findings: [WP57-R3G3-CLD-01, WP57-R3G3-CLD-02, WP57-R3G3-CLD-03]
blocking_findings: []
next_role: land_operator
manual_next_action: reconciler/Approver quyết định bước kế; Reviewer không merge/land
land_authorization: absent
issue_projection: state:reviewing
pr_state: draft
```"""

_EX_LAND_AUTH_WP57 = """\
## Land authorization — wp57 revision 3 / generation 3

```yaml
schema_version: 1
authorization_id: WP57-R3G3-LAND-AUTH-01
decision: approved
mission_id: gh-54
mission_revision: 3
change_request: MCR-54-02
packet_issue: 57
packet_id: wp57
packet_revision: 3
packet_generation: 3
spec_hash: 228ecb03adbaa1ac160fd1ea4b614c56300cbaab01809c8859aeef624f5de2fc
pr: https://github.com/ducthangho/tra-luat/pull/59
authorized_head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
authorized_tree_sha: 194bac05ceeefeafe4d3eff30fadfa27a311dcf1
authorized_base_sha: 0844c0bc24399fa4b8430750dc69f7388c23eb8b
target_branch: master
integration_mode: bootstrap_direct_canonical
merge_method: merge
actor: ducthangho
provider: codex
role: approver_land_operator
session_id: codex-20260808-wp57-r3g3-approver-land
issued_at: 2026-08-08T09:21:20Z
expires_at: 2026-08-08T11:21:20Z
review_assurance: cross_approved
executor_evidence_ids: [5225391077, 5225389852]
reviewer_evidence_ids: [5225459747, 5225459844]
ci_run_id: 31249160032
ci_check_run_ids: [93082632941, 93082632896]
cumulative_changed_paths: 10
blocking_findings: []
advisory_findings_deferred: [WP57-R3G3-CLD-01, WP57-R3G3-CLD-02, WP57-R3G3-CLD-03]
authorization_status: active
```"""

_EX_LAND_EVIDENCE_WP57 = """\
## Land evidence — wp57 revision 3 / generation 3

```yaml
schema_version: 1
land_evidence_id: WP57-R3G3-LAND-EVIDENCE-01
mission_id: gh-54
generation: 1
provider: codex
role: land_operator
session_id: codex-20260808-wp57-r3g3-approver-land
input_packet_generations: [wp57@3]
authorized_head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12
authorized_tree_sha: 194bac05ceeefeafe4d3eff30fadfa27a311dcf1
approver: ducthangho
authorization_url: https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225492673
land_operator: ducthangho
merge_method: merge
merge_commit: 3910bd2cb7a933fce82f22eb4d0b73b56f7ec8a3
canonical_tree_sha: 194bac05ceeefeafe4d3eff30fadfa27a311dcf1
pre_merge_checks:
  - {run_id: 31249160032, head_sha: 2a384acf14c374b58b6045b83d91694a16f65c12, conclusion: success, os: [ubuntu-latest, windows-latest]}
  - {review_issue_comment_id: 5225459747, review_pr_comment_id: 5225459844, assurance: cross_approved}
post_merge_checks:
  - {run_id: 31250454568, head_sha: 3910bd2cb7a933fce82f22eb4d0b73b56f7ec8a3, conclusion: success}
  - {job_id: 93085901542, os: ubuntu-latest, conclusion: success}
  - {job_id: 93085901565, os: windows-latest, conclusion: success}
bookkeeping:
  - pending: set Packet #57 projection state:landed
  - pending: close Packet #57 as completed
  - keep Mission #54 open; no mission-complete claim
advisory_findings_deferred: [WP57-R3G3-CLD-01, WP57-R3G3-CLD-02, WP57-R3G3-CLD-03]
status: applied_checks_green_pending_bookkeeping
```"""

_EVIDENCE = {
    "handoff": {
        "text": _EX_HANDOFF_WP57,
        "schema": "handoff.schema.json",
        "comment_id": 5225391077,
        "url": "https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225391077",
        "body_sha256": "1e8be09540e1f08c4afdeab11f105bebec0ae63d895013dda246fa68a7bc36d9",
        "excerpt_sha256": "3c8a630dd59ff78b7fc1ab8a8a465a52792cd08e7936be1c552bfce7cd9ddaa7",
    },
    "review": {
        "text": _EX_REVIEW_WP57,
        "schema": "review.schema.json",
        "comment_id": 5225459747,
        "url": "https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225459747",
        "body_sha256": "9889468ad2090807af359141f769675f62349841bb7f41afbe8390f79655f295",
        "excerpt_sha256": "6c722c054a6b59a1cec91206380048b1b36766c22935d9abf441ea7d451a4b18",
    },
    "land_authorization": {
        "text": _EX_LAND_AUTH_WP57,
        "schema": "land.schema.json",
        "comment_id": 5225492673,
        "url": "https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225492673",
        "body_sha256": "347a21c3273bd45758f87ee052d2fefb1fff8237a8a59cdb6b8aabf1864ab086",
        "excerpt_sha256": "66f1adacd918fc9c5c1f96dbefa09d10878eb62937c5b00d03f1349673f42604",
    },
    "land_evidence": {
        "text": _EX_LAND_EVIDENCE_WP57,
        "schema": "land.schema.json",
        "comment_id": 5225520427,
        "url": "https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225520427",
        "body_sha256": "986347c5a34460322de087a07dc0c8c123651dc47ec4bc6e8814ec861c45c9f5",
        "excerpt_sha256": "3850af9f98ba2e0b6c8e8757a268a97977f56f2305f6852d39bdc12014883a05",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# 7. Fixture chuan — mot tai lieu HOP LE cho moi schema/bien the
# ─────────────────────────────────────────────────────────────────────────────
#
# Fixture phai DAY DU (moi `required`, ke ca cac `required` long trong `$defs`, deu co mat) vi ca
# phan chung tong quat lay chinh chung lam diem xuat phat: gia tri co san thi moi go ra duoc.

_SHA_A = "3910bd2cb7a933fce82f22eb4d0b73b56f7ec8a3"
_SHA_SPEC = "33a04b6fb5215dd79cf553908ecb7c1a8790f6951c379029bc184acd965b54d4"

_FIXTURES = {
    "handoff.schema.json": {
        "schema_version": 1,
        "packet_id": "wp60",
        "generation": 1,
        "spec_hash": _SHA_SPEC,
        "provider": "claude",
        "role": "executor",
        "session_id": "claude-20260808-wp60-g1",
        "base_sha": _SHA_A,
        "head_sha": _SHA_A,
        "status": "done",
        "summary": "fixture chuan cua khoi handoff §7",
        "changed_paths": [".github/schemas/handoff.schema.json"],
        "tests": [
            {"name": "tl selftest", "status": "passed", "evidence": "1696/1696, rc 0"},
            {"name": "deploy parity", "status": "not_run", "evidence": "khong chay trong packet nay",
             "reason": "packet khong cham duong deploy"},
        ],
        "test_selection": {
            "gate_tier": "T2",
            "selector_policy_sha": None,
            "tested_sha": _SHA_A,
            "selected_groups": [],
            "full_fallback_reason": "packet sensitive; path .github/** chua duoc map",
        },
        "remaining_work": [],
        "next_role": "reviewer",
        "manual_next_action": "tao phien Reviewer Codex moi tren exact head",
        "copyable_prompt": "Ban la Reviewer moi, doc lap, chi review mot don vi cong viec.",
        "failure": {"fingerprint": None, "category": None},
        "successors": [{
            "successor_key": "wp60-successor-01",
            "objective": "hoi tu ten truong giua §7 va evidence that",
            "write_set": [],
            "depends_on": [],
            "executor": "codex",
            "environment": "local",
            "acceptance_criteria": [],
        }],
    },
    "review.schema.json": {
        "schema_version": 1,
        "packet_id": "wp60",
        "generation": 1,
        "provider": "codex",
        "role": "reviewer",
        "session_id": "codex-20260808-wp60-g1-review",
        "reviewed_sha": _SHA_A,
        "independent_from_executor_session": True,
        "review_axes": ["spec", "standards_security"],
        "tests": [{"name": "golden-test", "status": "passed", "evidence": "20 ca, 0 diff"}],
        "findings": [{"id": "WP60-R1G1-CDX-01", "severity": "P3", "blocking": False}],
        "verdict": "approve",
        "assurance": "cross_approved",
        "evidence_url": "https://github.com/ducthangho/tra-luat/issues/60",
    },
    "land.schema.json": {
        "schema_version": 1,
        "mission_id": "gh-54",
        "generation": 1,
        "provider": "codex",
        "role": "land_operator",
        "session_id": "codex-20260808-wp60-land",
        "input_packet_generations": ["wp60@1"],
        "authorized_head_sha": _SHA_A,
        "approver": "ducthangho",
        "authorization_url": "https://github.com/ducthangho/tra-luat/issues/60",
        "land_operator": "ducthangho",
        "merge_method": "merge",
        "merge_commit": _SHA_A,
        "pre_merge_checks": [],
        "post_merge_checks": [],
        "bookkeeping": [],
    },
    "state.schema.json": {
        "schema_version": 1,
        "mission_id": "gh-54",
        "mission_revision": 3,
        "mission_state": "running",
        "plan_hash": _SHA_SPEC,
        "last_consumed_event_id": 5225520427,
        "state_hash": _SHA_SPEC,
        "prev_event_hash": None,
        "packets": [{
            "packet_id": "wp60",
            "revision": 1,
            "spec_hash": _SHA_SPEC,
            "state": "running",
            "generation": 1,
            "lease": {
                "packet_id": "wp60",
                "executor": "claude",
                "environment": "local",
                "branch": "claude/wp60-g1-f3-01-github-schema",
                "write_set_hash": _SHA_SPEC,
                "generation": 1,
                "heartbeat_at": "2026-08-08T10:00:00Z",
                "lease_until": "2026-08-08T10:30:00Z",
            },
            "budget": {"used": 1, "reserved": 1, "limit": 3},
            "review_assurance": None,
            "head_sha": _SHA_A,
            "handoff_url": None,
        }],
    },
    "command.schema.json": {
        "schema_version": 1,
        "command": "/land apply",
        "actor": "ducthangho",
        "client": "issue_comment",
        "mission_id": "gh-54",
        "head_sha": _SHA_A,
        "override": True,
        "reason": "fixture chuan cho nhanh if/then cua §11",
        "issued_at": "2026-08-08T10:00:00Z",
    },
}

# Bien the thu hai cua land.schema.json - `oneOf` chi dung khi CA HAI nhanh deu co fixture rieng.
_FIXTURE_LAND_AUTH = {
    "schema_version": 1,
    "mission_id": "gh-54",
    "decision": "approved",
    "authorized_head_sha": _SHA_A,
    "approver": "ducthangho",
    "provider": "human",
    "merge_method": "merge",
    "review_assurance": "cross_approved",
    "authorization_status": "active",
}


# ─────────────────────────────────────────────────────────────────────────────
# 8. Suite — moi ca goi entrypoint qua subprocess va doc rc THAT
# ─────────────────────────────────────────────────────────────────────────────

def _run(argv, cwd=None):
    """Goi CHINH entrypoint nay trong mot tien trinh rieng. Tra (rc, payload-json-hoac-None, stdout)."""
    proc = subprocess.run(
        [sys.executable, str(_HERE)] + list(argv),
        cwd=str(cwd) if cwd else None,
        capture_output=True,
    )
    out = proc.stdout.decode("utf-8", "replace")
    payload = None
    try:
        payload = json.loads(out)
    except ValueError:
        payload = None
    return proc.returncode, payload, out + proc.stderr.decode("utf-8", "replace")


def _write(tmp, name, text):
    path = Path(tmp) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def _write_json(tmp, name, obj):
    return _write(tmp, name, json.dumps(obj, ensure_ascii=False, indent=2))


def _schema_copies(tmp):
    """Copy ca 5 schema sang thu muc tam de $ref cheo tep van giai duoc sau khi da bien doi mot tep."""
    dest = Path(tmp) / "schemas"
    dest.mkdir(parents=True, exist_ok=True)
    for src in sorted(_SCHEMA_DIR.glob("*.schema.json")):
        shutil.copyfile(str(src), str(dest / src.name))
    return dest


def _pointer_get(obj, pointer):
    node = obj
    for token in [t for t in pointer.split("/") if t]:
        token = token.replace("~1", "/").replace("~0", "~")
        if isinstance(node, list):
            node = node[int(token)]
        else:
            node = node[token]
    return node


def _doc_get(obj, pointer):
    return _pointer_get(obj, pointer)


# ── ca: provenance ───────────────────────────────────────────────────────────

def case_provenance_doan_trich_khop_sha256(tmp):
    for key, meta in _EVIDENCE.items():
        got = hashlib.sha256(meta["text"].encode("utf-8")).hexdigest()
        if got != meta["excerpt_sha256"]:
            print("  ! %s: doan trich bam %s, cho %s" % (key, got, meta["excerpt_sha256"]))
            return False
    return True


# ── ca: doc nguoc tren evidence THAT ─────────────────────────────────────────

def _validate_evidence(tmp, key):
    meta = _EVIDENCE[key]
    doc = _write(tmp, "%s.md" % key, meta["text"])
    return _run(["--schema", str(_SCHEMA_DIR / meta["schema"]), "--document", str(doc),
                 "--format", "markdown", "--json"])


def case_evidence_that_handoff_wp57_chi_thieu_copyable_prompt(tmp):
    """WP57-R3G3-CLD-03 duoc dong BANG CO CHE: khong phai «da luu y», ma la mot ca DO chi dung mot cho."""
    rc, payload, out = _validate_evidence(tmp, "handoff")
    if rc != RC_INVALID or payload is None:
        print("  ! rc=%s (cho 1); out=%s" % (rc, out[:400]))
        return False
    errs = payload["errors"]
    if len(errs) != 1:
        print("  ! cho DUNG 1 loi, gap %d: %s" % (len(errs), json.dumps(errs, ensure_ascii=False)))
        return False
    if errs[0]["path"] != "/copyable_prompt" or errs[0]["keyword"] != "required":
        print("  ! loi khong tro dung cho: %s" % json.dumps(errs[0], ensure_ascii=False))
        return False
    return True


def case_evidence_that_reviewer_wp57_chi_thieu_ba_truong_doc_lap(tmp):
    """`WP60-R1G1-CDX-03` duoc dong BANG CO CHE, va ca nay do NGUOC tren evidence THAT.

    Khoi reviewer §7 khai `independent_from_executor_session: true`, `review_axes: [spec,
    standards_security]` va `tests`. Evidence wp57 (comment 5225459747, viet TRUOC khi co schema) dung ba
    ten khac: `independence` dang van xuoi, `axes`, va khong co `tests`. Khi ba truong tren tro thanh
    `required`, validator phai chi DUNG BA cho do va khong cho nao khac - cung the loai bang chung duong
    nhu ca `copyable_prompt` ben tren, chu khong phai mot ca «hop le» nhat.
    """
    rc, payload, out = _validate_evidence(tmp, "review")
    if rc != RC_INVALID or payload is None:
        print("  ! rc=%s (cho 1); out=%s" % (rc, out[:400]))
        return False
    got = sorted((e["path"], e["keyword"]) for e in payload["errors"])
    want = sorted([
        ("/independent_from_executor_session", "required"),
        ("/review_axes", "required"),
        ("/tests", "required"),
    ])
    if got != want:
        print("  ! tap loi khong dung: %s" % json.dumps(payload["errors"], ensure_ascii=False))
        return False
    return True


def case_evidence_that_land_authorization_hop_le(tmp):
    rc, payload, out = _validate_evidence(tmp, "land_authorization")
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:600]))
    return rc == RC_OK


def case_evidence_that_land_evidence_hop_le(tmp):
    rc, payload, out = _validate_evidence(tmp, "land_evidence")
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:600]))
    return rc == RC_OK


def case_land_hai_bien_the_khong_duoc_nhap_nhang(tmp):
    """`oneOf` chi co nghia khi hai bien the LOAI TRU nhau. Tron ca hai vao mot tai lieu phai DO."""
    mixed = dict(_FIXTURES["land.schema.json"])
    mixed["decision"] = "approved"
    doc = _write_json(tmp, "mixed.json", mixed)
    rc, payload, out = _run(["--schema", str(_SCHEMA_DIR / "land.schema.json"),
                             "--document", str(doc), "--json"])
    if rc != RC_INVALID or payload is None:
        print("  ! rc=%s; %s" % (rc, out[:400]))
        return False
    if not any(e["keyword"] == "oneOf" and "nhieu hon mot" in e["message"] for e in payload["errors"]):
        print("  ! khong bao nhap nhang: %s" % json.dumps(payload["errors"], ensure_ascii=False))
        return False
    return True


# ── ca: fixture chuan ────────────────────────────────────────────────────────

def case_fixture_chuan_moi_schema_deu_qua(tmp):
    items = list(_FIXTURES.items()) + [("land.schema.json", _FIXTURE_LAND_AUTH)]
    for n, (schema, fixture) in enumerate(items):
        doc = _write_json(tmp, "fix%d.json" % n, fixture)
        rc, payload, out = _run(["--schema", str(_SCHEMA_DIR / schema), "--document", str(doc), "--json"])
        if rc != RC_OK:
            print("  ! %s rc=%s; %s" % (schema, rc, out[:600]))
            return False
    return True


# ── ca: phan chung tong quat (khong rong) ────────────────────────────────────

def _mutation_pairs(tmp, schema_dir=None):
    """Tra danh sach (schema, fixture, pair) tu chinh entrypoint - chi cac `required` THUC SU cuong che.

    `schema_dir` cho phep trace tren mot BAN SAO da bi sua, de chung minh kiem ke la ratchet that.
    """
    base = Path(schema_dir) if schema_dir else _SCHEMA_DIR
    items = list(_FIXTURES.items()) + [("land.schema.json", _FIXTURE_LAND_AUTH)]
    todo = []
    for n, (schema, fixture) in enumerate(items):
        doc = _write_json(tmp, "trace%d.json" % n, fixture)
        rc, payload, out = _run(["--schema", str(base / schema), "--document", str(doc),
                                 "--trace-required", "--json"])
        if rc != RC_OK or payload is None:
            raise AssertionError("trace tren %s that bai: rc=%s %s" % (schema, rc, out[:400]))
        for pair in payload["required_pairs"]:
            todo.append((schema, fixture, pair))
    return todo


def _pair_key(entry_schema, pair):
    """Danh tinh mot muc `required` duoc cuong che.

    Co CA schema vao lan schema dinh nghia: `test_result` bi cuong che qua ca handoff lan review, va neu
    khoa chi mang tep dinh nghia thi mat mot trong hai duong ma kiem ke khong doi - dung cai bay «so khong
    doi nen coi nhu khong mat gi» ma ratchet nay sinh ra de chan.
    """
    return "%s <- %s%s::%s@%s" % (entry_schema, pair["schema_file"], pair["schema_pointer"],
                                  pair["field"], pair["document_pointer"] or "/")


def _pair_keys(pairs):
    return set(_pair_key(entry, pair) for entry, _, pair in pairs)


# KIEM KE CHINH XAC cac muc `required` DUOC CUONG CHE THAT (WP60-R1G1-CDX-04).
#
# Day khong phai danh sach `required` doc tu schema: no la ket qua `--trace-required` chay tren
# fixture chuan, tuc la nhung muc thuc su chay toi va cuong che duoc - nhanh `oneOf`/`anyOf` khong
# khop thi khong co mat o day. Sinh lai bang:
#
#     python .github/checks/protocol_schema_test.py --schema .github/schemas/<S> \n#         --document <fixture>.json --trace-required --json
#
# Sua schema ma quen sua bang nay - hoac nguoc lai - thi suite DO. Do la muc dich.
_REQUIRED_INVENTORY = (
    "command.schema.json <- command.schema.json/allOf/0/then/required::head_sha@/",
    "command.schema.json <- command.schema.json/allOf/0/then/required::mission_id@/",
    "command.schema.json <- command.schema.json/allOf/1/then/required::reason@/",
    "command.schema.json <- command.schema.json/required::actor@/",
    "command.schema.json <- command.schema.json/required::command@/",
    "command.schema.json <- command.schema.json/required::schema_version@/",
    "handoff.schema.json <- handoff.schema.json/$defs/successor/required::objective@/successors/0",
    "handoff.schema.json <- handoff.schema.json/$defs/successor/required::successor_key@/successors/0",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/required::evidence@/tests/0",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/required::evidence@/tests/1",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/required::name@/tests/0",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/required::name@/tests/1",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/required::status@/tests/0",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/required::status@/tests/1",
    "handoff.schema.json <- handoff.schema.json/$defs/test_result/then/required::reason@/tests/1",
    "handoff.schema.json <- handoff.schema.json/$defs/test_selection/required::gate_tier@/test_selection",
    "handoff.schema.json <- handoff.schema.json/$defs/test_selection/required::tested_sha@/test_selection",
    "handoff.schema.json <- handoff.schema.json/required::copyable_prompt@/",
    "handoff.schema.json <- handoff.schema.json/required::generation@/",
    "handoff.schema.json <- handoff.schema.json/required::head_sha@/",
    "handoff.schema.json <- handoff.schema.json/required::manual_next_action@/",
    "handoff.schema.json <- handoff.schema.json/required::next_role@/",
    "handoff.schema.json <- handoff.schema.json/required::packet_id@/",
    "handoff.schema.json <- handoff.schema.json/required::provider@/",
    "handoff.schema.json <- handoff.schema.json/required::role@/",
    "handoff.schema.json <- handoff.schema.json/required::schema_version@/",
    "handoff.schema.json <- handoff.schema.json/required::session_id@/",
    "handoff.schema.json <- handoff.schema.json/required::spec_hash@/",
    "handoff.schema.json <- handoff.schema.json/required::status@/",
    "land.schema.json <- land.schema.json/$defs/land_authorization/anyOf/0/required::approver@/",
    "land.schema.json <- land.schema.json/$defs/land_authorization/required::authorized_head_sha@/",
    "land.schema.json <- land.schema.json/$defs/land_authorization/required::decision@/",
    "land.schema.json <- land.schema.json/$defs/land_authorization/required::mission_id@/",
    "land.schema.json <- land.schema.json/$defs/land_authorization/required::schema_version@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::approver@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::authorization_url@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::authorized_head_sha@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::bookkeeping@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::generation@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::input_packet_generations@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::land_operator@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::merge_commit@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::merge_method@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::mission_id@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::post_merge_checks@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::pre_merge_checks@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::provider@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::role@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::schema_version@/",
    "land.schema.json <- land.schema.json/$defs/land_evidence/required::session_id@/",
    "review.schema.json <- handoff.schema.json/$defs/test_result/required::evidence@/tests/0",
    "review.schema.json <- handoff.schema.json/$defs/test_result/required::name@/tests/0",
    "review.schema.json <- handoff.schema.json/$defs/test_result/required::status@/tests/0",
    "review.schema.json <- review.schema.json/$defs/finding/anyOf/1/required::id@/findings/0",
    "review.schema.json <- review.schema.json/required::assurance@/",
    "review.schema.json <- review.schema.json/required::findings@/",
    "review.schema.json <- review.schema.json/required::generation@/",
    "review.schema.json <- review.schema.json/required::independent_from_executor_session@/",
    "review.schema.json <- review.schema.json/required::packet_id@/",
    "review.schema.json <- review.schema.json/required::provider@/",
    "review.schema.json <- review.schema.json/required::review_axes@/",
    "review.schema.json <- review.schema.json/required::reviewed_sha@/",
    "review.schema.json <- review.schema.json/required::role@/",
    "review.schema.json <- review.schema.json/required::schema_version@/",
    "review.schema.json <- review.schema.json/required::session_id@/",
    "review.schema.json <- review.schema.json/required::tests@/",
    "review.schema.json <- review.schema.json/required::verdict@/",
    "state.schema.json <- state.schema.json/$defs/budget/required::limit@/packets/0/budget",
    "state.schema.json <- state.schema.json/$defs/budget/required::reserved@/packets/0/budget",
    "state.schema.json <- state.schema.json/$defs/budget/required::used@/packets/0/budget",
    "state.schema.json <- state.schema.json/$defs/lease/required::branch@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::environment@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::executor@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::generation@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::heartbeat_at@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::lease_until@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::packet_id@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/lease/required::write_set_hash@/packets/0/lease",
    "state.schema.json <- state.schema.json/$defs/packet_projection/required::generation@/packets/0",
    "state.schema.json <- state.schema.json/$defs/packet_projection/required::packet_id@/packets/0",
    "state.schema.json <- state.schema.json/$defs/packet_projection/required::revision@/packets/0",
    "state.schema.json <- state.schema.json/$defs/packet_projection/required::spec_hash@/packets/0",
    "state.schema.json <- state.schema.json/$defs/packet_projection/required::state@/packets/0",
    "state.schema.json <- state.schema.json/required::last_consumed_event_id@/",
    "state.schema.json <- state.schema.json/required::mission_id@/",
    "state.schema.json <- state.schema.json/required::mission_revision@/",
    "state.schema.json <- state.schema.json/required::mission_state@/",
    "state.schema.json <- state.schema.json/required::packets@/",
    "state.schema.json <- state.schema.json/required::schema_version@/",
    "state.schema.json <- state.schema.json/required::state_hash@/",
)


def case_kiem_ke_required_khop_chinh_xac(tmp):
    """RATCHET CHINH XAC cho `required` — dong `WP60-R1G1-CDX-04`.

    Nguong `len(pairs) >= 40` KHONG phai ratchet: go `actor` khoi `command.schema.json.required` lam so
    cap tut 87 -> 86 ma suite van xanh 40/40 (phan chung cua reviewer, chay trong ban sao ngoai kho).
    O day kiem ke la mot TAP CO DINH: them, bot hay doi vi tri BAT KY muc `required` nao cung lam ca nay
    DO, va ban va phai sua `_REQUIRED_INVENTORY` mot cach hien thi trong diff.
    """
    got = _pair_keys(_mutation_pairs(tmp))
    want = set(_REQUIRED_INVENTORY)
    if len(_REQUIRED_INVENTORY) != len(want):
        print("  ! kiem ke co muc trung lap")
        return False
    if got != want:
        for k in sorted(want - got):
            print("  ! MAT khoi schema (required bi go?): %s" % k)
        for k in sorted(got - want):
            print("  ! THEM ma kiem ke chua ghi: %s" % k)
        print("  ! kiem ke %d muc, trace %d muc" % (len(want), len(got)))
        return False
    print("  . kiem ke required khop chinh xac: %d/%d muc" % (len(got), len(want)))
    return True


def case_go_mot_required_khoi_schema_lam_kiem_ke_do(tmp):
    """Phan chung cua chinh ratchet tren: tai lap DUNG kich ban reviewer da dung de bac bo nguong >= 40."""
    dest = _schema_copies(tmp)
    patched = json.loads((_SCHEMA_DIR / "command.schema.json").read_text(encoding="utf-8"))
    if "actor" not in patched["required"]:
        print("  ! command.schema.json khong con `actor` trong required - phan chung mat nghia")
        return False
    patched["required"].remove("actor")
    (dest / "command.schema.json").write_text(json.dumps(patched, ensure_ascii=False, indent=2),
                                              encoding="utf-8", newline="\n")
    got = _pair_keys(_mutation_pairs(tmp, dest))
    want = set(_REQUIRED_INVENTORY)
    if got == want:
        print("  ! go `actor` ma kiem ke van khop - ratchet chi la trang tri")
        return False
    if (want - got) != {"command.schema.json <- command.schema.json/required::actor@/"}:
        print("  ! chenh lech khong dung mot muc `actor`: %s" % sorted(want - got))
        return False
    print("  . go 1 muc required -> kiem ke DO dung 1 cho (%d -> %d)" % (len(want), len(got)))
    return True


def _trace_keys_or_loi(tmp, schema_dir):
    """(`set` khoa, None) neu trace chay sach; (None, thong diep) neu chinh trace DO.

    Ca hai deu la tin hieu DO hop le cho ratchet: mot vi tri `required` bi go ra hoac lam kiem ke lech,
    hoac lam chinh bo fixture chuan khong con trace duoc - vi du go `decision` khoi nhanh
    `land_authorization` lam fixture `land_evidence` khop CA HAI nhanh `oneOf`. Cai KHONG chap nhan duoc
    la go ra ma moi thu van xanh y nguyen.
    """
    try:
        return _pair_keys(_mutation_pairs(tmp, schema_dir)), None
    except AssertionError as exc:
        return None, str(exc)


def case_go_bat_ky_required_nao_cung_do_dung_cho(tmp):
    """`WP60-R1G1-CDX-04` doi «go BAT KY required entry nao cung lam counter-proof do dung cho».

    Ca tren dung lai o MOT vi du - chinh vi du reviewer dua ra. Ca nay chay HET: voi moi vi tri
    `(tep schema, con tro required, ten truong)` thuc su duoc cuong che, no go DUNG vi tri do khoi ban
    sao schema roi doi mot tin hieu DO co dia chi. Mot vi tri schema co the sinh NHIEU muc kiem ke
    (`test_result/required::name` cuong che o `/tests/0`, `/tests/1` cua handoff va `/tests/0` cua
    review), nen phep so sanh la `want - got` phai bang DUNG chum muc cua vi tri vua go, khong nhieu
    khong it.
    """
    dest = _schema_copies(tmp)
    pairs = _mutation_pairs(tmp)
    want = set(_REQUIRED_INVENTORY)
    if _pair_keys(pairs) != want:
        print("  ! tap `required` lech kiem ke - xem case_kiem_ke_required_khop_chinh_xac")
        return False

    vi_tri = {}
    for entry, _, pair in pairs:
        loc = (pair["schema_file"], pair["schema_pointer"], pair["field"])
        vi_tri.setdefault(loc, set()).add(_pair_key(entry, pair))

    do_kiem_ke = 0
    do_trace = 0
    for (sfile, sptr, field), chum in sorted(vi_tri.items()):
        patched = json.loads((_SCHEMA_DIR / sfile).read_text(encoding="utf-8"))
        arr = _pointer_get(patched, sptr)
        if field not in arr:
            print("  ! %s%s khong chua %r" % (sfile, sptr, field))
            return False
        arr.remove(field)
        (dest / sfile).write_text(json.dumps(patched, ensure_ascii=False, indent=2),
                                  encoding="utf-8", newline="\n")
        got, loi = _trace_keys_or_loi(tmp, dest)
        shutil.copyfile(str(_SCHEMA_DIR / sfile), str(dest / sfile))

        if loi is not None:
            do_trace += 1
            continue
        if got == want:
            print("  ! go %r tai %s%s ma kiem ke VAN KHOP - ratchet thung o day" % (field, sfile, sptr))
            return False
        if (want - got) != chum:
            print("  ! go %r tai %s%s: mat %s, cho %s"
                  % (field, sfile, sptr, sorted(want - got), sorted(chum)))
            return False
        if got - want:
            print("  ! go %r tai %s%s lai SINH THEM muc: %s" % (field, sfile, sptr, sorted(got - want)))
            return False
        do_kiem_ke += 1

    print("  . %d vi tri required: %d lam kiem ke DO dung chum cua no, %d lam chinh trace DO"
          % (len(vi_tri), do_kiem_ke, do_trace))
    return do_kiem_ke + do_trace == len(vi_tri) and len(vi_tri) > 0


def case_moi_truong_required_deu_ganh_luc(tmp):
    """Phan chung TU CHUNG MINH KHONG RONG, hai chieu cho TUNG truong `required`:

      (a) go truong khoi TAI LIEU  ⇒ ca do (rc 1) va loi tro dung vi tri;
      (b) go truong khoi `required` cua SCHEMA ⇒ chinh tai lieu do lai xanh (rc 0).

    Khong co ve (b) thi ve (a) co the do vi mot ly do khac; khong co ve (a) thi `required` chi la trang
    tri. So cap duoc in ra de bao cao bang SO, khong khai suong.
    """
    schemas_tmp = _schema_copies(tmp)
    pairs = _mutation_pairs(tmp)
    # Khong dung nguong «>= N» nua: nguong do khong bat duoc viec BOT mot muc `required`
    # (`WP60-R1G1-CDX-04`). So cap phai khop DUNG kiem ke co dinh; ca rieng ben tren lo phan chung.
    if _pair_keys(pairs) != set(_REQUIRED_INVENTORY):
        print("  ! tap `required` lech kiem ke - xem case_kiem_ke_required_khop_chinh_xac")
        return False
    do_do = 0
    for idx, (schema, fixture, pair) in enumerate(pairs):
        field, dptr, sptr, sfile = pair["field"], pair["document_pointer"], pair["schema_pointer"], pair["schema_file"]
        mutant = copy.deepcopy(fixture)
        try:
            holder = _doc_get(mutant, dptr)
        except (KeyError, IndexError, ValueError):
            print("  ! khong tim thay vi tri tai lieu %r" % dptr)
            return False
        if field not in holder:
            print("  ! fixture thieu san %r tai %r - fixture phai DAY DU" % (field, dptr))
            return False
        del holder[field]
        doc = _write_json(tmp, "mut%d.json" % idx, mutant)

        rc_a, payload_a, out_a = _run(["--schema", str(_SCHEMA_DIR / schema), "--document", str(doc), "--json"])
        if rc_a != RC_INVALID:
            print("  ! (a) go %r tai %r khong lam ca do: rc=%s %s" % (field, dptr, rc_a, out_a[:300]))
            return False
        want = (dptr + "/" + field) or "/"
        if not any(e["path"] == want and e["keyword"] == "required" for e in (payload_a or {}).get("errors", [])):
            print("  ! (a) loi khong tro dung %r: %s" % (want, out_a[:300]))
            return False
        do_do += 1

        patched = json.loads((_SCHEMA_DIR / sfile).read_text(encoding="utf-8"))
        arr = _pointer_get(patched, sptr)
        if field not in arr:
            print("  ! (b) %s%s khong chua %r" % (sfile, sptr, field))
            return False
        arr.remove(field)
        (schemas_tmp / sfile).write_text(json.dumps(patched, ensure_ascii=False, indent=2),
                                         encoding="utf-8", newline="\n")
        rc_b, _, out_b = _run(["--schema", str(schemas_tmp / schema), "--document", str(doc), "--json"])
        shutil.copyfile(str(_SCHEMA_DIR / sfile), str(schemas_tmp / sfile))
        if rc_b != RC_OK:
            print("  ! (b) bo %r khoi %s%s ma ca van do: rc=%s %s" % (field, sfile, sptr, rc_b, out_b[:300]))
            return False
    print("  . %d cap required, ca %d cap deu do khi go khoi tai lieu va xanh lai khi go khoi schema"
          % (len(pairs), do_do))
    return True


# ── ca: quy tac tests[] ──────────────────────────────────────────────────────

def _handoff_with_tests(tmp, name, tests):
    fixture = copy.deepcopy(_FIXTURES["handoff.schema.json"])
    fixture["tests"] = tests
    doc = _write_json(tmp, name, fixture)
    return _run(["--schema", str(_SCHEMA_DIR / "handoff.schema.json"), "--document", str(doc), "--json"])


def case_tests_thieu_evidence_bi_bat(tmp):
    rc, payload, _ = _handoff_with_tests(tmp, "t1.json", [{"name": "golden", "status": "passed"}])
    return rc == RC_INVALID and any(
        e["path"] == "/tests/0/evidence" and e["keyword"] == "required" for e in (payload or {}).get("errors", []))


def case_tests_not_run_thieu_reason_bi_bat(tmp):
    rc, payload, _ = _handoff_with_tests(
        tmp, "t2.json", [{"name": "parity", "status": "not_run", "evidence": "bo qua"}])
    return rc == RC_INVALID and any(
        e["path"] == "/tests/0/reason" and e["keyword"] == "required" for e in (payload or {}).get("errors", []))


def case_tests_not_run_co_reason_duoc_qua(tmp):
    rc, _, out = _handoff_with_tests(
        tmp, "t3.json", [{"name": "parity", "status": "not_run", "evidence": "bo qua", "reason": "ngoai write set"}])
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_OK


def case_review_dung_chung_dinh_nghia_tests_qua_ref_cheo_tep(tmp):
    """review.schema.json khong tu dinh nghia `tests[]`; no `$ref` sang handoff. Ca nay chung minh
    rang rang buoc that su duoc cuong che qua bien gioi tep, khong phai mot ban chep im lang."""
    fixture = copy.deepcopy(_FIXTURES["review.schema.json"])
    fixture["tests"] = [{"name": "eol", "status": "not_run", "evidence": "bo qua"}]
    doc = _write_json(tmp, "r1.json", fixture)
    rc, payload, _ = _run(["--schema", str(_SCHEMA_DIR / "review.schema.json"), "--document", str(doc), "--json"])
    return rc == RC_INVALID and any(
        e["path"] == "/tests/0/reason" and e["keyword"] == "required" for e in (payload or {}).get("errors", []))


# ── ca: enum va nhanh if/then ────────────────────────────────────────────────

def _mutated(tmp, schema, name, changes, drop=()):
    fixture = copy.deepcopy(_FIXTURES[schema])
    fixture.update(changes)
    for key in drop:
        fixture.pop(key, None)
    doc = _write_json(tmp, name, fixture)
    return _run(["--schema", str(_SCHEMA_DIR / schema), "--document", str(doc), "--json"])


# ── ca: exact SHA o cho protocol rang buoc THAM QUYEN (WP60-R1G1-CDX-02) ─────
#
# `git_oid` cu la `["string","null"]` + `^[0-9a-f]{7,40}$`, dung lai o CA cho §7/§10.2 neo tham quyen.
# Nam probe cua reviewer deu rc 0: `/land apply` voi `head_sha: null`, `/land apply` voi `head_sha`
# viet tat, va land authorization voi `authorized_head_sha: null`. Sau ban va: `git_oid` la 40 hex
# KHONG null, con `git_oid_or_null` (chi handoff `head_sha` va projection `head_sha`) van cho null
# nhung VAN doi du 40 hex khi la chuoi. Moi dong duoi day la mot trong nhung probe do, dao chieu.

_SHA_VIET_TAT = "b5cc5d6"


def case_command_land_apply_head_sha_null_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "command.schema.json", "s1.json", {"head_sha": None})
    return rc == RC_INVALID and any(
        e["path"] == "/head_sha" and e["keyword"] == "type" for e in (payload or {}).get("errors", []))


def case_command_land_apply_head_sha_viet_tat_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "command.schema.json", "s2.json", {"head_sha": _SHA_VIET_TAT})
    return rc == RC_INVALID and any(
        e["path"] == "/head_sha" and e["keyword"] == "pattern" for e in (payload or {}).get("errors", []))


def case_land_authorization_head_sha_null_bi_bat(tmp):
    doc = _write_json(tmp, "s3.json", dict(_FIXTURE_LAND_AUTH, authorized_head_sha=None))
    rc, payload, out = _run(["--schema", str(_SCHEMA_DIR / "land.schema.json"),
                             "--document", str(doc), "--json"])
    if rc != RC_INVALID:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_INVALID


def case_land_evidence_merge_commit_viet_tat_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "land.schema.json", "s4.json", {"merge_commit": _SHA_VIET_TAT})
    return rc == RC_INVALID


def case_review_reviewed_sha_null_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "review.schema.json", "s5.json", {"reviewed_sha": None})
    return rc == RC_INVALID and any(
        e["path"] == "/reviewed_sha" and e["keyword"] == "type" for e in (payload or {}).get("errors", []))


def case_handoff_head_sha_null_van_hop_le(tmp):
    """Chieu NGUOC LAI: §7 khai handoff `head_sha` la `<git-oid-or-null>`, nen siet exact SHA KHONG duoc
    lam mat cho null that su hop le - neu khong thi ban va da di qua chinh cho protocol cho phep."""
    rc, _, out = _mutated(tmp, "handoff.schema.json", "s6.json", {"head_sha": None})
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_OK


def case_handoff_head_sha_viet_tat_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "handoff.schema.json", "s7.json", {"head_sha": _SHA_VIET_TAT})
    return rc == RC_INVALID and any(
        e["path"] == "/head_sha" and e["keyword"] == "pattern" for e in (payload or {}).get("errors", []))


def case_state_head_sha_null_van_hop_le(tmp):
    fixture = copy.deepcopy(_FIXTURES["state.schema.json"])
    fixture["packets"][0]["head_sha"] = None
    doc = _write_json(tmp, "s8.json", fixture)
    rc, _, out = _run(["--schema", str(_SCHEMA_DIR / "state.schema.json"), "--document", str(doc), "--json"])
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_OK


# ── ca: doc lap + hai truc + tests cua reviewer (WP60-R1G1-CDX-03) ───────────

def case_review_thieu_doc_lap_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "review.schema.json", "i1.json", {},
                              drop=("independent_from_executor_session",))
    return rc == RC_INVALID and any(
        e["path"] == "/independent_from_executor_session" and e["keyword"] == "required"
        for e in (payload or {}).get("errors", []))


def case_review_doc_lap_false_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "review.schema.json", "i2.json",
                              {"independent_from_executor_session": False})
    return rc == RC_INVALID and any(
        e["path"] == "/independent_from_executor_session" and e["keyword"] == "const"
        for e in (payload or {}).get("errors", []))


def case_review_thieu_truc_bi_bat(tmp):
    """`review_axes: [spec]` tung qua rc 0. Hai `contains` cua khoi §7 phai lam no DO."""
    rc, payload, _ = _mutated(tmp, "review.schema.json", "i3.json", {"review_axes": ["spec"]})
    return rc == RC_INVALID and any(
        e["path"] == "/review_axes" and e["keyword"] == "contains"
        for e in (payload or {}).get("errors", []))


def case_review_truc_ngoai_enum_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "review.schema.json", "i4.json",
                              {"review_axes": ["spec", "performance"]})
    return rc == RC_INVALID


def case_review_thieu_tests_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "review.schema.json", "i5.json", {}, drop=("tests",))
    return rc == RC_INVALID and any(
        e["path"] == "/tests" and e["keyword"] == "required" for e in (payload or {}).get("errors", []))


def case_review_tests_rong_van_hop_le(tmp):
    """Khoi reviewer §7 in dung `tests: []`. Doi `minItems` o day la CHE THEM luat ngoai protocol,
    nen schema chi doi truong PHAI CO MAT; cuong che du thuoc worker gate F3-06. Ca nay ghim ranh gioi
    do lai de mot ban va sau khong am tham sieu chuan hoa."""
    rc, _, out = _mutated(tmp, "review.schema.json", "i6.json", {"tests": []})
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_OK


def case_handoff_next_role_ngoai_enum_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "handoff.schema.json", "e1.json", {"next_role": "approver"})
    return rc == RC_INVALID and any(
        e["path"] == "/next_role" and e["keyword"] == "enum" for e in (payload or {}).get("errors", []))


def case_handoff_role_sai_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "handoff.schema.json", "e2.json", {"role": "reviewer"})
    return rc == RC_INVALID and any(
        e["path"] == "/role" and e["keyword"] == "const" for e in (payload or {}).get("errors", []))


def case_review_assurance_ngoai_bon_muc_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "review.schema.json", "e3.json", {"assurance": "self_approved"})
    return rc == RC_INVALID and any(
        e["path"] == "/assurance" and e["keyword"] == "enum" for e in (payload or {}).get("errors", []))


def case_command_ngoai_tap_lenh_dong_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "command.schema.json", "e4.json", {"command": "/mission complete"})
    return rc == RC_INVALID and any(
        e["path"] == "/command" and e["keyword"] == "enum" for e in (payload or {}).get("errors", []))


def case_command_land_apply_thieu_head_sha_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "command.schema.json", "e5.json", {}, drop=("head_sha",))
    return rc == RC_INVALID and any(
        e["path"] == "/head_sha" and e["keyword"] == "required" for e in (payload or {}).get("errors", []))


def case_command_khac_land_apply_khong_bi_doi_head_sha(tmp):
    rc, _, out = _mutated(tmp, "command.schema.json", "e6.json",
                          {"command": "/land prepare"}, drop=("head_sha", "mission_id"))
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_OK


def case_command_override_thieu_reason_bi_bat(tmp):
    rc, payload, _ = _mutated(tmp, "command.schema.json", "e7.json", {}, drop=("reason",))
    return rc == RC_INVALID and any(
        e["path"] == "/reason" and e["keyword"] == "required" for e in (payload or {}).get("errors", []))


def case_state_packet_state_ngoai_enum_bi_bat(tmp):
    fixture = copy.deepcopy(_FIXTURES["state.schema.json"])
    fixture["packets"][0]["state"] = "merged"
    doc = _write_json(tmp, "e8.json", fixture)
    rc, payload, _ = _run(["--schema", str(_SCHEMA_DIR / "state.schema.json"), "--document", str(doc), "--json"])
    return rc == RC_INVALID and any(
        e["path"] == "/packets/0/state" and e["keyword"] == "enum" for e in (payload or {}).get("errors", []))


def case_state_lease_thieu_truong_bi_bat(tmp):
    fixture = copy.deepcopy(_FIXTURES["state.schema.json"])
    del fixture["packets"][0]["lease"]["write_set_hash"]
    doc = _write_json(tmp, "e9.json", fixture)
    rc, payload, _ = _run(["--schema", str(_SCHEMA_DIR / "state.schema.json"), "--document", str(doc), "--json"])
    return rc == RC_INVALID and any(
        e["path"] == "/packets/0/lease/write_set_hash" and e["keyword"] == "required"
        for e in (payload or {}).get("errors", []))


def case_state_lease_null_van_hop_le(tmp):
    fixture = copy.deepcopy(_FIXTURES["state.schema.json"])
    fixture["packets"][0]["lease"] = None
    doc = _write_json(tmp, "e10.json", fixture)
    rc, _, out = _run(["--schema", str(_SCHEMA_DIR / "state.schema.json"), "--document", str(doc), "--json"])
    if rc != RC_OK:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_OK


# ── ca: Issue Form ───────────────────────────────────────────────────────────

def case_form_ba_bieu_mau_khop_khoi_normative(tmp):
    for name in sorted(_FORM_SECTION):
        rc, _, out = _run(["--check-form", str(_FORM_DIR / name), "--json"])
        if rc != RC_OK:
            print("  ! %s rc=%s; %s" % (name, rc, out[:600]))
            return False
    return True


def _form_mutant(tmp, slug, name, text):
    """Ban dot bien phai GIU NGUYEN TEN TEP: `--check-form` tra muc protocol theo ten form, doi ten se
    lam no tra rc 2 (khong biet muc) - mot ca 'do' vi ly do khac han cai dang do."""
    return _write(tmp, "%s/%s" % (slug, name), text)


def _bo_dong(text, needle):
    lines = text.split("\n")
    hit = [n for n, ln in enumerate(lines) if needle in ln]
    if len(hit) != 1:
        raise AssertionError("cho dung 1 dong chua %r, gap %d" % (needle, len(hit)))
    del lines[hit[0]]
    return "\n".join(lines)


_FORM_MUTANT_KEY = {
    "mission.yml": "objective:",
    "work-packet.yml": "objective:",
    "change-request.yml": "reason:",
}


def case_form_bo_mot_truong_bat_buoc_thi_do(tmp):
    for name, needle in sorted(_FORM_MUTANT_KEY.items()):
        raw = (_FORM_DIR / name).read_text(encoding="utf-8")
        path = _form_mutant(tmp, "bo-truong", name, _bo_dong(raw, needle))
        rc, payload, out = _run(["--check-form", str(path), "--json"])
        if rc != RC_INVALID:
            print("  ! %s bo %r ma van rc=%s: %s" % (name, needle, rc, out[:400]))
            return False
        if not any(e["keyword"] == "required" for e in (payload or {}).get("errors", [])):
            print("  ! %s: khong bao thieu truong normative: %s" % (name, out[:400]))
            return False
    return True


def case_form_spec_khong_bat_buoc_thi_do(tmp):
    raw = (_FORM_DIR / "mission.yml").read_text(encoding="utf-8")
    path = _form_mutant(tmp, "spec-tuy-chon", "mission.yml",
                        raw.replace("      required: true", "      required: false"))
    rc, payload, out = _run(["--check-form", str(path), "--json"])
    if rc != RC_INVALID:
        print("  ! rc=%s; %s" % (rc, out[:400]))
        return False
    return any(e["path"].endswith("/validations/required") for e in (payload or {}).get("errors", []))


def case_form_them_truong_phai_sinh_thi_do(tmp):
    """§3.2: `change_policy_sha` & co. do dispatcher bo sung; form khong duoc moi nguoi dung khai."""
    raw = (_FORM_DIR / "work-packet.yml").read_text(encoding="utf-8")
    patched = raw.replace("        depends_on: []",
                          "        change_policy_sha: <canonical-policy-sha>\n        depends_on: []")
    if patched == raw:
        print("  ! khong chen duoc truong phai sinh vao form")
        return False
    path = _form_mutant(tmp, "truong-phai-sinh", "work-packet.yml", patched)
    rc, payload, out = _run(["--check-form", str(path), "--json"])
    if rc != RC_INVALID:
        print("  ! rc=%s; %s" % (rc, out[:400]))
        return False
    return any(e["keyword"] in ("forbidden", "additionalProperties")
               for e in (payload or {}).get("errors", []))


def case_form_thieu_protocol_thi_rc2_khong_phai_xanh(tmp):
    """Fail-closed: mat nguon normative thi DUNG, khong duoc lang le bao xanh."""
    empty = Path(tmp) / "khong-co-docs"
    empty.mkdir(parents=True, exist_ok=True)
    rc, _, _ = _run(["--check-form", str(_FORM_DIR / "mission.yml"), "--root", str(empty), "--json"])
    return rc == RC_LOAD


# ── ca: bo phan tich YAML fail-closed ────────────────────────────────────────

def _dump_rc(tmp, name, text):
    path = _write(tmp, name, text)
    return _run(["--dump-document", str(path), "--format", "yaml", "--json"])


def case_yaml_tab_bi_tu_choi(tmp):
    rc, _, _ = _dump_rc(tmp, "tab.yaml", "a:\n\tb: 1\n")
    return rc == RC_LOAD


def case_yaml_anchor_alias_bi_tu_choi(tmp):
    rc, _, _ = _dump_rc(tmp, "anchor.yaml", "a: &neo 1\nb: *neo\n")
    return rc == RC_LOAD


def case_yaml_nhieu_document_bi_tu_choi(tmp):
    rc, _, _ = _dump_rc(tmp, "multi.yaml", "a: 1\n---\nb: 2\n")
    return rc == RC_LOAD


def case_yaml_khoa_lap_bi_tu_choi(tmp):
    rc, _, _ = _dump_rc(tmp, "dup.yaml", "a: 1\na: 2\n")
    return rc == RC_LOAD


def case_dump_giu_nguyen_url_timestamp_va_flow(tmp):
    """Ba dang de bi cat sai nhat trong evidence that: URL co `://`, timestamp co `:`, va flow long nhau."""
    doc = _write(tmp, "land.md", _EVIDENCE["land_evidence"]["text"])
    rc, payload, out = _run(["--dump-document", str(doc), "--format", "markdown"])
    if rc != RC_OK or payload is None:
        print("  ! rc=%s; %s" % (rc, out[:400]))
        return False
    want_url = "https://github.com/ducthangho/tra-luat/issues/57#issuecomment-5225492673"
    if payload.get("authorization_url") != want_url:
        print("  ! authorization_url bi cat: %r" % payload.get("authorization_url"))
        return False
    if payload.get("input_packet_generations") != ["wp57@3"]:
        print("  ! flow seq sai: %r" % payload.get("input_packet_generations"))
        return False
    if payload["pre_merge_checks"][0].get("os") != ["ubuntu-latest", "windows-latest"]:
        print("  ! flow long nhau sai: %r" % payload["pre_merge_checks"][0])
        return False

    auth = _write(tmp, "auth.md", _EVIDENCE["land_authorization"]["text"])
    rc2, payload2, out2 = _run(["--dump-document", str(auth), "--format", "markdown"])
    if rc2 != RC_OK or payload2 is None:
        print("  ! auth rc=%s; %s" % (rc2, out2[:300]))
        return False
    if payload2.get("issued_at") != "2026-08-08T09:21:20Z":
        print("  ! timestamp bi cat: %r" % payload2.get("issued_at"))
        return False
    return True


def case_dump_cat_binh_luan_dung_nghia_yaml(tmp):
    """Bo phan tich KHONG duoc de dai hon YAML that: ` #` van mo binh luan. Neo bang chinh evidence that,
    de neu ai do 'sua cho de doc hon' thi ca nay do va buoc doc lai §7 thay vi im lang doi nghia."""
    doc = _write(tmp, "land2.md", _EVIDENCE["land_evidence"]["text"])
    rc, payload, out = _run(["--dump-document", str(doc), "--format", "markdown"])
    if rc != RC_OK or payload is None:
        print("  ! rc=%s; %s" % (rc, out[:300]))
        return False
    book = payload.get("bookkeeping")
    if book != [{"pending": "set Packet"}, {"pending": "close Packet"}, "keep Mission"]:
        print("  ! bookkeeping khong theo nghia YAML: %r" % book)
        return False
    return True


# ── ca: fail-closed cua chinh entrypoint ─────────────────────────────────────

def case_schema_khong_ton_tai_thi_rc2(tmp):
    doc = _write_json(tmp, "x.json", _FIXTURES["handoff.schema.json"])
    rc, _, _ = _run(["--schema", str(Path(tmp) / "khong-co.json"), "--document", str(doc), "--json"])
    return rc == RC_LOAD


def case_document_khong_ton_tai_thi_rc2(tmp):
    rc, _, _ = _run(["--schema", str(_SCHEMA_DIR / "handoff.schema.json"),
                     "--document", str(Path(tmp) / "khong-co.md"), "--format", "markdown", "--json"])
    return rc == RC_LOAD


def case_markdown_khong_co_khoi_yaml_thi_rc2(tmp):
    doc = _write(tmp, "tron.md", "## chi co van xuoi, khong co khoi yaml\n")
    rc, _, _ = _run(["--schema", str(_SCHEMA_DIR / "handoff.schema.json"),
                     "--document", str(doc), "--format", "markdown", "--json"])
    return rc == RC_LOAD


def case_ref_cheo_tep_khong_giai_duoc_thi_rc2(tmp):
    lone = Path(tmp) / "lone"
    lone.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(str(_SCHEMA_DIR / "review.schema.json"), str(lone / "review.schema.json"))
    doc = _write_json(tmp, "rev.json", _FIXTURES["review.schema.json"])
    rc, _, out = _run(["--schema", str(lone / "review.schema.json"), "--document", str(doc), "--json"])
    if rc != RC_LOAD:
        print("  ! rc=%s; %s" % (rc, out[:300]))
    return rc == RC_LOAD


def case_khong_the_goi_hai_che_do_cung_luc(tmp):
    rc, _, _ = _run(["--schema", str(_SCHEMA_DIR / "handoff.schema.json"),
                     "--check-form", str(_FORM_DIR / "mission.yml")])
    return rc == RC_LOAD


def case_schema_json_hong_thi_rc2(tmp):
    bad = _write(tmp, "hong.schema.json", "{ khong phai json }")
    doc = _write_json(tmp, "y.json", _FIXTURES["handoff.schema.json"])
    rc, _, _ = _run(["--schema", str(bad), "--document", str(doc), "--json"])
    return rc == RC_LOAD


# ── ca: schema la JSON hop le va tu nhat quan ────────────────────────────────

def case_nam_schema_deu_la_json_hop_le(tmp):
    want = {"handoff.schema.json", "review.schema.json", "land.schema.json",
            "state.schema.json", "command.schema.json"}
    got = {p.name for p in _SCHEMA_DIR.glob("*.schema.json")}
    if got != want:
        print("  ! tap schema lech: thua %s, thieu %s" % (sorted(got - want), sorted(want - got)))
        return False
    for name in sorted(want):
        try:
            data = json.loads((_SCHEMA_DIR / name).read_text(encoding="utf-8"))
        except ValueError as exc:
            print("  ! %s: %s" % (name, exc))
            return False
        if not data.get("description", "").strip():
            print("  ! %s thieu description tro ve protocol" % name)
            return False
        if "PROTOCOL_DA_PHIEN.md" not in json.dumps(data, ensure_ascii=False):
            print("  ! %s khong tro ve docs/PROTOCOL_DA_PHIEN.md" % name)
            return False
    return True


# ── ca: mo ta chi TRO protocol, khong chep doctrine (WP60-R1G1-CDX-05) ───────
#
# Acceptance cua #60 doi schema/form chi hinh thuc hoa TRUONG va enum roi TRO ve protocol. Doi voi mot
# ban sao doctrine thi «da xoa mot lan» khong phai co che - no moc lai o ban va sau. Hai so duoi day la
# ratchet do duoc: TRAN DO DAI cho moi `description` cua schema va moi khoi `type: markdown` cua form,
# cong voi doi hoi con TRO ve tep protocol. NEN DO tren head cu `b5cc5d6` (do bang chinh `_mo_ta_trong`):
# description dai nhat 759 ky tu (`land.schema.json` goc), khoi markdown dai nhat 553 (`work-packet.yml`).
_TRAN_MO_TA_SCHEMA = 240
_TRAN_MARKDOWN_FORM = 360


def _mo_ta_trong(node, path="/"):
    """Duyet DE QUY moi khoa `description` trong mot schema, ke ca trong `$defs` va `properties`."""
    out = []
    if isinstance(node, dict):
        for key, val in node.items():
            if key == "description" and isinstance(val, str):
                out.append((path, val))
            else:
                out.extend(_mo_ta_trong(val, path + str(key) + "/"))
    elif isinstance(node, list):
        for n, item in enumerate(node):
            out.extend(_mo_ta_trong(item, path + str(n) + "/"))
    return out


def case_mo_ta_schema_khong_chep_doctrine(tmp):
    ok = True
    dem = 0
    dai_nhat = 0
    for path in sorted(_SCHEMA_DIR.glob("*.schema.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for ptr, text in _mo_ta_trong(data):
            dem += 1
            dai_nhat = max(dai_nhat, len(text))
            if len(text) > _TRAN_MO_TA_SCHEMA:
                print("  ! %s%s: description %d ky tu > tran %d - nghi chep doctrine"
                      % (path.name, ptr, len(text), _TRAN_MO_TA_SCHEMA))
                ok = False
        if "docs/PROTOCOL_DA_PHIEN.md" not in str(data.get("description", "")):
            print("  ! %s: description goc khong tro ve docs/PROTOCOL_DA_PHIEN.md" % path.name)
            ok = False
    if ok:
        print("  . %d description, dai nhat %d ky tu (tran %d)" % (dem, dai_nhat, _TRAN_MO_TA_SCHEMA))
    return ok


def case_form_markdown_khong_chep_doctrine(tmp):
    ok = True
    dai_nhat = 0
    for name in sorted(_FORM_SECTION):
        form = load_yaml((_FORM_DIR / name).read_text(encoding="utf-8"))
        khoi = [(item.get("attributes") or {}).get("value") or ""
                for item in form.get("body", [])
                if isinstance(item, dict) and item.get("type") == "markdown"]
        if not khoi:
            print("  ! %s khong co khoi markdown tro ve protocol" % name)
            ok = False
        for text in khoi:
            dai_nhat = max(dai_nhat, len(text))
            if len(text) > _TRAN_MARKDOWN_FORM:
                print("  ! %s: khoi markdown %d ky tu > tran %d - nghi chep doctrine"
                      % (name, len(text), _TRAN_MARKDOWN_FORM))
                ok = False
            if "docs/PROTOCOL_DA_PHIEN.md" not in text:
                print("  ! %s: khoi markdown khong tro ve docs/PROTOCOL_DA_PHIEN.md" % name)
                ok = False
    if ok:
        print("  . 3 form, khoi markdown dai nhat %d ky tu (tran %d)" % (dai_nhat, _TRAN_MARKDOWN_FORM))
    return ok


def case_tu_khoa_schema_la_thi_rc2_khong_phai_xanh(tmp):
    """Bo kiem tap con phai FAIL-CLOSED tren tu khoa no khong hieu.

    Neu no im lang bo qua, thi mot rang buoc go nham ten (`uniqueItem`, `containss`, `maxItems`) bien
    mat ma cong van xanh - dung the loai «cong xanh nho rc=0» ma CLAUDE.md canh bao.
    """
    dest = _schema_copies(tmp)
    patched = json.loads((_SCHEMA_DIR / "review.schema.json").read_text(encoding="utf-8"))
    patched["properties"]["review_axes"]["maxItems"] = 2
    (dest / "review.schema.json").write_text(json.dumps(patched, ensure_ascii=False, indent=2),
                                             encoding="utf-8", newline="\n")
    doc = _write_json(tmp, "k1.json", _FIXTURES["review.schema.json"])
    rc, payload, out = _run(["--schema", str(dest / "review.schema.json"), "--document", str(doc), "--json"])
    if rc != RC_LOAD:
        print("  ! rc=%s (cho 2); %s" % (rc, out[:300]))
        return False
    if "maxItems" not in ((payload or {}).get("load_error") or ""):
        print("  ! khong goi ten tu khoa la: %s" % ((payload or {}).get("load_error")))
        return False
    return True


CASES = [
    case_provenance_doan_trich_khop_sha256,
    case_nam_schema_deu_la_json_hop_le,
    case_fixture_chuan_moi_schema_deu_qua,
    case_evidence_that_handoff_wp57_chi_thieu_copyable_prompt,
    case_evidence_that_reviewer_wp57_chi_thieu_ba_truong_doc_lap,
    case_evidence_that_land_authorization_hop_le,
    case_evidence_that_land_evidence_hop_le,
    case_land_hai_bien_the_khong_duoc_nhap_nhang,
    case_kiem_ke_required_khop_chinh_xac,
    case_go_mot_required_khoi_schema_lam_kiem_ke_do,
    case_go_bat_ky_required_nao_cung_do_dung_cho,
    case_moi_truong_required_deu_ganh_luc,
    case_tests_thieu_evidence_bi_bat,
    case_tests_not_run_thieu_reason_bi_bat,
    case_tests_not_run_co_reason_duoc_qua,
    case_review_dung_chung_dinh_nghia_tests_qua_ref_cheo_tep,
    case_command_land_apply_head_sha_null_bi_bat,
    case_command_land_apply_head_sha_viet_tat_bi_bat,
    case_land_authorization_head_sha_null_bi_bat,
    case_land_evidence_merge_commit_viet_tat_bi_bat,
    case_review_reviewed_sha_null_bi_bat,
    case_handoff_head_sha_null_van_hop_le,
    case_handoff_head_sha_viet_tat_bi_bat,
    case_state_head_sha_null_van_hop_le,
    case_review_thieu_doc_lap_bi_bat,
    case_review_doc_lap_false_bi_bat,
    case_review_thieu_truc_bi_bat,
    case_review_truc_ngoai_enum_bi_bat,
    case_review_thieu_tests_bi_bat,
    case_review_tests_rong_van_hop_le,
    case_mo_ta_schema_khong_chep_doctrine,
    case_form_markdown_khong_chep_doctrine,
    case_tu_khoa_schema_la_thi_rc2_khong_phai_xanh,
    case_handoff_next_role_ngoai_enum_bi_bat,
    case_handoff_role_sai_bi_bat,
    case_review_assurance_ngoai_bon_muc_bi_bat,
    case_command_ngoai_tap_lenh_dong_bi_bat,
    case_command_land_apply_thieu_head_sha_bi_bat,
    case_command_khac_land_apply_khong_bi_doi_head_sha,
    case_command_override_thieu_reason_bi_bat,
    case_state_packet_state_ngoai_enum_bi_bat,
    case_state_lease_thieu_truong_bi_bat,
    case_state_lease_null_van_hop_le,
    case_form_ba_bieu_mau_khop_khoi_normative,
    case_form_bo_mot_truong_bat_buoc_thi_do,
    case_form_spec_khong_bat_buoc_thi_do,
    case_form_them_truong_phai_sinh_thi_do,
    case_form_thieu_protocol_thi_rc2_khong_phai_xanh,
    case_yaml_tab_bi_tu_choi,
    case_yaml_anchor_alias_bi_tu_choi,
    case_yaml_nhieu_document_bi_tu_choi,
    case_yaml_khoa_lap_bi_tu_choi,
    case_dump_giu_nguyen_url_timestamp_va_flow,
    case_dump_cat_binh_luan_dung_nghia_yaml,
    case_schema_khong_ton_tai_thi_rc2,
    case_document_khong_ton_tai_thi_rc2,
    case_markdown_khong_co_khoi_yaml_thi_rc2,
    case_ref_cheo_tep_khong_giai_duoc_thi_rc2,
    case_khong_the_goi_hai_che_do_cung_luc,
    case_schema_json_hong_thi_rc2,
]


def run_suite():
    dat = 0
    hong = []
    for case in CASES:
        with tempfile.TemporaryDirectory(prefix="protocol_schema_") as tmp:
            try:
                ok = bool(case(tmp))
            except Exception as exc:                     # noqa: BLE001 — bao loi, khong nuot
                ok = False
                print("  ! %s: %r" % (case.__name__, exc))
        print("%s %s" % ("PASS" if ok else "FAIL", case.__name__))
        if ok:
            dat += 1
        else:
            hong.append(case.__name__)
    print("\n%d/%d dat" % (dat, len(CASES)))
    if hong:
        print("HONG: %s" % ", ".join(hong))
    return RC_OK if not hong else RC_INVALID


if __name__ == "__main__":
    sys.exit(main())
