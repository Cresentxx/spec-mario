# Tasks: Super Mario Bros. — Implementation Task Breakdown

> 版本: 1.0 | 日期: 2026-05-20 | 状态: Draft

---

## Phase 1: Foundation (M1)

### Task 1.1: Project Scaffolding & Game Loop
> **User Story**: — (基础设施)
> **Depends on**: —
> **Files**: `src/main.py`, `src/core/constants.py`, `src/core/game.py`

- [ ] 创建项目目录结构 (src/, assets/, docs/)
- [ ] 实现 `constants.py`: 全局常量 (SCREEN_W=256, SCREEN_H=240, FPS=60, 物理参数, 颜色表)
- [ ] 实现 `main.py`: Pygame 初始化、窗口创建 (768×720, SCALED)、Clock、主循环
- [ ] 实现 `Game` 类骨架: 状态机 (TITLE/PLAYING/PAUSED/GAME_OVER)、run() 入口

**验证**: 运行 `python src/main.py` 弹出黑色窗口，稳定 60FPS，ESC 退出。

---

### Task 1.2: Input Handler
> **User Story**: US-1
> **Depends on**: 1.1
> **Files**: `src/input/input_handler.py`

- [ ] 实现 `InputHandler` 类: 封装 `pygame.event.get()`
- [ ] 维护按键状态字典: `keys_held` (持续按住), `keys_pressed` (单帧按下), `keys_released` (单帧松开)
- [ ] 映射表: ←/A → LEFT, →/D → RIGHT, Z/Space/↑ → JUMP, Shift → RUN, Enter/P → PAUSE
- [ ] 提供 `is_held(action)`, `just_pressed(action)`, `just_released(action)` 接口

**验证**: 打印按键状态到控制台，确认所有映射正确响应。

---

### Task 1.3: Physics Engine
> **User Story**: US-1
> **Depends on**: 1.1
> **Files**: `src/physics/physics.py`, `src/physics/collision.py`

- [ ] 实现 `PhysicsBody`: position (x,y), velocity (vx,vy), acceleration, hitbox (Rect)
- [ ] 实现重力系统: `gravity = 0.25`, `max_fall = 4.5`
- [ ] 实现 AABB 碰撞检测: `check_rect_overlap(rect_a, rect_b) → bool`
- [ ] 实现分轴碰撞解析: `resolve_x()` → `resolve_y()`，返回碰撞信息 (方向/修正位置)
- [ ] 实现可变跳跃: 松开跳跃键时截断上升速度 (`vy *= 0.5`)

**验证**: 单元测试 — 创建两个 Rect，验证碰撞检测结果和位置修正。

---

### Task 1.4: Player Character (移动与跳跃)
> **User Story**: US-1
> **Depends on**: 1.2, 1.3
> **Files**: `src/entities/player.py`

- [ ] 实现 `Player` 类 (继承 pygame.sprite.Sprite)
- [ ] 移动参数: walk_max=1.5, run_max=2.5, accel=0.06, decel=0.10
- [ ] 左右移动 (加速度驱动，非瞬移)
- [ ] 跳跃: 初速度 -4.0，按住跳跃键延长上升
- [ ] 加速跑: Shift 按住时使用 run_max
- [ ] 刹车和转身: 反方向按键减速/转向
- [ ] 简单矩形渲染 (占位，16×16 Small, 16×32 Big)
- [ ] 朝向 (面左/面右)

**验证**: Mario 可在空场景中移动、跑、跳，手感参数可通过常量调节。

**Checkpoint**: Mario 在空白场景中可控移动跳跃，物理手感基本正确。

---

## Phase 2: Terrain System (M2)

### Task 2.1: Tile Map System
> **User Story**: US-7, US-8
> **Depends on**: 1.1
> **Files**: `src/levels/tile_map.py`, `src/rendering/sprite_loader.py`

- [ ] 实现 `TileMap` 类: 从 2D 数组加载瓦片地图
- [ ] 瓦片大小 16×16，屏幕尺寸 16×15 tiles
- [ ] 实现 `SpriteLoader`: 加载 Sprite Sheet PNG，按 16×16 切片为瓦片图像
- [ ] 渲染: 仅绘制摄像机范围内的瓦片 (视口裁剪)
- [ ] 碰撞映射: 指定哪些 Tile ID 是实心的 (1,2,3,4,5,10-13)

