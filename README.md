# 基隆市立中山高級中學 AILEAD365 數位學習平台使用指南

繁體中文響應式靜態網站，以兩項內容為主：

1. **登入帳號說明（優先）**：高中、國中學生與教師身分切換、帳號格式、密碼取得方式及校內協助窗口。
2. **官方使用說明**：引導至 <https://www.leadu-edu.com/products/59/>，並提供學生、教師操作教學影片連結，不在本站重複長篇操作教學。

使用 HTML、CSS、原生 JavaScript，沒有後端、資料庫或網站執行相依套件。

## 本機預覽

在既有專案目錄執行，不需要另建 Git worktree：

```sh
cd /workspace/ailead365-guide
python3 -m http.server 8000 --bind 127.0.0.1
```

在自己的開發電腦開啟 `http://127.0.0.1:8000`，按 `Ctrl+C` 停止伺服器。雲端環境的本機網址僅供機器內部測試。也可直接開啟 `index.html`；網站不依賴 API、CDN 或遠端字型。

## 專案結構

```text
index.html                      # 登入帳號、三種身分資訊與官方使用說明入口
assets/styles.css               # 響應式版面與外觀
assets/app.js                   # 身分切換、鍵盤操作及行動選單
assets/favicon.svg              # 自製圖示（非正式校徽）
tests/validate.py               # 靜態檢查
tests/browser.cjs              # Playwright 瀏覽器驗收
.github/workflows/pages.yml     # GitHub Pages 部署
```

資源使用相對路徑，可部署於 `/ailead365-guide/` 子路徑。

## GitHub Pages 部署

1. 將修改提交並推送至 `shiujryi/ailead365-guide` 的 `main` 分支。
2. 在儲存庫 **Settings → Pages → Build and deployment → Source** 選擇 **GitHub Actions**。
3. 每次推送會觸發部署；也可至 **Actions → Deploy static site to Pages → Run workflow**，選擇 `main` 手動執行。
4. 確認 `validate-and-upload`、`deploy` 都成功，再開啟部署結果提供的網址。預期網址為 <https://shiujryi.github.io/ailead365-guide/>，以 Pages 設定為準。
5. 驗收手機及電腦的身分切換、登入按鈕與官方使用說明連結。

工作流程先檢查，再只上傳 `index.html` 與 `assets/`；README、測試及其他檔案不會發布至 Pages。部署 404 時先確認 Pages 已啟用並選擇 GitHub Actions，再重新執行工作流程。檔案推送成功與網站部署成功是不同狀態。

## 後續修改

- **登入資訊**：編輯 `index.html` 的 `panel-senior`、`panel-junior`、`panel-teacher`。保留分頁 ID 與 `aria-controls`、`aria-labelledby` 關係。
- **登入網址**：搜尋並更新 `https://csjhkl.ailead365.com/auth/login` 與畫面顯示的網域。
- **官方使用說明**：修改 `#guide` 內連結，目前使用需求指定的 `https://www.leadu-edu.com/products/59/`。
- **教學影片**：修改 `#guide` 內的 `.video-link`。目前學生影片為 <https://youtu.be/BMvBKnkbPfA?si=Q8i2r7RfLgb92Bi9>，教師影片為 <https://youtu.be/eTpssOyviU4?si=uCr1YcdNb-XpSWUK>；由需求提供者提供，點選後於 YouTube 另開分頁播放，本站不嵌入播放器。
- **外觀**：編輯 `assets/styles.css`，`:root` 控制色彩，媒體查詢處理手機版面。
- **互動**：編輯 `assets/app.js`；身分狀態只保存在當次頁面記憶體。

修改後執行檢查，再提交與推送。避免 `/assets/...` 這類網域根路徑，以免 GitHub Pages 子路徑載入失敗。

## 資料保護

學生帳號為 6 碼學號，教師原則上使用 OpenID 帳號。學生不可自行修改密碼；教師登入後可修改。密碼資訊僅由校內受控管道提供。

請勿提交師生 Excel／CSV 清冊、個資、固定密碼規則、共用初始密碼、金鑰或含個資截圖。隱藏的 HTML、前端切換與 Git 歷史均不適合保存私密資料。

本站不收集帳號密碼，不使用資料庫、Cookie、瀏覽器儲存或第三方追蹤碼。外連以 `noopener noreferrer` 另開分頁；登入與平台功能由外部平台處理。未使用真實師生帳號驗證登入。

## 測試

不需要安裝套件的檢查：

```sh
python3 tests/validate.py
node --check assets/app.js
```

已安裝 Playwright 與其 Chromium 時，保持本機伺服器執行，在另一個終端機執行：

```sh
node tests/browser.cjs
```

若尚未安裝，可在專案外安裝測試工具：

```sh
npm install --prefix /tmp/ailead365-browser-tools playwright@1.62.1
/tmp/ailead365-browser-tools/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/ailead365-browser-tools/node_modules node tests/browser.cjs
```

以 `CHROMIUM_PATH` 指定系統 Chromium，以 `SITE_URL` 指定含子路徑的測試網址（預設 `http://127.0.0.1:8000/`）。設定 `SCREENSHOT_DIR` 為已存在的目錄可輸出截圖。

瀏覽器驗收涵蓋 320、390、760、768、820、1024、1440px 寬度、三種身分帳號資訊、鍵盤切換、手機選單、登入與官方連結目的地，以及關閉 JavaScript 後的資訊可讀性。測試不會登入外部平台，也不代表官方站內容或可用性已驗證。Actions 僅執行靜態檢查，未執行完整瀏覽器驗收。
