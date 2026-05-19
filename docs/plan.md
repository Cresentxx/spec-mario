# Plan: Super Mario Bros. — Technical Implementation Plan

> 版本: 1.0 | 日期: 2026-05-20 | 状态: Draft

---

## 1. Technical Stack

| 组件 | 技术选型 | 说明 |
|------|---------|------|
| 语言 | Python 3.10+ | 类型提示、dataclass、match-case |
| 游戏引擎 | Pygame 2.5+ | 渲染、输入、音频 |
| 碰撞检测 | 自研 AABB | 基于 pygame.Rect |
| 音频 | pygame.mixer | BGM (.ogg) + SFX (.wav/.ogg) |
| 关卡数据 | JSON | 地形、敌人、道具配置 |
| 存档 | JSON 文件 | localStorage 替代方案 |
| 打包 | PyInstaller | 输出 Windows .exe |

---

## 2. Architecture Overview

```
src/
├── main.py                    # 入口点，游戏循环
├── core/
│   ├── game.py                # Game 类，状态机管理
│   ├── constants.py           # 全局常量 (分辨率/物理参数/颜色)
│   └── camera.py              # 摄像机系统 (不可回退滚动)
├── entities/
│   ├── player.py              # Mario 玩家角色
│   ├── enemies/
│   │   ├── base.py            # 敌人基类
│   │   ├── goomba.py          # Goomba
│   │   ├── koopa.py           # Koopa (绿/红)
│   │   ├── buzzy_beetle.py    # Buzzy Beetle
│   │   ├── hammer_bro.py      # Hammer Bro
│   │   ├── piranha_plant.py   # Piranha Plant
│   │   ├── bullet_bill.py     # Bullet Bill
│   │   ├── lakitu.py          # Lakitu + Spiny
│   │   ├── podoboo.py         # Podoboo
│   │   └── bowser.py          # Bowser (Boss)
│   ├── items/
│   │   ├── mushroom.py        # Super Mushroom + 1-UP
│   │   ├── fire_flower.py     # Fire Flower
│   │   ├── starman.py         # Starman
│   │   ├── coin.py            # Coin
│   │   └── fireball.py        # Fireball (玩家发射)
│   └── objects/
│       ├── block.py           # 方块系统 (Question/Brick/Hidden/Used/Hard)
│       ├── pipe.py            # 管道
│       ├── flagpole.py        # 旗杆
│       ├── moving_platform.py # 移动平台
│       ├── fire_bar.py        # 火焰棒 (城堡)
│       └── shell.py           # 龟壳
├── physics/
│   ├── physics.py             # 物理引擎 (重力/速度/AABB)
│   └── collision.py           # 碰撞检测系统
├── rendering/
│   ├── renderer.py            # 主渲染器
│   ├── sprite_loader.py       # Sprite Sheet 加载与切片
│   ├── animations.py          # 动画系统
│   └── effects.py             # 画面特效 (碎片/浮字/闪烁)
├── audio/
│   ├── sound_manager.py       # 音效管理器
│   └── music_manager.py       # 背景音乐管理器
├── levels/
│   ├── level_loader.py        # 关卡 JSON 加载器
│   ├── tile_map.py            # Tile Map 渲染
│   └── data/                  # 关卡数据文件
│       ├── 1-1.json
│       ├── 1-2.json
│       ├── 1-3.json
│       ├── 1-4.json
│       ├── 2-1.json
│       ├── 2-2.json
│       ├── 2-3.json
│       └── 2-4.json
├── ui/
│   ├── title_screen.py        # 标题画面
│   ├── hud.py                 # HUD 渲染
│   ├── pause_screen.py        # 暂停画面
│   ├── game_over.py           # Game Over 画面
│   └── score_tally.py         # 通关计分画面
├── input/
│   └── input_handler.py       # 键盘输入处理
├── save/
│   └── save_manager.py        # 存档管理 (JSON)
└── assets/                    # 资源文件 (不打包到 src)
    ├── sprites/               # Sprite Sheets (.png)
    ├── audio/
    │   ├── bgm/               # 背景音乐 (.ogg)
    │   └── sfx/               # 音效 (.wav/.ogg)
    └── fonts/                 # 像素字体
```

---

## 3. Data Model

### 3.1 核心数据结构

```python
@dataclass
class GameState:
    status: GameStatus          # TITLE, PLAYING, PAUSED, GAME_OVER, etc.
    world: int                  # 1-2
    level: int                  # 1-4
    score: int
    coins: int
    lives: int                  # 初始 3
    time_remaining: int         # 倒计时 (秒)
    second_quest: bool          # 是否 Second Quest

class GameStatus(Enum):
    TITLE = "title"
    PLAYING = "playing"
    PAUSED = "paused"
    DYING = "dying"
    LEVEL_CLEAR = "level_clear"
    GAME_OVER = "game_over"
    ENDING = "ending"

@dataclass
class PlayerState:
    form: PlayerForm            # SMALL, SUPER, FIRE
    invincible: bool            # Starman 无敌
    invincible_timer: int       # 无敌剩余帧数
    dead: bool

class PlayerForm(Enum):
    SMALL = "small"
    SUPER = "super"
    FIRE = "fire"
```

### 3.2 关卡数据格式