**验证**: 加载一个测试 Tile Map，屏幕正确渲染瓦片。

---

### Task 2.2: Level Loader (JSON)
> **User Story**: US-7, US-8
> **Depends on**: 2.1
> **Files**: `src/levels/level_loader.py`

- [ ] 定义关卡 JSON Schema (world, level, theme, time_limit, tiles, entities, blocks, flagpole)
- [ ] 实现 `LevelLoader.load(path) → LevelData`
- [ ] 解析 tiles 数组 → TileMap
- [ ] 解析 entities 列表 → 敌人初始位置
- [ ] 解析 blocks 列表 → 方块配置
- [ ] 解析 flagpole → 旗杆位置
- [ ] 创建测试关卡 `data/test.json` (宽 30 tiles 的简单地面)

**验证**: 加载测试关卡 JSON，TileMap 正确渲染地面。

---

### Task 2.3: Player-Terrain Collision
> **User Story**: US-1
> **Depends on**: 1.4, 2.1
> **Files**: `src/physics/collision.py` (更新)

- [ ] 实现玩家与 TileMap 的碰撞: 获取玩家周围的瓦片 (3×3 范围)
- [ ] 分轴检测: 先 X 后 Y
- [ ] 着地检测: Y 碰撞从上方 → `on_ground = True`
- [ ] 头部碰撞: Y 碰撞从下方 → 触发 `on_hit_block(tile_x, tile_y)`
- [ ] 墙壁碰撞: X 碰撞 → 停止水平移动
- [ ] 掉坑检测: y > level_height → 死亡

**验证**: Mario 在测试关卡上行走不穿墙、不卡地、可正常跳跃着地。

---

### Task 2.4: Camera System
> **User Story**: US-7
> **Depends on**: 1.4, 2.1
> **Files**: `src/core/camera.py`

- [ ] 实现 `Camera` 类
- [ ] 水平跟随: `camera_x = max(camera_x, player.x - SCREEN_W * 0.4)`
- [ ] 不可回退: camera_x 只增不减 (核心规则)
- [ ] 边界限制: `camera_x = min(camera_x, level_pixel_width - SCREEN_W)`
- [ ] 所有实体和瓦片渲染时减去 camera_x 偏移

**验证**: Mario 向右移动时画面滚动，向左走画面不回退。

**Checkpoint**: Mario 在有地形的关卡中可控移动，摄像机不可回退滚动正常。

---

## Phase 3: Block System (M2 续)

### Task 3.1: Block Entities
> **User Story**: US-3
> **Depends on**: 2.3
> **Files**: `src/entities/objects/block.py`

- [ ] 实现 `Block` 类: type (QUESTION/BRICK/HIDDEN/USED/HARD), content, animation_state
- [ ] 问号方块: 被顶 → 弹跳动画 → 弹出道具 → 变为 Used Block
- [ ] 砖块: Super/Fire 顶击 → 碎裂动画 (4 碎片) → 移除; Small 顶击 → 弹跳
- [ ] 隐藏方块: 不可见，顶击后出现 + 弹跳动画
- [ ] Used Block: 实心，无互动
- [ ] 弹跳动画: block.rect.y 偏移 -4 → 弹回

**验证**: Mario 从下方顶击问号方块有弹跳动画，方块变为 Used。

---

### Task 3.2: Block Content Spawning
> **User Story**: US-4
> **Depends on**: 3.1
> **Files**: `src/entities/objects/block.py` (更新)

- [ ] 方块 content 字段: "mushroom" / "fire_flower" / "starman" / "coin" / "1up"
- [ ] 顶击问号方块时根据 content 生成对应道具实体
- [ ] 蘑菇: 从方块中弹出，向右移动，遇壁反弹，受重力影响
- [ ] 火球花: 直接在方块上方出现
- [ ] 无敌星: 弹出后弹跳移动
- [ ] 金币: 弹出旋转上升动画 + 得分 +200

**验证**: 顶击问号方块后蘑菇弹出并在地面移动。

---

## Phase 4: Power-Up & State System (M4)

