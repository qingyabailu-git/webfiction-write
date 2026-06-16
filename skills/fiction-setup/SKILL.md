---
name: fiction-setup
description: |
  缃戠粶灏忚椤圭洰鍒濆鍖栥€傚垱寤烘爣鍑嗛」鐩洰褰曠粨鏋勩€佸垵濮嬮厤缃枃浠?state.json)銆?  璁惧畾闆嗛鏋躲€傚湪杩涘叆鏋勬€?fiction-conceive)鍓嶈繍琛屻€?  瑙﹀彂鏂瑰紡锛?fiction-setup銆併€屽缓椤圭洰銆嶃€屽垵濮嬪寲銆嶃€屽噯澶囧啓涔︺€嶃€屾惌鐜銆嶃€屽府鎴戝缓涓」鐩€嶃€屼粠闆跺紑濮嬨€嶃€?metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-setup锛氶」鐩垵濮嬪寲

鍒涘缓鏍囧噯椤圭洰楠ㄦ灦銆傚彧寤虹洰褰曞拰鍒濆閰嶇疆鏂囦欢锛屼笉鍋氭繁搴︽瀯鎬濄€?鏋勬€濈敱 fiction-conceive 瀹屾垚銆?
## 鎵ц娴佺▼

### Phase 1锛氱‘璁ら」鐩洰褰?
```bash
export PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
```

- 妫€鏌ユ槸鍚﹀凡瀛樺湪 `.novel/state.json`
- 瀛樺湪鍒欐彁绀?璇ラ」鐩凡鍒濆鍖栵紝鍙洿鎺?fiction-start 鎴?fiction-conceive"
- 涓嶅瓨鍦ㄥ垯缁х画
- 璇㈤棶鐢ㄦ埛涔﹀悕锛岀敓鎴愬畨鍏ㄥ寲鐩綍鍚?
### Phase 2锛氬垱寤烘爣鍑嗙洰褰曠粨鏋?
```
{椤圭洰鏍箎/
鈹溾攢 .novel/
鈹?  鈹溾攢 state.json            # 鐢卞悗缁楠ゅ～鍏?鈹?  鈹溾攢 idea_bank.json        # 鐢?fiction-conceive 濉厖
鈹?  鈹斺攢 tmp/                  # 杩愯鏃朵复鏃舵枃浠?鈹?鈹溾攢 璁惧畾闆?                    # 涓栫晫瑙傘€佽鑹层€佸姏閲忎綋绯荤瓑
鈹溾攢 澶х翰/                      # 鎬荤翰銆佸嵎绾层€佺珷绾?鈹溾攢 姝ｆ枃/                      # 鍚勭珷姝ｆ枃
鈹溾攢 杩借釜/                      # 涓婁笅鏂囥€佷紡绗斻€佹椂闂寸嚎銆佽鑹茬姸鎬?鈹溾攢 瀹℃煡鎶ュ憡/                   # review-pipeline 浜у嚭
鈹斺攢 鎷嗘枃搴?                    # fiction-analyze 鐨勫垎鏋愪骇鍑?```

### Phase 3锛氬垵濮嬪寲 state.json

```json
{
  "project": {
    "book_name": "",
    "genre": "",
    "target_words": 0,
    "target_platform": "fanqie",
    "author": ""
  },
  "progress": {
    "current_chapter": 0,
    "current_volume": 1,
    "total_chapters": 0,
    "total_volumes": 0,
    "writing_started": false
  },
  "versions": {
    "baseline_version": 0,
    "last_review_chapter": 0
  }
}
```

### Phase 4锛氬垱寤?.novel/active-book

鍐欏叆褰撳墠涔︾洰褰曞悕锛屼綔涓哄涔﹀垏鎹㈡寚閽堛€?
### Phase 5锛氳緭鍑哄畬鎴愪俊鎭?
- 鍒楀嚭鍒涘缓鐨勬枃浠跺拰鐩綍
- 寤鸿涓嬩竴姝ワ細fiction-conceive锛堟瀯鎬濓級鎴?fiction-start锛堝鏋滃凡鏈夋兂娉曪級

## 鍙傝€?
璇︾粏鐩綍缁撴瀯绾﹀畾瑙?`references/`锛堟殏鏃狅紝鎸変笂杩扮‖缂栫爜锛夈€?nove-cover 鍦ㄩ渶瑕佹椂鍗曠嫭璋冪敤锛屼笉鍦ㄦ澶勭敓鎴愩€?鎵宸ュ叿 fiction-scan 闇€瑕佹祻瑙堝櫒鎿嶄綔锛岃瑙佽 skill銆?鎷嗘枃宸ュ叿 fiction-analyze 闇€瑕佹彁渚涘皬璇存枃鏈紝璇﹁璇?skill銆?
<!-- fiction-setup: 锟斤拷始锟斤拷锟斤拷准锟斤拷目目录锟结构 -->

<!-- review-fix: fiction-setup-项目初始化 -->
