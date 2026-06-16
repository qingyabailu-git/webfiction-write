---
name: fiction-review
description: |
  璐ㄩ噺瀹℃煡銆備娇鐢ㄥ鏌ユā鍨嬭瘎浼扮珷鑺傝川閲忥紝鐢熸垚瀹℃煡鎶ュ憡骞跺啓鍥炲鏌ユ寚鏍囥€?  鏀寔鍗曠珷銆佹壒閲忥紙1-5锛夈€佹暣鍗凤紙--volume N锛夊鏌ャ€?  瑙﹀彂鏂瑰紡锛?fiction-review {绔犲彿鎴栬寖鍥磢銆併€屽鏌ャ€嶃€屽涓€涓嬨€嶃€屾鏌ヨ川閲忋€嶃€宺eview銆嶃€屽府鎴戠湅涓嬪啓寰楁€庝箞鏍枫€嶃€?metadata:
  openclaw:
    sources:
      - https://github.com/lingfengQAQ/webnovel-writer
      - https://github.com/worldwonderer/oh-story-claudecode
---

# fiction-review锛氳川閲忓鏌?
浣跨敤瀹℃煡妯″瀷璇勪及绔犺妭璐ㄩ噺锛岀敓鎴愮粨鏋勫寲鎶ュ憡鍜屽鏌ユ寚鏍囥€?


## 写作视角引导

审查不是为了挑刺，而是为了让书写得更好。审查时请帮用户关注：

1. **这章想让读者感受到什么情绪？** — 情绪对了吗？
2. **读完这章，读者会想翻下一页吗？** — 钩子/悬念够不够
3. **有没有地方让读者困惑？** — 连续性问题（人名、设定、时间线）
4. **爽点/虐点/甜点有没有打在正确的位置？** — 节奏对不对

给出具体建议，不说"写得不好"，而是说"这里如果改成XXX，读者会更有代入感"。

## 鎵ц娴佺▼

### Step 1锛氳В鏋愰」鐩牴

```bash
export PROJECT_ROOT="$(python -X utf8 "${SCRIPTS_DIR}/fiction.py" --project-root "${CLAUDE_PROJECT_DIR:-$PWD}" where)"
```

### Step 2锛氬姞杞藉鏌ュ弬鑰?
鎸夐渶鍔犺浇锛?- 鎬绘槸鍔犺浇锛氭牳蹇冪害鏉熴€乺eview-schema
- 娑夊強鐖界偣/閽╁瓙锛歝ool-points-guide
- 娑夊強澶氱嚎浜ょ粐锛歴trand-weave-pattern

### Step 3锛氳皟鐢?reviewer agent

蹇呴』閫氳繃 Agent 宸ュ叿璋冪敤 reviewer锛屼富绾夸笉寰椾吉閫犲鏌?JSON銆?
reviewer 鍙繑鍥炰弗鏍肩粨鏋勫寲 JSON锛屼笉璇勫垎锛屼笉鍙ｅご鎬荤粨銆備富绾胯礋璐ｆ妸杩斿洖鐨?JSON 鍐欏叆 `.novel/tmp/review_results.json`锛岀劧鍚庣敱 review-pipeline 瑕嗙洊涓烘爣鍑?review_result artifact銆?
reviewer 璺宠繃銆佸け璐ャ€佽緭鍑轰笉瀹屾暣銆佹鏂囦负绌?鈫?璁板綍闂锛屼笉绛夊悓浜庡凡瀹℃煡銆?
### Step 4锛氱敓鎴愭姤鍛婂苟钀藉簱

```bash
python -X utf8 "${SCRIPTS_DIR}/fiction.py" review-pipeline \
  --project-root "${PROJECT_ROOT}" \
  --chapter {绔犺妭鍙穧 \
  --review-results ".novel/tmp/review_results.json" \
  --metrics-out ".novel/tmp/review_metrics.json" \
  --report-file "瀹℃煡鎶ュ憡/绗瑊绔犺妭鍙穧绔犲鏌ユ姤鍛?md" \
  --save-metrics
```

### Step 5锛氬鐞嗛樆鏂?
瀛樺湪 blocking issue 鏃讹紝鐢ㄦ湁闄愰€夐」璁╃敤鎴疯鍐筹細
- 绔嬪嵆淇锛堣緭鍑鸿繑宸ユ竻鍗曪紝鏈€灏忎慨鏀癸級
- 浠呬繚瀛樻姤鍛婏紝绋嶅悗澶勭悊锛堜繚鐣欐姤鍛婂拰鎸囨爣锛岀粨鏉熸祦绋嬶級

## 鎵归噺瀹℃煡

```bash
fiction-review 1-5       # 鎵归噺瀹℃煡 1-5 绔?fiction-review --volume 1  # 鏁村嵎瀹℃煡
```

鎵归噺瀹℃煡閫愮珷鎵ц reviewer 鈫?閫愮珷鐢熸垚鎶ュ憡 鈫?姹囨€绘樉绀恒€?
## 鍐欏洖

- 瀹℃煡鎶ュ憡鍐欏叆 `瀹℃煡鎶ュ憡/绗瑊绔犲彿}绔犲鏌ユ姤鍛?md`
- review_metrics 鍐欏叆 `index.db`锛坮eview-pipeline --save-metrics锛?- review_results JSON 瀛樺叆 `.novel/tmp/review_results.json`
- Deep 妯″紡涓嬮澶栨洿鏂?`.story-system/reviews/chapter_{N}.review.json`

## 鎴愬姛鏍囧噯

1. 瑙ｆ瀽鐪熷疄椤圭洰鏍?2. 閫氳繃 reviewer 杈撳嚭缁撴瀯鍖?JSON 骞惰惤鐩?3. 瀹℃煡鎶ュ憡宸茬敓鎴愶紝metrics 宸插啓鍏?index.db
4. 瀛樺湪闃绘柇闂鏃剁敤鎴峰凡鏄庣‘閫夋嫨澶勭悊绛栫暐

## 鍙傝€?
reviewer schema 鐢?reviewer agent 鑷甫瀹氫箟锛屾湰 skill 涓嶅睍寮€銆?闃绘柇瑕嗙洊鎸囧紩瑙?blocking-override-guidelines锛堢敱 reviewer 寮曠敤锛夈€?鎵归噺瀹℃煡閫愮珷鐙珛鎵ц锛屼笉浜掔浉褰卞搷缁撴灉銆?瀹℃煡鎶ュ憡鏍煎紡鐢?review-pipeline 鍐冲畾锛屾湰 skill 涓嶅畾涔夈€?

## 与其他技能的协作

| 相关技能 | 关系 | 使用场景 |
|---------|------|---------|
| **fiction-write** | 审查→修改 | 审查发现问题后，建议用户用内建的大改/重写模式修复 |
| **fiction-polish** | 审查→润色 | 审查发现 AI 味或格式问题，路由到润色流程 |
| **fiction-plan** | 影响规划 | 整卷审查发现节奏问题时，可能触发重新规划章纲 |
| **fiction-doctor** | 配合诊断 | 审查发现大量缺失引用时，可能提醒跑项目体检 |

审查结果会写回项目指标体系（metrics），供后续写作时自动参考。



<!-- fiction-review: 锟斤拷锟接角对匡拷式锟斤拷锟斤拷锟斤拷锟?-->

<!-- review-fix: fiction-review-质量审查 -->
