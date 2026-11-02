# 基隆市立中山高級中學 AILEAD365 數位學習平台使用指南

繁體中文響應式靜態網站，供高中學生、國中學生及教師查閱登入方式、基本操作與常見問題。使用 HTML、CSS、原生 JavaScript，沒有後端、資料庫或建置相依套件。

## 本機預覽

在既有專案目錄執行（不需要另建 Git worktree）：

```sh
cd /workspace/ailead365-guide
python3 -m http.server 8000 --bind 127.0.0.1
```

在自己的開發電腦可使用瀏覽器開啟 `http://127.0.0.1:8000`。雲端環境中的相同網址僅供機器內部測試，不是對外預覽網址。按 `Ctrl+C` 停止。也可直接開啟 `index.html`；網站不使用模組載入、遠端字型、API 或 CDN。

## 網站結構

```text
index.html                      # 首頁、平台介紹、三種身分教學、常見問題
assets/styles.css               # 桌面、平板、手機版面與減少動態效果設定
assets/app.js                   # 身分分頁、鍵盤操作、行動選單與 FAQ 篩選
assets/favicon.svg              # 本站自製圖示（非學校正式校徽）
tests/validate.py               # 靜態結構、連結與公開檔案檢查
tests/browser.cjs               # 可選的 Playwright 瀏覽器互動驗收
.github/workflows/pages.yml     # GitHub Pages 部署與驗證
```

所有網站資源使用相對路徑，可部署於 `/ailead365-guide/` 子路徑。頁首識別圖案與首頁插畫皆為自製示意，非正式校徽或平台實際截圖。

## GitHub Pages 部署

本專案已提供 GitHub Actions 工作流程。這些檔案本身不代表網站已發布。

1. 將專案檔案提交並推送至 `shiujryi/ailead365-guide` 的 `main` 分支。
2. 在儲存庫 **Settings → Pages → Build and deployment → Source** 選擇 **GitHub Actions**。需具備相應儲存庫權限與支援 Pages 的方案；公開靜態內容請確認儲存庫及組織政策。
3. 在 **Actions → Deploy static site to Pages → Run workflow** 選擇 `main` 執行；之後每次推送到 `main` 會自動驗證並部署。
4. 確認 `validate-and-upload` 與 `deploy` 工作皆成功，使用部署結果提供的網址檢查網站。若沒有自訂網域，預期網址為 `https://shiujryi.github.io/ailead365-guide/`；以 Pages 設定顯示的網址為準。
5. 在手機與電腦確認三種身分、登入連結、FAQ、行動選單與所有樣式正常。

工作流程先執行靜態檢查，再只上傳 `index.html` 與 `assets/`。不會把 README、測試、Git 資料或其他專案檔案發布至 Pages。請勿在 `assets/` 放入私密檔案。

如果 Actions 部署失敗，先確認 Pages 已選擇 GitHub Actions、儲存庫允許執行 Actions，以及 `github-pages` 環境允許 `main` 部署。不要在網站檔案中加入權杖；流程使用 GitHub 提供的短期權限。

## 後續修改教學

- **更改文字或步驟**：編輯 `index.html`。三份指南位於 `panel-senior`、`panel-junior`、`panel-teacher`；保留對應的 tab ID、`aria-controls`、`aria-labelledby` 關係。
- **調整外觀**：編輯 `assets/styles.css`。開頭的 `:root` 控制顏色；媒體查詢處理手機與平板。
- **新增常見問題**：在 `.faq-content` 內複製一個 `<details class="faq-item">`，以 `data-category="login"` 或 `data-category="learning"` 分類，填入 `<summary>` 與 `.faq-answer`。篩選計數會自動更新。
- **更新登入網址**：在 `index.html` 搜尋 `https://csjhkl.ailead365.com/auth/login` 並逐一更新；也需同步檢查步驟文字中的網域與本文件。
- **更新互動**：編輯 `assets/app.js`。身分切換只保存在當次頁面記憶體，不保存登入資訊。
- **加入圖片**：僅使用具授權且不含個資的素材，放入 `assets/`，提供合適的替代文字，使用 `./assets/檔名` 相對路徑。

修改後執行檢查，再提交及推送。避免在 `index.html` 引用 `/assets/...` 這類網域根路徑，否則 GitHub Pages 專案子路徑會失效。

## 內容依據與上線核對