### Task 4.1: Item Entities
> **User Story**: US-4
> **Depends on**: 3.2, 1.3
> **Files**: `src/entities/items/mushroom.py`, `src/entities/items/fire_flower.py`, `src/entities/items/starman.py`, `src/entities/items/coin.py`

- [ ] `Mushroom` (红蘑菇): PhysicsBody, 向右移动, 遇壁反弹, 受重力, 拾取触发状态变化
- [ ] `Mushroom1UP` (绿蘑菇): 同红蘑菇行为，拾取 +1 生命
- [ ] `FireFlower`: 静止在方块上方，拾取触发状态变化
- [ ] `Starman`: 弹跳移动，拾取触发无敌
- [ ] `Coin`: 散布在关卡中的静态金币，拾取 +200 分 + 金币计数

**验证**: 蘑菇弹出后落地行走，Mario 接触后拾取，状态变化。

---

### Task 4.2: Player State Machine
> **User Story**: US-2
> **Depends on**: 1.4, 4.1
> **Files**: `src/entities/player.py` (更新)

- [ ] PlayerForm 枚举: SMALL, SUPER, FIRE
- [ ] Small → Super: 拾取红蘑菇，高度从 16→32，碰撞箱更新
- [ ] Super → Fire: 拾取火球花，外观变化
- [ ] 受击: Fire → Super → Small (递减)
- [ ] Small 受击 → 死亡
- [ ] Starman 无敌: `invincible = True`, 600 帧倒计时，闪烁渲染
- [ ] 无敌期间接触敌人直接击杀

**验证**: Small Mario 拾取蘑菇变大，顶击砖块碎裂；受击后变回 Small。

---

### Task 4.3: Fireball System
> **User Story**: US-2
> **Depends on**: 4.2
> **Files**: `src/entities/items/fireball.py`

- [ ] `Fireball`: Fire 状态按跳跃键发射
- [ ] 水平方向跟随面朝方向，速度 4.0
- [ ] 受重力影响，碰到地面/墙壁弹跳
- [ ] 最多 2 发同屏
- [ ] 碰到敌人 → 击杀 + 火球消失
- [ ] 碰到地形 (第 3 次弹跳或碰墙) → 消失

**验证**: Fire Mario 按跳跃键发射火球，火球弹跳前行。

**Checkpoint**: 玩家状态切换完整，道具拾取生效，火球可发射。

---

## Phase 5: Enemy System (M3)

### Task 5.1: Enemy Base & Goomba
> **User Story**: US-5
> **Depends on**: 2.3, 1.3
> **Files**: `src/entities/enemies/base.py`, `src/entities/enemies/goomba.py`

- [ ] `Enemy` 基类: PhysicsBody, HP, score_value, alive, direction
- [ ] 与地形碰撞 (遇壁转向/遇崖行为)
- [ ] 与玩家碰撞判定 (踩踏 vs 受伤)
- [ ] `Goomba`: 直线行走，遇崖不回头，踩踏 → 扁平动画 → 消失，速度 0.5

**验证**: Goomba 在地面上行走，Mario 踩踏后扁平消失。

---

### Task 5.2: Koopa Troopa & Shell
> **User Story**: US-5
> **Depends on**: 5.1
> **Files**: `src/entities/enemies/koopa.py`, `src/entities/objects/shell.py`

- [ ] `KoopaGreen`: 直线行走，遇壁转向，踩踏 → 缩壳
- [ ] `KoopaRed`: 巡逻模式，遇崖回头，踩踏 → 缩壳
- [ ] `Shell`: 静止龟壳，玩家触碰 → 踢飞
- [ ] 飞行 Shell: 水平移动，碰墙反弹，击杀沿途敌人
- [ ] 连杀计分: 维护 combo_counter, 递增分值 200→400→800→...→1UP

**验证**: Koopa 被踩后变壳，踢飞后沿地面滑行击杀 Goomba。

---

### Task 5.3: Remaining Ground Enemies
> **User Story**: US-5
> **Depends on**: 5.1 [P]
> **Files**: `src/entities/enemies/buzzy_beetle.py`, `src/entities/enemies/hammer_bro.py`

