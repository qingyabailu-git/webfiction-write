---
name: fiction-doctor
description: |
  椤圭洰浣撴璇婃柇銆傚彧璇绘鏌ラ」鐩洰褰曘€佹枃浠躲€丣SON銆佸簳鏈綋绯诲畬鏁存€с€?  鍙戠幇缂哄け鎴栧紓甯搁」鏃惰В閲婂奖鍝嶅拰淇寤鸿锛屼笉鑷姩淇銆?  瑙﹀彂鏂瑰紡锛?fiction-doctor銆併€屼綋妫€銆嶃€岃瘖鏂€嶃€屾鏌ラ」鐩€嶃€岄」鐩姸鎬併€嶃€屽府鎴戠湅鐪嬭繖涓」鐩湁娌℃湁闂銆嶃€屾鏌ヤ竴涓嬫枃浠躲€嶃€?metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-doctor锛氶」鐩綋妫€璇婃柇

鍙璇婃柇褰撳墠椤圭洰锛氱‘璁ゆ墍澶勯樁娈靛簲鏈夌殑鏂囦欢鏄惁瀹屾暣銆?
## 鍘熷垯

1. 鍙璇婃柇锛屼笉鍐欐枃浠讹紝涓嶈嚜鍔ㄤ慨澶嶏紝涓嶅畨瑁呬緷璧?2. 鍏?project-status 鍙栫煭鐘舵€侊紝鍐?doctor 鍋氶樁娈垫劅鐭ユ鏌?3. 缂哄け椤规寜闃舵瑙ｉ噴褰卞搷鍜屼慨澶嶅缓璁?
## 鎵ц

```bash
export WORKSPACE_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
export SCRIPTS_DIR="${CLAUDE_PLUGIN_ROOT:?}/scripts"

# 鐭姸鎬?python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${WORKSPACE_ROOT}" project-status --format summary

# 鏍囧噯浣撴
python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${WORKSPACE_ROOT}" doctor --format text

# 鎸囧畾绔犺妭锛堝彲閫夛級
# python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${WORKSPACE_ROOT}" doctor --chapter {N} --deep
```

## 杈撳嚭鏂瑰紡

鎶ュ憡鍖呭惈锛?- 褰撳墠 phase 鍜?target_chapter
- 鏄惁鏈?blocker銆佺己澶辨垨寮傚父鏂囦欢璺緞
- 搴曟湰/璁惧畾闆?杩借釜/姝ｆ枃瀹屾暣鎬?- 姣忎釜闂鐨勫奖鍝嶅拰淇寤鸿

涓嶆墽琛岀湡瀹炰慨澶嶏紝涓嶅睍绀烘垨瑕佹眰绮樿创 API key銆?
## 鍙傝€?
鍚勯樁娈电殑鏂囦欢瀹屾暣鎬ф爣鍑嗭細
- 寮€涔﹀墠锛?novel/state.json + 璁惧畾闆?*.md + 鎬荤翰鑽夋.md
- 寮€涔﹀悗锛氫笂杩?+ .story-system/ 搴曟湰 + 澶х翰/ + 姝ｆ枃/N绔?md
- 鍐欎綔涓細杩借釜/ 鏂囦欢榻愬叏銆佸簳鏈増鏈彿鍖归厤
鏈?skill 涓嶉噸澶嶅畾涔夊悇闃舵娓呭崟銆?濡傞渶涓诲姩淇锛屽厛杩愯 doctor 鏌ョ湅鎶ュ憡锛屽啀鎸夊缓璁墽琛屻€?濡傛灉 baseline_version 涓嶅尮閰嶏紝寤鸿杩愯 fiction-start 鍒锋柊搴曟湰銆?濡傛灉杩借釜鏂囦欢缂哄け锛岄噸鏂拌窇 fiction-write 瀵瑰簲绔犺妭浼氳嚜鍔ㄨˉ鍏ㄣ€?---
### 浣跨敤绀轰緥

```
> /fiction-doctor

浣撴鎶ュ憡
鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣
闃舵锛氬紑涔﹀悗锛堝凡鍐欒嚦绗?15 绔狅級

鉁?椤圭洰鐘舵€佹甯?  路 .novel/state.json 鉁?  路 璁惧畾闆?涓昏鍗?md 鉁?  路 璁惧畾闆?涓栫晫瑙?md 鉁?  路 璁惧畾闆?鏍稿績鍐茬獊.md 鉁?  路 澶х翰/鎬荤翰.md 鉁?  路 澶х翰/绗?鍗?璇︾粏澶х翰.md 鉁?  路 姝ｆ枃/ 1-15 绔犲畬鏁?鉁?  路 杩借釜/浼忕瑪.md 鉁?  路 杩借釜/鏃堕棿绾?md 鉁?  路 .story-system/MASTER_SETTING.json 鉁?  路 搴曟湰鐗堟湰鍙蜂竴鑷?鉁?
鈿狅笍 寤鸿娉ㄦ剰
  路 璺濅笂娆″鏌ュ凡杩?6 绔狅紙绗?9 绔犲悗鏈锛?  路 杩借釜/涓婁笅鏂?md 寤鸿褰掓。锛堝綋鍓?50 鏉¤褰曪級

鏃犻渶澶勭悊銆?```

```
> /fiction-doctor --deep

浣撴鎶ュ憡锛堟繁搴︼級
鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣鈹佲攣
...
鉂?闂锛氳瀹氶泦/涓栫晫瑙?md 寮曠敤浜嗕竴涓湭寤烘。鐨勯厤瑙?璧甸搧鏌?
  褰卞搷锛氬悗缁煡璇㈣鑹茶档閾佹煴鏃跺彲鑳借繑鍥炵┖缁撴灉
  寤鸿锛氳繍琛?fiction-export characters 妫€鏌ユ竻鍗曪紝鎴栨墜鍔ㄨˉ鍗?...
```

<!-- fiction-doctor: 锟斤拷目锟斤拷锟?锟斤拷 锟斤拷锟斤拷募锟斤拷峁癸拷锟阶憋拷锟斤拷锟斤拷锟斤拷 -->

<!-- review-fix: fiction-doctor-项目体检 -->