- 學校登入網址與帳號／權限說明依本專案需求提供；高中與國中學生使用 6 碼學號，教師原則上使用 OpenID 帳號，少數另建帳號，登入問題洽教務主任。
- 官方產品介紹參考入口：<https://www.leadu-edu.com/products-detail/34/>。
- 本次開發環境對官方站的請求遭代理回覆 `403 CONNECT`，未直接成功讀取該頁。後續由需求提供者貼上官方產品介紹與 19 項特色文字，網站據此整理 AI 測評、診斷分析、補強影片、教師派發、課綱版本、即時提問與學習歷程等重點；未自行聲稱實際登入測試通過。
- 公開發布前請由校內承辦人對照實際帳號畫面，核對教材、任務、結果紀錄及教師權限。獨立的官方國中版確切網址尚未提供，未虛構來源或影片連結；目前以提供的跨學段產品介紹為依據。
- 操作步驟是角色導向的文字教學，未宣稱按鈕的固定名稱、位置或版本；如需精確圖文操作，請取得不含個資且允許公開的實際截圖後再補充。

## 資料保護

本網站不提供登入表單，也不保存帳號、密碼、學習紀錄、Cookie 或瀏覽器儲存資料，未加入第三方分析碼。登入連結另開官方學校平台，並使用 `noopener noreferrer`。GitHub Pages 託管及外部平台本身的資料處理依其政策。

**不要提交** Excel／CSV 師生清冊、學生個資、密碼規則、共用初始密碼、API 金鑰或含個資截圖。公開的 HTML、JavaScript、註解、README 與 Git 歷史都不適合存放這些資訊；隱藏元素或前端身分切換不構成存取控制。密碼資訊應透過學校既有受控管道提供，不在本站建立密碼產生器或查詢功能。

學生不可自行修改密碼；教師可於登入後自行修改，建議首次登入即變更。網站未包含 Excel、CSV 或師生帳號清冊。

## 驗證方式

不需要安裝套件的靜態檢查：

```sh
python3 tests/validate.py
node --check assets/app.js
```

靜態檢查確認 HTML 資源及錨點、分頁關聯、外連保護、公開資產類型與非機密部署範圍。它不能驗證 AILEAD365 登入、校內帳號或官方產品功能。

瀏覽器驗收項目：

1. 於手機（含 320px 寬度）、平板與桌面確認無水平溢出。
2. 點選三種身分，確認只顯示所選指南，帳號及密碼變更政策正確。
3. 使用 Tab、方向鍵、Home、End 切換身分，檢查焦點與內容一致。
4. 手機選單可展開、點連結關閉、按 Escape 關閉並返回按鈕。
5. FAQ 的全部／登入／學習篩選與展開收合正常。
6. 所有登入按鈕均指向學校專屬網址；不輸入真實帳密進行網站測試。
7. 關閉 JavaScript 後，三份指南、導覽與所有 FAQ 仍可閱讀。
8. 在 `/ailead365-guide/` 子路徑測試 CSS、JavaScript 與圖示可讀取。

部署工作流程會執行 Python 靜態檢查；完整瀏覽器互動檢查需另外執行，未包含在 Actions 工作流程中。

### 自動化瀏覽器驗收（開發工具，可選）

已安裝 Playwright 與其 Chromium 時，保持前述本機伺服器執行，在另一個終端機執行：

```sh
node tests/browser.cjs
```

若尚未安裝，可將測試工具裝到專案外，不新增網站執行相依：

```sh
npm install --prefix /tmp/ailead365-browser-tools playwright@1.62.1
/tmp/ailead365-browser-tools/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/ailead365-browser-tools/node_modules node tests/browser.cjs
```

如已有系統 Chromium，可指定 `CHROMIUM_PATH=/usr/bin/chromium`；以 `SITE_URL` 指定其他測試網址（包含部署子路徑），預設為本機伺服器根路徑。設定 `SCREENSHOT_DIR` 為已存在的目錄可輸出桌面與手機截圖。測試不會嘗試登入外部平台或輸入師生資料。

本次在 Chromium 實際通過 320、390、760、768、820、1024、1440px 寬度的三種身分版面，以及鍵盤切換、FAQ、手機選單、無 JavaScript 閱讀與 `/ailead365-guide/` 子路徑載入檢查。尚未實測 Safari、Firefox、GitHub Actions 雲端部署或 AILEAD365 帳號登入。