- [ ] `BuzzyBeetle`: 同 Koopa 行走，免疫火球，踩踏 → 缩壳
- [ ] `HammerBro`: 跳跃巡逻 (在两个高度间跳跃)，周期投掷锤子，HP=2，踩踏击杀，火球 2 发击杀
- [ ] 锤子弹道: 抛物线飞行，碰到地形消失

**验证**: Buzzy Beetle 免疫火球；Hammer Bro 跳跃并投掷锤子。

---

### Task 5.4: Special Enemies
> **User Story**: US-6
> **Depends on**: 5.1 [P]
> **Files**: `src/entities/enemies/piranha_plant.py`, `src/entities/enemies/bullet_bill.py`, `src/entities/enemies/lakitu.py`, `src/entities/enemies/podoboo.py`

- [ ] `PiranhaPlant`: 绑定到管道，周期性伸缩 (上→停→下→停)，玩家在管道上方时不下伸
- [ ] `BulletBill`: 从画面边缘生成，直线水平飞行，速度 1.0
- [ ] `Lakitu`: 云上漂浮 (S 形路径)，周期投掷 Spiny，被踩/火球击杀后一段时间重新出现
- [ ] `Spiny`: 直线行走，不可踩踏 (踩踏伤害玩家)，仅火球击杀
- [ ] `Podoboo`: 岩浆中周期弹跳 (固定轨迹)，仅无敌击杀

**验证**: Piranha Plant 从管道伸缩；Bullet Bill 从边缘飞入。

---

### Task 5.5: Bowser Boss
> **User Story**: US-8
> **Depends on**: 5.1, 4.3
> **Files**: `src/entities/enemies/bowser.py`

- [ ] `Bowser`: 大型敌人 (32×32)，左右来回跳跃
- [ ] 周期喷火: 生成水平飞行的火球
- [ ] 周期投掷锤子: 抛物线轨迹
- [ ] 桥梁机制: 踩断桥梁按钮 (桥尾的开关) → Bowser 掉落
- [ ] 火球击杀: 5 发火球击杀 Bowser
- [ ] HP 系统或直接桥梁机制

**验证**: Bowser 在场景中跳跃并喷火，踩断桥梁后掉落。

**Checkpoint**: 所有敌人类型实现，踩踏/踢壳/火球击杀逻辑完整。

---

## Phase 6: Level Objects (M2 续)

### Task 6.1: Pipes & Flagpole
> **User Story**: US-7, US-8
> **Depends on**: 2.3
> **Files**: `src/entities/objects/pipe.py`, `src/entities/objects/flagpole.py`

- [ ] `Pipe`: 碰撞体 (实心)，玩家按 ↓ 可进入 (如果配置了 leads_to)
- [ ] 管道进出动画: Mario 缩小进入 → 场景切换 → 金币房间 → 管道出口
- [ ] `Flagpole`: 接触触发通关流程
- [ ] 下滑动画: Mario 沿旗杆下滑 (根据起始高度计算得分)
- [ ] 得分规则: 最高点 5000, 中高 2000-4000, 中低 100-800

**验证**: Mario 接触旗杆触发下滑动画和计分。

---

### Task 6.2: Castle Objects (World 2)
> **User Story**: US-8
> **Depends on**: 2.3 [P]
> **Files**: `src/entities/objects/moving_platform.py`, `src/entities/objects/fire_bar.py`

- [ ] `MovingPlatform`: 水平/垂直周期移动，玩家站上去随之移动
- [ ] `FireBar`: 中心点 + 旋转的火焰段 (4/6/8 节)，碰触伤害玩家
- [ ] 岩浆区域: 底部特殊瓦片，接触即死

**验证**: 火焰棒绕中心旋转，Mario 碰触受伤；移动平台可搭乘。

---

### Task 6.3: Visual Effects System
> **User Story**: US-12
> **Depends on**: 1.1
> **Files**: `src/rendering/effects.py`, `src/rendering/animations.py`

