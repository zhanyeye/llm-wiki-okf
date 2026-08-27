# wiki file — 图片管理

文件管理命令组：`upload-image` / `download-image`。

**图片工作流**：新建文档带图片时，先 `doc create` 拿到 URL → `file upload-image` 上传图片 → `doc update --content` 写入含图片的 Markdown。修改已有文档时，先 `file upload-image` 再 `doc update --replace` 插入图片引用。

**注意 — 图片 Markdown 引号陷阱**：`--content` 或 `--with` 时，**必须用双引号 `"..."`**（Windows bash 下单引号会把 `!` 转义为 `\!`，导致图片无法渲染）。

---

## upload-image — 上传图片

```bash
wiki file upload-image "https://wki.test.com/domains/59/wiki/3334/WIKI2021032500053" "./screenshot.png"
```

### 参数

| 参数 | 必填 | 说明 |
|-|-|-|
| `URL` | 是 | wiki 文档链接（必须是 Markdown 文档） |
| `FILE_PATH` | 是 | 本地图片文件路径 |

### 返回

```json
{
  "image_url": "https://wki.test.com/api/file/download/upload-v2/WIKI2021032500053/abc123/screenshot.png"
}
```

---

## download-image — 下载图片

```bash
wiki file download-image \
  "https://wki.test.com/api/file/download/upload-v2/WIKI2021032500053/abc123/screenshot.png" \
  "./downloads"
```

### 参数

| 参数 | 必填 | 说明 |
|-|-|-|
| `URL` | 是 | **图片资源完整下载地址**（来自 `upload-image` 返回的 `image_url`，不是文档 URL） |
| `DIR` | 是 | 本地保存目录（不存在会创建） |

### 返回

```json
{ "saved_path": "./downloads/screenshot.png" }
```

### 决策点

- URL 来源：`doc get` 返回的 `content` 字段中提取的 Markdown 图片 URL
O