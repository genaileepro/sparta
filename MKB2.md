# 먹깨비 피드 구현 가이드

## ✅ 가능 여부

네. Convex는 "Realtime DB + Serverless Functions"를 제공하므로,
사진 URL·타임스탬프·좋아요 수를 저장하고 Streamlit에서 실시간으로 불러오는 구조가 깔끔하게 동작합니다.

단, Convex는 바이너리 파일을 직접 저장하지 않으므로 Cloudinary·S3 등에 이미지를 업로드 → URL만 Convex에 보관하는 방식을 권장합니다.

## 1. 시스템 개요

```
[Streamlit] ──upload──▶  [Cloudinary] ──URL──▶
         │                                   │
         └──── GraphQL/HTTP (convex-python) ─┘
                      ▼
                 [Convex DB]
                   posts
```

| 엔티티 | 필드                             |
| ------ | -------------------------------- |
| posts  | id, image_url, created_at, likes |

## 2. Convex 설정

### 2-1. 프로젝트 초기화

```bash
npm install -g convex
convex init instagram-lite
cd instagram-lite
```

### 2-2. schema.ts

```typescript
import { defineSchema, v } from 'convex/server';

export default defineSchema({
    posts: {
        image_url: v.string(),
        created_at: v.number(), // Date.now()
        likes: v.number(), // 기본 0
    },
});
```

### 2-3. serverless 함수 (convex/posts.ts)

```typescript
import { mutation, query } from './_generated/server';
import { v } from 'convex/values';

export const createPost = mutation({
    args: { image_url: v.string() },
    handler: async (ctx, args) => {
        await ctx.db.insert('posts', {
            image_url: args.image_url,
            created_at: Date.now(),
            likes: 0,
        });
    },
});

export const likePost = mutation({
    args: { id: v.id('posts') },
    handler: async (ctx, { id }) => {
        const post = await ctx.db.get(id);
        if (post) await ctx.db.patch(id, { likes: post.likes + 1 });
    },
});

export const listPosts = query({
    args: {},
    handler: async (ctx) => ctx.db.query('posts').order('desc').collect(), // 최신순
});
```

```bash
convex deploy
```

배포 후 대시보드에서 deployment URL + API key 확인.

## 3. Streamlit 앱 (app.py)

```python
import os, io, time, urllib.parse, cloudinary.uploader as uploader
import streamlit as st
from convex import ConvexClient           # pip install convex-dev
from dotenv import load_dotenv

load_dotenv()
CONVEX_URL  = os.getenv("CONVEX_URL")
CONVEX_KEY  = os.getenv("CONVEX_KEY")
CLOUD_NAME  = os.getenv("CLOUD_NAME")
CLOUD_KEY   = os.getenv("CLOUD_KEY")
CLOUD_SECRET= os.getenv("CLOUD_SECRET")

convex = ConvexClient(CONVEX_URL, CONVEX_KEY)
uploader.config(cloud_name=CLOUD_NAME,
                api_key=CLOUD_KEY,
                api_secret=CLOUD_SECRET)

st.title("📸 먹깨비 피드 – 오늘 내가 먹은 것")

# --- 업로드 -------------------------------------------------
file = st.file_uploader("🍴 사진 올리기", type=["jpg", "png"], key="uploader")
if file:
    if st.button("업로드"):
        with st.spinner("업로드 중..."):
            # 1) Cloudinary 업로드
            res = uploader.upload(io.BytesIO(file.read()), folder="meokkaebi")
            url = res["secure_url"]

            # 2) Convex posts 컬렉션에 저장
            convex.mutation("posts:createPost", {"image_url": url})
            st.success("업로드 완료!")
            st.experimental_rerun()

st.divider()

# --- 피드 ---------------------------------------------------
posts = convex.query("posts:listPosts", {})
for post in posts:
    st.image(post["image_url"], use_column_width=True)
    col1, col2 = st.columns([1, 8])
    with col1:
        if st.button("❤️", key=f"like-{post['_id']}"):
            convex.mutation("posts:likePost", {"id": post["_id"]})
            st.experimental_rerun()
    with col2:
        st.write(f"{post['likes']} likes  •  {time.strftime('%Y-%m-%d', time.localtime(post['created_at']/1000))}")
    st.divider()
```

## 4. 환경 변수 (.env 예시)

```ini
# Convex
CONVEX_URL   = https://<deployment>.convex.cloud
CONVEX_KEY   = <admin_or_reader_key>

# Cloudinary
CLOUD_NAME   = xxxxxx
CLOUD_KEY    = xxxxxxxxx
CLOUD_SECRET = xxxxxxxxxxxxxxxxx
```

## 5. requirements.txt

```
streamlit>=1.33
convex-dev>=0.4
python-dotenv
cloudinary
```

## 🚀 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

이제 사진 업로드 → Cloudinary URL 저장 → Convex DB 기록 → 실시간 피드 렌더 + 좋아요 전 과정을 한 페이지에서 해결할 수 있습니다. 필요 시 댓글·프로필·무한 스크롤 등 기능을 Convex mutation/query로 손쉽게 확장하세요!