- [ ] `EffectManager`: 管理临时特效实体
- [ ] 砖块碎片: 4 个小方块向四方飞散 (抛物线 + 旋转)
- [ ] 金币弹出: 旋转上升动画 (8 帧)
- [ ] 得分浮字: 数字上浮 30 帧后消失
- [ ] 敌人扁平: Goomba 扁平压缩渲染 20 帧
- [ ] 无敌闪烁: 每 3 帧切换可见性
- [ ] 死亡动画: Mario 上浮 → 下落 → 消失
- [ ] 烟花: 粒子效果 (通关条件满足时)

**验证**: 顶碎砖块时碎片飞散；踩踏 Goomba 后扁平动画。

**Checkpoint**: 方块/管道/旗杆/特效系统完成，关卡物体交互正常。

---

## Phase 7: Level Construction (M5 + M6)

### Task 7.1: World 1 Levels (Overworld)
> **User Story**: US-7
> **Depends on**: 6.1, 5.1, 5.2, 4.2
> **Files**: `src/levels/data/1-1.json`, `src/levels/data/1-2.json`, `src/levels/data/1-3.json`, `src/levels/data/1-4.json`

- [ ] 1-1.json: 入门关卡，平地 + 少量 Goomba + 问号方块 + 旗杆，宽 210 tiles
- [ ] 1-2.json: 引入 Koopa + 更多悬崖 + 管道 + 隐藏方块
- [ ] 1-3.json: 高难度，移动平台 + Hammer Bro + 精确跳跃
- [ ] 1-4.json: 城堡主题 Boss 关 (简化版), Bowser + 桥梁

**验证**: 4 个关卡均可从起点到达旗杆/Boss 并通关。

---

### Task 7.2: World 2 Levels (Castle)
> **User Story**: US-8
> **Depends on**: 7.1, 6.2, 5.5
> **Files**: `src/levels/data/2-1.json`, `src/levels/data/2-2.json`, `src/levels/data/2-3.json`, `src/levels/data/2-4.json`

- [ ] 2-1.json: 城堡主题，引入火焰棒 + 岩浆 + Podoboo
- [ ] 2-2.json: 更多火焰棒 + 移动平台 + Buzzy Beetle
- [ ] 2-3.json: 高密度陷阱 + Hammer Bro + Lakitu + Spiny 组合
- [ ] 2-4.json: 最终 Boss，Bowser + 喷火 + 锤子 + 桥梁

**验证**: 4 个城堡关卡可通关，2-4 击败 Bowser 后游戏通关。

---

### Task 7.3: Theme Rendering
> **User Story**: US-7, US-8
> **Depends on**: 2.1 [P]
> **Files**: `src/rendering/renderer.py` (更新), `src/levels/tile_map.py` (更新)

- [ ] Overworld 主题: 天蓝背景 + 橙砖瓦片 + 装饰 (云/灌木/山)
- [ ] Castle 主题: 黑色背景 + 灰色瓦片 + 岩浆底部发光效果
- [ ] 关卡加载时根据 theme 字段选择 tileset 和背景色

**验证**: World 1 显示蓝天绿地；World 2 显示黑暗城堡。

**Checkpoint**: 全部 8 个关卡数据完整，两个主题渲染正确。

---

## Phase 8: UI & Audio (M7)

### Task 8.1: Title Screen
> **User Story**: US-10
> **Depends on**: 1.1
> **Files**: `src/ui/title_screen.py`

- [ ] 标题 Logo 渲染 (像素字体)
- [ ] "START GAME" 菜单项 (闪烁效果)
- [ ] 背景动画 (简化版: 静态 Mario + 管道场景)
- [ ] 按跳跃键/Enter → 进入 World 1-1

**验证**: 启动游戏显示标题画面，按键开始游戏。

---

### Task 8.2: HUD
> **User Story**: US-10
> **Depends on**: 1.1
> **Files**: `src/ui/hud.py`

- [ ] HUD 逻辑画面 (256×240 顶部 16px 区域)
- [ ] 左: "MARIO" + 6 位分数
- [ ] 中左: 金币图标 + ×数量 (2 位)
- [ ] 中右: "WORLD" + 关卡编号 (X-Y)
- [ ] 右: "TIME" + 3 位倒计时
- [ ] 像素字体渲染 (不遮挡游戏画面)

**验证**: 游戏中 HUD 实时更新分数、金币、关卡、时间。

---