```json
{
  "world": 1,
  "level": 1,
  "theme": "overworld",
  "time_limit": 400,
  "width": 210,
  "height": 15,
  "tiles": [
    [0, 0, 0, ...],
    [1, 1, 1, ...],
    ...
  ],
  "tileset": "overworld",
  "entities": [
    {"type": "goomba", "x": 32, "y": 208},
    {"type": "koopa_green", "x": 80, "y": 208}
  ],
  "blocks": [
    {"x": 16, "y": 160, "type": "question", "content": "mushroom"},
    {"x": 48, "y": 160, "type": "brick"},
    {"x": 96, "y": 144, "type": "hidden", "content": "1up"}
  ],
  "pipes": [
    {"x": 160, "y": 176, "height": 2, "leads_to": "coin_room_1"}
  ],
  "flagpole": {"x": 198, "y": 48}
}
```

### 3.3 Tile ID 映射

| ID | Tile 类型 |
|----|----------|
| 0  | 空气 (Air) |
| 1  | Hard Block (地面/墙壁) |
| 2  | Brick Block |
| 3  | Question Block |
| 4  | Used Block |
| 5  | Hidden Block |
| 10 | Pipe Top-Left |
| 11 | Pipe Top-Right |
| 12 | Pipe Body-Left |
| 13 | Pipe Body-Right |

---

## 4. Key Algorithms

### 4.1 碰撞检测 (分轴 AABB)

```
1. 更新 X 位置 → 检测 X 碰撞 → 修正 X
2. 更新 Y 位置 → 检测 Y 碰撞 → 修正 Y
   - Y 碰撞从上方 = 着地 (设置 on_ground = True)
   - Y 碰撞从下方 = 顶方块 (触发方块互动)
```

### 4.2 不可回退摄像机

```python
camera_x = max(camera_x, player.x - screen_width * 0.4)
camera_x = min(camera_x, level_width - screen_width)
```

### 4.3 可变跳跃高度

```python
# KEYDOWN → 设置跳跃初速度
# 持续按住 → 减小重力 (延长上升时间)
# 松开跳跃键 → 恢复正常重力
if not jump_held and velocity_y < 0:
    velocity_y *= 0.5  # 松键截断上升速度
```

### 4.4 踩踏判定

```python
# 玩家下落 + 底部碰到敌人顶部 → 踩踏
if player.vy > 0 and player.rect.bottom <= enemy.rect.centery:
    stomp_enemy(enemy)
    player.vy = bounce_velocity  # 弹跳
```

---

## 5. Rendering Pipeline

```
1. 清空逻辑画面 (256×240)
2. 绘制背景 (天空/黑色)
3. 绘制 Tile Map (基于 camera_x 偏移)
4. 绘制方块 (含动画状态)
5. 绘制道具实体
6. 绘制敌人实体
7. 绘制玩家 (含状态动画)
8. 绘制特效 (碎片/浮字/金币弹出)
9. 绘制 HUD
10. pygame.transform.scale 放大至窗口大小
11. pygame.display.flip()
```

---

## 6. Game State Machine

```
TITLE ──[Start]──▶ PLAYING
                     │  ├── [Pause] ──▶ PAUSED ──[Resume]──▶ PLAYING
                     │  ├── [Death] ──▶ DYING ──▶ (lives > 0 ? PLAYING : GAME_OVER)
                     │  ├── [Flagpole] ──▶ LEVEL_CLEAR ──▶ (next level / ENDING)
                     │  └── [Esc] ──▶ TITLE
GAME_OVER ──[Continue]──▶ PLAYING (world restart)
ENDING ──[按键]──▶ TITLE / SECOND_QUEST
```

---

## 7. Audio Strategy

| 类别 | 实现 | 格式 | 数量 |
|------|------|------|------|
| BGM | pygame.mixer.music | .ogg | 6 首 |
| SFX | pygame.mixer.Sound | .wav/.ogg | ~15 个 |
| 通道 | pygame.mixer.set_num_channels(16) | — | 16 |

BGM 按场景切换:
- 进入关卡 → 停止当前 BGM → 加载并播放新 BGM
- 无敌状态 → 切换 Starman Theme，无敌结束恢复关卡 BGM
- 暂停 → 暂停 BGM 播放

---

## 8. Build & Packaging

### 8.1 开发环境

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install pygame
pip install pyinstaller
```

### 8.2 打包命令

```bash
pyinstaller --onefile --windowed \
  --name "SuperMario" \
  --icon=assets/icon.ico \
  --add-data "assets;assets" \
  --add-data "src/levels/data;levels/data" \
  src/main.py
```

### 8.3 交付结构

```
dist/
└── SuperMario.exe     # 单一可执行文件 (含 assets 打包)
```

---

## 9. Risk Assessment

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| 跳跃手感不符原版 | 高 | 基于帧的物理参数，可调常量 |
| 碰撞检测穿墙 | 高 | 分轴检测 + 像素级修正 |
| PyInstaller 体积过大 | 中 | 使用 Nuitka 编译或压缩 assets |
| 城堡关卡性能 | 中 | 限制同屏实体数量，视野外实体不更新 |
| 音频资源版权 | 中 | 使用自制音效或 CC0 资源 |

---

## 10. Research Notes

- Pygame 的 `SCALED` 标志 (2.0+) 自动处理窗口缩放，无需手动 `transform.scale`
- `pygame.sprite.Group` 提供批量碰撞检测，适合管理大量同类实体
- 关卡 JSON 格式选择: 易于手动编辑和版本控制，相比二进制格式更透明
- Sprite Sheet 建议使用单张 PNG，通过 `Surface.subsurface()` 切片
