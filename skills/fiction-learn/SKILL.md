---
name: fiction-learn
description: |
  浠庡綋鍓嶄細璇濇彁鍙栨垚鍔熷啓浣滄ā寮忓苟鍐欏叆 project_memory.json銆?  绫诲瀷鍖呮嫭锛歨ook/pacing/dialogue/payoff/emotion/format/other銆?  鍚庣画鍐欎綔鏃惰嚜鍔ㄥ弬鑰冨凡绉疮鐨勬ā寮忋€?  瑙﹀彂鏂瑰紡锛?fiction-learn銆併€岃浣忚繖涓啓娉曘€嶃€屽涔犮€嶃€岃繖涓啓娉曞ソ銆嶃€屾妸杩欐嫑瀛樿捣鏉ャ€嶃€屼互鍚庨兘杩欎箞鍐欍€嶃€?metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-learn锛氬啓浣滄ā寮忔彁鍙?
浠庡璇濅腑鎻愬彇鍙鐢ㄧ殑鍐欎綔妯″紡锛岃拷鍔犲埌 project_memory.json銆?璁╃郴缁熻秺鍐欒秺鎳備綘锛岃嚜鍔ㄧН绱釜浜洪鏍笺€?
## 鎵ц娴佺▼

### 1. 瑙ｆ瀽椤圭洰鏍?
```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CLAUDE_PROJECT_DIR:-$PWD}" where)"
```

### 2. 瑙ｆ瀽鐢ㄦ埛杈撳叆

- 鐢ㄦ埛杈撳叆涓虹┖ 鈫?鍙栨湰娆″璇濅腑琚敤鎴疯鍙殑鍐欐硶
- 鐢ㄦ埛鏈夋樉寮忚緭鍏?鈫?鐩存帴浣跨敤

### 3. 褰掔被 pattern_type

| 绫诲瀷 | 绀轰緥 |
|------|------|
| hook | "寮€绡囩敤鍐茬獊鍓嶇疆锛岀涓€鍙ュ氨鏄煕鐩? |
| pacing | "杩囨浮绔犺妭鐢ㄥ弻绾垮苟琛屾潵淇濇寔鑺傚" |
| dialogue | "瀵硅瘽閲岀敤娼滃彴璇嶄唬鏇跨洿鐧? |
| payoff | "浼忕瑪閽╁瓙瑕佸湪 10 绔犲唴鍥炴敹" |
| emotion | "铏愮偣鏃跺厛寤虹珛鐢滆湝鍐嶆墦鐮? |
| format | "瀵硅瘽鍗曠嫭鎴愯锛屼笉鐢ㄥ紩鍙? |
| other | 鏃犳硶褰掔被鐨?|

### 4. 鍐欏叆 project_memory.json

```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" project-memory add-pattern \
  --pattern-type "{褰掔被}" \
  --description "{瀹屾暣鎻忚堪}" \
  --category "{鍒嗙被锛屽彲绌簘" \
  --importance "{high|medium|low}"
```

瑕佹眰锛?- 鍙拷鍔狅紝涓嶅垹闄ゆ棫璁板綍
- pattern_type + description 瀹屽叏鐩稿悓鏃惰烦杩囷紙鍘婚噸锛?- 閮ㄥ垎鐩镐技涓嶅幓閲?
## 鎴愬姛鏍囧噯

- project_memory.json 瀛樺湪涓旀牸寮忓悎娉?- 鏂?pattern 宸茶拷鍔犲埌 patterns 鏁扮粍
- 杈撳嚭鍖呭惈 status: success

## 澶辫触鎭㈠

| 鏁呴殰 | 鎭㈠鏂瑰紡 |
|------|---------|
| project_memory.json 涓嶅瓨鍦?| 鑴氭湰鑷姩鍒濆鍖?{"patterns": []} |
| JSON 瑙ｆ瀽澶辫触 | 涓嶅啓鍏ヨ剰鏁版嵁锛屽憡鐭ョ敤鎴锋枃浠舵崯鍧?|
| state.json 缂哄け鏃犳硶鍙栫珷鑺傚彿 | 鐢?source_chapter: null 璺宠繃锛屼笉闃绘柇 |

## 鍙傝€?
鍚庣画鍐欎綔鏃?project_memory.json 鐢?fiction-write 鐨?context-agent 鍔犺浇锛?浣滀负鏂囬鍙傝€冨拰鍘嗗彶妯″紡杈撳叆銆傛湰 skill 鍙礋璐ｅ啓鍏ワ紝涓嶈礋璐ｈ鍙栥€?姝ゅ涓嶉噸澶嶅疄鐜般€?
<!-- fiction-learn: 锟斤拷取锟缴癸拷写锟斤拷模式锟斤拷锟斤拷目锟斤拷锟斤拷锟?-->

<!-- review-fix: fiction-learn-模式积累 -->