### Task 8.3: Game Over & Pause Screens
> **User Story**: US-10
> **Depends on**: 8.1
> **Files**: `src/ui/game_over.py`, `src/ui/pause_screen.py`

- [ ] 暂停画面: 覆盖半透明层 + "PAUSED" 文字，BGM 暂停
- [ ] Game Over: 黑屏 + "GAME OVER" 文字居中 + 等待按键
- [ ] Continue 选项: Game Over 后按键 → 从当前 World 起点重新开始

**验证**: P 键暂停；死亡 3 次后显示 Game Over。

---

### Task 8.4: Level Clear & Score Tally
> **User Story**: US-9, US-10
> **Depends on**: 6.1, 8.2
> **Files**: `src/ui/score_tally.py`

- [ ] 通关流程: 旗杆下滑 → 走入城堡 → 过渡画面
- [ ] 计分画面: 剩余时间 × 50 逐个转换为分数 (动画)
- [ ] 烟花效果 (时间尾数为 1/3/6 时触发)
- [ ] 计分完成后加载下一关

**验证**: 通关后显示计分动画，分数正确累加。

---

### Task 8.5: Ending Screen
> **User Story**: US-10
> **Depends on**: 8.4
> **Files**: `src/ui/ending_screen.py`

- [ ] 击败 World 2-4 Bowser 后显示结局画面
- [ ] "CONGRATULATIONS" 文字 + 通关信息
- [ ] 显示最终分数
- [ ] 选项: "SECOND QUEST" (重新开始，难度提升) / "TITLE" (返回标题)
- [ ] Second Quest: Goomba→Buzzy Beetle 替换, 速度提升, 花变蘑菇

**验证**: 通关后显示结局，可选 Second Quest 重新开始。

---

### Task 8.6: Audio System
> **User Story**: US-11
> **Depends on**: 1.1 [P]
> **Files**: `src/audio/sound_manager.py`, `src/audio/music_manager.py`

- [ ] `MusicManager`: `play(theme)`, `stop()`, `pause()`, `resume()`
- [ ] BGM 切换: 进入关卡 → 加载对应 theme BGM → 循环播放
- [ ] `SoundManager`: `play_sfx(name)` → 从预加载的 Sound 字典播放
- [ ] 预加载所有 SFX 到内存
- [ ] 无敌状态: 切换 Starman Theme，无敌结束恢复关卡 BGM
- [ ] 暂停: 暂停 BGM

**验证**: 进入关卡播放 BGM，跳跃有音效，暂停时音乐停止。

**Checkpoint**: 完整 UI 流程 (标题→游戏→HUD→暂停→通关→结局→Game Over)，音效系统工作。

---

## Phase 9: Save & Polish (M8)

### Task 9.1: Save System
> **User Story**: US-9
> **Depends on**: 8.2
> **Files**: `src/save/save_manager.py`

- [ ] `SaveManager`: 读写 JSON 文件
- [ ] 保存最高分 Top 5 排行榜 (`save/highscores.json`)
- [ ] 保存设置: 音量 (`save/settings.json`)
- [ ] Game Over 时检查并更新排行榜

**验证**: 通关后高分记录到文件，重启后排行榜保留。

---

### Task 9.2: Game Flow Integration
> **User Story**: US-10
> **Depends on**: 8.1 ~ 8.6, 7.1, 7.2
> **Files**: `src/core/game.py` (更新)

- [ ] 完整状态机: TITLE → PLAYING → (通关 → 下一关 / 死亡 → 重试 / GAME_OVER)
- [ ] 死亡处理: lives -1 → 重试当前关 (保留分数/金币)
- [ ] Game Over → Continue: 从当前 World 第一关重新开始 (保留分数)
- [ ] World 通关: World 1-4 通关 → 进入 World 2-1
- [ ] 全局通关: World 2-4 通关 → Ending Screen
- [ ] Second Quest: 标记 `second_quest = True`，重新从 1-1 开始

**验证**: 完整通关流程: 标题 → 8 关依次通过 → 结局 → Second Quest。

---

### Task 9.3: Sprite Assets Integration
> **User Story**: US-1 ~ US-12
> **Depends on**: Phase 1-8 全部
> **Files**: `src/rendering/sprite_loader.py` (更新), `assets/sprites/`

