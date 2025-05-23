# 征服聖經

幫助使用者做讀聖經的紀錄，並且設立目標，協助可以讀完聖經。

## 功能

1. 註冊和登入
   - 帳號密碼登入
   - 第一次登入設定名稱

2. 個人首頁
   - 新約已讀百分比
   - 舊約已讀百分比
   - 全部已讀百分比
   - 目標進度百分比
   - 完整讀完次數

3. 閱讀進度
   - 選擇舊約或新約
   - 選擇書卷
   - 用表格呈現章節
   - 點擊章節標記已讀

4. 個人設定
   - 設定開始日期
   - 設定預計讀完時間
   - 重置閱讀進度

5. 管理者後台
   - 查看所有使用者
   - 查看使用者進度
   - 管理使用者資訊
   - 預設管理者：admin/1234567891

## 開發環境

本專案使用 Docker 進行開發和部署：

```
# 啟動開發環境
docker compose up -d

# 初始化資料庫
docker compose exec web python init_db.py
```

## 技術

- 後端：Flask
- 前端：HTML, CSS, jQuery
- 資料庫：PostgreSQL

## 安裝步驟

1. 複製專案
```
git clone https://github.com/yourusername/conquer_bible_v2.git
cd conquer_bible_v2
```

2. 啟動 Docker 環境
```
docker compose up -d
```

3. 初始化資料庫
```
docker compose exec web python init_db.py
```

4. 開啟瀏覽器，訪問 http://localhost:9527

## 埠口配置

- 網頁應用：9527
- 資料庫：6001

## Fly.io 部署

本專案已配置為可在 [Fly.io](https://fly.io) 平台上部署：

1. 安裝 Fly CLI
```
# 依照 https://fly.io/docs/hands-on/install-flyctl/ 安裝 Fly CLI
```

2. 登入 Fly.io
```
fly auth login
```

3. 部署應用
```
fly deploy
```

4. 查看部署狀態
```
fly status
```

5. 訪問應用
```
fly open
```

專案配置詳情可在 `fly.toml` 中查看，主要配置如下：
- 主要區域：香港 (hkg)
- 內部端口：9527
- 記憶體配置：1GB
- CPU 配置：共享，1 核心
