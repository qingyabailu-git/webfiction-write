---
name: fiction-export
description: |
  瀵煎嚭涓庡畬鏈綊妗ｃ€傚悎骞舵墍鏈夋鏂囦负 .txt/.docx 鏍煎紡锛?  鍙€夊幓鏍煎紡銆佸姞鐩綍銆佺敓鎴愬皝闈€傚畬鏈悗涓€閿綊妗ｉ」鐩枃浠躲€?  瑙﹀彂鏂瑰紡锛?fiction-export銆併€屽鍑恒€嶃€屽畬鏈€嶃€屽綊妗ｃ€嶃€屼笅杞姐€嶃€屽鍑簍xt銆嶃€屾垜瑕佸畬鏈簡銆嶃€?metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-export锛氬鍑轰笌瀹屾湰褰掓。

灏嗘鏂囧悎骞朵负鍙緵鍙戝竷/澶囦唤/鍒嗕韩鐨勬牸寮忋€?
## 瀵煎嚭妯″紡

### 姝ｆ枃鍚堝苟

- 鍚堝苟鎵€鏈夊凡鍐欑珷鑺備负涓€涓枃浠?- 鍙€夋牸寮忥細.txt锛堢函鏂囨湰锛? .docx
- 鍚堝苟鏃惰嚜鍔細鎸夌珷缂栧彿鎺掑簭銆佸幓 format 鏍囪銆佸彲閫夊姞绔犵洰褰?- 杈撳嚭鍒?`瀵煎嚭/` 鐩綍

```bash
# 瀵煎嚭鍏ㄩ儴宸插啓绔犺妭
python -X utf8 "${SCRIPTS_DIR}/fiction.py" export \
  --project-root "${PROJECT_ROOT}" \
  --format txt --output "瀵煎嚭/{涔﹀悕}_瀹屾湰.txt"
```

### 瀹屾湰褰掓。

瀹屾湰鍚庢墽琛岋細
1. 鏈€缁堜竴鑷存€ф鏌ワ紙鍙€?deep doctor锛?2. 鍚堝苟姝ｆ枃鏂囦欢
3. 褰掓。鍏抽敭椤圭洰鏂囦欢锛堣瀹氶泦/澶х翰/杩借釜锛夊埌 `褰掓。/` 鐩綍
4. 鐢熸垚瀹屾湰鍏冩暟鎹紙瀛楁暟/绔犳暟/鍐欎綔鍘嗘椂锛?
```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" export \
  --project-root "${PROJECT_ROOT}" \
  --output "褰掓。/{涔﹀悕}_瀹屾湰褰掓。.zip"
```

### 鏂囦欢娓呯悊

- 娓呯悊杩愯鏃朵复鏃舵枃浠讹紙`.novel/tmp/`锛?- 淇濈暀杩借釜/搴曟湰绛夋牳蹇冩暟鎹?
## 浣跨敤绀轰緥

```
> /fiction-export --format docx

鉁?宸插鍑猴細瀵煎嚭/鍓戞潵_瀹屾湰.docx锛?5 绔狅紝12.3 涓囧瓧锛?```

```
> /fiction-export --archive

鉁?宸插綊妗ｏ細褰掓。/鍓戞潵_瀹屾湰褰掓。.zip
鍖呭惈锛氭鏂?璁惧畾闆?澶х翰/杩借釜/搴曟湰
鎬诲瓧鏁帮細12.3 涓囧瓧 | 45 绔?| 鍘嗘椂 67 澶?```

## 鍙傝€?
鍚堝苟鑴氭湰鐢?`scripts/fiction.py` 鐨?`export` 鍜?`export` 瀛愬懡浠ゅ鐞嗐€?瀹屾湰褰掓。鍚庯紝椤圭洰鐩綍鍙Щ鍑烘椿璺冨伐浣滃尯銆?濡傞渶缁х画鍐欐柊涔︼紝杩愯 fiction-setup 鍒濆鍖栨柊椤圭洰銆?濡傛灉浣跨敤 `.docx` 鏍煎紡锛屼緷璧?Documents 鎻掍欢鐨?docx-js 搴撱€?瀵煎嚭鐨?.txt 鏂囦欢鍙洿鎺ョ敤浜庣暘鑼勫钩鍙版姇绋裤€?瀵煎嚭鐨?.docx 鏂囦欢鍙敤浜庤嚜鎴戝綊妗ｆ垨鎵撳嵃銆?---
### 鐣寗骞冲彴鎶曠娉ㄦ剰浜嬮」

鐣寗灏忚鎺ュ彈 .txt 鏍煎紡鎶曠锛岃姹傦細
- UTF-8 缂栫爜锛堟棤 BOM锛?- 绔犳爣棰樼敤 `绗?X 绔燻 鏍煎紡锛岄《鏍煎啓
- 姝ｆ枃娈典箣闂寸┖涓€琛?- 姣忕珷鏈熬绌轰袱琛?- 鏃犻澶栨牸寮忔爣璁?
鏈?skill 鐨?`export` 瀛愬懡浠ら粯璁ら伒瀹堜笂杩拌鑼冦€?浣跨敤 `--format fanqie` 鍙傛暟鍙嚜鍔ㄩ€傞厤鐣寗骞冲彴鏍煎紡瑕佹眰銆?```

<!-- fiction-export: 锟斤拷锟侥碉拷锟斤拷锟斤拷锟疥本锟介档 -->

<!-- review-fix: fiction-export-完本导出 -->