- [ ] 制作/获取像素风格 Sprite Sheets:
  - Mario (Small/Super/Fire 各 4 方向 × 3 帧动画)
  - 所有敌人 (行走/死亡各 2-3 帧)
  - 所有道具 (静态 + 弹出动画)
  - 瓦片集 (Overworld + Castle)
  - 装饰物 (云/灌木/山/管道)
  - HUD 元素 (金币图标/数字)
- [ ] 替换所有占位矩形为精灵图渲染
- [ ] 实现帧动画: walk cycle (3 帧), jump, die

**验证**: 所有角色和物体使用精灵图渲染，帧动画流畅。

---

### Task 9.4: Performance Optimization
> **Depends on**: 9.2
> **Files**: 多文件

- [ ] 视口外实体不更新逻辑 (仅更新摄像机范围内的敌人)
- [ ] TileMap 渲染裁剪 (仅绘制摄像机范围内瓦片)
- [ ] 精灵图预加载到内存，避免运行时 IO
- [ ] 帧率稳定性测试: 8 个关卡均稳定 60 FPS
- [ ] 内存占用检查: < 150 MB

**验证**: `Clock.get_fps()` 全程 ≥ 59。

---

### Task 9.5: Packaging (.exe)
> **Depends on**: 9.4
> **Files**: `build.spec` / 打包脚本

- [ ] 编写 PyInstaller spec 文件
- [ ] 配置资源文件打包 (`--add-data "assets;assets"`)
- [ ] 测试打包后的 .exe 在干净 Windows 环境运行
- [ ] 验证体积 < 50 MB
- [ ] 验证启动时间 < 3 秒

**验证**: 双击 `SuperMario.exe` 直接运行，完整通关无异常。

**Checkpoint**: 最终 .exe 可独立运行，性能达标。

---

## Dependency Graph

```
Phase 1: Foundation
  1.1 ──┬── 1.2 ──┐
        │          ├── 1.4 ──────────────────────────────────┐
        └── 1.3 ──┘                                         │
                                                              │
Phase 2: Terrain                                              │
  2.1 ── 2.2                                                  │
  │                            ┌──────────────────────────────┘
  └── 2.3 (depends on 1.4) ─── 2.4
       │
Phase 3: Blocks                                               
  3.1 ── 3.2                                                  

Phase 4: Power-Ups                                           
  4.1 ── 4.2 ── 4.3                                          

Phase 5: Enemies                                             
  5.1 ──┬── 5.2 ── 5.3 (P)                                  
        └── 5.4 (P) ── 5.5                                  

Phase 6: Objects                                             
  6.1, 6.2 (P), 6.3                                         

Phase 7: Levels                                              
  7.1, 7.2, 7.3 (P)                                         

Phase 8: UI & Audio                                          
  8.1 (P), 8.2 (P), 8.3, 8.4, 8.5, 8.6 (P)                 

Phase 9: Polish                                              
  9.1, 9.2, 9.3, 9.4, 9.5                                   
```

`[P]` = 可并行执行的任务

---

## Task Summary

| Phase | Tasks | 描述 | 依赖 |
|-------|-------|------|------|
| 1 | 1.1-1.4 | 基础框架: 循环/输入/物理/玩家 | — |
| 2 | 2.1-2.4 | 地形系统: 瓦片/关卡加载/碰撞/摄像机 | Phase 1 |
| 3 | 3.1-3.2 | 方块系统: 方块类型/内容生成 | Phase 2 |
| 4 | 4.1-4.3 | 道具状态: 道具实体/状态机/火球 | Phase 3 |
| 5 | 5.1-5.5 | 敌人系统: 全部敌人类型 | Phase 2, 4 |
| 6 | 6.1-6.3 | 关卡物体: 管道/旗杆/城堡/特效 | Phase 2, 5 |
| 7 | 7.1-7.3 | 关卡数据: 8 关 + 2 主题渲染 | Phase 6 |
| 8 | 8.1-8.6 | UI 音效: 标题/HUD/暂停/通关/结局/音频 | Phase 1 |
| 9 | 9.1-9.5 | 打磨发布: 存档/流程/精灵/优化/打包 | Phase 7, 8 |
